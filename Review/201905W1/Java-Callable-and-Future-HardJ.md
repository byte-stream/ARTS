## Java Callable and Future

**原文地址：<https://www.callicoder.com/java-callable-and-future-tutorial/>**

**原文作者：Rajeev Kumar Singh **

### Callable

​	Java提供了一个Callable接口来定义一个执行任务并返回结果。Callable接口和Runnable类似，不同的是它可以返回一个结果并返回一个受检查的异常。

​	Callable接口只有一个call()方法，这个方法包含了一个线程可以执行的代码。这是一个简单的Callable例子。

```java
Callable<String> callable = new Callable<String>() {
    @Override
    public String call() throws Exception {
        // Perform some computation
        Thread.sleep(2000);
        return "Return some result";
    }
};
```

​	使用Callable，你不需要使用try/catch代码块包含Thread.sleep()，因为Callable不同于Runnable，Callable可以抛出一个受检查异常。

​	你也可以使用一个lambda表达式

```java
Callable<String> callable = () -> {
    // Perform some computation
    Thread.sleep(2000);
    return "Return some result";
};
```

#### 使用ExecutorService执行Callable任务，使用Future获取结果

​	与Runnable类似，你能提交Callable给executor service来执行。但是Callable结果呢？怎么访问它？

​	executor service的submit()方法提交一个任务让线程执行。然而，你不知道提交任务的执行结果什么时候可用。因此，提交一个Callable任务后将返回一个Future对象，这个对象能够在结果可用的时候获取。

​	Future类似于其他语言中的Promise，例如Javascript。它表示将来某个时间点完成一个计算结果。

​	下面是一个Future 和 Callable的例子

```java
import java.util.concurrent.*;

public class FutureAndCallableExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ExecutorService executorService = Executors.newSingleThreadExecutor();

        Callable<String> callable = () -> {
            // Perform some computation
            System.out.println("Entered Callable");
            Thread.sleep(2000);
            return "Hello from Callable";
        };

        System.out.println("Submitting Callable");
        Future<String> future = executorService.submit(callable);

        // This line executes immediately
        System.out.println("Do something else while callable is getting executed");

        System.out.println("Retrieve the result of the future");
        // Future.get() blocks until the result is available
        String result = future.get();
        System.out.println(result);

        executorService.shutdown();
    }

}
```

```java
# Output
Submitting Callable
Do something else while callable is getting executed
Retrieve the result of the future
Entered Callable
Hello from Callable
```

ExecutorService.submit()方法可以返回一个Future。一旦获得了Future，你在你提交执行任务的同时并行执行其他任务，然后通过future.get()方法来接收future的返回结果。

注意，get()方法将一直阻塞直到任务完成。Future接口也提供了isDone()方法用于检查任务是否完成。

```java
import java.util.concurrent.*;

public class FutureIsDoneExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ExecutorService executorService = Executors.newSingleThreadExecutor();

        Future<String> future = executorService.submit(() -> {
            Thread.sleep(2000);
            return "Hello from Callable";
        });

        while(!future.isDone()) {
            System.out.println("Task is still not done...");
            Thread.sleep(200);
        }

        System.out.println("Task completed! Retrieving the result");
        String result = future.get();
        System.out.println(result);

        executorService.shutdown();
    }
}
```

```java
# Output
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task completed! Retrieving the result
Hello from Callable
```

#### 取消 Future

​	你能可以使用Future.cancel()方法取消Future。这个方法尝试取消任务的执行，当取消成功后将返回true，否则返回false。

​	cancel()方法接受一个boolean类型的参数 -- mayInterruptIfRunning。如果你使用true代替这个参数，则当前正在执行任务的线程将被打断，否则正在执行的任务将继续执行直到执行完成。

​	你可以使用isCancelled()方法来检查任务是否被取消。在取消任务后，isDone()将总是为true。

```java
import java.util.concurrent.*;

public class FutureCancelExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ExecutorService executorService = Executors.newSingleThreadExecutor();

        long startTime = System.nanoTime();
        Future<String> future = executorService.submit(() -> {
            Thread.sleep(2000);
            return "Hello from Callable";
        });

        while(!future.isDone()) {
            System.out.println("Task is still not done...");
            Thread.sleep(200);
            double elapsedTimeInSec = (System.nanoTime() - startTime)/1000000000.0;

            if(elapsedTimeInSec > 1) {
                future.cancel(true);
            }
        }

        System.out.println("Task completed! Retrieving the result");
        String result = future.get();
        System.out.println(result);

        executorService.shutdown();
    }
}
```

```java
# Output
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task is still not done...
Task completed! Retrieving the result
Exception in thread "main" java.util.concurrent.CancellationException
        at java.util.concurrent.FutureTask.report(FutureTask.java:121)
        at java.util.concurrent.FutureTask.get(FutureTask.java:192)
        at FutureCancelExample.main(FutureCancelExample.java:34)
```

​	如果允许上面程序，将抛出一个异常，因为future.get()方法将抛出`CancellationException`，如果任务已经被取消。我们能处理这个异常通过在接收结果前检查future是否被取消。

```java
if(!future.isCancelled()) {
    System.out.println("Task completed! Retrieving the result");
    String result = future.get();
    System.out.println(result);
} else {
    System.out.println("Task was cancelled");
}
```

#### 添加Timeouts

​	future.get()方法将阻塞并等待当前任务完成。如果你调用一个远程的服务在Callable实现中，但远程服务关闭了，则future.get()方法将永远被阻塞，这将导致当前应用失去响应。

​	为了防止这种情况，你可以在get()方法中添加timeout

```java
future.get(1, TimeUnit.SECONDS);
```

​	带时间参数的future.get()将抛出一个`TimeoutException`，当任务在指定的时间内没有完成的时候。

#### invokeAll

​	提交多个任务并等待他们完成。

​	你可以提交一个Callables集合给invokeAll()方法来执行多个任务。invokeAll()方法返回一个Futures集合。任何调用future.get()将被阻塞直到所有Future都执行完成。

```java
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.*;

public class InvokeAllExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ExecutorService executorService = Executors.newFixedThreadPool(5);

        Callable<String> task1 = () -> {
            Thread.sleep(2000);
            return "Result of Task1";
        };

        Callable<String> task2 = () -> {
            Thread.sleep(1000);
            return "Result of Task2";
        };

        Callable<String> task3 = () -> {
            Thread.sleep(5000);
            return "Result of Task3";
        };

        List<Callable<String>> taskList = Arrays.asList(task1, task2, task3);

        List<Future<String>> futures = executorService.invokeAll(taskList);

        for(Future<String> future: futures) {
            // The result is printed only after all the futures are complete. (i.e. after 5 seconds)
            System.out.println(future.get());
        }

        executorService.shutdown();
    }
}
```

```java
# Output
Result of Task1
Result of Task2
Result of Task3
```

在上面的程序中，第一个调用future.get()语句将阻塞直到所有futures都执行完成。所有结果将被打印在5秒以后。

#### invokeAny

提交多个任务，并等待其中一个任务完成。

invokeAny()方法接收一个`Callables` 集合，返回最快的Callable的执行结果。注意，这个方法没有返回一个Future。

```java
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.*;

public class InvokeAnyExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ExecutorService executorService = Executors.newFixedThreadPool(5);

        Callable<String> task1 = () -> {
            Thread.sleep(2000);
            return "Result of Task1";
        };

        Callable<String> task2 = () -> {
            Thread.sleep(1000);
            return "Result of Task2";
        };

        Callable<String> task3 = () -> {
            Thread.sleep(5000);
            return "Result of Task3";
        };

        // Returns the result of the fastest callable. (task2 in this case)
        String result = executorService.invokeAny(Arrays.asList(task1, task2, task3));

        System.out.println(result);

        executorService.shutdown();
    }
}
```

```java
# Output
Result of Task2
```