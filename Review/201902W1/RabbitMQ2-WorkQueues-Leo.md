# RabbitMQ2 - Work Queues

注：本文为翻译

**原文地址：https://www.rabbitmq.com/tutorials/tutorial-two-java.html**

## 工作队列

![img](https://www.rabbitmq.com/img/tutorials/python-two.png)

在第一章中，我们编写了用于从指定队列发送和接受消息的程序，在本章中，我们将创建一个工作队列，用于在多个工作者之间分配耗时的任务。

工作队列（又名：任务队列）背后的主要思想是避免立刻执行资源密集型任务并等待任务完成，相反，我们把任务安排在以后完成。我们将任务封装为消息并将其发送到队列，在后台运行的工作进程将弹出任务并最终执行作业。当您运行多个 worker 时，任务将在它们之间共享。

这个概念在 Web 应用中特别有用，因为在 Web 应用中，不可能在一个简短的 HTTP 请求窗口中处理复杂的任务。



## 准备

在上一章中，我们发送了一个包含 「Hello World!」的消息。现在我们将发送代表复杂任务的字符串。我们没有实际的任务，比如要调整图像大小或呈现 pdf 文件，所以我们使用 `Thread.sleep()` 函数假装我们很忙。我们将使用字符串中点(.) 的数量表示复杂度，每个点将表示 “工作” 的一秒钟，例如，Hello... 表示三秒钟。

我们将对前一个例子中的 `Send.java` 代码做轻微的改动，以允许从命令行中发送任意的消息。这个程序将把任务调度到我们的工作队列中，将它命名为：`NewTask.java`

```java
String message = String.join(" ", argv);

channel.basicPublish("", "hello", null, message.getBytes());
System.out.println(" [x] Sent '" + message + "'");
```

我们之前的 `Recv.jav`a 程序也需要做一些改变：它需要为消息体中的每个点(.) 伪造成一秒钟，这个程序将处理传递的消息并执行相应的任务，将它命名为：`Worker.java`

```java
DeliverCallback deliverCallback = (consumerTag, delivery) -> {
  String message = new String(delivery.getBody(), "UTF-8");

  System.out.println(" [x] Received '" + message + "'");
  try {
    doWork(message);
  } finally {
    System.out.println(" [x] Done");
  }
};
boolean autoAck = true; // acknowledgment is covered below
channel.basicConsume(TASK_QUEUE_NAME, autoAck, deliverCallback, consumerTag -> { });
```

我们模拟执行时间的伪任务：

```java
private static void doWork(String task) throws InterruptedException {
    for (char ch: task.toCharArray()) {
        if (ch == '.') Thread.sleep(1000);
    }
}
```

按照第一章的方式编译它们（使用工作目录中的 jar 文件和环境变量 CP）

```java
javac -cp $CP NewTask.java Worker.java
```



## 循环调度

使用任务队列的优点之一是能够轻松地并行化工作。如果我们积压了大量的工作，我们可以增加更多的 workers，这样就可以很容易地扩大规模。

首先，我们尝试同时启动两个 worker 实例，他们都将从队列中获取消息，但具体是如何获得消息的呢？让我们来看看。

你需要打开三个终端，两个运行 worker 程序，这两个终端将是我们的消费者 - C1 和 C2。

```shell
# shell 1
java -cp $CP Worker
# => [*] Waiting for messages. To exit press CTRL+C
```

```shell
# shell 2
java -cp $CP Worker
# => [*] Waiting for messages. To exit press CTRL+C
```

在第三个终端，我们将发布新任务，一旦你启动了消费者，你就可以发布一些消息：

```shell
# shell 3
java -cp $CP NewTask First message.
# => [x] Sent 'First message.'
java -cp $CP NewTask Second message..
# => [x] Sent 'Second message..'
java -cp $CP NewTask Third message...
# => [x] Sent 'Third message...'
java -cp $CP NewTask Fourth message....
# => [x] Sent 'Fourth message....'
java -cp $CP NewTask Fifth message.....
# => [x] Sent 'Fifth message.....'
```

让我们看看 worker 接收到了什么：

```shell
java -cp $CP Worker
# => [*] Waiting for messages. To exit press CTRL+C
# => [x] Received 'First message.'
# => [x] Received 'Third message...'
# => [x] Received 'Fifth message.....'
```

```shell
java -cp $CP Worker
# => [*] Waiting for messages. To exit press CTRL+C
# => [x] Received 'Second message..'
# => [x] Received 'Fourth message....'
```

默认情况下，RabbitMQ 将按顺序地将每一个消息发送给下一个消费者，平均每个消费者接收到相同数量的消息。这种分发消息的方式称为循环。你可以尝试三个或者更多的 workers。



## 消息确认

完成一项任务需要几秒钟，你可能想知道，如果其中一个消费者启动了一个很长的任务，但只完成了部分任务就挂了，那么会发生什么情况。使用我们当前的代码，一旦 RabbitMQ 将消息发送给了消费者，它立刻被标记为删除。在这种情况下，如果你杀死了一个 worker，我们将丢失它刚刚处理着的消息。我们还将丢失发送给该特定 worker 但尚未处理的所有消息。

但我们不想丢失任何任务，如果一个 worker 挂了，我们希望将任务交付给另一个 workder。

为了保证消息永远不会丢失，RabbitMQ 支持消息确认机制。消费者返回一个 ack 告诉 RabbitMQ 接收、处理了特定的消息，RabbitMQ 可以自由删除该消息。

如果一个消费者在没有发送 ack 的情况下挂了（通道关闭、连接关闭或 TCP 连接丢失），RabbitMQ 将认为消息没有被完全处理并放回队列。如果有其他消费者同时在线，它将很快重新交付给另一个消费者。这样您就可以确保不会丢失消息，即使 workers 偶尔会挂。

没有任何消息会超时，当消费者挂了，RabbitMQ 会重新传递消息。即使处理一条消息需要非常长的时间，这也没有关系。

默认情况下，手动消息确认是打开的，在前面的示例中，我们通过 `autoAck=true` 标志显式地关闭了它们。现在可以将此标志设置为 false，并在完成任务从 worker 发送确认消息。

```java
channel.basicQos(1); // accept only one unack-ed message at a time (see below)

DeliverCallback deliverCallback = (consumerTag, delivery) -> {
  String message = new String(delivery.getBody(), "UTF-8");

  System.out.println(" [x] Received '" + message + "'");
  try {
    doWork(message);
  } finally {
    System.out.println(" [x] Done");
    channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
  }
};
boolean autoAck = false;
channel.basicConsume(TASK_QUEUE_NAME, autoAck, deliverCallback, consumerTag -> { });
```

使用这个代码，可以确保即使通过 CTRL+C 杀死一个正在处理消息的 worker，也不会丢失任何消息。在该 worker 挂掉后不久，所有未确认的消息将被重新传递。

消息确认必须与它接收时使用的同一个通道（channel），尝试使用不同的通道将导致通道级别协议异常。

**忘记确认**

忘记使用 `basicAck` 进行消息确认会经常发生。这是个简单的错误，但是后果很严重。当你退出客户端后，消息会被重新交付（这看起来像是随机的重新交付），但是 RabbitMQ 将消耗越来越多的内存，因为它无法释放任何未确认的消息。

为了调试这种错误，你可以使用 rabbitmqctl 工具打印出 messages_unacknowledged 字段：

```shell
sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
```

在 Windows 上，去掉 sudo：

```shell
rabbitmqctl.bat list_queues name messages_ready messages_unacknowledged
```



## 消息持久化

我们学习了如何确保即使消费者挂了，任务也不丢失。但是如果 RabbitMQ 服务器停止，我们的任务仍然会丢失。

当 RabbitMQ  退出或崩溃时，它将忘记队列和消息，除非你告诉它不要这样做。确保消息不丢失我们需要两件事：我们需要将队列和消息都标记为持久的。

首先，我们需要确保 RabbitMQ 永远不会丢失队列。为了做到这一点，我们需要声明它是 持久的。

```java
boolean durable = true;
channel.queueDeclare("hello", durable, false, false, null);
```

尽管这段代码本身是正确的，但它在我们当前的设置中不生效，这是因为我们已经定义了一个名为 `hello` 的队列，它不是持久的，RabbitMQ 不允许您使用不同的参数重新定义现有的队列，并将向尝试这样做的任何程序返回错误。但这有一个快速的解决方案 -- 让我们声明一个具有不同名称的队列，例如 `task_queue`：

```java
boolean durable = true;
channel.queueDeclare("task_queue", durable, false, false, null);
```

这个队列声明的改动需要同时应用于生产者代码合消费者代码。

现在我们可以确保，即使 RabbitMQ 重启， `task_queue` 队列也不会丢失。现在我们需要标记消息持久化，通过设置 `MessageProperties`（实现了 `BasicProperties`） 的值为 `PERSISTENT_TEXT_PLAIN`。

```java
import com.rabbitmq.client.MessageProperties;

channel.basicPublish("", "task_queue",
            MessageProperties.PERSISTENT_TEXT_PLAIN,
            message.getBytes());
```

**关于消息持久化的说明**

标记消息持久化并不完全保证消息不会丢失。尽管配置了 RabbitMQ 将消息保存到磁盘，但是当 RabbitMQ 接收了一条消息并且还没有保存它时，仍然有一个很短的时间窗口。此外，RabbitMQ 并不对每条消息都执行 fsync(2) -- 它可能只是被保存到缓存中，而不是真正写到磁盘上。持久性保证并不强，但是对于我们简单的任务来说已经足够了。如果您需要更强的保证，您可以使用 [publisher confirms](https://www.rabbitmq.com/confirms.html).



## 公平分发

你可能已经注意到分派仍然不完全满足我们的预期。例如，在两个 worker 的情况下，当所有奇数号的消息任务是繁重的，偶数号的消息任务是轻松的，一个 worker 将会不断忙碌，另一个将几乎没任何工作。RabbitMQ 对此一无所知，仍然会均匀地分发消息。

出现这种情况是因为当消息进入队列时，RabbitMQ 只是分派一条消息，它不查看某个消费者未确认的消息数量，它只是盲目地将第 n 条消息分派给第 n 个消费者。

![img](https://www.rabbitmq.com/img/tutorials/prefetch-count.png)

为了解决这个问题，我们可以在 `basicQos` 方法中设置值 `prefetchCount = 1`。这是在告诉 RabbitMQ 不要一次向 RabbitMQ 发送多个消息。换句话说，在 worker 处理并确认千亿条消息之前，不要向其发送新消息。相反，它将把它发送给下一个不忙的 worker。

```java
int prefetchCount = 1;
channel.basicQos(prefetchCount);
```

**关于队列大小的说明**

如果所有的 worker 都很忙，你的队列可以排满，你需要关注这种情况，也许需要增加更多的 worker，或者有其他的策略。



## 整合所有的代码

NewTask.java 最终的代码：

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.MessageProperties;

public class NewTask {

  private static final String TASK_QUEUE_NAME = "task_queue";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    try (Connection connection = factory.newConnection();
         Channel channel = connection.createChannel()) {
        channel.queueDeclare(TASK_QUEUE_NAME, true, false, false, null);

        String message = String.join(" ", argv);

        channel.basicPublish("", TASK_QUEUE_NAME,
                MessageProperties.PERSISTENT_TEXT_PLAIN,
                message.getBytes("UTF-8"));
        System.out.println(" [x] Sent '" + message + "'");
    }
  }

}
```

Worker.java 最终的代码：

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

public class Worker {

  private static final String TASK_QUEUE_NAME = "task_queue";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    final Connection connection = factory.newConnection();
    final Channel channel = connection.createChannel();

    channel.queueDeclare(TASK_QUEUE_NAME, true, false, false, null);
    System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

    channel.basicQos(1);

    DeliverCallback deliverCallback = (consumerTag, delivery) -> {
        String message = new String(delivery.getBody(), "UTF-8");

        System.out.println(" [x] Received '" + message + "'");
        try {
            doWork(message);
        } finally {
            System.out.println(" [x] Done");
            channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
        }
    };
    channel.basicConsume(TASK_QUEUE_NAME, false, deliverCallback, consumerTag -> { });
  }

  private static void doWork(String task) {
    for (char ch : task.toCharArray()) {
        if (ch == '.') {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException _ignored) {
                Thread.currentThread().interrupt();
            }
        }
    }
  }
}
```

使用消息确认和 `prefetchCount ` 可以设置一个工作队列。持久化选项可以在 RabbitMQ 重启的情况下保证任务存活。

有关 `Channel` 方法和 `MessageProperties` 的更多信息请查阅 [JavaDocs online](https://rabbitmq.github.io/rabbitmq-java-client/api/current/).