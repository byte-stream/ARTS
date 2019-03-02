搭建 ELK 过程中的部分笔记，没有系统整理，整个 ELK 学习完后再做整理。

**Nginx**

配置文件：etc/nginx/nginx.conf

启动 nginx：systemctl start nginx

查看 nginx 状态：systemctl status nginx

停止 nginx：systemctl stop nginx

日志：/var/log/nginx/access_json.log



**ElasticSearch**

配置文件：etc/elasticsearch/elasticsearch.yml

修改主机 ip：netword.host:10.0.1.210

默认端口：9200

测试 es 是否连通：访问 ip:9200，页面返回一个 json

es 默认安装到/usr/share/elasticsearch目录下

Elasticsearch默认将数据存储在/var/lib/elasticsearch路径下

查看 es 状态：systemctl status elasticsearch，包含内存大小、Java 堆栈等信息

常用配置

cluster.name: huanqiu                            # 组名（同一个组，组名必须一致）

node.name: elk-node1                            # 节点名称，建议和主机名一致

path.data: /data/es-data                         # 数据存放的路径

path.logs: /var/log/elasticsearch/             # 日志存放的路径

bootstrap.mlockall: true                         # 锁住内存，不被使用到交换分区去

network.host: 0.0.0.0                            # 网络设置

http.port: 9200                                    # 端口



**Kibana**

Kibana 默认端口为 5601

kibana默认安装在/opt/kibana目录下

Kibana配置文件路径为 /opt/kibana/config/kibana.yml

配置：

server.host: "192.168.0.228"  指定服务器

elasticsearch.url: "http://192.168.0.228:9200"  指定 es



**Logstash**

logstash 默认安装在 /opt/logstash 目录

logstash 默认配置文件目录 rpm -qc logstash

logstash 配置目录：/etc/logstash/conf.d

指定配置文件启动 logstash：logstash -f json.conf 

/etc/logstash/conf.d/ 目录下编写收集文件，比如以下配置可以指定要收集的日志，并且指定格式为 json。此处的前提是在 nginx 配置好 nginx 日志输出文件。



命令行参数：

-e 执行

--config 或 -f 指定配置文件或配置文件的目录

--configtest 或 -t 测试，测试配置文件语法是否正确

--log 或 -l  指定 Logstash 的默认输出输出到日志文件

--filterworkers 或 -w 强制 Logstash 为过滤插件运行几个线程