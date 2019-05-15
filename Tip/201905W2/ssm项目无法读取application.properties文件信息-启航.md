## ssm项目无法读取application.properties文件信息

本意是想将属性信息写到配置文件中，易于后面修改，下面就是我整个出错并修改的流程

1.将配置信息写到文件后，没有修改接收的对象类型(之前是Integer，后来修改成String)，导致转换异常，如图1

[图1](https://wx3.sinaimg.cn/mw690/005upnwVly1g30n281gl7j30vi069aau.jpg)

2.修改之后拿到的DADI_IDENTIFY 为“${DADI_IDENTIFY}”，如图2

[图2](https://wx3.sinaimg.cn/mw690/005upnwVly1g30n50xhspj30ra01eaa0.jpg)

3.而且在其他地方报了一个异常*Could not resolve placeholder*（关键点），如图3

[图3](https://wx4.sinaimg.cn/mw690/005upnwVly1g30n5ijm6oj30o802imx7.jpg)

3.当时想的是springMvc配置文件中没有开启包扫描，然后在dispatcherServlet.xml看了下发现已经开启，那么既然已经包扫描，为什么还是读不到值呢，然后网上找了下，发现是applicationContext.xml中没有配置application.properties的路径。zzz，添加之后就能成功读取配置文件的值了。添加如图4中的属性即可

[图4](https://wx4.sinaimg.cn/mw690/005upnwVly1g30n5vdoktj30v0054jrm.jpg)



[参照链接](https://www.cnblogs.com/YingYue/p/5699962.html)