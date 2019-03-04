## java项目中@Value读取配置文件的问题

``` java
最近在写后台管理系统，我在写完配置文件之后通过 @Value("{name}")获取属性值，但是出乎意料的是读不到值，开始以为是路径不对，所以在类上添加了一个@PropertySource("classpath:application.properties")注解来读取配置文件的路径，可是尝试之后发现也不对，后在网上找到类似的案例，要通过 @Value("propertiesReader{name}")才可以读取
  关键字：spring注解中使用properties配置文件
```