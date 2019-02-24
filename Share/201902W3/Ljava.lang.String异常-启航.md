## Ljava.lang.String异常

​	最近遇到的一个问题，前端（Ext）提交表单对象，在Oracle保存的时候，报noSuchMethodException :  btManager.SetId(),  (Ljava.lang.String)

​	当时第一反应是id没有加get，set方法，后来发现加了，

然后网上找了一些例子，看了下出现这个问题的原因，实体类中的id是long类型，我前端往后传的是类型Long的id（默认为null），我后台接收使用的是long接收，这是一个基本数据类型（默认值0L），我没给id赋值，则id在oracle中自增时出现了异常，后来将实体类中的id类型改为Long后正常。	

​	关键：基本数据类型和包装类的区别

​		包装类默认值为null

| 基本数据类型  | 默认值            |
| ------- | -------------- |
| char    | '/uoooo'(null) |
| byte    | (byte)0        |
| short   | (short)0       |
| int     | 0              |
| long    | 0L             |
| float   | 0.0f           |
| double  | 0.0d           |
| boolean | false          |