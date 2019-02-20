## 修改Git Commit Message

最近遇到手误写错`commit message`的情况，这里记下如何修改`commit message`

### git commit --amend

amend 是在上一次提交的基础上修改内容，包括 `commit message`

如果新增文件修改，需要先执行

```bash
git add <file>
```

如果是想要修改上一次提交的`commit message`,我们只需要执行

```bash
git commit --amend
```

在跳出的页面中修改即可。

不过修改后，需要使用force，才能提交至远端库。

```bash
git push <remote> -f
```

### git rebase -i

这里我建了一个demo， `git logg` 查看一下历史commit，如图

> git logg='logg = log --graph --decorate --oneline --abbrev-commit --all'  可在.gitconfig文件中添加此alias

![修改前的commit message](http://picture.wzmmmmj.com/rebase_1.png)

**例：这里我想修改中间两个commti message**

只需要找到对应commit 的前一个hash值`3fdcc3e`，执行

```bash
git rebase -i 3fdcc3e
```

![rebase](http://picture.wzmmmmj.com/rebase_2.png)

> git rebase -i 的功能很强大， 这里讲下`reword`，具体使用可以google

这里我们选择reword，就像注释所说`use commit ,but edit the commit message`，这是专门来修改`commit message`的，将需要更改的commit 前缀改为`r 或 reword`

![rebase](http://picture.wzmmmmj.com/rebase_3.png)

`:wq`后，弹出修改页面，修改相应的`commit message`即可

![rebase](http://picture.wzmmmmj.com/rebase_4.png)

再次查看`git logg`，可以发现`commit message`已经被修改了，不过还可以发现rebase过的commit hash也变了，~~`rebase -i`是重新生成了一个commit~~，具体需要google

![修改后的commit message](http://picture.wzmmmmj.com/rebase_5.png)