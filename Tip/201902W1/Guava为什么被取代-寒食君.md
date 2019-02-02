前段时间在为一个模块做本地缓存的时候，一开始我使用的是HashMap,但是后来考虑到线程安全问题，转用了ConcurrentHashMap,再后来为了避免OOM问题，考虑使用类库。

Guava作为大名鼎鼎的第三方开发包，内置了诸多JDK不支持的方便功能，本地缓存是其中一个被高频使用的功能。

如果只是将其作为JavaBean来集成，没有什么问题，但是后来准备直接使用Spring framework来配置本地缓存，发现竟然已经不再被支持。

取而代之的，是caffine。既然SpringBoot团队这么做，必然有其原因。啰嗦了这么多，上面其实提出了三个问题：

1. HashMap -> ConcurrentHashmap
2. ConcurrentHashmap -> OOM ->Guava
3. Guava -> caffine

要解释这三个问题，需要查询一些资料以及结合自己的实际使用感受，篇幅较长，这边只是提供一个思考过程，具体的理解和实践我准备后面单独整理成文。

