[SOLID Principles every Developer Should Know](<https://blog.bitsrc.io/solid-principles-every-developer-should-know-b3bfa96bb688>) 每个开发者都该知道的 SOLID 原则，深度好文，推荐阅读。

作者主要讲了面对对象编程的 5 个原则：

- S：Single Responsibility Principle（单一职责原则）
- O：Open-Closed Principle（开闭原则）
- L：Liskov Substitution Principle（里氏替换原则）
- I：Interface Segregation Principle（接口隔离原则）
- D：Dependency Inversion Principle（依赖倒置原则）

##### 单一职责原则

当设计类的时候，我们应该把相关的功能放到一起，这样就算要修改也是因为相同的原因修改。同时，对于不同原因带来的改动要进行功能拆分。

##### 开闭原则

软件实体（类、模块、函数）应该对扩展开放，对修改关闭。比如，要添加功能时，在原来的基础上修改 if-else 实现，还是把共有的方法抽取出来通过继承来实现呢，显然要扩展而不是修改。

##### 里氏替换原则

子类可以替代它的父类。满足 LSP 的两个要求：

- 如果父类有一个接收父类型参数的方法，那么它的子类应当接收父类型或者其子类型作为参数。
- 如果父类方法的返回值是父类型，那么它的子类应当返回父类型或者其子类型。

##### 接口隔离原则

使用类不应该被强制要求实现它们不需要的接口。一个全能的接口，什么事都可以干，我们不需要它，我们只要专心做一件事的接口。

##### 依赖倒置原则

依赖倒置因该针对抽象而不是具体。

- 高层模块不该依赖低层模块，它们都该依赖抽象类。
- 抽象不该依赖具体，具体应当依赖抽象。

点评：文中举了几个例子，非常简洁易懂。为了写出可读可维护的代码，我们尽量还是要遵循SOLID 原则。
