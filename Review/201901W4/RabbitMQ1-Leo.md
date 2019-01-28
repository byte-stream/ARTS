# RabbitMQ1 - Hello World

注：本文为翻译

**原文地址：https://www.rabbitmq.com/tutorials/tutorial-one-java.html**

##简介

RabbitMQ 是一个消息代理（消息中间件）：接收以及转发消息。你可以把它想象成一个邮局：当你把你想要寄的邮件放入邮箱时，你可以确信邮递员最终会把邮件寄给你的收件人。在这个类比中，RabbitMQ 是一个邮箱、一个邮局和一个邮递员。

RabbitMQ 和邮局主要区别在于它不处理纸张，而是接收、存储并且转发二进制数据消息。

RabbitMQ 和消息通常使用一些术语。

- 生产只不过是发送，发送消息的程序是生产者：

  ![img](https://www.rabbitmq.com/img/tutorials/producer.png)

- 队列是一个驻留在 RabbitMQ 中邮箱的名称。尽管消息流经 RabbitMQ 和应用程序，但它们只能存储在队列中。队列只受主机内存和磁盘的限制，它本质上是一个大型消息缓冲区。许多生产者可以发送消息到一个队列，许多消费者可以尝试从一个队列接收数据。这是我们表示队列的方式：

  ![img](https://www.rabbitmq.com/img/tutorials/queue.png)

- 消费与接收有相似的含义。消费者是一个主要等待接收消息的程序：

  ![img](https://www.rabbitmq.com/img/tutorials/consumer.png)

请注意，生产者、消费者和代理不必在同一台主机；实际上在许多应用中确实如此。同时，一个程序既可以是生产者，也可以是消费者。



## “Hello World”

在这一节中，我们将使用 Java 编写两个程序：发送单个消息的生产者和接受消息并将其打印出来的消费者。我们将会忽略 Java API 中的一些细节，专注于一个非常简单的例子作为开始，它是一个 「Hello World」消息。

在下面的图表中，「P」是生产者，「C」是消费者。中间的方块是队列 - RabbitMQ 代表消费者保存的消息缓冲区。

![img](https://www.rabbitmq.com/img/tutorials/python-one.png)

### 

> #### 拓展：Java 客户端库
>
> RabbitMQ 使用多种协议，本教程使用 AMQP 0-9-1，这是一种开放的，通用的消息传递协议。RabbitMQ 有许多不同语言的客户端，我们使用 RabbitMQ 提供的 Java 客户端。
>
> 下载[客户端库](http://central.maven.org/maven2/com/rabbitmq/amqp-client/5.5.1/amqp-client-5.5.1.jar)以及它的依赖（[SLF4J API](http://central.maven.org/maven2/org/slf4j/slf4j-api/1.7.25/slf4j-api-1.7.25.jar)和 [SLF4J Simple](http://central.maven.org/maven2/org/slf4j/slf4j-simple/1.7.25/slf4j-simple-1.7.25.jar)），将这些文件复制到你的工作目录。
>
> 请注意，对本教程来说，SLF4J Simple 已经足够了，但是在生产环境中你应该使用完整的日志比如 [Logback](https://logback.qos.ch/)。
>
> RabbitMQ Java 客户端也存在于 Maven 中央仓库，groupId 是 `com.rabbitmq`，artifactId 是 `amqp-client`



现在有了  Java 客户端以及依赖包，我们可以编写一些代码。

#### 发送

![img](https://www.rabbitmq.com/img/tutorials/sending.png)

我们将调用消息发布者（生产者）Send 和消息消费者（消费者）Recv。生产者会连接到 RabbitMQ ，发送一条消息，然后退出。

在 Send.java 中，我们需要导入一些类

```java
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
```

创建及初始化设置一个类并命名队列：

```java
public class Send {
  private final static String QUEUE_NAME = "hello";
  public static void main(String[] argv) throws Exception {
      ...
  }
}  
```

然后创建服务器连接：

```java
ConnectionFactory factory = new ConnectionFactory();
factory.setHost("localhost");
try (Connection connection = factory.newConnection();
     Channel channel = connection.createChannel()) {

}
```

该连接对 socket 连接进行了抽象，并负责协议版本协商和身份验证等。在这里我们连接到本地机器上的代理 - 即本地主机。如果我们想要连接到另一台机器上的代理，只需要指定它的名称或 IP 地址。

接下来，我们创建一个通道，其中存放了大多数用于完成任务的 API。注意，我们可以使用 `try-with-resources  `语句，因为 `Connection` 和 `Channel` 都实现了 `java.io.Closeable` 接口，通过这种方式我们不需要在代码中显式地关闭它们。

要发送消息，必须声明要发送到的队列，然后我们将消息发布到队列，所有这些都在 `try-with-resources` 语句块中：

```java
channel.queueDeclare(QUEUE_NAME, false, false, false, null);
String message = "Hello World!";
channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
System.out.println(" [x] Sent '" + message + "'");
```

声明队列是幂等的 - 只有在队列不存在时才创建队列。消息内容是一个字节数组，因此可以在其中对任何内容进行编码。

[这里是完整的 Send.java 类](http://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/Send.java)

> #### 发送不生效
>
> 如果这是你第一次使用 RabbitMQ，你没有看到发送的消息，然后你可能会摸不着头脑，想知道出了什么问题。可能是代理启动时没有足够的磁盘空间（默认情况下需要至少 200 MB 空闲空间），因此代理拒绝接受消息。检查代理日志文件以确认并且在必要时减少限制。[配置文件文档](http://www.rabbitmq.com/configure.html#config-items) 会引导你如何设置磁盘限制



#### 接收

以上是生产者（消息发布者）。消费者监听来自 RabbitMQ 的消息，因此与发送单个消息的生产者不同，我们将它保持运行状态，持续监听消息并且将其输出。

![img](https://www.rabbitmq.com/img/tutorials/receiving.png)

消费者相关的代码（[Recv.java](http://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/Recv.java)）导入的类和 [Send.java](http://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/Send.java) 几乎一样。

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;
```

额外的 `DefaultConsumer`  是实现了 `Consumer` 接口的类，我们将使用这个接口来缓冲服务器推送给我们的消息。

初始设置一个类与生产者是一样的，打开一个连接和通道，并且声明要从中消费的队列，需要注意的是，声明的队列要与生产者声明的队列名称匹配。

```java
public class Recv {

  private final static String QUEUE_NAME = "hello";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    Connection connection = factory.newConnection();
    Channel channel = connection.createChannel();

    channel.queueDeclare(QUEUE_NAME, false, false, false, null);
    System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

  }
}
```

注意我们在这里也声明了队列，因为我们可能在启动生产者之前启动消费者，我们要确保，在尝试消费消息之前，消息队列已经存在。

为什么这里不使用 `try-with-resource`语句去自动关闭通道和连接呢？这样做的话我们只需让程序运行、关闭连接，然后退出！这不合适，因为我们希望程序保持运行状态，以让消费者监听异步到达的消息。

我们将告诉服务器向我们发送来自队列的消息。因为它将异步地推送消息，所以我们以对象的形式提供回调，它将缓存消息，直到我们准备使用它为止。这就是 `DeliverCallback` 类所做的。

```java
DeliverCallback deliverCallback = (consumerTag, delivery) -> {
    String message = new String(delivery.getBody(), "UTF-8");
    System.out.println(" [x] Received '" + message + "'");
};
channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> { });
```

[这里是完整的 Recv.java 类](http://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/Recv.java)



#### 查看队列

你可能希望了解 RabbitMQ 有哪些队列以及其中有多少消息，可以使用 rabbitmqctl 工具（需要有足够权限）查看：

Linux 下：

```shell
sudo rabbitmqctl list_queues
```

Windows 下：

```bash
rabbitmqctl.bat list_queues
```



## 生产(非)适用性免责声明

请记住，这只是教程。只是演示一些新的概念，可能会有意地建华一些事情而忽略其他的。例如，为了简洁起见，连接管理、错误处理、连接恢复、并发性和度量搜集等主题在很大程度上被省略。这种简化的代码不应该被认为可以投入生产。

在使用您的应用程序之前，请查看其余的文档。我们特别推荐以下指南:[发布者确认和消费者确认](https://www.rabbitmq.com/confirms.html)、[生产检查表](https://www.rabbitmq.com/production-checklist.html)和[监控](https://www.rabbitmq.com/monitoring.html)。