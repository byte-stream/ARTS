## Java锁和原子变量-HardJ

**原文地址：<https://www.callicoder.com/java-locks-and-atomic-variables-tutorial/>**

**原文作者：Rajeev Kumar Singh**

在多线程程序中，访问共享变量必须通过synchronized来防止竞态条件。

在前面的章节中，我们学习了如何使用synchronized方法和synchronized代码块防止并发的访问共享变量和避免竞态条件。

Java的synchronized关键字内部使用与对象关联的内置锁获取对象成员变量的独占访问。

也可以通过会用各种Java提供的并发API对锁定机制提供更加细粒度的控制，而不是使用内置锁关键字synchronized。

在本章节中，我们将学习到如何使用这些Java提供的锁定类进行共享变量的同步访问。

最后，我们也将寻找一些Java并发API提供的线程同步原子类实现线程同步的现代方式。

#### Locks

 1. ReentrantLock

    ReentrantLock是一个互斥锁。与通过`synchronized` 关键字进行内置锁访问方式相同。ReentrantLock，顾名思义，具有可重入的特性。这意味着一个当前拥有锁的线程可以再次获取锁。

    下面展示了如何通过ReentrantLock创建一个线程安全的方法。

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

    这个例子比较简单，任何调用increment方法的线程首先获取锁，然后增加count变量。当他完成变量增加后，可以释放锁以便于其他等待这个锁的线程能够获取它。

    另外，上面的例子中使用了try/finally代码块。finally代码块代码块确保即使出现一些异常代码块也能释放。

    ReentrantLock也为更细粒度的控制提供了多种方法

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

    ```java
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

    tryLock()方法尝试在不中断线程情况下获取锁。也就是说，如果线程由于持有其他相同的锁导致无法获取锁，将立即返回而不是等待锁的释放。

    也可以在tryLock()方法中指定超时时间以等待锁可用。

    ```java
    lock.tryLock(1, TimeUnit.SECONDS);
    ```

    此时线程将暂停1秒钟并等待线程可用。如果线程不能在1秒内获取，则将立即返回。

    2. ReadWriteLock

       ReadWriteLock由一对锁组成-一个用于读访问、一个用于写访问。读锁可以被任何线程持有，只要写锁不被任何线程持有。

       在读多写少的应用中，它展现了更好的性能。

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

       ​	在上面的例子中，多个线程可以同时执行getCount方法，只要没有线程执行incrementAndGetCount方法。如果有任何线程调用incrementAndGetCount方法获取写锁，所有读线程将暂停等待写线程返回。

       #### Atomic变量

       ​	Java并发API在[`java.util.concurrent.atomic`](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/package-summary.html)中定义了几个类，支持单变量原子操作。Atomic类内部使用现代CPU指令 [compare-and-swap](https://en.wikipedia.org/wiki/Compare-and-swap)实现同步。这些指令比锁快得多。

       ​	在下面的例子中，我们使用AtomicInteger类来确保count变量增加是原子性的。

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

       AtomicInteger.incrementAndGet()方法的执行时原子的，所以多个线程可以并发地调用，确保count变量的访问是同步的。

       下面是 [`java.util.concurrent.atomic`](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/package-summary.html)包定义的一些其他原子类。

       - [AtomicBoolean](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/AtomicBoolean.html)

       - [AtomicLong](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/AtomicLong.html)

       - [AtomicReference](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/AtomicReference.html)

如果可以的话应该使用Atomic类代替synchronized关键字和synchronized锁，因为他们更快，更易于使用，而且具有更好的可扩展性和可伸缩性。

​         