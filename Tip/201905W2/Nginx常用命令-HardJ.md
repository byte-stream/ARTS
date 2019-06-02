#### Nginx常用命令

​	在Linux中，需要使用命令行控制Nginx服务器的启动与停止、重新加载配置文件等行为。默认情况下，nginx被安装在/usr/local/nginx中，编译后的二进制文件在/usr/local/nginx/sbin/nginx中，配置文件在/usr/local/nginx/conf/nginx.conf中。

1. 默认方式启动

   直接执行Nginx二进制程序，读取默认路径下的配置文件/usr/local/nginx/conf/nginx.conf

   ```nginx
   /usr/local/nginx/sbin/nginx
   ```

2. 指定配置文件的方式启动

   使用-c参数指定配置文件

   ```nginx
   /usr/local/nginx/sbin/nginx -c /tmp/nginx.conf
   ```

3. 另行指定安装目录的启动方式

   使用-p参数指定Nginx的安装目录

   ```nginx
   /usr/local/nginx/sbin/nginx -p /usr/local/nginx
   ```

4. 另行指定全局配置项的启动方式

   通过-g参数临时指定一些全局配置项，以使新的配置项生效。

   ```nginx
   # 指定master进程pid存放位置
   /usr/local/nginx/sbin/nginx -g "pid /var/nginx/test.pid"
   ```

   通过-g指定的配置项不能与默认路径下的nginx.conf配置项冲突，否则无法启动。如果执行上面命令且在默认配置中有pid logs/nginx.pid则无法启动。

   通过-g指定的配置项启动nginx服务后，需要执行其他命令时，需要把-g参数带上，否则可能出现配置项不匹配的情况。

   ```nginx
   /usr/local/nginx/sbin/nginx -g "pid /var/nginx/test.pid" -s stop
   ```

5. 测试配置信息是否有误

   在不启动Nginx服务的情况下，使用-t参数测试配置文件是否有误。

   ```nginx
   /usr/local/nginx/sbin/nginx -t
   ```

6. 测试配置信息是否有误,不输出信息

   ```nginx
   /usr/local/nginx/sbin/nginx -t -q
   ```

7. 显示版本信息

   使用-v参数显示Nginx的版本信息

   ```nginx
   /usr/local/nginx/sbin/nginx -v
   ```

8. 显示编译阶段的参数

   使用-V参数显示编译阶段信息,包含版本

   ```nginx
   /usr/local/nginx/sbin/nginx -V
   ```

9. 快速停止服务

   使用-s stop可以强制停止nginx服务。-s参数向正在运行的Nginx服务中的master进行发送信号来快速关闭Nginx服务。

   ```nginx
   /usr/local/nginx/sbin/nginx -s stop
   ```

   通过kill命令向Nginx的master进程发送终止信息

   ```nginx
   ps -ef|grep nginx
   root      9517     1  0 Mar16 ?        00:00:00 nginx: master process 
   nobody   19768  9517  0 Apr30 ?        00:00:01 nginx: worker process
   
   
   # 下面两条命令与/usr/local/nginx/sbin/nginx -s stop一样
   kill -s SIGTERM 9517
   	or
   kill -s SIGINT 9517
   ```

10. "优雅"停止服务

    如果希望Nginx服务可以正常处理完所有请求再停止

    ```nginx
    /usr/local/nginx/sbin/nginx -s quit
    or
    kill -s SIGQUIT <nginx master pid>
    ```

    该命令与快速停止Nginx服务有区别。快速停止服务work和master进程在收到信息号后会立刻退出进行。而"优雅"停止服务会先关闭监听端口，停止建立新连接，然后把当前正在处理的连接都处理完再退出进程。

    如果系统"优雅"停止work进程可以向该进行发送WINCH信号

    ```nginx
    kill -s SIGWINCH <nginx worker pid>
    ```

11. 让运行中的Nginx服务重新读取配置

    使用 -s reload 参数让运行中的nginx服务重新加载nginx.conf文件

    ```nginx
    /usr/local/nginx/sbin/nginx -s reload
    or
    kill -s SIGHUP <nginx master pid>
    ```

12. 日志文件回滚

    使用-s reopen参数可以重新打开日志文件，运行前可以先把当前日志文件改名或转移到其他目录进行备份，然后执行该命令重新生成新的日志文件。这个命令使得日志文件不至于过大。

    ```nginx
    /usr/local/nginx/sbin/nginx -s reopen
    or
    kill -s SIGUSR1 <nginx master pid>
    ```

13. 平滑升级Nginx

    当nginx服务升级新的版本时，必须要将旧的二进制文件Nginx替换掉，这需要重启服务，但nginx支持不重启服务完成新版本的平滑升级。

    升级时包括以下步骤：

    1. 通知正在运行的旧版本nginx准备升级。通过向master进程发送USR2信号

       ```nginx
       kill -s SIGUSR2 <nginx master pid>
       ```

       这时，运行中的Nginx会将pid文件(存放master pid的文件)重命名，如：/usr/local/nginx/logs/nginx.pid重命名为/usr/local/nginx/logs/nginx.pid.oldbin，这样新的Nginx才可能启动成功。

     2. 启动新版本的Nginx，可以使用上面介绍的启动方法。通过ps命令可以发现新旧版本的nginx同时运行。

     3. 通过kill命令向旧版本的master进程发送SIGQUIT信号，以“优雅”的方式关闭旧版本的Nginx，完成平滑升级。

14. 显示命令行帮助

    使用-h或者-?参数显示支持的所有命令行参数

#### 参考

- 《深入理解Nginx》