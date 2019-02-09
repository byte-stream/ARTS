# RabbitMQ6 - RPC

注：本文为翻译

**原文地址：https://www.rabbitmq.com/tutorials/tutorial-six-java.html**

## 远程过程调用 (RPC)

在第 2 章中，我们学习了如何试用 Work Queues 在多个 workers 之间分配耗时的任务。

但是，如果我们需要在远程计算机上运行一个函数并等待结果呢？这就得另当别论了，这种模式通常称为远程过程调用或 RPC。

在本章中，我们将使用 RabbitMQ 构建 RPC 系统，客户端和可伸缩 RPC 服务器。由于我们没有任何值得分发的耗时任务，所以我们将创建一个返回斐波那契数的虚拟 RPC 服务。



## Client 接口

为了演示如何使用 RPC 服务，我们将创建一个简单的 client 类，它将包含一个名为 call 的方法，该方法发送 RPC 请求并阻塞，直到收到返回结果：	

```java
FibonacciRpcClient fibonacciRpc = new FibonacciRpcClient();
String result = fibonacciRpc.call("4");
System.out.println( "fib(4) is " + result);
```



**RPC 注意事项**

尽管 RPC 是计算机中非常常见的模式，但它经常收到批评。当程序员不知道函数调用的是本地的还是缓慢的 RPC 时，就会出现问题。这样的迷惑在系统中会产生不可预知的结果，并增加不必要的调试复杂性。错误使用RPC 非但不能简化软件，反而会导致不可维护的意大利面条式代码。

考虑到这一点，请考虑以下建议：

- 明确那个函数调用是本地的，那个函数调用是远程的；
- 对系统做文档说明，明确各组件之间的依赖关系；
- 处理错误情况，当 RPC 服务器长时间宕机时，客户端应该如何响应？

当有疑问时，避免使用 RPC。如果可以的话，您应该使用异步管道（asynchronous pipeline）结果将异步推送到下一个计算阶段，而不是类似 RPC 的阻塞。



## 回调队列

通常，通过 RabbitMQ 执行 RPC 很容易。客户端发送请求消息，服务器返回响应详细。为了接收响应，我们需要发送一个 「回调」队列地址与请求，我们可以使用默认队列（在 Java 客户端中是独有的）：

```java
callbackQueueName = channel.queueDeclare().getQueue();

BasicProperties props = new BasicProperties
                            .Builder()
                            .replyTo(callbackQueueName)
                            .build();

channel.basicPublish("", "rpc_queue", props, message.getBytes());

// ... then code to read a response message from the callback_queue ...
```

**消息的属性**

AMQP 0-9-1 协议预先定义了一组包含 14 个属性的消息。大多数属性很少被使用，除了以下几点:

- deliveryMode：将消息标记为持久的（值为 2）或瞬态的（任何其他值），您可能还记得第2 章使用过这个属性。
- contentType：用于描述编码的 mime 类型。例如，对于经常使用的JSON 编码，最好将此属性设置为: application/ JSON。
- replyTo：通常用于命名回调队列。
- correlationId：用于将 RPC 响应与请求关联起来。

我们需要导入新的类：

```java
import com.rabbitmq.client.AMQP.BasicProperties;
```



## 关联 Id

在上述方法中，我们建议为每个 RPC 请求创建一个回调队列。这非常低效，但幸运的是，有一种更好的方法：让我们为每个客户端创建一个回调队列。

这就产生了一个新的问题，在队列中接收到响应后，并不清楚响应属于哪个请求，这就是使用 correlationId 属性时，我们会为每个请求设置一个唯一值。稍后，当我们在回调队列中接收到一条消息时，我们将查看这个属性，并在此基础上，我们将能够将响应与请求匹配起来。如果我们看到一个未知的 correlationId 值，我们可以安全地丢弃消息，因为它不属于我们的请求。

您可能会问，为什么我们应该忽略回调队列中的未知消息，而不是认为错误导致失败？这是由于服务器端存在竞争条件的可能性，虽然不太可能，但 RPC 服务器可能在发送响应之后宕机。但是在为请求发送确认消息之前宕机，如果发生这种情况，重新启动的 RPC 服务器将再次处理请求。这就是为什么在客户端我们必须优雅地处理重复响应，RPC 在理想情况下应该是幂等的。



## 总结

![img](https://www.rabbitmq.com/img/tutorials/python-six.png)

我们的 RPC 将像这样工作：

对于 RPC 请求，客户端发送具有两个属性的消息：replyTo 和 correlationId，前者设置为仅为请求创建的匿名独占队列，后者设置为每个请求的唯一值。

请求被发送到 rpc_queue 队列。

RPC 工作程序（又名：服务器）正在等待该队列上的请求。当一个请求出现时，它执行这个任务，并使用  replyTo 字段中的队列将结果发送回客户端。

客户端等待应答队列上的数据，当出现一条消息时，它检查 correlationId 属性。如果匹配请求的值，则返回应用程序的响应。



## 整合

斐波那契数任务：

```java
private static int fib(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return fib(n-1) + fib(n-2);
}
```

我们声明 fibonacci 函数。它假设只有有效的正整数输入。(不要期望这个方法适用于较大的数，它可能是最慢的递归实现)。

RPC 服务端代码：[RPCServer.java](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/RPCServer.java).

服务端代码相当简单：

像往常一样，我们首先建立连接、通道和声明队列。 

我们可能希望运行多个服务器进程。为了在多个服务器上平均分配负载，我们需要在 `channel.basicQos` 中设置 `prefetchCount` 的值。

我们使用 `basicConsume`来访问队列，在队列中，我们以对象(DeliverCallback)的形式提供一个回调函数，它将执行工作并将响应发回。

RPC 客户端代码：[RPCClient.java](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/RPCClient.java).

客户端代码稍微复杂一些：

我们建立一个连接和通道。 

我们的 `call` 方法发出实际的RPC请求。

在这里，我们首先生成一个唯一的 correlationId 号并保存它——消费者回调将使用这个值来匹配适当的响应。

然后，我们为响应创建专用的独占队列并订阅它。接下来，我们发布带有两个属性的请求消息：replyTo 和 correlationId。 

在这一点上，我们可以坐下来等待合适的响应结果。

由于消费者处理是在一个单线程中进行的，因此我们需要在响应到达之前挂起主线程，使用 `BlockQueue`是一种可能的解决方案。这里我们创建的 `ArrayBlockingQueue` 的容量设置为 1，因为我们只需要等待一个响应。

消费者正在做一项非常简单的工作，对于每一个消费的响应消息，它都会检查 correlationId 是否是我们要查找的。如果是，它将响应放入BlockingQueue。

同时，主线程正在等待从 BlockingQueue 中获取响应。

最后，我们将响应返回给用户。

客户请求：

```java
RPCClient fibonacciRpc = new RPCClient();

System.out.println(" [x] Requesting fib(30)");
String response = fibonacciRpc.call("30");
System.out.println(" [.] Got '" + response + "'");

fibonacciRpc.close();
```

现在是时候看看完整的示例源码（包括基本的异常处理）：[RPCClient.java](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/RPCClient.java) 和 [RPCServer.java](https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/java/RPCServer.java).

与之前一样编译运行代码：

```bash
javac -cp $CP RPCClient.java RPCServer.java
```

现在 RPC 服务准备好了，可以启动它：

```bash
java -cp $CP RPCServer
# => [x] Awaiting RPC requests
```

要请求一个斐波那契数运行客户端:

```bash
java -cp $CP RPCClient
# => [x] Requesting fib(30)
```

这里介绍的设计不是 RPC 服务的唯一可能实现，但是它有一些重要的优点:

- 如果RPC服务器太慢，您可以通过运行另一个RPC 服务器来进行扩展。尝试在新的控制台中运行第二个 RPCServer。 
- 在客户端，RPC 只需要发送和接收一条消息。不需要像 queueDeclare 这样的同步调用。因此，RPC客户机对于单个 RPC 请求只需要一个网络往返。

我们的代码仍然非常简单，没有试图解决更复杂(但重要)的问题，如:

- 如果没有服务器在运行，客户机应该如何响应? 
- 客户机是否应该为RPC设置某种超时? 
- 如果服务器出现故障并引发异常，是否应该将其转发给客户机? 
- 在处理之前防止无效传入消息(如检查边界、类型)。

如果您想进行试验，您可能会发现管理UI对于查看队列非常有用。