# IDEA 调试远程服务器代码

编辑运行配置

![1550754020640](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550754020640.png)

选择 remote 配置，填写主机 ip 和指定一个用于连接的端口，会自动生成一串 JVM 参数

![1550754052834](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550754052834.png)

保存好



将参数添加到 java 启动命令行中：![1550754266753](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550754266753.png)



在服务器启动应用后，在 IDEA 本地启动 remote，将会连接到服务器

![1550754393725](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550754393725.png)



打断点后，就可以像在本地调试一样，只是通过 socket 连接，依赖于网速，所以调试很慢。

