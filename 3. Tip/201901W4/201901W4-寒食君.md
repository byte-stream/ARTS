# 谈一谈ThreadLocal

由于经验尚浅，我在编程中很少用到ThreadLocal，今天突然想起它，就决定写一写。

在Java中使用多线程，变量是可以被多个线程访问的（按照Java的内存模型，变量其实也不是直接被线程访问，而是工作线程操作副本，再刷新到主线程中，对变量进行加锁或者volatile，可以实现一定程度上的线程通信）

## 那么ThreadLocal有什么用呢？

使用ThreadLocal创建的变量只能被当前线程访问，其他线程无法访问和修改。它的目的是为了解决多线程访问资源时的共享问题。这里需要注意，解决的是“资源的共享问题”，不是“共享资源的问题”，这是有区别的，ThreadLocal变量是当前线程的独立副本，并不共享。

可以总结为以下三点：

- 每个 Thread 内有自己的实例副本，且该副本只能由当前 Thread 使用。这是也是 ThreadLocal 命名的由来
- 既然每个 Thread 有自己的实例副本，且其它 Thread 不可访问，那就不存在多线程间共享的问题
- ThreadLocal通常被`private static`来定义，即内存中只存在一份实例，线程需要使用时，会初始化一份实例副本，当线程结束时，实例副本全部被回收。


既然是这样，那么有的同学就会产生疑问：既无共享，何来同步问题，又何来解决同步问题一说？

总的来说，ThreadLocal 适用于每个线程需要自己独立的实例且该实例需要在多个方法中被使用，也即变量在线程间隔离而在方法或类间共享的场景。


## ThreadLocal是如何实现的？
篇幅较长，暂略。


## 使用场景：

满足如下二者：

- 每个线程需要有自己单独的实例
- 实例需要在多个方法中共享，但不希望被多线程共享

比如Java web中的 session。每个线程需要有自己单独的session实例，程序需要对session进行读写，而且session作为保存用户状态的实例，很多类和方法都需要使用它。此时使用ThreadLocal来存储session实例，就十分简洁优雅。

用代码来展示使用与不使用ThreadLocal的区别，能够更好地理解使用ThreadLocal的好处（代码摘自互联网）：


1. 不使用ThreadLocal：

```
public class SessionHandler {

  @Data
  public static class Session {
    private String id;
    private String user;
    private String status;
  }

  public Session createSession() {
    return new Session();
  }

  public String getUser(Session session) {
    return session.getUser();
  }

  public String getStatus(Session session) {
    return session.getStatus();
  }

  public void setStatus(Session session, String status) {
    session.setStatus(status);
  }

  public static void main(String[] args) {
    new Thread(() -> {
      SessionHandler handler = new SessionHandler();
      Session session = handler.createSession();
      handler.getStatus(session);
      handler.getUser(session);
      handler.setStatus(session, "close");
      handler.getStatus(session);
    }).start();
  }
}
```

评价： 需要显式初始化Seesion实例，并且显式传递session对象，


2. 使用ThreadLocal：

```
public class SessionHandler {

  public static ThreadLocal<Session> session = new ThreadLocal<Session>();

  @Data
  public static class Session {
    private String id;
    private String user;
    private String status;
  }

  public void createSession() {
    session.set(new Session());
  }

  public String getUser() {
    return session.get().getUser();
  }

  public String getStatus() {
    return session.get().getStatus();
  }

  public void setStatus(String status) {
    session.get().setStatus(status);
  }

  public static void main(String[] args) {
    new Thread(() -> {
      SessionHandler handler = new SessionHandler();
      handler.getStatus();
      handler.getUser();
      handler.setStatus("close");
      handler.getStatus();
    }).start();
  }
}
```

评价:简洁、优雅、耦合低。





