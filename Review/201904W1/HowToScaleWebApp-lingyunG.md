这周阅读了一篇[文章](https://arcentry.com/blog/scaling-webapps-for-newbs-and-non-techies/)，文章给非技术人员生动有趣地讲解了Web服务该如何随着用户量的不断增加而扩展系统，提到了许多平时听到过的名词但是没有在项目中用到的名词。比如“Reverse proxy”,"Load Balancer"等。

Web服务发展可以分为以下几个步骤:
1 A single server + database
2 Adding a Reverse Proxy/Load Balancer
3 Growing you Database
4 使用微服务架构拆解系统
5 使用Caching && CDN 使系统更高效
7 采用Message Queues服务
8 分区，将不同来源的请求分发到不同的区域处理，每个区域里面的服务也都是完整的
9 引用DNS域名服务器

在讲完上述步骤之后，作者提到云服务是解决上述所有问题的方案，但是这也并不意味这云服务就一点问题都没有。