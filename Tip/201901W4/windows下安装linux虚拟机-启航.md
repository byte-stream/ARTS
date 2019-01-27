# windows下安装linux虚拟机

#### 1.关于linux

 Linux基于GPL(Genaral PublicLicene)协议，是一个自由的，免费的，源码开放的操作系统。 存在着许多不同的Linux版本，但它们都使用了Linux内核。它的特点是稳定：可使用多年不重启，应用版本多是命令界面。他被广泛应用于服务器系统（Web应用服务器、数据库服务器、游戏服务器、接口服务器）以及嵌入式系统（路由器、手机等）

市场常见的有（redhat，ubantu，centos），这里安装的是centos

#### 2.安装前准备

- 下载VMware Workstation，版本可自行选择，在windows安装 [地址](https://my.vmware.com/en/web/vmware/free#desktop_end_user_computing/vmware_workstation_player/15_0)  
- 下载centos，[地址](https://www.centos.org/download/)

#### 3.安装linux

1. 启动vmvare
2. 点击file--> new virtual machine 创建虚拟机
3. 在弹出框中选择典型安装，next
4. 选择 i will install  the operation system later(稍后安装)，next
5. 选择引导系统是linux 并选择系统版本是centos ， next
6. 选择linux安装位置，以及虚拟机的名称，next
7.  然后选择你本次想安装的linux占用磁盘空间， next
8. 选择安装前的硬件设置（customize hard...）,在弹出框中配置虚拟机的内存，推荐1-2G，当然如果你的计算机内存足够大，可以往上加，  然后选择ISO映像文件（即刚才下载的linux文件），close ，finish
9. 在vmvare，我的计算机中找到刚才安装的centos ，开启此虚拟机如弹出welcome to centos ..    点击install or update an existing system，探后弹出一个disc found 框， 选择 skip 跳过，引导安装，next
10. 选择中文，next ，选择美国英语，next
11. 选择基本存储设备，然后选择是，忽略所有数据
12. 命名主机名(建议英文，不要有特殊字符)，然后配置网络，选中system eth0 编辑，勾选自动连接，并应用，next
13. 选择城市亚洲上海，接着输入管理员密码（要自己能记住就行）一般个人使用root，选择无论如何使用，然后选择使用所有空间，将修改写入磁盘
14. 选择basic server基础版服务，等待安装
15. 安装完之后，重新引导，输入刚才的用户名密码，进入系统。到此安装结束