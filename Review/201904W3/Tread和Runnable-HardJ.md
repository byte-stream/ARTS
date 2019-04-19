## 并发编程基础

**原文地址：https://www.callicoder.com/java-multithreading-thread-and-runnable-tutorial/**

**原文作者：Rajeev Kumar Singh**

### 创建并启动一个线程

使用Java创建线程有两种方式

1. 通过继承Thread类

通过继承Thread类并重写run方法可以创建一个新的线程。run()方法中的代码在新线程中被执行。一旦线程被创建，你可以调用start()方法来运行它。

```java
public class ThreadExample extends Thread {

    // run() method contains the code that is executed by the thread.
    @Override
    public void run() {
        System.out.println("Inside : " + Thread.currentThread().getName());
    }

    public static void main(String[] args) {
        System.out.println("Inside : " + Thread.currentThread().getName());

        System.out.println("Creating thread...");
        Thread thread = new ThreadExample();

        System.out.println("Starting thread...");
        thread.start();
    }
}
```

```
# Output
Inside : main
Creating thread...
Starting thread...
Inside : Thread-0
```

​	Thread.currentThread()返回当前正在执行的线程引用。在上面的例子中，使用了线程方法getName()来打印当前线程的名称。

​	每个线程都有一个名称。你可以使用Thread(String name)构造器函数创建一个自定义名称的线程。如果没有指定名称，会自动的为这个线程指定一个名称。

2. 通过提供一个Runnable对象

   ​	Runnable是任何打算通过线程执行对象的主要模板。它定义了一个单独的方法run(),该方法包含了通过线程执行的代码。任何需要通过线程执行的类实例应该实现Runnable接口。

   ​	Thread这个类本身使用一个run()方法的空实现来实现了Runnable接口。

   ​	要创建一个新线程，需要创建一个实现Runnable接口的类实例然后传入Thread(Runnable target)的构造器中。

   ```
   public class RunnableExample implements Runnable {
   
       public static void main(String[] args) {
           System.out.println("Inside : " + Thread.currentThread().getName());
   
           System.out.println("Creating Runnable...");
           Runnable runnable = new RunnableExample();
   
           System.out.println("Creating Thread...");
           Thread thread = new Thread(runnable);
   
           System.out.println("Starting Thread...");
           thread.start();
       }
   
       @Override
       public void run() {
           System.out.println("Inside : " + Thread.currentThread().getName());
       }
   }
   ```

   ```
   # Output
   Inside : main
   Creating Runnable...
   Creating Thread...
   Starting Thread...
   Inside : Thread-0
   ```

   ​	注意，你可以使用Java匿名内部类语法创建一个匿名的Runnable对象来取代通过实现Runnable接口并实例化这个类来得到Runnable对象的方式。

   ​	匿名内部类使你的代码有更多的选择。他们能够使你声明并同时实例化一个类。

   ```
   public class RunnableExampleAnonymousClass {
   
       public static void main(String[] args) {
           System.out.println("Inside : " + Thread.currentThread().getName());
   
           System.out.println("Creating Runnable...");
           Runnable runnable = new Runnable() {
               @Override
               public void run() {
                   System.out.println("Inside : " + Thread.currentThread().getName());
               }
           };
   
           System.out.println("Creating Thread...");
           Thread thread = new Thread(runnable);
   
           System.out.println("Starting Thread...");
           thread.start();
       }
   }
   ```

   ​	上面的例子能够使用java8 lambda表达式使其变得更短。

   ```
   public class RunnableExampleLambdaExpression {
   
       public static void main(String[] args) {
           System.out.println("Inside : " + Thread.currentThread().getName());
   
           System.out.println("Creating Runnable...");
           Runnable runnable = () -> {
               System.out.println("Inside : " + Thread.currentThread().getName());
           };
   
           System.out.println("Creating Thread...");
           Thread thread = new Thread(runnable);
   
           System.out.println("Starting Thread...");
           thread.start();
   
       }
   }
   ```

   

   #### Runnable和Thread应该选择哪一个？

   ​	对于第一种方式，通过继承Thread类来创建一个线程是非常受限的，因为一旦继承Thread类，因为Java不允许多继承，所以你不能继承其他的类。

   ​	此外，如果你遵守一个好的设计实践，继承意味着扩展父类的功能，但当你创建一个线程时，你不继承Thread类的功能，仅仅只提供run()方法的实现。

   ​	所以，在一般情况下，你应该总是Runnable对象来创建一个线程。这种方式更加灵活，它允许你的类继承其他类。你也可以使用匿名内部类并且使用Java 8的Lambda表达式语法规则来使你的代码变得更家简洁。

   

   #### 使用sleep()方法使线程暂停执行

   ​	通过使用Thread类的sleep()方法允许你指定暂停当前正在执行的线程的毫秒数。

   ```
   public class ThreadSleepExample {
   
       public static void main(String[] args) {
           System.out.println("Inside : " + Thread.currentThread().getName());
   
           String[] messages = {"If I can stop one heart from breaking,",
                   "I shall not live in vain.",
                   "If I can ease one life the aching,",
                   "Or cool one pain,",
                   "Or help one fainting robin",
                   "Unto his nest again,",
                   "I shall not live in vain"};
   
           Runnable runnable = () -> {
               System.out.println("Inside : " + Thread.currentThread().getName());
   
               for(String message: messages) {
                   System.out.println(message);
                   try {
                       Thread.sleep(2000);
                   } catch (InterruptedException e) {
                       throw new IllegalStateException(e);
                   }
               }
           };
   
           Thread thread = new Thread(runnable);
   
           thread.start();
       }
   }
   ```

   ```
   # Output
   Inside : main
   Inside : Thread-0
   If I can stop one heart from breaking,
   I shall not live in vain.
   If I can ease one life the aching,
   Or cool one pain,
   Or help one fainting robin
   Unto his nest again,
   I shall not live in vain
   ```

   ​	上面的例子包含一个在messages数组迭代的for循环，打印当前消息，调用Thread.sleep()等待2秒，然后进行下一次迭代。

   ​	如果任何线程终端当前线程，sleep()方法将抛出一个IllegalStateException异常。IllegalStateException是一个受检查异常，所以必须被处理。

#### 使用join()方法等待另一个线程完成

​	join()方法允许一个线程等待其他线程完成。在下面的例子中，线程2通过调用Thread.join(1000)对于线程1的完成等待1000毫秒，然后再开始执行。

```
public class ThreadJoinExample {

    public static void main(String[] args) {
        // Create Thread 1
        Thread thread1 = new Thread(() -> {
            System.out.println("Entered Thread 1");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                throw new IllegalStateException(e);
            }
            System.out.println("Exiting Thread 1");
        });

        // Create Thread 2
        Thread thread2 = new Thread(() -> {
            System.out.println("Entered Thread 2");
            try {
                Thread.sleep(4000);
            } catch (InterruptedException e) {
                throw new IllegalStateException(e);
            }
            System.out.println("Exiting Thread 2");
        });

        System.out.println("Starting Thread 1");
        thread1.start();

        System.out.println("Waiting for Thread 1 to complete");
        try {
            thread1.join(1000);
        } catch (InterruptedException e) {
            throw new IllegalStateException(e);
        }

        System.out.println("Waited enough! Starting Thread 2 now");
        thread2.start();
    }
}
```

```
Starting Thread 1
Waiting for Thread 1 to complete
Entered Thread 1
Waited enough! Starting Thread 2 now
Entered Thread 2
Exiting Thread 1
Exiting Thread 2
```

Thread.join()的等待时间等于MIN(线程终止所使用的时间，即方法参数指定的毫秒数)

join()方法也能被无参调用。在这种情况下，只是等待下去直到线程死亡。