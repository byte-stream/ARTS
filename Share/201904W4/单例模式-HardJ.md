## 单例模式

​	单例模式又称为单件模式，确保一个类只有一个实例，提供全局访问点。是Java中比较常用的一种模式。写起来也比较容易。

​	以下是几种Java实现的单例模式

1. 懒汉模式

```java
private volatile static Singleton singleton;

private Singleton(){}

public static Singleton getSingleton() {
    if(singleton == null) {
        synchronized (Singleton.class) {
            if(singleton == null){
                singleton = new Singleton();
            }
        }
    }
    return singleton;
}
```

2. 饿汉模式
```java
private static Singleton singleton = new Singleton();

private Singleton(){}

public static Singleton getSingleton() {
    return singleton;
}
```

3. 饿汉模式

```java
private Singleton(){}

private static class Instance{
	private static final Singleton SINGLETON = new Singleton();
}

public static Singleton getSingleton() {
	return Instance.SINGLETON;
}
```

4. 枚举
```java
public enum  SingletonEnum {
    INSTANCE;
}
```

5. CAS(引用：<https://mp.weixin.qq.com/s/nt31pbECsQvf3NY-MT2_Ng>)
```java
private static final AtomicReference<Singleton> INSTANCE = new AtomicReference<>();

    private Singleton(){}

    public static Singleton getSingleton() {
        while (true) {
            Singleton singleton = INSTANCE.get();

            if(singleton != null) {
                return singleton;
            }

            singleton = new Singleton();
            if(INSTANCE.compareAndSet(null, singleton)) {
                return INSTANCE.get();
            }

        }
    }
```