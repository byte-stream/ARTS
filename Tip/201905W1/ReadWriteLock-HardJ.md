ReadWriteLock

​	应用程序中有一种非常常见的并发场景，就是读多写少。在这个场景下所涉及的数据一般都不怎么会变化，但是使用的地方非常多。

​	Java并发包中针对并发场景提供了很多API包，如支持fail—safe(安全失败)的集合容器、读写锁ReadWriteLock。

#### 读写锁

​	读写锁是一种通用技术，在其他编程语言或者数据库中都有对应实现。读写锁一般遵守下面三条规则：

1. 允许多个线程获取读锁

2. 只允许一个线程获取写锁

3. 如果某个线程获取了写锁，其他线程不能再获取读锁

   由于规则1多个线程在只读的情况下可以同时读取数据获取共享变量，所以读写锁优于互斥锁。

#### 使用读写锁实现缓存

```java
class CachedData {
  Object data;
  volatile boolean cacheValid;
  final ReadWriteLock rwl =
    new ReentrantReadWriteLock();
  // 读锁  
  final Lock r = rwl.readLock();
  // 写锁
  final Lock w = rwl.writeLock();
  
  void processCachedData() {
    // 获取读锁
    r.lock();
    if (!cacheValid) {
      // 释放读锁，因为不允许读锁的升级
      r.unlock();
      // 获取写锁
      w.lock();
      try {
        // 再次检查状态  
        if (!cacheValid) {
          data = ...
          cacheValid = true;
        }
        // 释放写锁前，降级为读锁
        // 降级是可以的
        r.lock(); 
      } finally {
        // 释放写锁
        w.unlock(); 
      }
    }
    // 此处仍然持有读锁
    try {use(data);} 
    finally {r.unlock();}
  }
}
```

​	上面的例子，来自于极客时间Java并发编程实战专栏，使用ReentrantReadWriteLock得到了一个读锁和一个写锁，在获取数据时，如果需要对数据进行修改，那么要释放读锁，因为ReadWriteLock,不支持锁升级，仅支持锁降级，在获取写锁后，数据懒加载(需要时再获取)成功后可以将写锁降级为读锁，当数据加载完成后可以释放写锁，此时，读锁仍然存在，最后将读锁释放。

​	在上例子中使用了ReadWriteLock的子类ReentrantReadWriteLock实现读写锁实现数据缓存，并且由这个子类实现的锁是可重入的，底层依赖于一个同步器框架AbstractQueuedSynchronizer简称AQS。所以要理解可重入的读写锁这个类的实现必须先弄清楚AQS帮助这个类实现了哪些功能。

#### AQS（AbstractQueuedSynchronizer）

​	AQS提供了一个同步器框架，内部实现了FIFO的等待队列锁阻塞和相关的同步唤醒机制。并且相关同步器的值依赖于一个int值state表示内部同步状态，实现该类的子类必须定义改变此状态的protect方法，以及获取或释放锁来改变状态的方法，而且必须以原子方式修改该状态值。实现AQS的子类应该定义为内部非公共类，用来封闭同步属性。**也就是说，在AQS内部实现的队列中的每个节点都可以去操作state状态值，但是操作必须以原子的方式进行，并且操作间接操作state状态值的是AQS定义的模板方法(子类自行实现)。**

![](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/weqw.png)

```java
/**
* The synchronization state.
*/
private volatile int state;

protected final int getState() {
    return state;
}

protected final void setState(int newState) {
    state = newState;
}

protected final boolean compareAndSetState(int expect, int update) {
    // See below for intrinsics setup to support this
    return unsafe.compareAndSwapInt(this, stateOffset, expect, update);
}
```

上面是AQS的部分代码，volatile语义保证了可见性，get和set通过原子性方式操作值，compareAndSetState依赖CPU指令也保证了原子性操作值。

​	AQS这个类默认支持独占模式和共享模式。当以独占模式获取时，其他线程无法再获取锁。 当以共享模式获取时，队列中的下一个等待线程需要判断是否也可以获取。在读写锁实现缓存的代码中，ReentrantReadWriteLock中的readLock()和writeLock()所获取的读锁和写锁对应AQS的独占模式和共享模式，在ReentrantReadWriteLock中依赖于AQS实现的同步器只需要维护好state等一些状态值就可以了，至于阻塞、唤醒或释放等待线程已经由AQS框架保证了。

​	自定义的同步器需要实现以下方法，由这几个方法的实现可以看出，如果子类没有重新实现只会抛异常。自定义的同步器实现这些方法必须要是线程安全的。

```java
// 判断线程是否独占资源，仅在ConditionObject方法内部调用，如果不使用条件，不需要定义
protected boolean isHeldExclusively() {	throw new UnsupportedOperationException();}
// 尝试以独占模式获取资源。 该方法应该查询对象的状态是否允许以独占模式获取，如果是，则获取它。
protected boolean tryAcquire(int arg) {	throw new UnsupportedOperationException();}
// 尝试设置状态以独占模式释放资源。
protected boolean tryRelease(int arg) {	throw new UnsupportedOperationException();}
// 尝试以共享模式获取。 该方法应该查询对象的状态是否允许在共享模式下获取该对象，如果是这样，就可以获取它。
protected int tryAcquireShared(int arg) { throw new UnsupportedOperationException();}
// 尝试设置状态以共享模式释放资源。
protected boolean tryReleaseShared(int arg) { throw new UnsupportedOperationException();}
```

AQS部分源码：

​	acquire:

```java
// 以独占模式获取,可用于实现方法Lock.lock() 
public final void acquire(int arg) {
if (!tryAcquire(arg) &&
    acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
    selfInterrupt();
}
```

​	acquire实现中，tryAcquire方法尝试获取资源，获取成功直接返回，获取失败调用addWaiter方法将线程加入到等待队列，并标记为独占模式。acquireQueued方法表示将自己加入到等待队列，并等待时机获取资源，当当前节点(线程)成为队列的Head时，并且state正确获取时表示成功获取资源并返回，否则获取不到将一直获取，如果被终端返回true，否则返回false。selfInterrupt方法表示将当前线程设置为已中断状态。

​	release：

```java
  public final boolean release(int arg) {
        if (tryRelease(arg)) {
            Node h = head;
            if (h != null && h.waitStatus != 0)
                unparkSuccessor(h);
            return true;
        }
        return false;
    }
```

​	release方法的实现中，首先通过tryRelease返回值判断资源是否已经成功释放。而tryRelease属于模板方法，由实现独占模式的子类同步器来实现，如果资源已经释放返回true，否则返回false。unparkSuccessor方法用于唤醒排在当前节点(当前线程)的下一个节点(下一个线程)，借助LockSupport类实现。

​	acquireShared：

```java
 public final void acquireShared(int arg) {
        if (tryAcquireShared(arg) < 0)
            doAcquireShared(arg);
    }
```

​	acquireShared方法实现中tryAcquireShared同样为一个模板方法，由子类同步器自行实现，该方法返回值大于等于0表示获取成功，否则调用doAcquireShared加入等待队列。在doAcquireShared的实现中，如果获取的资源足够唤醒阻塞队列后续线程，则会继续唤醒后续线程(共享)。

​	releaseShared：

```java
public final boolean releaseShared(int arg) {
    if (tryReleaseShared(arg)) {
        doReleaseShared();
        return true;
    }
    return false;
}
```

​	上面代码中tryReleaseShared也是一个模板方法，由子类实现。如果tryReleaseShared返回true表示资源释放成功，调用doReleaseShared方法唤醒队列后面的共享兄弟节点。

#### ReentrantReadWriteLock

​	回到ReadWriteLock，ReentrantReadWriteLock是ReadWriteLock的一个实现。从名字可以看出这个类是支持锁重入的。在这个类中定义了抽象类Sync实现上面提到的同步器框架AbstractQueuedSynchronizer。

在ReentrantReadWriteLock中有两个设置AQS状态值的方法

```java
static final int SHARED_SHIFT   = 16; 
static final int EXCLUSIVE_MASK = (1 << SHARED_SHIFT) - 1; //65535
/** Returns the number of shared holds represented in count  */
 static int sharedCount(int c)    { return c >>> SHARED_SHIFT; }
 /** Returns the number of exclusive holds represented in count  */
 static int exclusiveCount(int c) { return c & EXCLUSIVE_MASK; }
```

​	其中sharedCount方法用于同步器框架子类实现的tryAcquire和tryRelease中，exclusiveCount方法用于tryAcquireShared和tryReleaseShared方法中。ReentrantReadWriteLock因为支持锁重入，并且读锁与写锁互斥、读锁与读锁不互斥，写锁与写锁互斥，所以在state状态值变量中保存了读写锁的重入次数。

​	但这会存在两个问题，**1：**读写锁如何保存的重入如何保存在一个state变量中 **2：**读锁支持多线程访问，如何存储其中某个线程的重入次数确保在这个线程退出所有重入锁后真正的释放资源。

​	**对于第一个问题**，ReentrantReadWriteLock使用了state变量的前32位存储共享模式下state变量数，后32位存储独占模式下state变量数。可从上面两个方法看出，当获取共享模式下state持有数量时将传入的state变量进行右16位获取共享模式下state变量状态数，当需要获取独占模式下state变量资源数就将传入的state变量与上65535得到后16位的state数。

![图2](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/sdas.png)

​	**对于第二个问题**，ReentrantReadWriteLock使用了ThreadLocal来保存共享模式下某个线程state数，也就是说当一个一个线程重复持有读锁时，对应的state状态值有进行两处更新，一处是线程对应的ThreadLocal，一处是对state变量的前16位数值进行更新。这里的ThreadLocal由于底层对应于每个线程自己维护的map，数据并不在多个线程共享，所以是线程安全的。

ReentrantReadWriteLock对部分模板方法的实现

​	tryAcquire:

```java
protected final boolean tryAcquire(int acquires) {
       /*
             * Walkthrough:
             * 1. If read count nonzero or write count nonzero
             *    and owner is a different thread, fail.
             * 2. If count would saturate, fail. (This can only
             *    happen if count is already nonzero.)
             * 3. Otherwise, this thread is eligible for lock if
             *    it is either a reentrant acquire or
             *    queue policy allows it. If so, update state
             *    and set owner.
             */
       Thread current = Thread.currentThread();
    	// 获取AQS的state变量
       int c = getState();
    	// 获取写锁state变量值
       int w = exclusiveCount(c);
       if (c != 0) {
           // (Note: if c != 0 and w == 0 then shared count != 0)
           // w == 0：当前已存在读锁，current != getExclusiveOwnerThread()：不属于写锁重入
           if (w == 0 || current != getExclusiveOwnerThread())
               return false;
           if (w + exclusiveCount(acquires) > MAX_COUNT)
               throw new Error("Maximum lock count exceeded");
           // Reentrant acquire
           // 更新写锁对应的state变量
           setState(c + acquires);
           return true;
       }
    	// 当前不存在读锁和写锁，可以更新state获取写锁
       if (writerShouldBlock() ||
           !compareAndSetState(c, c + acquires))
           return false;
    	// 将当前线程设置独占模式下拥有这线程
       setExclusiveOwnerThread(current);
       return true;
}
```
​	tryRelease:
```java
protected final boolean tryRelease(int releases) {
    		// 判断要释放资源的线程是否为当前已经获取锁的线程
            if (!isHeldExclusively())
                throw new IllegalMonitorStateException();
    		// 释放资源或退出重入锁
            int nextc = getState() - releases;
    		// 获取state值的后16位，写锁对应state值
            boolean free = exclusiveCount(nextc) == 0;
            if (free)
                setExclusiveOwnerThread(null);
            setState(nextc);
            return free;
  }
```
​	tryAcquireShared:
```java
 protected final int tryAcquireShared(int unused) {
            /*
             * Walkthrough:
             * 1. If write lock held by another thread, fail.
             * 2. Otherwise, this thread is eligible for
             *    lock wrt state, so ask if it should block
             *    because of queue policy. If not, try
             *    to grant by CASing state and updating count.
             *    Note that step does not check for reentrant
             *    acquires, which is postponed to full version
             *    to avoid having to check hold count in
             *    the more typical non-reentrant case.
             * 3. If step 2 fails either because thread
             *    apparently not eligible or CAS fails or count
             *    saturated, chain to version with full retry loop.
             */
            Thread current = Thread.currentThread();
     		// 获取state变量值
            int c = getState();
     		// 已经有线程获取写锁，并且写锁不是当前线程(如果是当前线程可以获取，因为锁降级)
            if (exclusiveCount(c) != 0 &&
                getExclusiveOwnerThread() != current)
                return -1;
     		// 获取state变量值中读锁(共享模式)的state值
            int r = sharedCount(c);
            if (!readerShouldBlock() &&
                r < MAX_COUNT &&
                // 更新共享模式下的资源值，更新state前16位
                compareAndSetState(c, c + SHARED_UNIT)) {
                if (r == 0) {// 第一个获取读锁的线程
                    firstReader = current;
                    firstReaderHoldCount = 1;
                } else if (firstReader == current) {// 第一个获取读锁的线程
                    firstReaderHoldCount++;
                } else {
                    HoldCounter rh = cachedHoldCounter;
                    if (rh == null || rh.tid != getThreadId(current))
                        cachedHoldCounter = rh = readHolds.get();
                    else if (rh.count == 0)
                        readHolds.set(rh);
                    // cas成功后设置ThreadLocal中的重入数
                    rh.count++;
                }
                return 1;
            }
     		// cas失败，自旋重试
            return fullTryAcquireShared(current);
}	
```

​	tryReleaseShared:

```java
 protected final boolean tryReleaseShared(int unused) {
            Thread current = Thread.currentThread();
     		// 第一个获取读锁的线程
            if (firstReader == current) {
                // assert firstReaderHoldCount > 0;
                if (firstReaderHoldCount == 1)
                    firstReader = null;
                else
                    firstReaderHoldCount--;
            } else {
                // 更新非第一个读锁线程中的ThreadLocal值
                HoldCounter rh = cachedHoldCounter;
                if (rh == null || rh.tid != getThreadId(current))
                    rh = readHolds.get();
                int count = rh.count;
                if (count <= 1) {
                    readHolds.remove();
                    if (count <= 0)
                        throw unmatchedUnlockException();
                }
                --rh.count;
            }
            for (;;) {
                // 更新state值中读锁对应的资源值
                int c = getState();
                int nextc = c - SHARED_UNIT;
                if (compareAndSetState(c, nextc))
                    // Releasing the read lock has no effect on readers,
                    // but it may allow waiting writers to proceed if
                    // both read and write locks are now free.
                    return nextc == 0;
            }
        }
```

#### 通过AQS自定义一个锁

```java
/**
 * 通过AQS自定义锁
 */
public class DiyLock implements Lock {

	private Sync sync = new Sync();

	private class Sync extends AbstractQueuedSynchronizer {

		@Override
		protected boolean tryAcquire(int arg) {

			// 获取state资源值
			int state = getState();
			Thread t = Thread.currentThread();

			if (state == 0) {
				// cas设置state值,获取独占锁成功
				if (compareAndSetState(0, arg)) {
					setExclusiveOwnerThread(t);
					return true;
				}
				// 支持重入
			} else if (getExclusiveOwnerThread() == t) {
				setState(state + 1);
				return true;
			}
			return false;
		}

		@Override
		protected boolean tryRelease(int arg) {

			// 如果调用释放资源的线程不是当前持有线程抛出异常
			if (Thread.currentThread() != getExclusiveOwnerThread()) {
				throw new RuntimeException();
			}

			int state = getState() - arg;

			boolean flag = false;

			// 释放资源
			if (state == 0) {
				setExclusiveOwnerThread(null);
				flag = true;
			}

			// 退出重入锁/释放资源
			setState(state);

			return flag;
		}

		/*
		* 条件变量
		 */
		Condition newCondition() {
			return new ConditionObject();
		}

	}

	@Override
	public void lock() {
		sync.acquire(1);
	}

	@Override
	public void lockInterruptibly() throws InterruptedException {
		sync.acquireInterruptibly(1);
	}

	@Override
	public boolean tryLock() {
		return sync.tryAcquire(1);
	}

	@Override
	public boolean tryLock(long time, TimeUnit unit) throws InterruptedException {
		return sync.tryAcquireNanos(1, unit.toNanos(time));
	}

	@Override
	public void unlock() {
		sync.release(1);
	}

	@Override
	public Condition newCondition() {
		return sync.newCondition();
	}

}
```

#### 参考

- <https://www.jianshu.com/p/da9d051dcc3d>
- <http://www.cnblogs.com/waterystone/p/4920797.html>