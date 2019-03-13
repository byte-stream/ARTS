数据增强即是通过对图片进行随机的旋转、裁剪、设置图片亮度、对比度、高斯模糊、添加椒盐噪声等操作，使原来的一张图片变成多张图片，从而扩大样本容量，提高训练模型的准确率。

在这里我们用 opencv 来读取图片，然后用 tensorflow 来对图片进行增强处理。最后通过 PIL 来显示/保存图片。

注意：opencv 是通过 BGR 的通道顺序处理图片的，而 PIL 显示则是 RGB，在最后保存和显示图片时，要提前进行通道转换。

框架代码如下：

```python
with tf.Session() as sess:
    filename = "*.jpg"
    img_cv2_data = cv2.imread(filename)
    # bgr-> rgb
    b,g,r = cv2.split(img_cv2_data) 
    img = cv2.merge([r,g,b])

    # 获取 shape
    shape = img_cv2_data.shape 
    original_image_spatial_shape = tf.constant([shape[0], shape[1],3])

    img = tf.identity(img)
    
    # 显示图片
    plt.imshow(img.eval())
    plt.show()
    
    # 调用 preprocessing，进行数据增强
    img = preprocessing.preprocess(img,original_image_spatial_shape, is_training=True)
    
    # 显示图片
    plt.imshow(img.eval())
    plt.show()
    
    # 保存图片
    img = sess.run(img)
    img = img.astype(np.uint8) 
    img = Image.fromarray(img)
    img.save(filename[:-4] + "_bac.jpg")
```

我们将每一个数据增强方法都定义在 preprocessing 中。

### 随机裁剪

```python
def _crop(image, offset_height, offset_width, crop_height, crop_width):
  original_shape = tf.shape(image)

  rank_assertion = tf.Assert(
      tf.equal(tf.rank(image), 3),
      ['Rank of image must be equal to 3.'])
  with tf.control_dependencies([rank_assertion]):
    cropped_shape = tf.stack([crop_height, crop_width, original_shape[2]])

  size_assertion = tf.Assert(
      tf.logical_and(
          tf.greater_equal(original_shape[0], crop_height),
          tf.greater_equal(original_shape[1], crop_width)),
      ['Crop size greater than the image size.'])

  offsets = tf.to_int32(tf.stack([offset_height, offset_width, 0]))

  # Use tf.slice instead of crop_to_bounding box as it accepts tensors to
  # define the crop size.
  with tf.control_dependencies([size_assertion]):
    image = tf.slice(image, offsets, cropped_shape)
  return tf.reshape(image, cropped_shape)


def _random_crop(image_list, crop_height, crop_width):
  if not image_list:
    raise ValueError('Empty image_list.')

  # Compute the rank assertions.
  rank_assertions = []
  for i in range(len(image_list)):
    image_rank = tf.rank(image_list[i])
    rank_assert = tf.Assert(
        tf.equal(image_rank, 3),
        ['Wrong rank for tensor  %s [expected] [actual]',
         image_list[i].name, 3, image_rank])
    rank_assertions.append(rank_assert)

  with tf.control_dependencies([rank_assertions[0]]):
    image_shape = tf.shape(image_list[0])
  image_height = image_shape[0]
  image_width = image_shape[1]
  crop_size_assert = tf.Assert(
      tf.logical_and(
          tf.greater_equal(image_height, crop_height),
          tf.greater_equal(image_width, crop_width)),
      ['Crop size greater than the image size.'])

  asserts = [rank_assertions[0], crop_size_assert]

  for i in range(1, len(image_list)):
    image = image_list[i]
    asserts.append(rank_assertions[i])
    with tf.control_dependencies([rank_assertions[i]]):
      shape = tf.shape(image)
    height = shape[0]
    width = shape[1]

    height_assert = tf.Assert(
        tf.equal(height, image_height),
        ['Wrong height for tensor %s [expected][actual]',
         image.name, height, image_height])
    width_assert = tf.Assert(
        tf.equal(width, image_width),
        ['Wrong width for tensor %s [expected][actual]',
         image.name, width, image_width])
    asserts.extend([height_assert, width_assert])

  # Create a random bounding box.
  #
  # Use tf.random_uniform and not numpy.random.rand as doing the former would
  # generate random numbers at graph eval time, unlike the latter which
  # generates random numbers at graph definition time.
  with tf.control_dependencies(asserts):
    max_offset_height = tf.reshape(image_height - crop_height + 1, [])
  with tf.control_dependencies(asserts):
    max_offset_width = tf.reshape(image_width - crop_width + 1, [])
  offset_height = tf.random_uniform(
      [], maxval=max_offset_height, dtype=tf.int32)
  offset_width = tf.random_uniform(
      [], maxval=max_offset_width, dtype=tf.int32)

  return [_crop(image, offset_height, offset_width,
                crop_height, crop_width) for image in image_list]
```

### 随机上下左右翻转

```python
def _random_flip(image, left_right_proportion, up_down_proportion):
    """random flip
    
    Args:
    image: A image tensor,
    left_right_proportion: the random proportion to do left right flip
    up_down_proportion: the random proportion to do up down flip

    Returns:
        A preprocessed image.
    """
    #image = tf.image.random_flip_left_right(image)
    #image = tf.image.random_flip_up_down(image)
    
    left_right_theshold = tf.constant(left_right_proportion, dtype=tf.float32)
    up_down_theshold = tf.constant(up_down_proportion, dtype=tf.float32)
    rand = tf.random_uniform([2], minval=0.0, maxval=1.0, dtype=tf.float32) 
    image = tf.cond(rand[0] < left_right_theshold, 
                    lambda: tf.image.flip_left_right(image), 
                    lambda: tf.identity(image)) 
    image = tf.cond(rand[0] < up_down_theshold, 
                    lambda: tf.image.flip_up_down(image), 
                    lambda: tf.identity(image)) 
    return image
```

### 转置

```python
def _transpose_image(image, proportion):
    theshold_const = tf.constant(proportion, dtype=tf.float32)
    rand = tf.random_uniform([1], minval=0.0, maxval=1.0, dtype=tf.float32) 
    image = tf.cond(rand[0] < theshold_const,   
                    lambda: tf.image.transpose_image(image),
                    lambda: tf.identity(image))
    return image
```

### 旋转

```python
def _rot90(image, proportion, k):
    theshold_const = tf.constant(proportion, dtype=tf.float32)
    rand = tf.random_uniform([1], minval=0.0, maxval=1.0, dtype=tf.float32) 
    image = tf.cond(rand[0] < theshold_const, 
                    lambda: tf.image.rot90(image, k=k),
                    lambda: tf.identity(image))
    return image
```

### 高斯模糊

```python
def _gauss_kernel(image, shape):
    r = 1 # random.randint(1,3) 
    s = 1 # random.uniform(1, 1.5)   sigma
    summat = 0
    PI = 3.14159265358979323846
    _gauss_kernel = np.zeros((2*r+1,2*r+1,3,3))
    for i in range(0,2*r+1):
        for j in range(0,2*r+1):
            gaussp = (1/(2*PI*(s**2))) * math.e**(-((i-r)**2+(j-r)**2)/(2*(s**2))) 
            _gauss_kernel[i,j,0,0] = gaussp
            _gauss_kernel[i,j,1,1] = gaussp
            _gauss_kernel[i,j,2,2] = gaussp
            summat += gaussp
    for i in range(0,2*r+1):
        for j in range(0,2*r+1):
            _gauss_kernel[i,j,0,0] = _gauss_kernel[i,j,0,0]/summat
            _gauss_kernel[i,j,1,1] = _gauss_kernel[i,j,1,1]/summat
            _gauss_kernel[i,j,2,2] = _gauss_kernel[i,j,2,2]/summat
    
    image = tf.reshape(image, shape=(1,shape[0],shape[1],3))
    image = tf.cast(image, tf.float32)
    gauss_kernel = tf.constant(_gauss_kernel, dtype=tf.float32)
    image = tf.nn.conv2d(image, gauss_kernel,strides=[1,1,1,1], padding='SAME')
    image = tf.reshape(image, shape=shape)
    image = tf.cast(image, dtype="uint8")
    return image

def _gauss(image, shape, proportion):
    """random gauss fuzzy
    
    Args:
    image: A image tensor

    Returns:
        A preprocessed image.
    """
    theshold_const = tf.constant(proportion, dtype=tf.float32)
    rand = tf.random_uniform([1], minval=0.0, maxval=1.0, dtype=tf.float32) 
    image = tf.cond(rand[0] < theshold_const, 
                    lambda: _gauss_kernel(image, shape), 
                    lambda: tf.identity(image)) 
    return image
```

### 随机亮度

```python
def _random_brightness(image, proportion):
    theshold_const = tf.constant(proportion, dtype=tf.float32)
    rand = tf.random_uniform([1], minval=-proportion, maxval=proportion, dtype=tf.float32) 
    #rand = tf.random_uniform([1], minval=0.0, maxval=1.0, dtype=tf.float32) 
    image = tf.cond(rand[0] < theshold_const, 
                    lambda: tf.image.random_brightness(image, max_delta=10./255), 
                    lambda: tf.identity(image)) 
    return image
```

### 随机对比度

```python
def _random_contrast(image, proportion):   
    theshold_const = tf.constant(proportion, dtype=tf.float32)
    rand = tf.random_uniform([1], minval=0.0, maxval=1.0, dtype=tf.float32) 
    image = tf.cond(rand[0] < theshold_const, 
                    lambda: tf.image.random_contrast(image, lower=200./255, upper=320./255),
                    lambda: tf.identity(image))
    return image
```

### 随机色度

```python
def _adjust_hue(image, proportion):
    theshold_const = tf.constant(proportion, dtype=tf.float32)
    rand = tf.random_uniform([1], minval=0.0, maxval=1.0, dtype=tf.float32) 
    image = tf.cond(rand[0] < theshold_const,   # 0.01，>1
                    lambda: tf.image.adjust_hue(image, 0.01), 
                    lambda: tf.identity(image)) 
    return image
```

### 随机饱和度

```python
def _random_saturation(image, proportion):
    theshold_const = tf.constant(proportion, dtype=tf.float32)
    rand = tf.random_uniform([1], minval=0.0, maxval=1.0, dtype=tf.float32) 
    image = tf.cond(rand[0] < theshold_const,   
                    lambda: tf.image.random_saturation(image, lower=0.9, upper=1.1),
                    lambda: tf.identity(image))
    return image
```

### 椒盐噪声

```python
def _salt_noise(image, minval, maxval):
    shape_array = tf.shape(image).eval()
    height = shape_array[0]
    width = shape_array[1]
    image = image + tf.cast( tf.random_uniform(shape=[height, width, 3],
                   minval=minval, maxval=maxval), tf.uint8)
    return image
```

### 调用方法：

```python
def preprocess(image, img_shape, is_training):
    # random crop
    # 长宽成比例裁剪
    rate = 0.6
    shape_array = tf.shape(image).eval()
    height = int(shape_array[0] * rate)
    width = int(shape_array[1] * rate)
    image = tf.random_crop(image, [height, width, 3])
    
    # random flip 随机上下左右反转
    image = _random_flip(image, left_right_proportion=0.7, up_down_proportion=0.3)
    
    # 转置
    image = _transpose_image(image, 0.8)
    
    # 旋转 k * 90
    image = _rot90(image, 0.8, k=2)
    
    # gauss
    image = _gauss(image, img_shape, 0.8)   
    
    # 随机亮度 danger 有bug 取值会越界 ./255 即可
    image = _random_brightness(image, proportion=66)
    
    # 对比度
    image = _random_contrast(image, 0.8) 
    
    # 图像灰度 max_delta 在0-0.5
    image = _adjust_hue(image, 0.8)
    
    # 图像饱和度，
    image = _random_saturation(image, 0.8)    
    
    # 椒盐噪声  
    image = _salt_noise(image, minval=0.8, maxval=1.001)
    
    return image
```



