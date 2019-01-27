>本周看了一篇石衫的架构笔记中的 [拜托！面试请不要再问我Spring Cloud底层原理](https://juejin.im/post/5be13b83f265da6116393fc7)，感觉讲得很好，通俗易懂，对几个Spring Cloud中的组件有了初步的认识，以下选自文章中的总结  
Eureka：各个服务启动时，Eureka Client都会将服务注册到Eureka Server，并且Eureka Client还可以反过来从Eureka Server拉取注册表，从而知道其他服务在哪里  
Ribbon：服务间发起请求的时候，基于Ribbon做负载均衡，从一个服务的多台机器中选择一台  
Feign：基于Feign的动态代理机制，根据注解和选择的机器，拼接请求URL地址，发起请求  
Hystrix：发起请求是通过Hystrix的线程池来走的，不同的服务走不同的线程池，实现了不同服务调用的隔离，避免了服务雪崩的问题  
Zuul：如果前端、移动端要调用后端系统，统一从Zuul网关进入，由Zuul网关转发请求给对应的服务  
