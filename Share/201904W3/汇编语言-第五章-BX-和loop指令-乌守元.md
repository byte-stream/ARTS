##第五章 [BX]和loop指令

1. [bx] 和内存单元的描述

   [bx] 表示内存单元，它的偏移地址是 bx，和 [0] 类似。

   ![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552351282483.png)

2. loop

   这个指令和循环有关。

3. 我们定义的描述性符号：“()”

   用 () 描述一个寄存器或一个内存单元中的内容。

   ![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552351439228.png)

4. 约定符号 idata 表示常量

   ![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552351599979.png)

   ![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552351612663.png)

### 5.1 [BX]

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552351723716.png)

### 5.2 Loop 指令

loop 指令的格式是：loop 标号，CPU 执行 loop 指令的时候，要进行两步操作，①(cx)=(cx)-1；②判断 cx 中的值，不为零则转至标号处执行程序，如果为零则向下执行。

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552352237650.png)

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552352252560.png)

用 cx 和 loop 指令相配合实现循环功能的要点：

- 在 cx 中存放循环次数；
- loop 指令中的标号所标识的地址要在前面；
- 要循环执行的程序段，要写在标号和 loop 指令的中间。

### 5.3 在 Debug 中跟踪用 loop 指令实现的循环程序

在汇编源程序中，数据不能以字母开头，要在前面加 0。

Debug -g 执行到指定位置，再 Debug。

Debug -p 自动执行循环。

### 5.4 Debug 和汇编编译器 masm 对指令的不同处理

在 Debug 中，mov ax,[0] 表示将 ds:0 处的数据送入 ax 中，但在汇编源程序中，它被当作 mov ax,0 处理。

那么如何在源程序中，将数据送入寄存器？目前的方式是将偏移地址送入 bs 寄存器中，用 [bx] 的方式来访问内存单元，或者在 [] 前显式地给出段地址所在的段寄存器。

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552354196854.png)

### 5.5 loop 和 [bx] 的联合应用

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552354386553.png)

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552354409565.png)

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552354502478.png)

### 5.6 段前缀

在偏移地址 [bx] 前显示地给出段地址 ds 。

mov ax,ds:[bx]

### 5.7 一段安全的空间

在不能确定一段内存空间中是否存放着中啊哟的数据或代码的时候，不能随意向其中写入内容。0:200\~0:2ff(00200h~002ffh) 的 256 个字节的空间一般不会被 DOS 和其他合法的程序使用，所以这段空间是安全的。

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552354952016.png)

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552354969103.png)

### 5.8 段前缀的使用

将内存 ffff:0~ffff:b 单元中的数据复制到 0:200~0:20b 单元中。

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552355161755.png)

每次循环都要设置两次 ds，效率不高，优化如下：

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/汇编语言-第五章-BX-和loop指令/1552355206433.png)