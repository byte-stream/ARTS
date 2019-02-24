> Docker官方教程三，接着上周的文章继续翻译。  
  
## 服务  
  
#### 先要条件  
- 安装Docker 1.13或更高版本。

- 获取Docker Compose。在适用于Mac的Docker Desktop和适用于Windows的Docker Desktop上，它已预先安装，因此您可以随意使用。在Linux系统上，您需要直接安装它。在没有Hyper-V的 Windows 10系统之前 ，请使用Docker Toolbox。

- 阅读第1部分中的方向。

- 在第2部分中了解如何创建容器。

- 确保已 `friendlyhello` 通过将其创建到注册表来发布您创建的图像 。我们在这里使用该共享图像。

- 确保您的图像作为已部署的容器运行。运行此命令，在您的信息开槽`username`，`repo`和`tag`：`docker run -p 4000:80 username/repo:tag`，然后访问`http://localhost:4000/`。  
  
#### 介绍  
在第3部分中，我们扩展应用程序并启用负载平衡。为此，我们必须在分布式应用程序的层次结构中提升一级： **服务**。  
- 堆
- **服务**（你在这里）
- 容器（第2部分）  
  
#### 关于服务  
在分布式应用程序中，应用程序的不同部分称为“服务”。例如：你假设一个视频共享站点，它可能包括一个用于在数据库中存储应用程序的服务，一个用户在上传内容后在后台进行视频转码的服务，一个用于前端的服务，等等。  
  
服务实际上只是“生产中的容器”。服务只运行一个镜像，但它定义了镜像的运行方式——它运行的端口，应该运行多少个镜像副本以便提供服务所需的容量，等等。扩展服务会更改运行该软件的容器实例的数量，从而为流程中的服务分配更多计算资源。  
  
幸运的是，使用Docker平台定义，运行和扩展服务非常容易 - 只需编写一个`docker-compose.yml`文件即可。  
  
#### 你的第一个`docker-compose.yml`文件  
`docker-compose.yml`文件是一个YAML文件，它定义了 Docker 容器在生产中的操作。  
  
#### `docker-compose.yml`  
把 `docker-compose.yml` 文件保存在你想要的任何位置上，确保已经将第 2 部分的镜像推送到注册表，并通过修改你容器信息中的 `username/repo:tag` 来更新这个 `.yml` 文件。  
  
    version: "3"
    services:
        web:
        # 用你的名字和镜像信息替换 username/repo:tag
        image: username/repo:tag
        deploy:
            replicas: 5
            resources:
                limits:
                    cpus: "0.1"
                    memory: 50M
            restart_policy:
                condition: on-failure
        ports:
            - "4000:80"
        networks:
            - webnet
    networks:
        webnet:  
  
这个 `docker-compose.yml` 文件告诉 Docker 执行以下操作：  

- 拉我们在步骤2中上传的图像从注册表。

- 将该映像的5个实例作为调用的服务运行web，限制每个实例使用，最多10％的CPU（跨所有内核）和50MB的RAM。

- 如果一个失败，立即重启容器。

- 将主机上的端口4000映射到web端口80。

- 指示web容器通过称为负载平衡的网络共享端口80 webnet。（在内部，容器本身web在短暂的端口发布到 80端口。）

- webnet使用默认设置（负载平衡的覆盖网络）定义网络。  
  
#### 运行新的负载均衡应用程序  
  
在我们运行 `docker stack deploy` 命令之前，先执行：  
  
    docker swrm init  
  
> 注意：我们在第4部分中介绍了该命令的含义。如果您没有运行 `docker swarm init` 则会收到“此节点不是群集管理器”的错误。  
  
现在，我们运行它，你需要给你的应用程序命名，在这里它将会被设置为 `getstartedlab` :  
  
    docker stack deploy -c docker-compose.yml getstartedlab  
  
我们的单个服务堆栈在一台主机上运行已部署镜像的5个容器实例。让我们来研究一下。  
  
在我们的应用程序中获取一项服务的服务ID：  
  
    docker service ls  
  
输出以你应用程序名字为前缀的 `web` 服务信息。如果你把它命名和示例中的一样，则名称为 `getstartedlab_web`。此外，还列出了服务ID、实例副本数、镜像名字和暴露的端口。  
  
或者你可以运行`docker stack services`，加上你的堆栈名字。以下示例命令允许您查看与`getstartedlab`堆栈关联的所有服务 ：  
  
    docker stack services getstartedlab
    ID                  NAME                MODE            REPLICAS            IMAGE               PORTS
    bqpve1djnk0x        getstartedlab_web   replicated          5/5                 username/repo:tag   *:4000->80/tcp  
  
在服务中运行的单个容器称为任务。任务被赋予以数字递增的唯一ID，最大为你在`docker-compose.yml`上定义的`replicas`属性大小。列出您的服务任务：  
  
    docker service ps getstartedlab_web  
  
如果您只列出系统上的所有容器，则任务也会显示，但不会被服务过滤：  

    docker container ls -q  

你可以在命令行中多次运行`curl -4 http://localhost:4000`，或者打开浏览器跳转到该URL并点击几次刷新。   

![](https://docs.docker.com/get-started/images/app80-in-browser.png)  
  
无论哪种方式，容器ID都会发生变化，从而证明实现了负载均衡。对于每个请求，以循环方式选择5个任务中的一个来响应。容器ID为上一条命令`docker container ls -q`输出的一致。  
  
要查看堆栈的所有任务，你可以运行`docker stack ps`加上你的应用程序名，如以下示例所示：  
  
    docker stack ps getstartedlab
    ID                  NAME                  IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
    uwiaw67sc0eh        getstartedlab_web.1   username/repo:tag   docker-desktop      Running             Running 9 minutes ago                       
    sk50xbhmcae7        getstartedlab_web.2   username/repo:tag   docker-desktop      Running             Running 9 minutes ago                       
    c4uuw5i6h02j        getstartedlab_web.3   username/repo:tag   docker-desktop      Running             Running 9 minutes ago                       
    0dyb70ixu25s        getstartedlab_web.4   username/repo:tag   docker-desktop      Running             Running 9 minutes ago                       
    aocrb88ap8b0        getstartedlab_web.5   username/repo:tag   docker-desktop      Running             Running 9 minutes ago  
  
> #### 运行在Windows 10上？  
> 在Windows 10 PowerShell上可以使用 `curl`,如果无法使用，你可以使用一个Linux终端，如GitBASH，或者下载wget for Windows等类似的命令行终端。  
  
> #### 响应时间慢？  
> 根据你环境的网络配置，容器最多可能需要30秒才能响应HTTP请求。这并不表示Docker或swarm性能，而是我们在本教程后面讨论的未满足的Redis依赖性。目前，访客柜台因同样的原因不起作用; 我们还没有添加服务来保存数据。  
  
#### 扩展应用程序  
你可以通过更改`docker-compose.yml`的`replicas`值，保存更改后重新运行`docker stack deploy`命令来扩展程序。  
  
    docker stack deploy -c docker-compose.yml getstartedlab  
  
Docker执行是热更新，无需首先拆除堆栈或结束任何容器进程。  
  
现在，重新运行`docker container ls -q`以查看已重新配置的已部署实例。如果提高实例副本数量，则会启动更多任务，从而启动更多容器。  
  
#### 关闭容器和集群  

- 将应用程序关闭`docker stack rm`：  
 
        docker stack rm getstartedlab  

- 关闭集群：  
  
        docker swarm leave --force 
  
使用Docker建立和扩展你等应用程序变得简单。你已经朝着学习如何在生产中运行容器迈出了一大步，接下来，你将学习如何在Docker机器群集上运行此应用程序作为真正的群体。  