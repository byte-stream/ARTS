#### 适配器模式与外观模式

> 适配器模式：将一个类的接口，转换成客户期望的另一个接口。适配器让原本接口不兼容的类可以合作无间。

> 外观模式：提供一个统一的接口，用来访问子系统中的一群接口。外观定义了一个高层接口，让子系统更容易使用。

​	通过上面的两个定义可以看出，两个模式都比较容易理解。

#### 适配器模式：

​	早期的集合类型(Vector、Stack、Hashtable)都实现了elements方法，该方法会返回一个Enumeration类型。它可以像for一样遍历集合内容。后来更新了集合类，开始使用Iterator接口，每个新的集合类几乎都有iterator方法返回一个实现了Iterator接口的子类。Iterator和Enumeration类似，但是Iterator还提供了删除接口。

​	如果看到较早期的代码发现返回的是Enumeration类型，但是后期维护又想要使用Iterator类型，就可以提供一个适配器，找出两个类型方法的映射，将Enumeration类型的行为适配到Iterator类型中。

1. 找出两个类型的对应方法

![](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/222222.png)

2. 需要一个实现了目标接口的适配器，目标接口将请求转为被适配者。

![](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/222221.png)

```java
/**
 * Enumeration适配
 */
public class EnumerationAdapter implements Iterator{
    // 为了让适配器看起来像一个迭代器，让适配器实现迭代器接口

    Enumeration enumeration;

    // 使用组合的方式将枚举注入到适配器中
    public EnumerationAdapter(Enumeration enumeration) {
        this.enumeration = enumeration;
    }

    // 调用迭代器的方法后将功能委托给Enumeration
    @Override
    public boolean hasNext() {
        return enumeration.hasMoreElements();
    }

     // 调用迭代器的方法后将功能委托给Enumeration
    @Override
    public Object next() {
        return enumeration.nextElement();
    }

    // Enumeration接口没有对应remove实现
    @Override
    public void remove() {
        throw new UnsupportedOperationException("remove");
    }
}

```

客户端使用适配器的过程：

1. 客户通过目标接口调用适配器的方法对适配器发出请求。

2. 适配器使用被适配接口把请求转化为被适配的一个或者多个接口。

##### 对象和类的适配器：

​	实际上适配器有两类，分别是类适配器和对象适配器。Java中不支持类适配器，所以上面的例子属于对象适配器。通过上面的例子我们知道对象适配器是通过组合的方式来适配被适配者的，而类适配器则是通过多继承的方式进行适配，但Java并不支持多继承。

![](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/21312.png)

虽然类适配不如对象适配(组合)的弹性伸缩(能适配指定的类及其任何子类)，但是类适配也有优点，对象适配需要实现目标类的所有接口，而类适配则不需要，因为多继承，不需要重新实现整个被适配者，也可以覆盖被适配者的行为。

##### 适配器模式与装饰者模式：

​	适配器模式与装饰者模式看起来非常类似，都是将对象包装起来再增加一点东西。但适配器更倾向于将对象包装起来，并改变对外接口。而装饰者模式则是将一个对象包装起来以增加新的行为，在不改变接口的情况下加入新行为。	

#### 外观模式：

​	如果用户端需要调用一系列数量庞大的接口。而使用外观模式只提供几个简单的接口，通过几个简化接口将原本数量庞大的一系列接口全部暴露出来。不仅仅是简化，外观模式也使调用方与数量庞大的被调用方进行解耦。

##### 日志框架中的外观模式：

​	《阿里巴巴Java开发手册》，其中有一条规范做了『强制』要求： 

![](https://upload-images.jianshu.io/upload_images/12148101-704d0dd693bdeb6e.png)

​	在平时开发中，都遵守上面的要求，使用slf4j日志框架。这里的门面模式就是外观模式。slf4j中的门面模式主要是两个目的：

 	1. 外部与一个子系统的通信必须通过一个统一的外观对象进行，使得子系统更易于使用。 
  2. 降低应用于日志框架的耦合性。
     ![image](https://upload-images.jianshu.io/upload_images/12148101-4f7771c1dbb38f74.png)

     在平时开发中，主要使用下面这句就可以方便的在程序任何位置打印日志。

```java
private static Logger logger = LoggerFactory.getLogger(BsUserServiceImpl.class);
```

​	然后我们跟进去看一下LoggerFactory.getLogger的代码

```java
public static Logger getLogger(Class<?> clazz) {
        Logger logger = getLogger(clazz.getName());
        if (DETECT_LOGGER_NAME_MISMATCH) {
            Class<?> autoComputedCallingClass = Util.getCallingClass();
            if (autoComputedCallingClass != null && nonMatchingClasses(clazz, autoComputedCallingClass)) {
                Util.report(String.format("Detected logger name mismatch. Given name: \"%s\"; computed name: \"%s\".", logger.getName(), autoComputedCallingClass.getName()));
                Util.report("See http://www.slf4j.org/codes.html#loggerNameMismatch for an explanation");
            }
        }
        return logger;
    }
```

​	传入打印类的全路径类名

```java
public static Logger getLogger(String name) {
	ILoggerFactory iLoggerFactory = getILoggerFactory();
	return iLoggerFactory.getLogger(name);
}	
```

​	获取相应的日志工厂,判断日志容器是否已经初始化，如果没有则进行同步初始化。

```java
public static ILoggerFactory getILoggerFactory() {
        if (INITIALIZATION_STATE == 0) {
            Class var0 = LoggerFactory.class;
            synchronized(LoggerFactory.class) {
                if (INITIALIZATION_STATE == 0) {
                    INITIALIZATION_STATE = 1;
                    // 1 初始化
                    performInitialization();
                }
            }
        }
        switch(INITIALIZATION_STATE) {
        case 1:
            return SUBST_FACTORY;
        case 2:
            throw new IllegalStateException("org.slf4j.LoggerFactory in failed state. Original exception was thrown EARLIER. See also http://www.slf4j.org/codes.html#unsuccessfulInit");
        case 3:
            // 2 调用StaticLoggerBinder类获取日志工厂的方法    
            return StaticLoggerBinder.getSingleton().getLoggerFactory();
        case 4:
            return NOP_FALLBACK_FACTORY;
        default:
            throw new IllegalStateException("Unreachable code");
        }
    }
```

```java
private static final void performInitialization() {
        bind();
        if (INITIALIZATION_STATE == 3) {
            versionSanityCheck();
        }

    }
```

​	在绑定方法中，findPossibleStaticLoggerBinderPathSet方法会通过类org/slf4j/impl/StaticLoggerBinder.class

```java
  private static final void bind() {
        String msg;
        try {
            Set<URL> staticLoggerBinderPathSet = null;
            if (!isAndroid()) {
                // 类加载器加载所有实现StaticLoggerBinder的类
                staticLoggerBinderPathSet = findPossibleStaticLoggerBinderPathSet();
                reportMultipleBindingAmbiguity(staticLoggerBinderPathSet);
            }
            StaticLoggerBinder.getSingleton();
            INITIALIZATION_STATE = 3;
            reportActualBinding(staticLoggerBinderPathSet);
            fixSubstituteLoggers();
            replayEvents();
            SUBST_FACTORY.clear();
        } catch (NoClassDefFoundError var2) {
            msg = var2.getMessage();
            if (!messageContainsOrgSlf4jImplStaticLoggerBinder(msg)) {
                failedBinding(var2);
                throw var2;
            }
            INITIALIZATION_STATE = 4;
            Util.report("Failed to load class \"org.slf4j.impl.StaticLoggerBinder\".");
            Util.report("Defaulting to no-operation (NOP) logger implementation");
            Util.report("See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.");
        } catch (NoSuchMethodError var3) {
            msg = var3.getMessage();
            if (msg != null && msg.contains("org.slf4j.impl.StaticLoggerBinder.getSingleton()")) {
                INITIALIZATION_STATE = 2;
                Util.report("slf4j-api 1.6.x (or later) is incompatible with this binding.");
                Util.report("Your binding is version 1.5.5 or earlier.");
                Util.report("Upgrade your binding to version 1.6.x.");
            }
            throw var3;
        } catch (Exception var4) {
            failedBinding(var4);
            throw new IllegalStateException("Unexpected initialization failure", var4);
        }
    }
```

```java
static Set<URL> findPossibleStaticLoggerBinderPathSet() {
        LinkedHashSet staticLoggerBinderPathSet = new LinkedHashSet();

        try {
            ClassLoader loggerFactoryClassLoader = LoggerFactory.class.getClassLoader();
            Enumeration paths;
            // 使用系统类加载器或应用程序类加载器
            if (loggerFactoryClassLoader == null) {
                paths = ClassLoader.getSystemResources(STATIC_LOGGER_BINDER_PATH);
            } else {
                paths = loggerFactoryClassLoader.getResources(STATIC_LOGGER_BINDER_PATH);
            }

            while(paths.hasMoreElements()) {
                URL path = (URL)paths.nextElement();
                staticLoggerBinderPathSet.add(path);
            }
        } catch (IOException var4) {
            Util.report("Error getting resources from path", var4);
        }

        return staticLoggerBinderPathSet;
    }
```
StaticLoggerBinder类中获取工厂的方法,被LoggerFactory类的getILoggerFactory方法调用

```java
 public ILoggerFactory getLoggerFactory() {
        if (!this.initialized) {
            return this.defaultLoggerContext;
        } else if (this.contextSelectorBinder.getContextSelector() == null) {
            throw new IllegalStateException("contextSelector cannot be null. See also http://logback.qos.ch/codes.html#null_CS");
        } else {
            return this.contextSelectorBinder.getContextSelector().getLoggerContext();
        }
    }
```

在log4j和logback等常用日志框架中都会发现其中的LoggerContext类实现了slf4j定义的ILoggerFactory接口,slf4j通过getLoggerFactory拿到各自工厂，创建各自logger对象。

##### 适配器模式与外观模式：

​	适配器模式可以将一个或多个类接口转变成用户所期望的一个接口。外观模式也可以针对一系列复杂接口提供简化的接口。两种模式的差异不在于包装了多少个类，而在于它们的意图。适配器模式的意图是改变接口以符合用户的需要，外观模式是提供一系列复杂接口的一个简化接口。	

