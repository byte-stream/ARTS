# AWS 云平台资源成本管理

想必大家都接触过虚拟机，云上虚拟机或者对象存储等资源应该也用过，比如阿里云的 ECS 以及 OSS，这些资源我们购买一年也就几百元。不必考虑成本，一次性购买。但对于公司来说，使用的云不仅仅是阿里云，而是使用更前沿的 AWS 以及 Azure，并且使用的资源也不仅仅是虚拟机，云上的服务有上百种，公司用了几十种，那么管理这些资源就成了一个问题，而且公司使用资源的开销都是以百万 / 年计算的，最近在管理管理这方面的成本，我也有幸参与到其中做部分工作，下面分享在 AWS 上我所学到的一个成本管理服务 - AWS Cost Explorer。

它只是 AWS 众多应用中的一个服务：

![1550321613137](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550321613137.png)

在主页面可以看到详细的开销，并且有图表直观展示

![1550321706781](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550321706781.png)



在子菜单下 Explore Cost & Usage 可以对所有资源进行详细分析，根据各种过滤器进行筛选，按不同维度查看价格，并且可以将做好的维度进行保存，生成 report，下次直接点开即可查看。

![1550321806015](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550321806015.png)



除了最基本的图表以外，还有详细的数据信息

![1550321967464](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550321967464.png)



以上是 AWS 提供查看应用开销的一个服务，除此以外，还可以在账单下查看另一种详细的价格，还能看到各种不同类型资源的单价。

![1550322132813](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550322132813.png)

![1550322167286](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550322167286.png)



还可以导出 CSV 文件，结合 EXCEL 分析这些资源。除此之外，还能通过首选项设置，将每天的数据以 CSV 文件导出到指定的 S3 存储桶，这样随时就可以分析资源的价格了。

![1550322301418](C:\Users\zhiyu.zeng\AppData\Roaming\Typora\typora-user-images\1550322301418.png)



市面上各种云平台，AWS 是最完善的，并且我目前也只发现 AWS 有这么好用的账单管理服务，Azure 也有自家的账单管理，但并没有这么好的使用体验。国内的云平台就更不用说了，很多服务都还没有，不过阿里云做得也很不错了，只能说 AWS 比较强，当然价格也是很贵的。