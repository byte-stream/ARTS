UI 开发是 Android 中的基本操作，优美绚丽的界面是最容易打动人的。但是，Android 的碎片化太严重，各种硬件层出不穷，为了实现设计师妹子的效果，再苦再累也是值得。下面我会介绍 Android 绘制的内容，知其所以然很重要。

#### 1. 屏幕与适配

对于屏幕碎片化问题，Android 推荐使用 dp 作为尺寸单位，首先要了解 dp、px、density 等概念。

![Android屏幕尺寸概念](http://upload-images.jianshu.io/upload_images/1820210-0365a33477cbafd7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用 dp 是 Android 推荐的屏幕适配方式，但是以下存在问题：dpi 与 ppi 不一致导致控件大小不统一。

目前业界常用的 UI 适配方法主要有下面几种：
- 限制符适配。包括宽高限定符和 smallestWidth 限定符适配，可以参考：[Android 目前稳定高效的UI适配方案](https://mp.weixin.qq.com/s?__biz=MzAxMTI4MTkwNQ==&mid=2650826381&idx=1&sn=5b71b7f1654b04a55fca25b0e90a4433&chksm=80b7b213b7c03b0598f6014bfa2f7de12e1f32ca9f7b7fc49a2cf0f96440e4a7897d45c788fb&scene=21#wechat_redirect)
- 今日头条适配方案。通过反射修改系统的 density，可以参考 [一种极低成本的Android屏幕适配方式](https://mp.weixin.qq.com/s/oSBUA7QKMWZURm1AHMyubA)

#### 2. CPU 与 GPU

UI 渲染依赖两个核心硬件：CPU 和 GPU。UI 组件在绘制到屏幕之前，需要经过栅格化操作，而栅格化非常耗时。GPU 主要用于处理图形运算，可以加快栅格化的过程。

![软硬件绘制](http://upload-images.jianshu.io/upload_images/1820210-62fd602463eee1dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对于硬件绘制，Android 使用 OpenGL 在 GPU 上完成，OpenGL 是扩平台的图形 API，为 2D/3D 图形处理硬件制定了标准的软件接口。软件绘制使用的是 Skia 库，它能在低端设备上呈现高质量的 2D 跨平台图形。

#### 3. 渲染

Android 图形系统的整体架构和它包含的主要组件。

![Android图形系统](http://upload-images.jianshu.io/upload_images/1820210-eb80549b966a7cae.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果把应用程序图形渲染过程当作一次绘画过程。那么绘画过程中，Android 的各个图形组件的作用是：

- 画笔：Skia 或者 OpenGL。我们可以用 Skia 画笔绘制 2D 图形，也可以用 OpenGL 来绘 制2D/3D图形。正如前面所说,前者使用CPU绘制,后者使用 GPU 绘制。

- 画纸：Surface。所有的元素都在 Surface 这张画纸上进行绘制和渲染。在 Android 中，Window 是 View 的容器，每个窗口都会关联一个 Surface。而 Windowmanager 则负责管理这些窗口，并且把它们的数据传递给 Surfaceflinger。

- 画板：Graphic Buffer。Graphic Buffer 缓冲用于应用程序图形的绘制，在 Android 4.1 之前使用的是双冲机制；在 Android 4.1 之后，使用的是三缓冲机制。

- 显示：Surfaceflinger。它将 Windowmanager 提供的所有 Surface，通过硬件合成器 Hardware Composer 合成并输出到显示屏。

#### 4. 硬件加速

从 Android 3.0 开始，支持硬件加速，到 4.0 时，默认开启硬件加速。

![硬件加速绘制](http://upload-images.jianshu.io/upload_images/1820210-b0b26afca431962d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

硬件加速绘制与软件绘制整个流程差异非常大，最核心就是我们通过 GPU 完成 Graphic Buffer 的内容绘制。此外硬件绘制还引入了ー个 Display List 的概念，每个 View 内部都有个 Displaylist，当某个 View 需要重绘时，将它标记为 Dirty。

当需要重绘时，仅仅只需要重绘一个 View 的 Display List，而不是像软件绘制那样需要向上递归。这样可以大大减少绘图的操作数量，因而提高了渲染效率。

硬件加速大大提高来 Android 系统显示和刷新的速度，但是也存在一些问题：一方面内存消耗，OpenGL API 和Graphic Buffer 缓冲区占用内存。还存在兼容性问题。

[官方文档](https://source.android.com/devices/graphics)