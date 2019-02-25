> 写这篇文章的目的：Android 音视频开发的初级阶段实践，能够在 Android 平台上展示音视频内容。

实际上，为了实现展示音视频内容（**绘制一张图片**）的目的，Android 系统 API 已经提供了控件，用来展示多媒体数据：ImageView / SurfaceView / 自定义View。

# 0 总结

Android 平台上展示图片有多种方法：ImageView / SurfaceView / 自定义View，但这些方法的原理和实现逻辑是不同，以及对应的显示效果也不同。另外，还涉及到一些陌生的类：`BitmapFactory` / `Bitmap` / `SurfaceView` / `SurfaceHolder`。自定义 `View` 的内容也是需要强化的！

# 1 ImageView

Android 平台封装了能够显示图片的控件：ImageView，具体做法：

~~~java

private String photoFilePathPrefix = Environment.getExternalStorageDirectory()
		.getPath() + File.separator + "photo" + File.separator;

@Override
protected void onCreate(Bundle savedInstanceState) {
	super.onCreate(savedInstanceState);
	setContentView(R.layout.activity_main);

	imageView = this.findViewById(R.id.image_show);

	int photoFileCount = getSdcardPhotoFileInfo(Environment.getExternalStorageDirectory()
			.getPath() + File.separator + "photo");
	LogUtil.d(TAG, "图片文件总数：" + photoFileCount);
	if (photoFileCount > 0) {
		Bitmap src = BitmapFactory.decodeFile(photoFilePathPrefix + "1.jpg");

		// 图片真实的宽高像素值
		int height = src.getHeight();
		int width = src.getWidth();
		LogUtil.d(TAG, "height:" + height + "; width:" + width);

		if (src != null) {
			imageView.setImageBitmap(src);
		}
	}
}

~~~

基本逻辑思路：从 sdcard 中读取图片文件，使用 `BitmapFactory.decodeFile()` 编码图片文件并获取到 `Bitmap` 对象。ImageView 控件可以直接显示这个 Bitmap 对象！

关键的类有 2 个：

* `android.graphics.Bitmap`：这个类无非是关于图片对象的封装类，包括：获取 Bitmap 对象，以及对应的属性。需要注意的是：无法通过这个类获取以图片文件作为参数的 Bitmap 实例。
* `android.graphics.BitmapFactory`：工厂类，能够将不同的来源的数据转化为 Bitmap 对象，包括：文件、输入输出流以及字节数组。

# 2 SurfaceView

`SurfaceView`的类描述：`Provides a dedicated drawing surface embedded inside of a view hierarchy. `嵌入在视图层次结构内部的专用绘图表面！

~~~java
surfaceView.getHolder().addCallback(new SurfaceHolder.Callback() {

	@Override
	public void surfaceCreated(SurfaceHolder holder) {
		if (holder == null) {
			return;
		}

		Paint paint = new Paint();
		paint.setAntiAlias(true);
		paint.setStyle(Paint.Style.STROKE);

		Bitmap src = BitmapFactory.decodeFile(photoFilePathPrefix + "1.jpg");
		if (src != null) {
            // 通过 SurfaceHolder 获取到对应的 Canvas
			Canvas canvas = holder.lockCanvas();
            // 在 Canvas 上绘制图片
			canvas.drawBitmap(src, 0, 0, paint);
			holder.unlockCanvasAndPost(canvas);
		}

		int width = surfaceView.getWidth();
		int height = surfaceView.getHeight();
		LogUtil.d(TAG, "surface height:" + height + "; width:" + width);
	}

	@Override
	public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
        
	}

	@Override
	public void surfaceDestroyed(SurfaceHolder holder) {

	}
});
~~~

基本思路：获取`SurfaceView`上的 `SurfaceHolder`实例，并获取对应的 `Canvas` 对象，再在上面绘制图片。

对比 ImageView 和 SurfaceView 显示的不同，布局文件中，上述 2 个控件设置成：

~~~xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <ImageView
        android:id="@+id/image_show"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:scaleType="center"
        android:visibility="gone"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <SurfaceView
        android:id="@+id/surface_view_show"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</android.support.constraint.ConstraintLayout>
~~~

但实际显示同一张图片效果有差异！其中图片大小为：800 * 480，和屏幕分辨率一样！下部分导航栏未隐藏，占据屏幕 48 像素大小控件。

* `ImageView`：设置属性`android:scaleType="center"`会显示图片大小居中显示，能够全部显示图片内容；
* `SurfaceView`：控件的实际大小为：`surface height:432; width:800`，仅仅显示了图片的一部分！

上述两者存在区别的原因：`ImageView`将载入的图片文件自动做了缩放处理，而`SurfaceView`则没有做缩放，实际能够载入多大图片以及显示区域，都和自身`View`的实际大小有关系。

> 为什么这个时候的 `SurfaceView` 没能够完整显示图片？
>
> 解决办法：自己做图片缩放处理，以在 `SurfaceView` 中显示完整的图片。https://blog.csdn.net/renzaijianghu12354/article/details/40084403

# 3 自定义View

实现方法：

~~~java
package com.arthur.displayimage.ui;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.os.Environment;
import android.support.annotation.Nullable;
import android.util.AttributeSet;
import android.view.View;

import com.arthur.displayimage.util.LogUtil;

import java.io.File;

public class PicDisplayView extends View {
    private static final String TAG = PicDisplayView.class.getSimpleName();
    private String photoFilePathPrefix = Environment.getExternalStorageDirectory()
            .getPath() + File.separator + "photo" + File.separator;

    private Paint paint = new Paint();
    private Bitmap bitmap;

    public PicDisplayView(Context context) {
        super(context);
    }

    public PicDisplayView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);

        paint.setAntiAlias(true);
        paint.setStyle(Paint.Style.STROKE);

        bitmap = BitmapFactory.decodeFile(photoFilePathPrefix + "1.jpg");
    }

    public PicDisplayView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if (bitmap != null) {
            canvas.drawBitmap(bitmap, 0, 0, paint);
        }

        int viewWidth = this.getWidth();
        int viewHeight = this.getHeight();
        LogUtil.d(TAG, "viewWidth width:" + viewWidth + "; viewHeight:" + viewHeight);
    }
}
~~~

基本逻辑：自定义 `View` 继承自 `android.view.View` 类，布局文件中引入该自定义 `View`，执行初始化方法并载入图片文件生成 `Bitmap` 对象，在 `onDraw()` 中该自定义 `View` 载入该图片。

从实现的角度来看，这种方式和 `SurfaceView` 类似。可想而知，其结果也和 `SurfaceView` 相同！
