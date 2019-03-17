> Docker官方教程四，接着之前的文章继续翻译  
  
## 群  
#### 介绍  
在第3部分中，您使用了你在第2部分中编写的应用程序，并通过将其转换为服务来定义它应如何在生产中运行，在此过程中将其扩展5倍。

在第4部分中，你将此应用程序部署到集群上，在多台计算机上运行它。多容器，多机应用程序通过连接多台机器到称为一个“Dockerized”的集群称为群  
  
#### 了解群
群是一组运行Docker并加入集群的计算机。在此之后，你继续运行你习惯使用的Docker命令，但现在它们由群管理器在集群上执行。群中的机器可以是物理的或虚拟的。加入群组后，它们被称为节点。  
  
群管理器可以使用多种策略来运行容器，例如“最空的节点”--容器中利用率最少的计算机。或者“全局”，它确保每台机器只获得指定容器的一个实例。你指示群管理器在Compose文件中使用这些策略，就像你已经使用的那样。  
  
群管理器是群中唯一可以执行命令的机器，或者授权其他机器充当群中的工人一样加入群。这些“工人”只提供运行能力，没有权利告诉其他机器它能干什么不能干什么。  
  
到目前为止，你一直在本地计算机上以单主机模式使用Docker。但是Docker可以切换到群模式，这就是使用群的原因。立即使用群模式，使当前的计算机成为群管理器，从此，Docker的命令将会在群中执行，而不仅仅是当前的机器。  
  
#### 设置你的群  
群由多个可以是物理或虚拟机的节点组成。基本概念很简单：运行`docker swarm init`以启用群模式并使当前计算机成为一个群管理器，然后`docker swarm join`在其他计算机上运行 以使它们作为“工人”加入群。选择下面的标签，了解它在各种情况下的效果。我们使用VM快速创建一个双机集群并将其转换为群。  
  
#### 创建一个集群  
本地计算机上的VM（MAC，LINUX，WINDOWS 7和8） 
> 注意：如果您使用的是安装了Hyper-V的Windows系统（如Windows 10），则无需安装VirtualBox，而应使用Hyper-V。单击上面的Hyper-V选项卡查看Hyper-V系统的说明。如果你使用的是Docker Toolbox，你应该已经安装了VirtualBox作为其中的一部分，所以你可以开心使用它。  
  
现在使用`docker-machine`创建一个双机集群，使用VirtualBox 驱动程序：  
  
    docker-machine create --driver virtualbox myvm1
    docker-machine create --driver virtualbox myvm2  
  
列出虚拟机并获取其IP地址  
您现在创建了两个名为myvm1和 myvm2 的虚拟机。  
使用此命令列出虚拟机并获取其IP地址。  
> 注意：您需要以管理员身份运行一下命令，否则您将无法获得任何合理的输出，进获得 UNKNOW。  
  
    docker-machine ls  
  
以下是此命令的示例输出：  

    $ docker-machine ls
    NAME    ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER        ERRORS
    myvm1   -        virtualbox   Running   tcp://192.168.99.100:2376           v17.06.2-ce
    myvm2   -        virtualbox   Running   tcp://192.168.99.101:2376           v17.06.2-ce  
  
初始化群，并添加节点
第一台机器充当管理器，它执行管理命令并验证工人加入群，第二台是工人。  
您可以使用`docker-machine ssh`命令向VM发送命令。使用`docker swarm init`指示`myvm1` 成为一个群管理器并查找如下输出：  
  
    $ docker-machine ssh myvm1 "docker swarm init --advertise-addr <myvm1 ip>"
    Swarm initialized: current node <node ID> is now a manager.

    To add a worker to this swarm, run the following command:

    docker swarm join \
    --token <token> \
    <myvm ip>:<port>

    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.  
  
> 端口2377和2376  
> 运行`docker swarm init` 和 `docker swarm join` 加端口2377（群管理器端口），或者不指定端口，使用默认端口。  
> 使用`docker-machine ls`将会列出机器的IP地址包括Docker的守护进程端口2376，不要使用此端口，否则将会报错。  
  
> 使用SSH时遇到问题？试试--native-ssh标志  
> Docker Machine 可以让您使用自己系统的SSH，如果由于某种原因您无法向群管理器发送命令。只需在调用`ssh`命令时指定 `--native-ssh`标志。

    docker-machine --native-ssh ssh myvm1 ...
  
如你所见，使用`docker swarm init`命令后需要预先配置`docker swarm join`让你运行你想要添加的节点。复制该命令，然后通过`docker-machine ssh`发送到`myvm2`,使`myvm2`作为工人加入你的群：  

    $ docker-machine ssh myvm2 "docker swarm join \
    --token <token> \
    <ip>:2377"

    This node joined a swarm as a worker.  
  
恭喜你，你成功创建了第一个群。  
运行`docker node ls`来查看你在这个群的节点：  
  
    $ docker-machine ssh myvm1 "docker node ls"
    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
    brtu9urxwfd5j0zrmkubhpkbd     myvm2               Ready               Active
    rihwohkh3ph38fhillhhb84sk *   myvm1               Ready               Active              Leader  
  
> 离开群   
> 如果你重新开始，可以从每个节点上运行：`docker swarm leave`  
  
#### 在群集群集上部署您的应用程序  
艰难的部分结束了。现在，您只需重复第3部分中使用的过程即可部署到新的swarm上。 请记住，只有群体管理员`myvm1`执行Docker命令; 工人只是为了提供能力。 
  
#### 为群管理器配置一个 `docker-machine` shell  
到目前为止，您已经将Docker命令`docker-machine ssh`包装在与虚拟机通信中。另一种选择是运行`docker-machine env <machine>`以获取并运行一个命令，该命令将当前shell配置为与虚拟机上的Docker守护程序通信。此方法适用于下一步，因为它允许您使用本地`docker-compose.yml`文件“远程”部署应用程序，而无需将其复制到任何位置。  
  
输入`docker-machine env myvm1`，然后复制粘贴并运行作为输出的最后一行提供的命令，以配置要与之通信的shell（`myvm1`群管理器）。 
  
配置shell的命令因Mac，Linux或Windows而异，因此每个示例都显示在下面的选项卡上。 

MAC或LINUX上的DOCKER机器SHELL环境  
运行`docker-machine env myvm1`以获取命令以配置要与`myvm1`通信的shell。
  
    $ docker-machine env myvm1
    export DOCKER_TLS_VERIFY="1"
    export DOCKER_HOST="tcp://192.168.99.100:2376"
    export DOCKER_CERT_PATH="/Users/sam/.docker/machine/machines/myvm1"
    export DOCKER_MACHINE_NAME="myvm1"
    # Run this command to configure your shell:
    # eval $(docker-machine env myvm1)  
  
运行给定命令以配置要与 `myvm1` 通信的shell。  
  
    eval $(docker-machine env myvm1)  
  
运行`docker-machine ls`以验证`myvm1`现在是有效的计算机，如旁边的星号所示。  
  
    $ docker-machine ls
    NAME    ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER        ERRORS
    myvm1   *        virtualbox   Running   tcp://192.168.99.100:2376           v17.06.2-ce
    myvm2   -        virtualbox   Running   tcp://192.168.99.101:2376           v17.06.2-ce  
  
#### 在群管理器上部署应用程序  
现在，你可以使用`myvm1`作为群管理器，在`myvm1`上，你通过使用在第三部分使用的相同命令`docker stack deploy`和本地复制的文件`docker-compose.yml`来部署应用。该命令将会花费一点时间来完成部署。在群管理器使用`docker service ps <service_name>`命令来验证所有的服务是否被重新部署。  
  
你可以通过配置`docker-machine`shell来连接`myvm1`，你仍然可以访问你的本地文件，在此之前，你要确保你位于包含你在第三部分创建的`docker-compose.yml`目录下。 

和之前一样，运行一下命令在`myvm1`上部署你的应用程序。  
  
    docker stack deploy -c docker-compose.yml getstartedlab  
  
就是这样，应用程序部署在一个群集群中！