### Travis CI持续集成工具

`Travis ci` 因为与github集成的非常好，而且配置简单，所以一些github项目都会使用`Travis ci`，作为项目的CI/CD工具，具体啥是CI/CD，可以自行google。

如果想在Github repo 中 使用`Travis ci`，只需要简单三步即可

#### 1.  Travis-ci中添加项目

项目所属的Github账号登录`Travis-ci.org`， 在`settings`中开启项目

> 点击项目边上的标签，生成CI的URL，可以加在项目的README.md中，标记项目是否成功

#### 2. 填写.travis.yml配置文件

项目根目录中增加配置文件 [.travis.yml](../../.travis.yml) ，如下图

> 更多语法可以google，最主要的还是根据需求写script中的语句

```yaml
language: python  # 定义语言

python: "3.6"     # 语言版本

branches:         # 分支
    only:         # 触发分支
        - master
        - script
    
script:           # 执行语句
    python ./script/weekly.py

notifications:    # 通知
    email: false

```

#### 3. 提交代码至Github

提交代码到Github后，[commit页面](https://github.com/byte-stream/ARTS/commits/master)，每次提交边上都会有✔或者✘，代表了CI是否通过，如果是多人项目，在提PR的时候也会有CI检查。