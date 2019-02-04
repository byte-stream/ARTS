# RabbitMQ3 - Publish/Subscribe

为了保持专注做一件事情并尽快做完，于是最近把除算法以外的三个指标都写成 RabbitMQ 相关的，否则一周翻译学习一篇太慢了，学个 RabbitMQ 不知道要学到啥时候。

注：本文为翻译

**原文地址：https://www.rabbitmq.com/tutorials/tutorial-three-java.html**



## 发布 / 订阅

在前一章中，我们创建了工作队列。工作队列背后的假设是，每个任务只交付给一个工作者。在这一部分中，我们将做一些完全不同的事情：我们将向多个消费者传递消息，这种模式称为「发布 / 订阅」

为了演示该模式，我们将构建一个简单的日志系统，它将由两个程序组成：第一个程序将发出日志消息，第二个程序将接受并打印它们。

在我们的日志系统中，接收程序的每个运行副本都将获得消息。这样我们就可以运行一个接收器并将日志定向到磁盘，同时，我们可以运行另一个接收器在屏幕上看到日志。

实际上，发布的日志消息将广播给所有接收方。



## 交换器

在前一几章，我们向队列发送和接收消息。现在是时候在 Rabbit 中引入完整的消息模型了。

让我们快速回顾一下我们在之前的章节中介绍的内容：

- 生产者是发送消息的用户应用程序
- 队列是存储消息的缓冲区
- 消费者是接收消息的用户应用程序

RabbitMQ 中消息模型的核心思想是：生产者从不直接向队列发送任何消息。实际上，生产者通常根本不知道消息是否会被传递到任何队列。

相反，生产者只能向交换器发送消息。交换是一件很简单的事情。一方面，它接收来自生产者的消息，另一个方面，它将消息推送到队列中，交换器必须明确地知道如何处理它接受到的消息。是否应该将其附加到特定队列中？它应该添加到许多队列中吗？或者它应该被丢弃。这些规则都由交换类型来定义。

![img](https://www.rabbitmq.com/img/tutorials/exchanges.png)

有几种可用的交换类型：direct、topic、headers 和 fanout。我们将关注最后一个 fanout。让我们创建这种类型的交换，并将其称为 logs：

```java
channel.exchangeDeclare("logs", "fanout");
```

fanout 交换器非常简单，正如您可能从名称猜到，它只是将接收到的所有消息广播到它知道的所有队列。这正是我们的日志记录器所需要的。



**列出交换器**

要列出服务器上的交换器，可以使用非常有用的 rabbitmqctl 工具：

```shell
sudo rabbitmqctl list_exchanges
```

在这个列表中会有一些 amq.* 交换器和默认（未命名）的交换器，这些都是默认创建的，但是您现在不太可能需要使用它们。



**无名交换器**

在前面的章节中，我们对交换器一无所知，但仍然能够将消息发送到队列。这是可能的，因为我们使用的是默认交换器，它由空字符串（""）标识。

回想一下我们之前是如何发布消息的：

```java
channel.basicPublish("", "hello", null, message.getBytes());
```

第一个参数是交换器的名称。空字符串标识默认的或没有名称的交换器：如果消息存在，则将使用路由关键字（队列名称）指定的名称将消息路由到队列。



现在，我们可以发布消息到有名称的交换器：

```java
channel.basicPublish( "logs", "", null, message.getBytes());
```



## 临时队列

您可能还记的，以前我们使用具有特定名称的队列（还记得 hello 和 task_queue 吗？）。能够命名队列对我们来说非常重要 -- 我们需要将 worker 指向相同的队列。当您希望在生产者和消费者之间共享队列时，为队列指定名称非常重要。

但对于我们的日志记录器来说，情况并非如此。我们希望了解所有日志消息，而不仅仅是其中的一个子集。我们还只对当前的消息流感兴趣，而对旧消息不感兴趣。要解决这个问题，我们需要如下两件事：

- 首先，当我们连接到 Rabbit 时，我们需要一个全新的空队列。为此，我们可以创建一个具有随机名称的队列，或者更好的方法是：让服务器为我们选择一个随机队列名称。
- 其次，一旦断开对消费者的连接，队列应该被自动删除。

在 Java 客户端中，当我们不向 queueDeclare() 提供参数时，我们将创建一个非持久的、自动删除队列，并使用生成的名称：

```java
String queueName = channel.queueDeclare().getQueue();
```

你可以在[队列指南](https://www.rabbitmq.com/queues.html)中了解关于 exclusive 标志和其他队列属性的更多信息。

此时，队列名称包含一个随机的队列名称。例如，它可能看起来像 amq.gen-JzTY20BRgKO-HjmUJj0wLg。



## Bindings

![img](https://www.rabbitmq.com/img/tutorials/bindings.png)

我们已经创建了一个 fanout 交换器和一个队列。现在我们需要告诉交换器向队列发送消息。交换器和队列之间的关系成为绑定（binding）。

```java
channel.queueBind(queueName, "logs", "");
```

从现在开始，日志交换器将向队列添加消息。



**列出 Bindings**

你可以列出现有的 bindings

```shell
rabbitmqctl list_bindings
```



## 将整个模型组装起来

![img](https://www.rabbitmq.com/img/tutorials/python-three-overall.png)

生产者发出日志消息，它看起来与前一章没有太大的不同。最重要的修改是，我们现在希望将消息发布到命名为 logs 的日志交换器中，而不是将消息发布到无名的交换器中。我们需要在发送时提供一个 routingKey，但是对于 fanout 类型的交换器，它的值被忽略了，不生效。下面是 `EmitLog.java` 程序代码：

```java
public class EmitLog {

  private static final String EXCHANGE_NAME = "logs";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    try (Connection connection = factory.newConnection();
         Channel channel = connection.createChannel()) {
        channel.exchangeDeclare(EXCHANGE_NAME, "fanout");

        String message = argv.length < 1 ? "info: Hello World!" :
                            String.join(" ", argv);

        channel.basicPublish(EXCHANGE_NAME, "", null, message.getBytes("UTF-8"));
        System.out.println(" [x] Sent '" + message + "'");
    }
  }
}
```

如您所见，在建立连接后，我们声明了交换。此步骤是必要的，因为禁止向不存在的交换器发布内容。

如果还没有队列绑定到交换器，则消息将丢失，但现在这对我们来说没问题，如果没有消费者在监听，我们可以安全地丢弃消息。

消费者 `ReceiveLogs.java` 代码如下：

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

public class ReceiveLogs {
  private static final String EXCHANGE_NAME = "logs";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    Connection connection = factory.newConnection();
    Channel channel = connection.createChannel();

    channel.exchangeDeclare(EXCHANGE_NAME, "fanout");
    String queueName = channel.queueDeclare().getQueue();
    channel.queueBind(queueName, EXCHANGE_NAME, "");

    System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

    DeliverCallback deliverCallback = (consumerTag, delivery) -> {
        String message = new String(delivery.getBody(), "UTF-8");
        System.out.println(" [x] Received '" + message + "'");
    };
    channel.basicConsume(queueName, true, deliverCallback, consumerTag -> { });
  }
}
```

像之前一样进行编译

```shell
javac -cp $CP EmitLog.java ReceiveLogs.java
```

如果您想将日志保存到文件中，只需打开控制台并输入：

```shell
java -cp $CP ReceiveLogs > logs_from_rabbit.log
```

如果您希望在屏幕上看到日志，打开一个新的终端并运行：

```shell
java -cp $CP ReceiveLogs
```

当然，要发送日志：

```shell
java -cp $CP EmitLog
```

使用 `rabbitmqctl list_bindings` 命令，您可以验证是否按预期创建了 bindings 和 队列。运行两个 ReceiveLogs.java 程序你应该会看到如下结果：

```shell
sudo rabbitmqctl list_bindings
# => Listing bindings ...
# => logs    exchange        amq.gen-JzTY20BRgKO-HjmUJj0wLg  queue           []
# => logs    exchange        amq.gen-vso0PVvyiRIL2WoV3i48Yg  queue           []
# => ...done.
```

结果很明显：来自日志交换器的数据进入两个具有服务器分配名称的队列，这正是我们预期的结果。