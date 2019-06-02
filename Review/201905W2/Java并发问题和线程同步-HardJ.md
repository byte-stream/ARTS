## Java并发问题和线程同步

**原文地址：<https://www.callicoder.com/java-concurrency-issues-and-thread-synchronization/>**

**原文作者：Rajeev Kumar Singh**

#### 并发问题

​	多线程是一个非常强大的工具，但是我们通过多线程读取和写入共享数据时需要格外注意。当我们尝试读或写共享数据时将会产生两个问题。

 	1. 线程干扰错误
 	2. 内存一致性错误

 	让我们一个一个的理解这些问题。

#### 竞态条件

​	对于下面的类，每次调用被调用后count的值都会加1。

```java
class Counter {
    int count = 0;

    public void increment() {
        count = count + 1;
    }

    public int getCount() {
        return count;
    }
}
```

​	当几个线程同时调用increment()方法时

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class RaceConditionExample {

    public static void main(String[] args) throws InterruptedException {
        ExecutorService executorService = Executors.newFixedThreadPool(10);

        Counter counter = new Counter();

        for(int i = 0; i < 1000; i++) {
            executorService.submit(() -> counter.increment());
        }

        executorService.shutdown();
        executorService.awaitTermination(60, TimeUnit.SECONDS);
    
        System.out.println("Final count is : " + counter.getCount());
    }
}
```

​	上面的例子运行结果小于1000。

​	当执行increment()方法时，以下三个步骤将被执行。1、检查当前current值。 2、将当前值加1。3、将增加的值存回count。

​	我们假设线程A和线程B按顺序执行以下操作。

 1. ThreadA：得到count，初始值为0

 2. ThreadB：得到count，初始值为0

 3. ThreadA：将count加1

 4. ThreadB：将count加1

 5. ThreadA：存储count值，count值为1

 6. ThreadB：存储count值，count值为1

​	两个线程都试图增加线程的值，但最终count的值是1不是2，因为两个线程相互交错执行。线程A的操作是丢失的。上面的执行顺序仅仅是一种可能性。程序重复执行可能会导致输出结果不一致。
​	当多个线程尝试并发地读或者写共享变量时，在执行的时候读或者写操作将会被覆盖，然后最终输出结果依赖于读或者写操作发生的顺序，这将是不可预测的。这种现象被称为竞态条件。
​	在共享变量允许被访问的代码段被称为临界代码段。

​	线程访问错误能够被避免通过同步访问共享变量。

#### 缓存一致性错误

​	当不同的线程对相同数据有不同的缓存时就会发生缓存一致性问题。当一个线程更新内存数据时，这个更新没有同步到其他线程，导致其他线程还在使用旧的数据，这个问题就发生了。

​	这个问题发生可能有很多原因。编译器会对你的程序做一些优化来提升性能。它也可以重排序指令为了提升性能。处理器也试图优化一些东西，例如，处理器可能从临时寄存器中读取一个当前值(这个值是最后一次读取的值，但不是内存中的最新值)。

​	下面的例子为我们展示了内存一致性错误。

```java
public class MemoryConsistencyErrorExample {
    private static boolean sayHello = false;

    public static void main(String[] args) throws InterruptedException {

        Thread thread = new Thread(() -> {
           while(!sayHello) {
           }

           System.out.println("Hello World!");

           while(sayHello) {
           }

           System.out.println("Good Bye!");
        });

        thread.start();

        Thread.sleep(1000);
        System.out.println("Say Hello..");
        sayHello = true;

        Thread.sleep(1000);
        System.out.println("Say Bye..");
        sayHello = false;
    }
}
```

​	在理想的情况下，上面的程序的执行顺序是：

 	1. 等待一秒，在sayHello变成true之后打印出Hello World!
 	2. 再等待一秒，在sayHello变成false之后打印Good Bye!

```java
# Ideal Output
Say Hello..
Hello World!
Say Bye..
Good Bye!
```

​	但实际上程序的输出是：

```java
# Actual Output
Say Hello..
Say Bye..
```

​	而且程序甚至不会终止，这就是内存一致性错误。主线程对sayHello变量的改变对于第一个线程来说是未知的。

#### 同步

​	通过以下两点，线程执行结果的不确定性和缓存一致性错误可以被避免。

1. 支持只有一个线程可读写共享变量，当一个线程正在访问共享变量时，其他线程应该等待知道这个线程执行完成。这可以确保这个线程的操作是原子性的，从而避免多个线程互相干扰。

2. 任何线程修改共享变量时，同步确保后续其他线程对共享变量的读和写都自动建立起一个happens-before关系。这可以确保一个线程对共享变量进行更改对其他线程时可见的。

   java有一个synchronized关键字，它可以使线程同步的访问任何共享资源，从而避免上面两种错误。

#### Synchronized方法

​	下面是Counter类的同步版本。我们使用synchronized关键字在increment方法上从而禁止多个线程并发的访问这个方法。

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class SynchronizedCounter {
    private int count = 0;

    // Synchronized Method 
    public synchronized void increment() {
        count = count + 1;
    }

    public int getCount() {
        return count;
    }
}

public class SynchronizedMethodExample {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService executorService = Executors.newFixedThreadPool(10);

        SynchronizedCounter synchronizedCounter = new SynchronizedCounter();

        for(int i = 0; i < 1000; i++) {
            executorService.submit(() -> synchronizedCounter.increment());
        }

        executorService.shutdown();
        executorService.awaitTermination(60, TimeUnit.SECONDS);

        System.out.println("Final count is : " + synchronizedCounter.getCount());
    }
}
```

​	上面的程序执行结果是不变的。没有竞态条件的产生。synchronized关键字能确保每次只有一个线程进入increment方法。

​	同步总是与一个对象相关。在之前的例子中，在一个`SynchonizedCounter` 实例上多次调用increment方法会导致竞态条件。我们使用synchronized关键字来防止这种情况发生，而且如果多个线程安全地调用increment方法在不同的SynchonizedCounter实例上也不会导致竞态条件的发生。对于静态方法来说，同步归类对象所有。

#### **Synchronized同步代码块**

​	Java内部使用一个内部锁或者同步监视器锁来保证线程同步。每一个对象都有一个内部锁。当一个线程使用synchronized在一个对象上时，线程将自动获取和释放对象的内置锁。当方法抛出异常时锁也会被释放。

​	对于静态方法来说，线程从Class对象获取内置锁，与其他实例的内置锁不同。synchronized也能使用在代码块上，与使用在方法上不同，必须指定一个提供内置锁的对象。

```java
public void increment() {
    // Synchronized Block - 

    // Acquire Lock
    synchronized (this) { 
        count = count + 1;
    }   
    // Release Lock
}
```

​	当一个线程获取一个内置锁在一个对象上，其他线程想要再去获取就必须等待。然而，当前拥有锁的线程可以多次的获取这把锁(重入)。

#### Volatile关键字

​	Volatile关键字在程序中使用可以避免缓存一致性错误。它告诉编译器禁止对修饰变量做任何优化。如果将一个变量标记为volatile，编译器不会优化或重排序变量周围的指令。而且，变量的值总是从主内存获取而不是从临时寄存器。

​	我们使用volatile关键字对之前的程序中涉及变量做标记。

```java
public class VolatileKeywordExample {
    private static volatile boolean sayHello = false;

    public static void main(String[] args) throws InterruptedException {

        Thread thread = new Thread(() -> {
           while(!sayHello) {
           }

           System.out.println("Hello World!");

           while(sayHello) {
           }

           System.out.println("Good Bye!");
        });

        thread.start();

        Thread.sleep(1000);
        System.out.println("Say Hello..");
        sayHello = true;

        Thread.sleep(1000);
        System.out.println("Say Bye..");
        sayHello = false;
    }
}
```

运行上面程序就获取下面的结果

```java
# Output
Say Hello..
Hello World!
Say Bye..
Good Bye!
```

