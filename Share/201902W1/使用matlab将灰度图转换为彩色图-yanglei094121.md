# 第二周 Share
## 使用matlab将灰度图转换为彩色图
#### 通常问题：将rgb图像转化为灰色图:
这是简单的，因为rgb图像有三个维度的信息，每种颜色相当于一个三维向量。表示时，相当于同一个向量在不同坐标轴下的表示。<br>
#### 反问题：灰度图转化为rgb图像
灰度图像只有一个维度的信息，那么rgb图像转为灰色图问题相当于将三维坐标投影为一维坐标。明显反过程（由灰色图像转换为彩色图）是不可能的，除非添加信息。即如果想完成反过程，就必须存储另外两个维度的信息，合在一起就是原来的三维向量，即rgb图像。<br>
#### matlab程序
CSDN上有一个非常有趣的matlab function：gray2rgb，<br>地址:<a>https://blog.csdn.net/u012150360/article/details/67656823</a><br>
这个function需要输入两个参数，第一个为灰度图，第二个图为rgb图像，function将第一幅灰度图赋予第二张彩色图的颜色。看示例效果是非常好的，可是我自己上手的时候发现没有非常理想。可能是要找相似图像进行复制颜色？进一步实验再看看。一个非常明显的缺点，两个循环嵌套，运行非常非常的慢，一幅图大概需要半个小时。。。但是示例效果是非常非常好了。<br>

<img src="https://img-blog.csdn.net/20170328220312430?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMjE1MDM2MA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast">