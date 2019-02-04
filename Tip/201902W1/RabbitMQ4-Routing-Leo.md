# RabbitMQ4 - Routing

为了保持专注做一件事情并尽快做完，于是最近把除算法以外的三个指标都写成 RabbitMQ 相关的，否则一周翻译学习一篇太慢了，学个 RabbitMQ 不知道要学到啥时候。

注：本文为翻译

**原文地址：https://www.rabbitmq.com/tutorials/tutorial-four-java.html**



## 路由

在前一章我们构建了一个简单的日志系统，我们能够向许多接收者广播日志消息。

在本章中，我们将向它添加一个特性，我们将使它只订阅消息的一个子集。例如，我们只将关键错误消息定向到日志文件（以节省磁盘空间），同时仍然能够在控制台打印所有日志消息。



## 绑定

在前一个例子中，我们已经创建了绑定。你可能会想起如下代码：

```java
channel.queueBind(queueName, EXCHANGE_NAME, "");
```

一个绑定是交换器和队列之间的关系。这可以简单地理解为：队列对来自此交换器的消息感兴趣。

绑定可以接受额外的 `routingKey` 参数。为了避免与 `basic_publish` 参数混淆，我们可以将它称为 `binding key`。这是我们如何创建一个带有 key 的 binding：

```java
channel.queueBind(queueName, EXCHANGE_NAME, "black");
```

绑定键的含义取决于交换类型。我们之前使用的 fanout 交换器会忽略这个值。



## Direct 交换器

上一章中，我们的日志系统向所有消费者广播所有消息。我们希望对其进行扩展，以允许根据消息的重要级别对其进行过滤。例如，我们希望只把关键的错误消息写入到磁盘，而不是在警告或者信息级别的日志消息上浪费磁盘空间。

我们使用的是 fanout 交换器，这并没有给我们多大的灵活性 - 它只会不假思索地广播。

我们将改用 direct 交换器。direct 交换器背后的路由算法很简单 - 消息进入的队列满足 binding key 与 routing key 完全匹配。

为了说明这一点，请考虑以下设置：

![img](https://www.rabbitmq.com/img/tutorials/direct-exchange.png)

在这个设置中，我们可以看到 direct 交换器 X 与两个队列绑定在一起。第一个队列用绑定键 orange 绑定，第二个队列有两个绑定，一个绑定键为 black，另一个绑定键为 green。

在这种设置中，使用路由键 orange 发布到交换器中的消息将被路由到队列 Q1，black 和 green 路由键的消息将被转发到 Q2，其他所有消息将被丢弃。



## Multiple bindings

![img](https://www.rabbitmq.com/img/tutorials/direct-exchange-multiple.png)

使用相同的绑定键绑定多个队列是完全合理的。在我们的示例中，我们可以使用 black 绑定键在 X 和 Q1 之间添加绑定，在这种情况下，direct 交换方式表现得像 fanout 方式，并将消息广播到所有匹配的队列。带有路由键 black 的消息将同时发送到 Q1 和 Q2。



## 发送日志

我们将在日志系统中使用这个模型。我们将消息发送到 direct 类型的交换器，而不是 fanout 类型。我们将提供日志严重级别作为 routing key，这样，接收程序将能够选择它希望接收到的严重性日志，让我们首先关注发送日志。

如之前一样，我们需要先创建一个交换器：

```java
channel.exchangeDeclare(EXCHANGE_NAME, "direct");
```

然后我们开始发送消息：

```java
channel.basicPublish(EXCHANGE_NAME, severity, null, message.getBytes());
```

为了简化问题，我们假设「严重性」可以是「info」、「warning」、「error」之一。



## 订阅

接收消息的工作原理与上一章中一样，只有一个例外 - 我们将自定义所需要的严重性级别并创建对应的绑定。

```java
String queueName = channel.queueDeclare().getQueue();

for(String severity : argv){
  channel.queueBind(queueName, EXCHANGE_NAME, severity);
}
```



## 组装整个模型

![img](https://www.rabbitmq.com/img/tutorials/python-four.png)

`EmitLogDirect.java`  代码如下：

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

public class EmitLogDirect {

  private static final String EXCHANGE_NAME = "direct_logs";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    try (Connection connection = factory.newConnection();
         Channel channel = connection.createChannel()) {
        channel.exchangeDeclare(EXCHANGE_NAME, "direct");

        String severity = getSeverity(argv);
        String message = getMessage(argv);

        channel.basicPublish(EXCHANGE_NAME, severity, null, message.getBytes("UTF-8"));
        System.out.println(" [x] Sent '" + severity + "':'" + message + "'");
    }
  }
  //..
}
```



`ReceiveLogsDirect.java `代码 如下：

```java
import com.rabbitmq.client.*;

public class ReceiveLogsDirect {

  private static final String EXCHANGE_NAME = "direct_logs";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    Connection connection = factory.newConnection();
    Channel channel = connection.createChannel();

    channel.exchangeDeclare(EXCHANGE_NAME, "direct");
    String queueName = channel.queueDeclare().getQueue();

    if (argv.length < 1) {
        System.err.println("Usage: ReceiveLogsDirect [info] [warning] [error]");
        System.exit(1);
    }

    for (String severity : argv) {
        channel.queueBind(queueName, EXCHANGE_NAME, severity);
    }
    System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

    DeliverCallback deliverCallback = (consumerTag, delivery) -> {
        String message = new String(delivery.getBody(), "UTF-8");
        System.out.println(" [x] Received '" +
            delivery.getEnvelope().getRoutingKey() + "':'" + message + "'");
    };
    channel.basicConsume(queueName, true, deliverCallback, consumerTag -> { });
  }
}
```

照常编译（有关编译和类路径建议，请参阅第 1 章）。为了方便起见，我们将在运行示例时为类路径使用环境变量 $CP（在 Windows 上是 %CP%）

```bash
javac -cp $CP ReceiveLogsDirect.java EmitLogDirect.java
```

如果你只想保存「warning」和「error」级别的日志到文件中，打开终端并输入：

```bash
java -cp $CP ReceiveLogsDirect warning error > logs_from_rabbit.log
```

如果你想在终端上看到所有级别的日志消息，打开终端并输入：

```bash
java -cp $CP ReceiveLogsDirect info warning error
# => [*] Waiting for logs. To exit press CTRL+C
```

例如，要发出错误日志消息，只需输入：

```bash
java -cp $CP EmitLogDirect error "Run. Run. Or it will explode."
# => [x] Sent 'error':'Run. Run. Or it will explode.'
```

完整的代码请查看：[(EmitLogDirect.java source)](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/EmitLogDirect.java) 和 [(ReceiveLogsDirect.java source)](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/ReceiveLogsDirect.java)

下一章将介绍如何基于模式匹配侦听消息。