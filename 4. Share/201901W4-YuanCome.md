## SpringBoot 和 Vue 前后端分离开发与合并   
> 一开始不知道分享什么好，一直找不到好的分享点，恰好昨晚一位做前端的朋友问我SpringBoot + Vue 前后端分离开发完成后如何进行项目合并。我觉得这个可以作为分享点，给大家参考一下。  
     
现在的项目开发大多数都是前后端分离，以便快速完成开发项目，现在SpringBoot 和 Vue结合，大致有两种方案：  
1. 在html中直接使用script标签引入vue和一些常用的组件，这种方式和以前传统的开发是一样的，只是可以使用vue的双向数据绑定，适合于普通的全栈开发。  
2. 使用vue官方的脚手架创建单独的前端工程项目，做到和后端完全独立开发和部署，后端单独部署一个纯restful的服务，而前端直接采用nginx来部署，这种称为完全的前后端分离架构开发模式，但是在分离中有很多api权限的问题需要解决，包括部署后的vue router路由需要在nginx中配置rewrite规则。  
  
采用前后端开发后整合合并，在传统行业中比较常见，整合合并之后只需要打一个SpringBoot包。  
  
### 下面讲讲如何整合合并：  
  
- #### 简单方法：  
  
前端开发好后将build构建好的dist下static中的文件拷贝到springboot的resource的static下，index.html则直接拷贝到springboot的resource的static下。   

Vue代码目录结构：  

![](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/dkwuWwLoRKicqyOtax0Hhl3efDCpqTAB7oHM7ftVnibAF5YfjicDiakxWYdehCVibksdzwX5wmk4u5QFYBDiarGMcGxA/640?wx_fmt=png)  
[图片来源](https://blog.csdn.net/liyanlei5858/article/details/80771713)
  
SpringBoot代码目录结构： 
  
![](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/dkwuWwLoRKicqyOtax0Hhl3efDCpqTAB7VX7dtKkWdjlWptMTHTiabibdo0JQ6RacPTnicKvZ9LM4JkbAdEgwr2umA/640?wx_fmt=png)  
[图片来源](https://blog.csdn.net/liyanlei5858/article/details/80771713)
  
这种方式**不适合工程项目**，也没有做到真正的**前后端代码分离**。我们更应该使用构建工具进行项目整合的构建，在构建springboot时触发前端构建并编写自动化脚本将前端webpack构建好的资源拷贝到springboot下再进行jar的打包，最后就得到了一个完全包含前后端的springboot项目了。  
  
合并的核心问题：  
1. 无法正常访问静态资源。
2. vue router路由的路径无法正常解析。  
  
关于问题1，只需要在SpringBoot代码中修改静态资源的路径即可。  
  
参考例子：  

![](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/dkwuWwLoRKicqyOtax0Hhl3efDCpqTAB7Cuia31NS6qiayqm7mszraDMylFBia5cWOibvMQ6qAtWw2SgNKJhf110L4w/640?wx_fmt=png, "参考例子")  
  
关于问题2：需要在 Vue 中修改路由的路径，然后交由 router 来处理，修改路由路径的时候可以使用同一的前缀或者后缀，然后 SpringBoot 添加相应的拦截器进行拦截。  
  
关于 SpringBoot 和 Vue 的整合大题就是这些内容。  
  
**如果有足够的资源条件下，更推荐前后端独立开发部署**。