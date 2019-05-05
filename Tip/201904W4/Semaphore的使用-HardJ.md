#### Semaphore 的使用

​	Semaphore 是Java8中juc并发包下提供了一个类。一个计数信号量。一个Semaphore 维护着一组许可证集合。目前几乎所有的并发编程语言都支持信号量。

信号量模型主要包括：一个计数器，一个等待队列，三个方法，对应到Semaphore中有：

Semaphore的主要方法有三个：

- Semaphore()，主要用于初始化，并设置计数器值
- acquire()，将计数器的值减1，如果计数器小于0，则当前线程被阻塞。
- release(),将计数器的的值加1，如果当前计数器值小于等于0，则从等待队列中唤醒一个线程。

Semaphore借助AQS实现公平与非公平的获取机制，实现的过程中使用CAS实现原子性。

###### 实现互斥

​	Semaphore 可以像Java的SDK提供的Lock或关键字synchronized一样实现互斥。例如单例

```java
 private volatile static Singleton singleton;

    private final static Semaphore s = new Semaphore(1);

    private Singleton(){}

    public static Singleton getSingleton() {
        try {
            s.acquire();
            if(singleton == null) {
                singleton = new Singleton();
            }
            return singleton;
        } catch (InterruptedException e) {
            e.printStackTrace();
        }finally {
            s.release();
        }
        return singleton;
    }
```

###### 多个线程同时获取

​	在上面的例子中，通过将计数器设为了1来实现单个线程访问临界区，单Semaphore还有一种是Lock和synchronized不容易实现的就是多个线程同时进入临界区。

例如下面例子，把学校食堂窗口比作计数器，而学生比作线程，每次只允许固定数量(计数器数量)的学生打菜，如果某个学生付完钱走了(线程离开临界区)，下一个学生(线程)就可以打菜了(进入临界区)。

```java
public class Canteen{
  // 用信号量实现限流器
  final Semaphore sem;
  final ExecutorService students;
  final private int studentNum;
  final CountDownLatch countDownLatch;
  // 初始化窗口数量 num，学生数量 studentNum
  Canteen(int num, int studentNum){
    sem = new Semaphore(num);
    this.studentNum = studentNum;
    countDownLatch = new CountDownLatch(studentNum);
    students = Executors.newFixedThreadPool(studentNum);
  }
  // 执行任务
  void exec() throws InterruptedException, ExecutionException, TimeoutException {
    for (int i = 0; i < studentNum; i++) {
      final int temp = i;
      students.submit(() -> {
        try {
          sem.acquire();
          System.out.println(temp + "号同学正在打菜");
          Thread.sleep(3000);
        } catch (InterruptedException e) {
          e.printStackTrace();
        } finally {
          System.out.println(temp + "号同学打菜离开");
          countDownLatch.countDown();
          sem.release();
        }});
    }
    countDownLatch.await();
    students.shutdown();
  }
}
```





