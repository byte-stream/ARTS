> Docker官方教程二，接着上周的文章继续翻译。  
## Docker容器  
#### 先要条件：   

- 安装Docker 1.13或更高版本
- 查看第一部分的[安装教程](https://docs.docker.com/get-started/)  
- 给你的环境进行快速测试以确保你完成所有设置：   
      

    docker run hello-world  
  
#### 介绍  
  
  现在是时候通过 Docker 构建一个应用了。我们从一个应用程序的层次结构的底部开始，这个层次包含一个容器，容器层次的上一层是服务，它定义了容器在生产中的行为方式。关于服务会在[第三部分](https://docs.docker.com/get-started/part3/)讲述，最后是在顶层的堆栈，它定义了服务之间的交互。关于堆栈会在[第五部分](https://docs.docker.com/get-started/part5/)讲述。  
   
   - 堆栈  
   - 服务  
   - 容器（你在这里）  
   
#### 你的新开发环境  
在过去，你想要编写一个 Python 程序，第一件事情是先安装 Python 运行环境到你的计算机上，但是这会导致你的计算机上的环境需要非常适合你的程序按预期运行，同时也需要你的生产环境相匹配。  
  
使用Docker，你可以使用可移植的 Python 运行环境作为镜像来获取，无需进行安装。你可以在 Python 基础镜像上构建你的应用程序代码，确保你的应用程序、依赖项和运行环境一起运行。  
  
#### 使用 `Dockerfile` 定义容器  
Dockerfile定义了容器内部发生的事情。访问在此环境中虚拟化的网络接口和磁盘驱动器等资源，该环境与系统的其他部分隔离，所以你需要将端口映射到外部，并明确哪些文件你想要复制到这个环境中。然而，在执行这些操作后，你可以预料 `Dockerfile` 定义的应用程序构建，使应用程序运行在其他环境完全相同（平台无关性）。  
  
#### `Dockerfile`  
在你的计算机本地创建一个空目录，将当前目录（`CD`）更改为新目录，创建一个名为 `Dockerfile` 的文件，将以下内容复制并粘贴到该文件中，然后保存。记下解释新 Dockerfile 中每个语句的注释。  
  
    # 使用一个官方 Python 运行环境作为父镜像
    FROM python:2.7-slim
    # 把 /app 目录作为工作目录
    WORKDIR /app
    # 将当前目录的内容复制到 /app 目录下的容器中
    COPY . /app
    # 安装在 requirements.txt 文件中指定需要的包
    RUN pip install --trusted-host pypi.python.org -r requirements.txt
    # 将容器的80端口暴露到外部
    EXPOSE 80
    # 定义环境变量
    ENV NAME World
    # 当容器启动时运行 app.py 程序
    CMD ["python", "app.py"]  
  
这 `Dockerfile` 是指我们尚未创建的几个文件，即 `app.py` 和 `requirements.txt`。让我们来创建它们。  
  
#### 应用程序本身  
创建两个文件，`requirements.txt` 和 `app.py`，然后将它们放入有 `Dockerfile` 的文件夹中。这就完成了我们的应用程序，你可以看到它非常简单。当上面的 `Dockerfile` 被构建到一个镜像内，`app.py` 和 `requirements.txt`被置入到镜像是因为 `Dockerfile` 的 `COPY` 命令，得益于 `EXPOSE` 命令，你可以通过HTTP访问得到 `app.py` 输出的结果。  
  
#### `requirements.txt`  
  
    Flask
    Redis  
  
#### `app.py`  
  
    from flask import Flask
    from redis import Redis, RedisError
    import os
    import socket

    # 连接Redis
    redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

    app = Flask(__name__)

    @app.route("/")
    def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=80)  
          
现在我们发现 `pip install -r requirements.txt` 命令为Python安装了 Flask 和 Redis 库，应用程序打印了环境变量 `NAME`，以及调用 `socket.gethostname()` 输出主机名称，最后因为Redis没有运行（因为我们只安装了Python库而不是Redis本身），我们尝试使用Redis失败了并产生了错误信息。  
> 注意：在容器内部访问容器ID时，访问主机名称，这类似于正在运行可执行文件的进程ID。  
  
  就是这样！你不需要在你的计算机系统中安装Python或其他在 `requirements.txt` 中描述的库，也不需要在你的计算机系统中构建或运行镜像。看起来你并没有设置 Python 和 Flask 的环境，但是实际上你已经设置了。  
  
  #### 构建应用程序  
  我们准备构建应用程序，确保你仍然处于根目录下。一下是 `ls` 命令显示的目录内容：  
    
    $ ls
    Dockerfile		app.py	  requirements.txt  
      
现在运行构建命令，这将创建一个镜像。我们将使用 `--tag` 选项来为镜像命名，如果你想使用短选项可以使用 `-t`。  
  
    docker build --tag=friendlyhello .  
      
你构建的镜像在哪里呢？它将会出现在你计算机的本地Docker镜像注册表中：  
  
    $ docker image ls
    REPOSITORY            TAG                 IMAGE ID
    friendlyhello         latest              326387cea398  
     
注意标签的默认值是 `latest`,标签选项的完整语法类似于： `--tag=friendlyhello:v0.0.1`。 
> #### Linux故障诊断  
> 代理服务器设置  
> 代理服务器可以在你的应用程序启动并运行后阻止其连接。如果你使用代理服务器，请使用 `ENV` 命令将以下内容添加到你的 Dockerfile 中，以指定代理服务器的主机和端口:
>>     # 设置代理服务器, 用你的服务器ip和端口号更换 host:port
>>     ENV http_proxy host:port
>>     ENV https_proxy host:port  
> #### DNS 设置  
> DNS 设置错误会产生 `pip` 错误，你需要设置你自己的 DNS 服务器地址使 `pip` 正常运行。你可能想要修改 Docker 守护进程的 DNS 设置，你可以在 `/etc/docker/daemon.json` 路径下使用 `dns` 关键字编辑（创建）配置文件，来设置 DNS。如下所示：  
>> {
  "dns": ["your_dns_address", "8.8.8.8"]
}  

> 在上面示例中，列表的第一个元素是 DNS 服务器的地址，第二个元素是 Google 的 DNS，可以在第一个元素无法使用时使用。  
> 在继续之前，请保存 `daemon.json` 并重新启动 docker 服务。  
>> `sudo service docker restart` 

> 重启后重新运行 `build` 命令。  
  
#### 运行应用程序  
运行应用程序，使用 `-p` 选项将计算机的4000端口映射到容器的80端口：  
  
    docker run -p 4000:80 friendlyhello  
你应该看到Python把你的应用程序运行在 `http://0.0.0.0:80` 地址上。但是该消息是来自容器内部，它不知道你已经将该容器的 80 端口映射到计算机的 4000 端口从而生成了当前正确的 URL `http://localhost:4000`.  
在 Web 浏览器中跳转到该 URL 中可以查看在网页商提供显示的内容。  

![](https://docs.docker.com/get-started/images/app-in-browser.png)  
  
> 注意：如果你在 windows7 上使用 Docker Toolbox，请使用 Docker Machine IP 而不是 `localhost`。例如：http:\\192.168.99.100:4000/。要查找 Docker Machine IP 地址，请使用 `docker-machine ip` 命令。  
  
 你还可以在 shell 中使用 `curl` 命令来查看相同内容。 
>     $ curl http://localhost:4000
>     <h3>Hello World!</h3><b>Hostname:</b> 8fc990912a14<br/><b>Visits:</b> <i>cannot connect to Redis, counter disabled</i>  
  
当运行 `docker run -p` 命令映射 `4000:80`端口来演示 `Dockerfile` 和 `publish` 之间暴露的值不同。在最后一步中，将主机的4000端口映射到容器的80端口中并使用 `http://localhost` 地址。  

在你的终端中点击 `CTRL+C`退出。  
  
> #### 在 Windows 上显示停止容器  
> 在 Windows 系统上，`CTRL+C` 不会停止容器。因此，首先键入 `CTRL+C` 以获取提示（或打开另一个shell），然后键入 `docker container ls` 列出正在运行的容器，然后使用 `docker container stop <Container NAME or ID>` 命令停止容器。否则，当您尝试在下一步中重新运行容器时，会从守护进程收到错误响应。  
  
现在让我们在后台以分离模式运行应用程序：  
  
    docker run -d -p 4000:80 friendlyhello  
  
你获得了运行该应用程序的容器 ID 然后返回到终端。你的容器现在正在后台运行。你可以使用 `docker container ls` 查看缩写的容器ID（并且在运行命令时两者可以互换）：  

    $ docker container ls
    CONTAINER ID        IMAGE               COMMAND             CREATED
    1fa4ab2cf395        friendlyhello       "python app.py"     28 seconds ago  
  
注意：`CONTAINER ID` 的内容是在 `http://localhost:4000` 地址上。  
  
现在使用 `docker container stop` 命令和 `CONTAINER ID` 来结束容器进程,像这样：  
  
    docker container stop 1fa4ab2cf395  
  
#### 分享你的镜像  
为了演示我们刚刚创建的内容的可移植性，让我们上传我们构建的图像并在其他地方运行它。  
毕竟，当你想要将容器部署到生产环境时，您需要知道如何推送到注册表。  
注册表是存储库的集合，存储库是图像的集合 - 类似于GitHub存储库，除了代码已经构建。注册表上的帐户可以创建许多存储库。该 `docker` CLI默认使用 Docker 公共注册表。  
> 注意：我们使用 Docker 的公共注册表仅仅是因为它是免费的和默认配置的，但是这里也有许多公共注册表可供选择。你甚至可以使用 [Docker Trusted Registry ](https://docs.docker.com/datacenter/dtr/2.2/guides/)设置你自己的私人注册表  
  
#### 使用你的 Docker ID 登录  
如果你没有 Docker 帐户，请在 [hub.docker.com](https://hub.docker.com/)上注册一个帐户。记下你的用户名。登录本地计算机上注册的 Docker 公共注册表。  

    $ docker login    
  
#### 标记镜像  
将本地镜像与注册表上的存储库相关联的表示法是  `username/repository:tag`。标签是可选的，但建议使用，因为它是注册管理机构用来为 Docker 镜像提供版本的机制。为存储库提供存储库和标记有意义的名称，例如  `get-started:part2`。这会将镜像放入 `get-started` 存储库并将其标记为 `part2` 。  
现在，把它们放在一起来标记镜像。 `docker tag image` 使用您的用户名，存储库和标记名称运行，以便将镜像上传到所需的目标位置。该命令的语法是：  
  
    docker tag image username/repository:tag  
  
例如：  
  
    docker tag friendlyhello gordon/get-started:part2   
  
运行 `docker image ls` 以查看新标记的镜像。  
  
    $ docker image ls 
    REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
    friendlyhello            latest              d9e555c53008        3 minutes ago       195MB
    gordon/get-started         part2               d9e555c53008        3 minutes ago       195MB
    python                   2.7-slim            1c7128a655f6        5 days ago          183MB
    ...  
  
#### 发布镜像  
将标记的镜像上传到存储库：  
  
    docker push username/repository:tag  
      
完成后，此上传的结果将公开发布。如果您登录到[Docker Hub](https://hub.docker.com/)，则会看到其中的新镜像及其pull命令。  
  
#### 从远程存储库中拉出并运行镜像  
从现在开始，您可以使用 `docker run` 以下命令在任何计算机上使用和运行您的应用程序：  

    docker run -p 4000:80 username/repository:tag  
  
如果镜像在本地不可用，则 Docker 会从存储库中提取镜像。  
  
    $ docker run -p 4000:80 gordon/get-started:part2
    Unable to find image 'gordon/get-started:part2' locally
    part2: Pulling from gordon/get-started
    10a267c67f42: Already exists
    f68a39a6a5e4: Already exists
    9beaffc0cf19: Already exists
    3c1fe835fb6b: Already exists
    4c9f1fa8fcb8: Already exists
    ee7d8f576a14: Already exists
    fbccdcced46e: Already exists
    Digest: sha256:0601c866aab2adcc6498200efd0 f754037e909e5fd42069adeff72d1e2439068
    Status: Downloaded newer image for gordon/get-started:part2
     * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)  
  
无论在哪里 `docker run` 执行，它都会提取你的镜像，以及 Python 和所有依赖项 requirements.txt ，并运行你的代码。它们都在一个整洁的小包中一起旅行，你不需要在主机上安装任何东西让 Docker 运行它。  
  
#### 第二部分总结  
这就是这个页面的全部内容。在下一节中，我们将学习如何通过在服务中运行此容器来扩展应用程序。  
  
以下是此页面中基本 Docker 命令的列表，以及一些相关的命令：  
  
    docker build -t friendlyhello .  # Create image using this directory's Dockerfile
    docker run -p 4000:80 friendlyhello  # Run "friendlyname" mapping port 4000 to 80
    docker run -d -p 4000:80 friendlyhello         # Same thing, but in detached mode
    docker container ls                                # List all running containers
    docker container ls -a             # List all containers, even those not running
    docker container stop <hash>           # Gracefully stop the specified container
    docker container kill <hash>         # Force shutdown of the specified container
    docker container rm <hash>        # Remove specified container from this machine
    docker container rm $(docker container ls -a -q)         # Remove all containers
    docker image ls -a                             # List all images on this machine
    docker image rm <image id>            # Remove specified image from this machine
    docker image rm $(docker image ls -a -q)   # Remove all images from this machine
    docker login             # Log in this CLI session using your Docker credentials
    docker tag <image> username/repository:tag  # Tag <image> for upload to registry
    docker push username/repository:tag            # Upload tagged image to registry
    docker run username/repository:tag                   # Run image from a registry