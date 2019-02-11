# dlv调试  

dlv整体调试Go语言的流程如下  

```
1,./dlv debug xxxx(程序名)    ##启动dlv调试

2,r(restart)  

3,c(continue)

4,b(break)                   ##打断点，可以打函数名，也可以打文件下对应的行号

5,n(next)或s(step)           ##n按一次单步执行，后面只需一直按回车；遇到需要深究的函数按s进去查看

##如果碰到多线程，建议在线程内打个断点

6,bt(stack)                  ##查看堆栈

7,frame                      ##查看指定堆栈的内容

8,q(exit)                    ##退出调试
```
