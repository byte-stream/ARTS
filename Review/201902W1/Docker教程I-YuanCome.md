> 最近在了解docker然后看了一些国内互联网公司对自己系统进行容器化的文章/新闻，然后之前也了解过一下Docker，觉得从官方文档的教程开始学习挺好的，就打算Review Docker的官方教程（PS：主要是找好的Review内容比较难，官方文档是最好的：））  
> 原文链接：https://docs.docker.com/get-started/  
  
## Docker概念  
Docker是开发人员和系统管理员使用容器进行开发、部署和运行应用程序的平台，使用Linux容器部署应用程序被称为容器化。容器不是一项新的技术，但是它们的使用让部署应用程序变得简单。  
  
#### 容器化变得越来越受欢迎，因为：
- 灵活性：即使是最复杂的应用程序都能被容器化。 
- 轻量级：容器利用和共享主机的内核资源。  
- 可交换：你可以部署动态更新和升级。  
- 便携性：你可以在本地构建然后部署到云端，随处运行。  
- 扩展性：你可以增加和自动分配容器副本。  
- 堆叠性：你可以即时垂直堆叠服务。  
  
#### 镜像和容器  
  
镜像是一个可执行的包，它包括运行应用程序的所有内容——代码、运行环境、库、环境变量、配置环境。通过运行镜像来启动容器。  
  
容器是镜像的运行实例——当被执行时，图像的状态或用户进程在内存中的情况，当你在使用 Linux 时，你可以通过`docker ps`命令来查看正在运行的容器列表。  
  
#### 容器和虚拟机  
  
一个容器运行在原生Linux上与其他容器共享主机内核。容器轻量级表现在其运行在一个**独立**的进程上，不占用其他可执行文件的内存资源。  
  
相比之下，虚拟机运行一个完整的“客户”操作系统，通过虚拟机管理程序对虚拟机资源进行访问。通常虚拟机提供的环境比大多数应用程序需要的资源要多。  

<img src="https://docs.docker.com/images/Container%402x.png" width=40% height=40%  /><img src="https://docs.docker.com/images/VM%402x.png" width=40% height=40% align="right" />
  
#### 准备安装Docker  
在[支持的平台](https://docs.docker.com/ee/supported-platforms/)上安装[维护版本](https://docs.docker.com/install/)的Docker社区版或Docker企业版   
  
> 完整的Kubernetes集成
> - [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/kubernetes/)上的[Kubernetes](https://docs.docker.com/docker-for-mac/kubernetes/)可在[17.12 Edge（mac45）](https://docs.docker.com/docker-for-mac/edge-release-notes/#docker-community-edition-17120-ce-mac45-2018-01-05)或 [17.12 Stable（mac46）](https://docs.docker.com/docker-for-mac/release-notes/#docker-community-edition-17120-ce-mac46-2018-01-09)及更高版本中使用。
> - [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/kubernetes/) 上的[Kubernetes](https://docs.docker.com/docker-for-mac/kubernetes/)仅在 [18.02 Edge（win50）](https://docs.docker.com/docker-for-windows/edge-release-notes/#docker-community-edition-18020-ce-rc1-win50-2018-01-26)和更高的版本中提供。  
#### 测试Docker版本  
  
1. 运行`docker --version`并确保您拥有支持的Docker版本：   
  

    docker --verison   
    Docker version 17.12.0-ce, build c97c6d6  

2. 运行`docker info`或（`docker version` 不添加`--`） 查看更多关于Docker的安装信息  
  
  
    docker info  

    Containers: 0
    Running: 0
    Paused: 0
    Stopped: 0
    Images: 0
    Server Version: 17.12.0-ce
    Storage Driver: overlay2
    ...  
  
> 为了避免权限错误（以及使用`sudo`），请把你的用户添加到`docker`组中。[请查看](https://docs.docker.com/install/linux/linux-postinstall/)  
  
#### 测试Docker安装  
1.通过运行简单的Docker镜像[hello-world](https://hub.docker.com/_/hello-world/)来测试安装是否有效：  
  
  
    docker run hello-world

    Unable to find image 'hello-world:latest' locally
    latest: Pulling from library/hello-world
    ca4f61b1923c: Pull complete
    Digest: sha256:ca0eeb6fb05351dfc8759c20733c91def84cb8007aa89a5bf606bc8b315b9fc7
    Status: Downloaded newer image for hello-world:latest

    Hello from Docker!
    This message shows that your installation appears to be working correctly.
    ...  
  
2. 列出下载到你计算机上的`hello-word`镜像 
    

    docker image ls  
  
3. 列出`hello-world`在其退出后显示（由镜像生成）信息，如果它仍在运行，你不需要使用`--all`选项：  
  
  
    docker container ls --all
    CONTAINER ID     IMAGE           COMMAND      CREATED            STATUS
    54f4984ed6a8     hello-world     "/hello"     20 seconds ago     Exited (0) 19 seconds ago  
  
#### 回顾  
  
  
    ## List Docker CLI commands
    docker
    docker container --help

    ## Display Docker version and info
    docker --version
    docker version
    docker info

    ## Execute Docker image
    docker run hello-world

    ## List Docker images
    docker image ls

    ## List Docker containers (running, all, all in quiet mode)
    docker container ls
    docker container ls --all
    docker container ls -aq  
      
#### 第一部分总结  
容器化使[CI/CD](https://www.docker.com/solutions/cicd)无缝。例如：  

- 应用程序没有系统依赖性
- 可以将更新推送到分布式应用程序的任何部分
- 资源密度可优化
  
使用Docker你的应用程序将只是一个可执行文件，而不是运行繁重的虚拟机。