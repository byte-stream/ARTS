
# git 操作
> 在实际开发过程中，我们可能需要采用 git 作为版本控制工具。所以对 git 的基本操作需要非常熟练，以至于我们能够应付工作上的需求。当然这里推荐一篇博文[廖雪峰的git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000),有更详细的介绍。我这里对git的一般操作进行归纳总结。一篇文章让你快速学会使用git并能够应付工作的需求。

git 操作流程:

[![kcDezV.md.png](https://s2.ax1x.com/2019/02/18/kcDezV.md.png)](https://imgchr.com/i/kcDezV)

通过上图我们先一次解释下几个概念：
1.工作区：本地电脑存放文件的地方
2.暂存区：在使用 git 管理项目文件的时候，本地项目文件会有一个.git 的隐藏文件夹，将这个.git 文件夹称为版本库。这个文件夹包含了两个部分：stage（暂存区)和本地仓库
3.本地仓库：使用commit 可以将暂存区中文件添加到本地仓库中的分支中
4.远程仓库：远程 git 服务器的仓库。


[![kcDKLF.md.png](https://s2.ax1x.com/2019/02/18/kcDKLF.md.png)](https://imgchr.com/i/kcDKLF)

> git的一般操作其实就是：将工作区文件 add 到暂存区，然后将暂存区文件 commit 到本地仓库的分支中去，最后 push 远程仓库中，不过推送到远程仓库时，有时候需要 pull 更新一下（当团队其他成员推送了更新，就要pull一下更新一下本地仓库，来解决本地仓库和远程仓库不一致的冲突问题。）

操作如下：

## git init 将当前目录初始化为 git 管理的目录
```
$ git init 
初始化空的 Git 仓库于 /home/wangxinlong/Desktop/notes/.git/
```
### git clone [url]  : clone 远程仓库到本地，同时将本地目录也自动成为 git 管理目录
```
$ git clone [url]
```
## git status 查看状态
```
$ git status

位于分支 master

初始提交

未跟踪的文件:
  （使用 "git add <文件>..." 以包含要提交的内容）

	"\347\224\250java\350\247\243\345\216\213\346\226\207\344\273\266.md"

提交为空，但是存在尚未跟踪的文件（使用 "git add" 建立跟踪）
```
## git add 添加工作区内容到暂存区
git add files

这个时候查看 git status 可以看到
```
$ git add git操作指令.md 

位于分支 master

初始提交

要提交的变更：
  （使用 "git rm --cached <文件>..." 以取消暂存）

	新文件：   "\347\224\250java\350\247\243\345\216\213\346\226\207\344\273\266.md"
```
## git commit 一次性将暂存区的所有修改提交到分支
git commit -m"message" ,git commit 需要加上-m"message" 添加此次提交的信息，为了规范，一般描述此次提交所完成的功能或者修改。
```
$ git commit -m"first commit"
[master （根提交） 9dda572] first commit
 1 file changed, 165 insertions(+)
 create mode 100644 "\347\224\250java\350\247\243\345\216\213\346\226\207\344\273\266.md"
```
这个时候暂存区里就没有内容了
输入 git status 会显示如下内容：

```
位于分支 master
无文件要提交，干净的工作区
```
## 添加远程仓库
git remote add origin repository
## 查看添加的仓库
git remote -v
## git push 推送到远程仓库
git push origin master 推送本地仓库主分支到远程仓库主分支
## git pull 拉取远程仓库的更新
git pull origin developer 拉取远程仓库 developer 分支下的更新
> 当我们 fork 了其他人的项目到自己远程仓库时,我们对自己的远程仓库的推送和之前一样，git add 后 git commit 然后 git push 即可。然后自己的远程仓库网页上点击"pull request"一直下一步即可，即可将自己的更改推送到fork的原仓库下。或者直接 git remote add origin upstream [源仓库url] 添加源仓库，然后git push 到源仓库上去。但是一般情况下，我们都没有权限直接推送到源仓库上。一般都是推送到自己的远程仓库，然后pull request。
## git log 从最近一次提交显示到最远一次提交信息
```
$ git log

commit b9f2c9a2135ed129f25562094d43344b042ec860
Author: xxx@xxx.com <starichat@163.com>
Date:   Mon Feb 18 13:47:20 2019 +0800

    second commit

commit 9dda57206e373dd57e862a121e090ce96a8a9640
Author: xxx@xxx.com <starichat@163.com>
Date:   Mon Feb 18 13:44:31 2019 +0800

    first commit
```
## git reset --hard HEAD  将工作区文件回退到指定版本号的状态
```
$ git reset --hard  9dda57206e373dd57e862a121e090ce96a8a9640
HEAD 现在位于 9dda572 first commit
```

$ git reset --hard 9dda57206e373dd57e862a121e090ce96a8a9640
HEAD 现在位于 9dda572 first commit
$ git log
commit 9dda57206e373dd57e862a121e090ce96a8a9640
Author: xxx@xxx.com <starichat@163.com>
Date:   Mon Feb 18 13:44:31 2019 +0800

    first commit
## git reflog 显示所有提交
```
$ git reflog
9dda572 HEAD@{0}: reset: moving to 9dda57206e373dd57e862a121e090ce96a8a9640
6f4b918 HEAD@{1}: commit: third commit
b9f2c9a HEAD@{2}: reset: moving to b9f2c9a2135ed129f25562094d43344b042ec860
9dda572 HEAD@{3}: reset: moving to 9dda57206e373dd57e862a121e090ce96a8a9640
b9f2c9a HEAD@{4}: commit: second commit
9dda572 HEAD@{5}: commit (initial): first commit
```
我们只要拿到 head 就可以将工作区改为任意一个版本了,完全不用担心修改了不能退回到之前版本了，可以尽情尽兴开发。

## 修改
每次修改,如果没有add 需要先 add 才能 commit
### 撤销修改
git checkout -- file 撤销工作区对file 的修改
一种是file自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态；
一种是file已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。
git reset HEAD <file> 将暂存区的修改回退到工作区,当我们用HEAD时表示最新的版本
## 删除文件
- 先在本地磁盘上删除文件，如果确定需要删除，将版本库中的文件也删除的话 ，就继续执行 git rm file 最后 git commit file 就将该文件从工作区和版本库中都删除了。
- 如果发现本地文件删错了,可以git checkout --file 从版本库中恢复工作区文件。


## 分支管理
git merge developer 将developer 合并到 master 分支
## 解决冲突

git checkout -b feature 创建并切换分支
git branch -d frature 删除分支
git log --graph 分支合并图
## bug分支
git stash 将当前工作现场储藏起来,等以后恢复现场在继续工作。
git stash 之后 工作区是干净的。
git checkout master 切换到master 分支去处理
git stash list 查看stash 内容存放的位置
恢复的方法有:
- 一是用git stash apply恢复，但是恢复后，stash内容并不删除，你需要用git stash drop来删除；
- 另一种方式是用git stash pop，恢复的同时把stash内容也删了：
## 删除分支
如果要丢弃一个没有被合并过的分支，可以通过git branch -D <name>强行删除。

## git branch --set-upstream branch-name 建立本地分支和远程分支的关联
使用origin/branch-name；
rebase操作可以把本地未push的分叉提交历史整理成直线；

rebase的目的是使得我们在查看历史提交的变化时更容易，因为分叉的提交需要三方对比。





