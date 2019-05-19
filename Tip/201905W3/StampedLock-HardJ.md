### StampedLock

​	在Java1.8版本中提供了性能比读写锁更高的StampedLock。在ReadWriteLock中支持两种模式，一种是读锁，一种是写锁。而StampedLock中支持三种模式：写锁、悲观读锁和乐观读锁。其中，写锁、悲观读锁的语义和ReadWriteLock的写锁和读锁类似，允许多个线程同时获取悲观读锁，但只有一个线程可以获取写锁，写锁与悲观读锁之间是互斥的。

​	StampedLock中的写锁和悲观读锁加锁成功后会返回一个stamp;然后解锁的时候需要传入这个stamp。

```java
final StampedLock sl = new StampedLock();

long stamp = sl.readLock();
try {
  // .........
} finally {
  sl.unlockRead(stamp);
}

long stamp = sl.writeLock();
try {
  // .........
} finally {
  sl.unlockWrite(stamp);
}

```

​	在ReadWriteLock中，当多个线程同时读时，写操作将被会阻塞。而StampedLock提供的乐观读(无锁，性能好于读锁)允许多个线程同时读时，一个线程可以获取写锁。所以StampedLock性能比ReadWriteLock好。

​	虽然StampedLock对于读多写少的场景来说性能好，但是不支持重入的，而且悲观读、写锁也不支持条件变量。另外还要注意，如果线程阻塞在StampedLock的readLock()或writeLock()中，调用阻塞线程的interrupt()方法将会导致CPU飙升。

```java
final StampedLock lock
  = new StampedLock();
Thread T1 = new Thread(()->{
      // 获取写锁
      lock.writeLock();
      // 永远阻塞在此处，不释放写锁
      LockSupport.park();
});
T1.start();
// 保证 T1 获取写锁
Thread.sleep(100);
Thread T2 = new Thread(()->
  // 阻塞在悲观读锁
  lock.readLock()
);
T2.start();
// 保证 T2 阻塞在读锁
Thread.sleep(100);
// 中断线程 T2
// 会导致线程 T2 所在 CPU 飙升
T2.interrupt();
T2.join();

```

在上面代码中，T1线程获取写锁之后将自己阻塞，T2线程尝试获取悲观读锁，也会阻塞。如果此时调用线程T2的interrupt()方法来中断线程T2的话，将会引起执行T2线程的CPU飙升。

在使用StampedLock的时候一定不要调用中断操作，如果需要中断，一定使用可中断的readLockInterruptibly和writeLockInterruptibly。

实际中常使用的代码模板(来自《极客时间》)

##### StampedLock 读模板： 

```java
final StampedLock sl = new StampedLock();
// 乐观读
long stamp = sl.tryOptimisticRead();
// 读入方法局部变量
......
// 校验 stamp
if (!sl.validate(stamp)){
  // 升级为悲观读锁
  stamp = sl.readLock();
  try {
    // 读入方法局部变量
    .....
  } finally {
    // 释放悲观读锁
    sl.unlockRead(stamp);
  }
}
// 使用方法局部变量执行业务操作
......
```

##### StampedLock 写模板：

```java
long stamp = sl.writeLock();
try {
  // 写共享变量
  ......
} finally {
  sl.unlockWrite(stamp);
}
```

​	