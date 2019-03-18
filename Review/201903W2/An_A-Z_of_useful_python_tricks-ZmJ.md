## An A-Z of useful Python tricks

原文地址：[An A-Z of useful Python tricks](https://medium.freecodecamp.org/an-a-z-of-useful-python-tricks-b467524ee747)

Python 是世界上最受欢迎，需求量最大的编程语言之一。这是几个重要原因：

- 易学
- 涉及范围广
- 大量的模块和库

作为数据科学家， 每天使用Python是我工作的一部分。这一路上，我发现了一些实用的技巧。

这里我尝试分享一些以A-Z开头的技巧。

但是，主要归功于它 `awesome-python.com`，我在上面发现了4或5个技巧。 这里有数百个有趣的Python工具和模块精选列表。值得浏览从而获取灵感。

### all or any

为什么Python是一个受欢迎的语音，其中一个原因是因为它可读性以及表达能力强。

人们经常开玩笑的说`Python是可执行的伪代码`，但是当你可以编写这样的代码时，很难用其他方法反驳。

```python
x = [True, True, False]
if any(x):
    print("At least one True")
if all(x):
    print("Not one False")
if any(x) and not all(x):
    print("At least one True and one False")
```

### bashplotlib

如果你想在控制台中绘制图形？

```bash
pip install bashplotlib
```

你可在控制台中显示图表

### collections

Python有许多优秀的数据类型，但是有时候它们都不是实现我们想要的。

幸运的是，Python标准库提供了`collection`模块。这个组件提供了更多便利的数据类型。

```python
from collections import OrderedDict, Counter
# Remembers the order the keys are added!
x = OrderedDict(a=1, b=2, c=3)
# Counts the frequency of each character
y = Counter("Hello World!")
```

### dir

有时候你想知道Python对象中有哪些属性？

当然，你可以，命令行中：

```bash
>>> dir()
>>> dir("Hello World")
>>> dir(dir)
```

当以交互式运行Python以及动态查看正在使用的对象和模块时，这可能是一个非常实用的功能。

### emoji

```bash
pip install emoji
```

不要假装你不会尝试一下（作者皮了一下）

```python
from emoji import emojize

print(emojize(":thumbs_up:"))

👍
```

### from __ future __ import * 

Python受欢迎的一个后果是，一直会开发新版本。新版本意味着新功能，除非你的版本已过时。

但是，不要紧张，`__future__`模块运行你从未来版本的Python中导入功能，它就像时间旅行，魔术，或其他。

```python
from __future__ import print_function

print('Hello Wolrd')
```

### geopy

对应程序员来说，地理位置可能会是一个具有挑战性的领域。但是`geopy`模块让它变得非常简单。

```bash
pip install geopy
```

它的工作原理是抽象出一系列不同地理编码服务的API。它使你可以获得一个位置的街道全称，经纬度甚至高度。

它还有一个实用的距离类，它可以计算出两个你最喜欢的测量单位之间的距离。

```python
from geopy import GoogleV3
place = "221b Baker Street, London"
location = GoogleV3().geocode(place)
print(location.address)
print(location.location)
```

### howdoi

遇到编码问题而忘记了之前看过的解决方案？需要查看`StackOverflow`，但不想离开终端？

你需要这个[实用的命令行工具](https://github.com/gleitz/howdoi)

```bash
pip install howdoi
```

它会尽力回答你所问的问题。

```bash
$ howdoi vertical align css
$ howdoi for loop in java
$ howdoi undo commits in git
```

> 它从`StackOverfolw`的高赞答案中检索代码，可能并不总能提供有用的信息

```bash
$ howdoi exit vim
```

### inspect

Python的`inspect`模块非常适合去理解在幕后发生的事。你甚至可以自己调用他的方法。

下面示例代码调用`inspect.getsource()`去打印它自己的源代码，它还可以使用`inspect.getmodule()`去打印模块在哪里被定义。

最后一行代码则是打印出自己的行号。

```python
import inspect
print(inspect.getsource(inspect.getsource))
print(inspect.getmodule(inspect.getmodule))
print(inspect.currentframe().f_lineno)
```

### Jedi

`Jedi`库是一个自动补全和代码分析的库，它可以使编写代码更加快速从而提高生产效率。

除非你正在开发自己的IDE，否则你可能对使用Jedi插件更感兴趣，幸运的是，已经可用了。

也许你已经在使用Jedi了，IPython就利用Jedi实现了代码自动补全功能。

### **kwargs

学习任何语言时，会有许多里程碑。Python中，理解神秘的`**kwargs`语法可能算作一个。

字典对象前面的双星号允许你将字典的内容作为命名参数传递给函数。

字典的键是参数的命名， 值是传递给函数的值，你甚至不需要称它为`kwargs`

```python
dictionary = {"a": 1, "b": 2}
def someFunction(a, b):
    print(a + b)
    return
# these do the same thing:
someFunction(**dictionary)
someFunction(a=1, b=2)
```

在你编写可以处理事先未定义的命名参数的函数时，这非常有用。

### List comprehensions

我最喜欢使用Python的一点是它的列表推导式。这些表达式可以很容易的编写非常干净的代码，几乎就想自然语言一样。

``` python
numbers = [1,2,3,4,5,6,7]
evens = [x for x in numbers if x % 2 is 0]
odds = [y for y in numbers if y not in evens]
cities = ['London', 'Dublin', 'Oslo']
def visit(city):
    print("Welcome to "+city)
for city in cities:
    visit(city)

```

### map

Python通过许多内置功能支持函数式编程。其中`map()`是最实用的，尤其是在和`lambda`函数一起使用时。

``` python
x = [1, 2, 3]
y = map(lambda x : x + 1 , x)
# prints out [2,3,4]
print(list(y))
```

在上面的示例中，`map()`将一个简单的`lambda`函数应用于x中的每个元素。它返回一个map对象，可以将其转换为某个可迭代对象，例如list或tuple

### newspaper3k

如果你还没有见过它，那么请准备好让你的思绪被Python的`newspaper`所震撼。

它允许你从一系列国际出版物中检索新闻文章和相关的元数据。您可以检索图像，文本和作者姓名。

它甚至还有一些内置的NLP功能，所以如果你想在你下一个项目中使用`BeautifulSoup`或一些DIY

页面编写库，那么请节省时间和精力，然后`pip install newspaper3k` 

### operator overloading

Python提供了对运算符重载的支持，这使你听起来像一个合法的计算机科学家的术语之一。

实际上，这是一个简单的概念。有没有想过为什么Python允许使用`+`运算符来添加数字以及连接字符串？这就是运算符的重载。

你可以按照自己的特定方式定义使用Python标准运算符符号的对象，这使你可以在与你使用的对象相关的上下文中使用它们。

```python
class Thing:
    def __init__(self, value):
        self.__value = value
    def __gt__(self, other):
        return self.__value > other.__value
    def __lt__(self, other):
        return self.__value < other.__value
something = Thing(100)
nothing = Thing(0)
# True
something > nothing
# False
something < nothing
# Error
something + nothing
```

### pprint

Python默认的`print`函数可以完成他的工作，但是尝试打印任何嵌套大的对象，结果很丑陋。

这是标准库的`pretty-print`模块的用武之地。它可以打印出易于阅读的结构化对象。

它是任何使用不规律数据的Python开发人员必备的

```python
import requests
import pprint
url = 'https://randomuser.me/api/?results=1'
users = requests.get(url).json()
pprint.pprint(users)
```

### Queue

Python支持多线程，标准库的`Queue`模块为此提供了便利。

这个模块可以让你实现队列数据结构。这些是根据特定规则添加和检索的数据结构。

先进先出（FIFO）队列允许你按照添加的顺序检索对象，而后进先出（LIFO）队列则允许你首先访问最近添加的对象。

最后，优先级队列允许你根据对象的排列顺序检索对象。

### __ repr __

在Python中定义类或对象时，提供一种将该对象表示为字符串的方法，例如：

```python
>>> file = open('file.txt', 'r')
>>> print(file)
<open file 'file.txt', mode 'r' at 0x10d30aaf0>
```

这让DEBUG代码更为轻松，添加到的你类定义到中，如下：

```python
class someClass:
    def __repr__(self):
        return "<some description here>"
someInstance = someClass()
# prints <some description here>
print(someInstance)
```

### sh

Python是一个优秀的脚本语言，有时候使用标准的操作系统和字进程库可能会让人头痛

`sh`库提供了整洁的替代品。

它允许你调用任何程序，就像是一个普通函数一样，对于自动化工作流程和任务十分有益。

```python
import sh
sh.pwd()
sh.mkdir('new_folder')
sh.touch('new_file.txt')
sh.whoami()
sh.echo('This is great!')
```

### Type hints

Python是一个动态类型语言，在你定义变量，函数，类时，你不用指定数据类型。

这允许快速开发，然而，有一些事情比简单的键入问题导致的运行时错误更令人讨厌。

从Python3.5开始，你可以选择在定义函数时，提供类型提示。

```python
import sh
sh.pwd()
sh.mkdir('new_folder')
sh.touch('new_file.txt')
sh.whoami()
sh.echo('This is great!')
```

你也可以定义类型别名

```python
from typing import List
Vector = List[float]
Matrix = List[Vector]
def addMatrix(a : Matrix, b : Matrix) -> Matrix:
  result = []
  for i,row in enumerate(a):
    result_row =[]
    for j, col in enumerate(row):
      result_row += [a[i][j] + b[i][j]]
    result += [result_row]
  return result
x = [[1.0, 0.0], [0.0, 1.0]]
y = [[2.0, 1.0], [0.0, -2.0]]
z = addMatrix(x, y)
```

虽然不是强制性的，但类型注释可以使你的代码更容易理解。

### uuid

Python标准库`uuid`，是一个生成唯一ID(或uuid)的快捷方法

```python
import uuid
user_id = uuid.uuid4()
print(user_id)
```

这会创建一个随机的128位苏子，几乎肯定是唯一的。

实际上，可以生成超过2的122次方个可能的UUID，这超过50万亿，在给定集合中找到重复的概率非常低，即使有万亿UUID，重复存在的可能性也远远低于十亿分之一。

### Virtual environments

这可能是我最喜欢的Python的东西了。

任何时候，在处理多个Python项目，不幸的是，有时两个项目将依赖同一个依赖项目的不同版本。

幸运的是，Python对虚拟环境的支持让你拥有两全其美的有事，从命令行：

```bash
python -m -venv my-project
source my-project/bin/activate
pip install all-the-moudules
```

现在你可以在同一台电脑上运行独立版本和Python的安装。

### wikipedia

维基百科有一个很棒的API，允许用户以编程方式访问无以伦比的完全免费的知识和信息。

在`wikipedia`中，使访问API变得异常方便。

```python
import wikipedia

result = wikipedia.page('freeCodeCamp')
print(result)
for link in result.links:
    print(link)
```

与真实网站一样，该模块提供对多种语言的支持，页面消歧，随机页面检索，甚至还有一种，`donate()`方法。

### xkcd

幽默是Python语言的一个关键特征，毕竟，他是英国喜剧`Monty Python`的飞行马戏团命名的，Python大部分官方文档都引用了该剧最著名的草图。

但，幽默感并不局限与文档，按以下方式运行

```python
import antigravity
```

### YAML

YAML代表`YAML Is Not Markup Language`。它是一种数据格式化语言，是Json的超集。

与Json不同的是，它可以存储更复杂的对象，并引用他自己的元素。你也可以写一些注释，使其特别适合编写配置文件。`PyYAML`模块让你通过Python使用YAML，安装如下：

```bash
pip install pyyaml
```

导入模块到项目：

```python
import yaml
```

PyYAML 允许你存储任何数据类型的Python对象，以及任何用户定义类的实例。

### zip

最后一个技巧，曾经有需要从两个列表中形成字典吗？

```python
keys = ['a', 'b', 'c']
vals = [1, 2, 3]
zipped = dict(zip(keys, vals))
```

`zip()`内置函数接受可迭代对象并返回元祖列表，每个元祖按位置索引对输入对象的元素进行分组 。

你也可以通过使用`*zip()` ，对它们进行解包。