## Java ExecutorService and 线程池

**原文地址：<https://www.callicoder.com/java-executor-service-and-thread-pool-tutorial/>**

**原文作者：Rajeev Kumar Singh **

### Executors Framework

​	在之前的章节中，我们学习了在Java中继承Thread类或实现Runnable接口来创建一个线程。

​	虽然这可以使得创建一个或二个线程并运行它们非常容易，当时当你的应用需要创建20或者30个线程来并发的运行任务时，使用之前的方式将会出现问题。

​	而且，毫不夸张的说，大型多线程应用如果没有同时运行数千个线程也将会运行着数百个线程。所以，将线程的创建和管理从应用的其余部分分离开是有意义的。

**我们来看看Executors，这是一个创建和管理线程的框架。**

1. 线程创建：它提供了多种方法对于创建线程，更具体的说是一个线程池，你的应用能使用它来并发的运行任务。
2. 线程管理：它管理着在线程池中线程的生命周期。你不需要担心线程池中的线程是运行的还是阻塞的或是死亡的在提交一个可执行的任务之前。
3. 任务的提交和执行：Executors框架提供了在线程池中提交执行任务的多个方法，并且给予你权力决定这些任务将何时被执行。例如，你可以提交一个现在要执行的任务或者是稍后要执行的任务或者是定期执行的任务。

Java 并发API定义了以下三种executor接口，它们包括创建和管理线程需要的所有内容。

- Executor - 一个简单的接口包含一个方法execute() 用于启动一个由Runnable对象指定的任务。
- ExecutorService - 是Executor的子接口，它添加了管理任务生命周期的功能。
- ScheduledExecutorService -  ExecutorService 的子接口，它添加了定期执行任务的功能。

除了上面的三个接口，并发API还提供了一个Executors类，该类包含了创建不同类型Executor服务的工厂方法。

### ExecutorService 案例

让我们来看一下一个简单的例子来更好的理解它。在下面的例子中，我们首先使用一个工作者线程创建了一个ExecutorService,然后提交了一个要在工作者线程内部执行的任务。

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ExecutorsExample {
    public static void main(String[] args) {
        System.out.println("Inside : " + Thread.currentThread().getName());

        System.out.println("Creating Executor Service...");
        ExecutorService executorService = Executors.newSingleThreadExecutor();

        System.out.println("Creating a Runnable...");
        Runnable runnable = () -> {
            System.out.println("Inside : " + Thread.currentThread().getName());
        };

        System.out.println("Submit the task specified by the runnable to the executor service.");
        executorService.submit(runnable);
    }
}
```

```java
# Output
Inside : main
Creating Executor Service...
Creating a Runnable...
Submit the task specified by the runnable to the executor service.
Inside : pool-1-thread-1		
```

上面的例子展示了怎样创建一个executor服务并在executor中执行任务。我们使用Executors.newSingleThreadExecutor()方法创建了一个ExecutorService，它使用了单个的工作者线程执行任务。如果一个任务被提交执行而当前线程忙于其他任务，则新任务将在队列中等待直到线程空闲。

如果你跑上面的程序，你将注意到这个程序没有退出，因为这个executor服务将一直保持对新任务的监听直到我们显示的关闭它。

### 关闭ExecutorService

ExecutorService提供了两个方法关闭executor

- shutdown() - 当executor service调用shutdown()方法后，它将停止接收新任务，然后等待之前提交的任务完成，然后关闭executor。
- shutdownNow() - 这个方法将中断线程，停止正在运行的任务，并立即关闭executor。

我们可以在我们程序的最后添加这段代码，让它可以优雅的退出

```
System.out.println("Shutting down the executor");
executorService.shutdown();
```

### 包含多个线程和多任务的ExecutorService

​	在之前的例子中，我们使用一个工作线程创建了一个ExecutorService。但是ExecutorService真正强大的力量来自于创建线程池并且在线程池中并发的执行多个任务。

​	下面的例子，展示了创建线程池和并发执行多个任务的executor service

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ExecutorsExample {
    public static void main(String[] args) {
        System.out.println("Inside : " + Thread.currentThread().getName());

        System.out.println("Creating Executor Service with a thread pool of Size 2");
        ExecutorService executorService = Executors.newFixedThreadPool(2);

        Runnable task1 = () -> {
            System.out.println("Executing Task1 inside : " + Thread.currentThread().getName());
            try {
                TimeUnit.SECONDS.sleep(2);
            } catch (InterruptedException ex) {
                throw new IllegalStateException(ex);
            }
        };

        Runnable task2 = () -> {
            System.out.println("Executing Task2 inside : " + Thread.currentThread().getName());
            try {
                TimeUnit.SECONDS.sleep(4);
            } catch (InterruptedException ex) {
                throw new IllegalStateException(ex);
            }
        };

        Runnable task3 = () -> {
            System.out.println("Executing Task3 inside : " + Thread.currentThread().getName());
            try {
                TimeUnit.SECONDS.sleep(3);
            } catch (InterruptedException ex) {
                throw new IllegalStateException(ex);
            }
        };


        System.out.println("Submitting the tasks for execution...");
        executorService.submit(task1);
        executorService.submit(task2);
        executorService.submit(task3);

        executorService.shutdown();
    }
}
```

```java
# Output
Inside : main
Creating Executor Service with a thread pool of Size 2
Submitting the tasks for execution...
Executing Task2 inside : pool-1-thread-2
Executing Task1 inside : pool-1-thread-1
Executing Task3 inside : pool-1-thread-1
```

上面的例子中，我们创建了一个线程池大小为2的executor 服务。一个固定的线程池是非常常见的线程池类型，经常被使用在多线程的应用中。

在一个固定的线程池中，executor 服务确保线程池总是有固定数量的线程在运行。如果任何一个线程由于某些原因死亡了，它将立即被其他线程替代。

当有新任务被提交时，executor服务将从线程池中挑选一个可用线程，并在这个线程上执行任务。如果我们提交更多的任务超过可用的线程数量，则所有的线程将忙于执行已经存在的任务，然后新的任务将在队列中等待。

### 线程池

​	大多数的executor实现都是用线程池来执行任务。一个线程池只不过是一堆工作者线程，它们独立于Runnable或Callable任务，由executor管理。

​	创建一个线程时非常昂贵的操作，它应该被最小化限制。拥有工作者线程可以将线程的创建开销最小化。executor服务使得我们只需要创建一次线程池，然后便可以重用线程执行任何任务。

​	在前面的章节中，我们已经看到了一个线程池的例子。它被称为固定线程池。

​	任务通过一个被称为Blocking Queue的中间队列提交到线程池。如果任务数量超过活动线程的数量，它们将被插入到阻塞队列中等待直到线程可用。如果阻塞队列是满的，新任务将被拒绝。

![](<https://www.callicoder.com/assets/images/post/large/executor-service-thread-pool-blocking-queue-example.jpg>)

### ScheduledExecutorService案例

ScheduledExecutorService 通常被用于定期或指定延迟之后执行任务。

在下面的例子中，我们指定一个任务在延迟5秒之后执行。

```java
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class ScheduledExecutorsExample {
    public static void main(String[] args) {
        ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(1);
        Runnable task = () -> {
          System.out.println("Executing Task At " + System.nanoTime());
        };

        System.out.println("Submitting task at " + System.nanoTime() + " to be executed after 5 seconds.");
        scheduledExecutorService.schedule(task, 5, TimeUnit.SECONDS);
        
        scheduledExecutorService.shutdown();
    }
}
```

```java
# Output
Submitting task at 2909896838099 to be executed after 5 seconds.
Executing Task At 2914898174612
```

scheduledExecutorService.schedule()函数包括一个Runnable,一个延迟指定值和一个延迟的时间单位。

上面的程序在提交5秒后执行任务。

现在让我们来看一个定期执行任务的例子。

```java
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class ScheduledExecutorsPeriodicExample {
    public static void main(String[] args) {
        ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(1);

        Runnable task = () -> {
          System.out.println("Executing Task At " + System.nanoTime());
        };
        
        System.out.println("scheduling task to be executed every 2 seconds with an initial delay of 0 seconds");
        scheduledExecutorService.scheduleAtFixedRate(task, 0,2, TimeUnit.SECONDS);
    }
}
```

```java
# Output
scheduling task to be executed every 2 seconds with an initial delay of 0 seconds
Executing Task At 2996678636683
Executing Task At 2998680789041
Executing Task At 3000679706326
Executing Task At 3002679224212
.....
```

scheduledExecutorService.scheduleAtFixedRate()方法包含一个Runnable，一个初始化延迟值，一个任务执行周期和一个时间单位。它在指定的延迟时间后开始执行给定的任务，然后定期地在period值指定的时间间隔中执行任务。	

注意，如果任务遇到异常，任务的后续执行将被取消。否则，任务仅在关闭executor或杀死程序时才会被终止。