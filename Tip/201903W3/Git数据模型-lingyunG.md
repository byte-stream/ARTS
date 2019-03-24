如何在GitBash完成ARTS任务

在工作中用sourceTree来完成git的pull，commit，merge，push，fetch这几个操作，已经这样用了很久，直到上周的任务提交失败之后找寒食君帮我看问题，我才知道其实我没有懂怎么去使用git。在这里我先记录一下
如何在GitBash里正确操作，完成ARTS的提交。

前提条件
已经在git上fork这个项目，并添加了本地电脑的 ssh key到GitHub账户里

每次提交我需要操作的步骤
1）git remote -v
2)git fetch "上游路径"
3）git pull“上游路径”
4）git status： 这一步可以查看更改了哪些文件
5）git add ./
