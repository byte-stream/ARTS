# Java Locks and Atomic Variables Tutorial

原文：https://www.callicoder.com/java-locks-and-atomic-variables-tutorial/

![Java Locks and Atomic Variables Tutorial](https://www.callicoder.com/assets/images/post/large/java-locks-and-atomic-variables-tutorial.jpg)

在多线程程序中，必须同步地访问共享变量才能避免条件竞争。

在前面的章节中，我们学习了如何使用 `synchronized `修饰方法和代码块去保证并发地访问共享变量，避免条件竞争。

Java 的 `synchronized `关键字内部是使用了与对象关联的固有锁来获得对对象成员字段的独占访问权。

你可以使用 Java 并发 API 提供给的各种锁来对锁定机制提供更细粒度的控制，而不是通过 synchronized 关键字使用内部锁。

在本节中，我们将学习 Java 提供的这些锁类同步访问共享变量。

最后，我们还将研究通过 Java 并发 API 提供的各种原子类实现线程同步的现代方法。



### Locks

1. ReentrantLock

   ReentrantLock 是一个互斥锁，具有与通过  `synchronized` 关键字访问的内部 / 隐式锁相同的行为。

   顾名思义，ReentrantLock 具有可重入特征，这意味着当前拥有该锁的线程可以多次获取该锁而不会出现任何问题。

   下面的例子展示了如何通过 ReentrantLock 创建一个线程安全的方法

   

   ```java
   import java.util.concurrent.locks.ReentrantLock;
   
   class ReentrantLockCounter {
       private final ReentrantLock lock = new ReentrantLock();
   
       private int count = 0;
   
       // Thread Safe Increment
       public void increment() {
           lock.lock();
           try {
               count = count + 1;
           } finally {
               lock.unlock();
           }
       }
   }
   ```

   其思想非常简单，任何调用 `increment()` 方法的线程都将首先获得锁，然后递增 `count` 变量。当它完成变量的递增时，它可以释放锁，以便其他等待锁的线程可以获取它。

   另外，请注意，我在上面的示例中使用了 `try/finally` 块。`finally` 块确保即使发生异常，也释放锁。

   ReentrantLock 还提供了用于更细粒度控制的各种方法:

    

   ```java
   import java.util.concurrent.ExecutorService;
   import java.util.concurrent.Executors;
   import java.util.concurrent.locks.ReentrantLock;
   
   class ReentrantLockMethodsCounter {
       private final ReentrantLock lock = new ReentrantLock();
   
       private int count = 0;
   
       public int incrementAndGet() {
           // Check if the lock is currently acquired by any thread
           System.out.println("IsLocked : " + lock.isLocked());
   
           // Check if the lock is acquired by the current thread itself.
           System.out.println("IsHeldByCurrentThread : " + lock.isHeldByCurrentThread());
   
           // Try to acquire the lock
           boolean isAcquired = lock.tryLock();
           System.out.println("Lock Acquired : " + isAcquired + "\n");
   
           if(isAcquired) {
               try {
                   Thread.sleep(2000);
                   count = count + 1;
               } catch (InterruptedException e) {
                   throw new IllegalStateException(e);
               } finally {
                   lock.unlock();
               }
           }
           return count;
       }
   }
   
   public class ReentrantLockMethodsExample {
   
       public static void main(String[] args) {
           ExecutorService executorService = Executors.newFixedThreadPool(2);
   
           ReentrantLockMethodsCounter lockMethodsCounter = new ReentrantLockMethodsCounter();
   
           executorService.submit(() -> {
              System.out.println("IncrementCount (First Thread) : " +
                      lockMethodsCounter.incrementAndGet() + "\n");
           });
   
           executorService.submit(() -> {
               System.out.println("IncrementCount (Second Thread) : " +
                       lockMethodsCounter.incrementAndGet() + "\n");
           });
   
           executorService.shutdown();
       }
   }
   ```

    

   ```bash
   # Output
   IsLocked : false
   IsHeldByCurrentThread : false
   Lock Acquired : true
   
   IsLocked : true
   IsHeldByCurrentThread : false
   Lock Acquired : false
   
   IncrementCount (Second Thread) : 0
   
   IncrementCount (First Thread) : 1
   ```

   `tryLock()` 方法尝试在不暂停线程的情况下获取锁。也就是说，如果线程因为被其他线程持有而无法获取锁，那么它将立即返回，而不是等待锁被释放。

   您还可以在 `tryLock()` 方法中指定一个超时来等待锁 -

    `lock.tryLock(1, TimeUnit.SECONDS);`

    线程现在将暂停一秒钟，等待锁可用。如果1秒内无法获取锁，则线程返回。

   

2. ReadWriteLock

   `ReadWriteLock` 由一对锁组成——一个用于读访问，一个用于写访问。只要写锁不被任何线程持有，那么读锁可以由多个线程同时持有。

   `ReadWriteLock` 允许增加并发级别。与应用程序中写操作比读操作少的其他锁相比，它的性能更好。

   ```java
   import java.util.concurrent.locks.ReadWriteLock;
   import java.util.concurrent.locks.ReentrantReadWriteLock;
   
   class ReadWriteCounter {
       ReadWriteLock lock = new ReentrantReadWriteLock();
   
       private int count = 0;
   
       public int incrementAndGetCount() {
           lock.writeLock().lock();
           try {
               count = count + 1;
               return count;
           } finally {
               lock.writeLock().unlock();
           }
       }
   
       public int getCount() {
           lock.readLock().lock();
           try {
               return count;
           } finally {
               lock.readLock().unlock();
           }
       }
   }
   ```



在上面的例子中，只要没有线程调用 `incrementAndGetCount()`，多个线程就可以执行 `getCount()` 方法。如果任何线程调用 `incrementAndGetCount()` 方法并获得写锁，那么所有读取线程将暂停执行并等待写入线程返回。

### Atomic Variables

Java 的并发 api 在 java .util.concurrent 中定义了几个类。支持单变量原子操作的原子包。

原子类在内部使用现代 cpu 支持的 CAS 指令来实现同步。这些指令通常比锁快得多。

考虑下面的示例，其中我们使用 `AtomicInteger` 类来确保 `count` 变量的增量以原子方式发生。

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

class AtomicCounter {
    private AtomicInteger count = new AtomicInteger(0);

    public int incrementAndGet() {
        return count.incrementAndGet();
    }

    public int getCount() {
        return count.get();
    }
}

public class AtomicIntegerExample {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService executorService = Executors.newFixedThreadPool(2);

        AtomicCounter atomicCounter = new AtomicCounter();

        for(int i = 0; i < 1000; i++) {
            executorService.submit(() -> atomicCounter.incrementAndGet());
        }

        executorService.shutdown();
        executorService.awaitTermination(60, TimeUnit.SECONDS);

        System.out.println("Final Count is : " + atomicCounter.getCount());
    }
}
```

```java
# Output
Final Count is : 1000
```

`incrementandget()` 方法是原子的，因此可以从多个线程同时安全地调用它，并确保对 `count` 变量的访问是同步的。

下面是 java.util.concurrent 中定义的其他一些原子类、原子包。

- AtomicBoolean
- AtomicLong
- AtomicReference

您应该尽可能使用这些原子类，而不是 synchronized 关键字和锁，因为它们更快、更容易使用、更易于阅读和可伸缩。