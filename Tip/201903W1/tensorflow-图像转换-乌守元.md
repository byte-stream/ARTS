opencv 读取 image 直接通过 cv2.imread. 获取的图片格式为 BGR (三通道图像)，是已经编码过的图像。Tensorflow 通过 tf.gfile.FastGFile(filename,’rb’).read() 读取的图像，是图像的原始数据，还需要经过解码，才能获取图像的数据，数据的格式为 RGB (三通道图像)。

```python
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import numpy as np

img_cv2_data = cv2.imread("190109_181616_00154204.jpg")
shape = img_cv2_data.shape
img = tf.identity(img_cv2_data)
original_image_spatial_shape = tf.constant([shape[0], shape[1]])

boxes_value = np.array([[168,158,287,197],[98,255,198,305]])
groundtruth_boxes = tf.constant(boxes_value)
with tf.Session() as sess:
    img_array = img.eval()  # 将tensor对象转成数组
    plt.imshow(img_array)
    plt.show()
```

