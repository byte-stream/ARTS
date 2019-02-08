# RabbitMQ5 - Topics

注：本文为翻译

**原文地址：https://www.rabbitmq.com/tutorials/tutorial-five-java.html**

## Topics

在前面的教程中，我们改进了日志系统。我们没有试用只能进行虚拟广播的 `fanout` 交换器，而是使用了 `direct` 交换器，并实现了选择性接受日志。

虽然使用了 `direct` 交换器改进了我们的系统，但它仍然有局限性 - 不能基于多个条件进行路由。

在我们的日志系统中，我们可能不仅希望订阅基于严重级别的日志，还希望基于发出日志源进行订阅。你可能从 `syslog unix`工具了解这个概念，该工具根据严重级别（info/warn/crit...）和功能（auto/cron/kern）路由日志。

这将给我们带来很大的灵活性 - 我们可能希望只监听来自 「cron」的关键错误，但也要监听来自「kern」的所有日志。

为了在日志系统中实现这一点，我们需要学习更复杂的 `topic` 交换器的知识。

## Topic 交换器

发送到 `topic` 交换器的消息不能是任意的 `routing_key` - 它必须是单词列表，由点分隔。可以是任意单词，但通常他们指定与消息连接的一些特性。几个有路由键的示例：「stock.usd.nyse」、「nyse.vmw」、「quick.range.rabbit」。路由键中可以有任意多的单词，最多 255 字节。

绑定键的形式也必须相同，topic 交换器背后的逻辑类似于 direct 交换器 - 使用特定路由键发送的消息将被传递到符合模式匹配绑定键绑定的所有队列。然而，绑定键有两种重要的特殊情况：

- *（星号）只能替代一个单词
- \#（井号）可以代替零个或多个单词

用一个例子来解释这个问题最简单：

![img](https://www.rabbitmq.com/img/tutorials/python-five.png)

在本例中，我们将发送描述动物的消息。消息将使用由三个单词（两个点）组成的路由键发送，第路由键中的第一个单词将描述速度，第二个单词描述颜色，第三个单词描述物种：「<速度>.<颜色>.<物种>」。

我们创建了三个 `binding`：Q1  使用绑定键「\*.orange.\*」、Q2 是 「\*.\*.rabbit」和 「lazy.\#」。

这些 binding 可以概括为：

- Q1 对所有橙色的动物都感兴趣
- Q2 对兔子以及 lazy 属性的动物感兴趣

一条路由键设置为 「quick.orange.rabbit」的消息，将被传递到两个队列。「lazy.orange.elephant」也会被传递到两个队列。「quick.orange.fox」将只会传递到第一个队列，「lazy.brown.fox」只会传递到第二个队列，「lazy.pink.rabbit」只会被传递到第二个对类一次，即使它匹配了两个绑定，「quick.brown.fox」不匹配任何绑定，因此会被丢弃。

如果我们违反规则，发送一个或者四个单词的路由键的消息，比如「orange」或「quick.orange.male.rabbit」，会发生什么？这些消息将不匹配任何绑定，并将丢失。

另外，尽管「lazy.orange.male.rabbit」有四个单词，但它将匹配最后一个绑定，并将发送到第二个队列。

**Topic 交换器**

Topic 交换器功能强大，可以像其他交换器一样工作。

当队列被「\#」绑定时，它将接受所有消息，无论路由键是什么 - 就像 `fanout` 交换器一样

不使用特殊符号「\*」和「\#」时，topic 交换器就像 direct 交换器一样。



## 将整个模型组装起来

我们将在日志系统中使用 topic 交换器，我们将从一个工作假设开始，即日志的路由键将有两个单词：「\<facility\>.\<severity\>」。

代码与前一章几乎一样。

`EmitLogTopic.java`

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

public class EmitLogTopic {

  private static final String EXCHANGE_NAME = "topic_logs";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    try (Connection connection = factory.newConnection();
         Channel channel = connection.createChannel()) {

        channel.exchangeDeclare(EXCHANGE_NAME, "topic");

        String routingKey = getRouting(argv);
        String message = getMessage(argv);

        channel.basicPublish(EXCHANGE_NAME, routingKey, null, message.getBytes("UTF-8"));
        System.out.println(" [x] Sent '" + routingKey + "':'" + message + "'");
    }
  }
  //..
}
```



`ReceiveLogsTopic.java:`

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

public class ReceiveLogsTopic {

  private static final String EXCHANGE_NAME = "topic_logs";

  public static void main(String[] argv) throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost("localhost");
    Connection connection = factory.newConnection();
    Channel channel = connection.createChannel();

    channel.exchangeDeclare(EXCHANGE_NAME, "topic");
    String queueName = channel.queueDeclare().getQueue();

    if (argv.length < 1) {
        System.err.println("Usage: ReceiveLogsTopic [binding_key]...");
        System.exit(1);
    }

    for (String bindingKey : argv) {
        channel.queueBind(queueName, EXCHANGE_NAME, bindingKey);
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

如前几章一样编译和运行代码，在 Windows 中，将 $CP 换成 %CP%

编译：

```bash
javac -cp $CP ReceiveLogsTopic.java EmitLogTopic.java
```

接收所有日志：

```bash
java -cp $CP ReceiveLogsTopic "#"
```

接收所有来自「kern」的日志：

```bash
java -cp $CP ReceiveLogsTopic "kern.*"
```

仅接受「critical」的日志：

```bash
java -cp $CP ReceiveLogsTopic "*.critical"
```

你可以创建多个绑定：

```bash
java -cp $CP ReceiveLogsTopic "kern.*" "*.critical"
```

发送一个路由键为「kern.critical」的日志：

```bash
java -cp $CP EmitLogTopic "kern.critical" "A critical kernel error"
```

注意，代码没有对路由和绑定键做任何假设，您可以试用两个以上的路由键参数。

完整源码：[EmitLogTopic.java](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/EmitLogTopic.java)  [ReceiveLogsTopic.java](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/ReceiveLogsTopic.java)