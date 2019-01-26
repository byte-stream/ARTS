## ImagePy简单介绍 
ImagePy是基于Python的超轻量级开源图像处理框架，官网网址为：http://www.imagepy.org/

## 安装过程（anacond python）

在anaconda promt中依次输入：

python -m pip install numpy

python -m pip install scipy

python -m pip install shapely

python -m pip install wxpython

git clone https://github.com/yxdragon/imagepy.git


五条输入回车完毕后在**anaconda头部所示路径**中得到GitHub克隆来的imagepy的文件夹。



![上述五部操作结果显示](https://img-blog.csdnimg.cn/20190125233308429.png)
进入该文件夹中：

![进入路径](https://img-blog.csdnimg.cn/20190125233358952.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MDc1ODc0OA==,size_16,color_FFFFFF,t_70)
运行__main.py__
![ImagePy可爱的界面](https://img-blog.csdnimg.cn/20190125233420628.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MDc1ODc0OA==,size_16,color_FFFFFF,t_70)
程序页面就出现在你面前啦。感觉这个小蛇非常可爱，哈哈。

知乎上有imagepy专栏：https://zhuanlan.zhihu.com/imagepy

imagepy：

 - 支持bmp, rgb, png等常用图像格式List item
 - 可以处理灰度图像和多通道（彩色）图像，支持图像栈（序列）操作
 - 可以进行常用的各种数学运算，常用的滤波器操作支持各种选区操作（点，线，面，多线，多面，镂空多边形）
 - 可以进行像图像测量，以及像素统计
 - 能够进行dem地表重建，图像序列的三维重建
 - 支持宏录制,可接入scikit-image, opencv, itk等基于numpy的第三方库

我尝试使用了一些功能，比如读取tiff文件并显示，rgb图像转8-bit图像，转为灰度图，灰度图转为伪彩色图像，还是非常不错的。
