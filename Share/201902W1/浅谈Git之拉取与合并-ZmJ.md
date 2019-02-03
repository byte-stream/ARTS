# 浅谈 Git (一) 之 拉取与合并

> Git 应该是现阶段使用最多的版本管理系统，日常多人开发时，或多或少都要用到一些git 操作，就比如新写好功能准备提pr时，一般远端库也会有更新，这个时候正常流程就是去拉取最新的代码，有冲突也可以早点解决。


这篇文章主要讲 `git中拉取与合并代码`的几种操作，下图可以很好的诠释了几个操作代码流向。

![操作流程图](http://picture.wzmmmmj.com/git1.jpg)



先介绍两种拉取代码的姿势

## 1.git pull

```shell
git pull <远程主机名> <远程分支名>:<本地分支名>
```

pull 操作简单粗暴，直接将远端代码拉取并合并到本地，对，就是这么不讲道理，实际上`pull ≈ fetch + merge` 。

## 2.git fetch

```shell
git fetch <远程主机名> <远程分支名>:<本地分支名>
```

fetch 是将远端代码全部保存到本地，但此时并没有合并到代码中，而是存放在了`.git/FETCH_HEAD`文件中

这里肯定需要提一波FETCH_HEAD了

> FETCH_HEAD指的是: 某个branch在服务器上的最新状态， 每一个执行过fetch操作的项目都会存在一个，FETCH_HEAD列表, 这个列表保存在 `.git/FETCH_HEAD` 文件中，其中每一行对应于远程服务器的一个分支commit_id， 当前分支指向的FETCH_HEAD, 就是这个文件第一行对应的那个分支。

fetch操作的优点，可以在合并时，查看一波代码的变化，如下面事例，而不是不讲道德的合并然后解冲突。

```shell
git fetch origin master
git diff master..origin/master
git merge origin/master  # git rebase origin/master
```

此时如果想要更新本地代码就需要进一步merge 或 rebase 操作。

## 3.git merge

```shell
git merge <远程主机名> <远程分支名>  # <本地分支名>
```

顾名思义就是将某分支的内容合并到当前分支，如下图，c4分支合并c5分支。

![merge 分支变化](http://picture.wzmmmmj.com/git2.png)

## 4.git rebase

> 吐槽：用的不熟练真的让人头皮发麻

其实 rebase 与 merge 操作结果一致，不过方式有所不同。

![rebase 分支变化](http://picture.wzmmmmj.com/git3.png)

rebase 会将分支移动到master 分支后，有效的将master的分支合并。不过这里与merge不同的地方是，rebase 不会像merge 一样新生成一个合并提交，而是改变了历史提交，从而使项目历史呈现出线性结构。

不过对于刚接触此操作的人，比如我，就会经常出现用了rebase后，提交中会混入其他人的commit，让人头疼的不行。一个有效的操作时，改变rebase 的历史提交`git rebase -i   commit_id`   ，它会打开一个编辑页， 可对其中的commit 进行合并，移除等操作。

```shell
p, pick = use commit
r, reword = use commit, but edit the commit message
e, edit = use commit, but stop for amending
s, squash = use commit, but meld into previous commit  (保留修改，向前合并commit)
f, fixup = like "squash", but discard this commit's log message
x, exec = run command (the rest of the line) using shell
d, drop = remove commit (直接将修改弹出，撤销commit)
```

更多rebase操作，可`git rebase --help`查看，或查看官方文档

> ==温馨提示==：pull merge rebase 操作后，如果有报`CONFLICT (content): Merge conflict in xxxx.py` ，不好意思，我们需要手动解冲突了(惊不惊喜，意不意外)。



### 最后记一个正常提交流程

- git fetch
- git rebase
  - 以下为有冲突的情况下，并解完冲突
  - git add .
  - git  rebase --continue
  - git rebase --abort  （撤回此次rebase）

- git push


## 总结一句：git真好用
