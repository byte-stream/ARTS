为了能更方便的浏览各位大佬每周写的文章，又因为我们的项目构成都是md格式文件，所以就有了这个[ARTS-GitBook页面](www.wzmmmmj.com/ARTS)

这里介绍下我们`ARTS-Gitbook`是如何生成的

### 1. gitbook install

因为gitbook需要使用npm进行安装，所以需要本地先装有node.js，然后

```bash
npm install -g gitbook-cli
```

可通过 `gitbook --verison`查看是否安装成功

### 2. gitbook init

通过`gitbook init`可以初始化项目，生成`README.md` 和 `SUMMARY.md`两个必须的文件

README.md 是对书籍的简单介绍， 而SUMMARY.md就是gitbook的关键文件，在页面是显示的目录结构就是由这个文件中的结构生成的。结构大致如下。

```markdown
* [Chapter1](chapter1/README.md)
  * [Section1.1](chapter1/section1.1.md)
  * [Section1.2](chapter1/section1.2.md)
* [Chapter2](chapter2/README.md)
```

因为显示的效果是根据SUMMARY.md 生成的，所以这个文件十分关键

### 3. gitbook serve

写好SUMMARY.md后，我们可以通过`gitbook serve`本地起服务查看，页面效果，如果效果有问题，说明我们的`SUMMARY.md`文件有些问题。



### 4. 渲染静态页面

> 这里贪图方便， 我使用github来渲染静态页面，不过gitbook的样式比较好看。

首先在我们项目下新建分支 `gh-pages`，不过前提是github上有项目名为`<github-name>.github.io`的项目，没有则新建一个，因为最终我们需要使用github提供的静态页面渲染

在`gh-pages`分支上进行`gitbook build`，根据`SUMMARY.md`文件生成静态文件， 或者`gitbook serve`看看效果。

如果效果满意，我们将分支推到自己仓库即可。最后我们通过路径`<github-name>.github.io/ARTS`查看生成的gitbook页面