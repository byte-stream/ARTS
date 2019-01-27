# Django查询优化之select_related、prefetch_related

`select_related`和  `prefetch_related` 是Django最常见的数据库层查询性能优化方案，合理的使用可以减少查库次数，从而提升查询性能。当然，不需要的时候也不要乱用，否则会事倍功半。虽然两者的设计目的一致，都是减少查库次数，不过两者的实现方法不同。通过几个例子，了解两个方法的使用。


## Example models

> **本文的查询都基于这些models**，最好可以新建一个Django demo，进行调试

```python
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.ForeignKey(City)  # 城市

class Publisher(models.Model):
    name = models.CharField(max_length=300)

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

class Store(models.Model):
    name = models.CharField(max_length=300)
    book = models.ManyToManyField(Book)
```



## Tips

为了能更直观的查看orm的查询次数，我们可以在`settings`文件 中加入一段`logging`配置，可以在console 中执行orm时，同时输出对应SQL，从而更直观的进行性能比较。

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}
```



## select_related

`select_realted` 用于`OneToOneFiled, ForeignKey`字段，相当于SQL层面的 `INNER JOIN` ，在查询时将标记的相

关表关联起来，再取出需要的字段。

### *fields 参数

**例：查看所有书籍的出版社名字**

优化：

![优化](http://picture.wzmmmmj.com/use_select_related.png)

未优化：

![未优化](http://picture.wzmmmmj.com/no_use_select_related.png)



对比两次查询，可发现在使用`select_realted`后 ，SQL中使用了`INNER JOIN`进行连表，从而整个循环只查库一次，反观不加优化的查询，因为需要跨表，导致查库4次，当数据量增大会加大对db层面查询压力。

如果想连续连接好几个表可以如下操作，两者结果相同。

```python
from app.models import Book

Book.objects.all().select_related('author', 'publisher')
# or
Book.objects.all().select_related('author').select_related('publisher') # Django1.7后
```

有时候我们会遇到更深层次的查询，可以使用`__`（双下划线），查询外键的外键表字段

**例如: 查询所有书作者的所在城市**

```python
from app.models import Book

Book.objects.all().select_related('author__city')
```

### 无参数

如果未指定了参数，Django会尽可能深的去遍历所有`OneToOneFiled, ForeignKey`字段。不过不建议使用，因为这样会导致一些问题

- Django可能会将所有表关联，造成不必要的性能浪费
- Django本身可能会有定深度上限，会在不知道的跳出遍历，导致与结果不一致

## prefetch_related

`prefetch_related`适用于`ManyToManyField, OneToManyField（也就是ForeignKey的反向查询）`，不同于`select_related`，`prefetch_related`的优化方案是，分别查询每个表，通过Python处理表之间的关系，而不是和`select_related`一样在SQL层通过JOIN语句进行优化。

### *lookup 参数

用法与`select_related`基本相同，也支持链式写法。

```python
from app.models import Store

Store = Store.objects.all().prefetch_related('books')
```



**例： 获取每个书店的所有书籍**

优化：

![优化](http://picture.wzmmmmj.com/use_prefetch_related.png)

未优化：

![未优化](http://picture.wzmmmmj.com/no_use_prefetch_related.png)

通过看使用`prefetch_related`的查询SQL，可以发现在第二查询的时候，加了WHERE 条件`where store.id in (1,2,3)`，从而查库1+1次，而不是未使用优化时，每次遇到`store.books.all()`，才去查库，导致查库1+3次。

## 总结

- `select_related`主要针一对多和多对多关系进行优化；
- `prefetch_related`通过分别获取各个表的内容，然后用Python处理他们之间的关系来进行优化；
-  两者相比，能使用`select_related`时，尽量使用。
