最近在阅读《深入理解java虚拟机：jvm高级特性与最佳实践》，担心有些地方自己记不住，所以做一些读书笔记以供自己日后查阅。

Java 虚拟机运行时数据区

1 程序计数器

1）记录当前所执行的字节码的行号指示器

2）唯一一个在java虚拟机中没有规定OutOfMemoryError情况的区域

2 Java虚拟机栈

1）这部分存储和程序计数器一样是线程私有

2）用于存储局部变量，操作数栈，动态链接，方法出口等信息

3）会抛出StackOverFlowError 和 OutOfMemoryError异常信息

3 本地方法栈

1）与虚拟机栈一样，只不过它调用的是本地native方法

2）会抛出StackOverFlowError 和 OutOfMemoryError异常信息

4 Java堆

1）Java虚拟机所管理的内存中最大的一块

2）垃圾收集器管理的主要区域

3）各个线程共享的内存区域

5 方法区

1）运行时常量池是方法区的一部分

2）各个线程共享的区域

3）会抛出OutOfMemory异常