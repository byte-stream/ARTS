## CSS 文章排版小技巧

之前写的文章排版都是 Markdown 写完直接丢出来，比较随意，最近特意学了一下 CSS 的一些常见操作，把自己的文章排版设计了一个简单的模板，后面再细细优化。记录一些值得注意的地方。

### a 标签

不显示 line：

```css
text-decoration: none;
```

悬浮显示 line：

```css
a:hover, a:focus {
    text-decoration: underline;
}
```

调节 line 距离和动态显示：

```css
a:hover, a:focus {
    text-decoration: none;
    padding: 2px;
    border-bottom-style: solid;
    border-bottom-width: 1px;
}
```

![click.gif](https://i.loli.net/2019/01/19/5c42e67f1da86.gif)

<center>悬浮效果</center>

### 字体 

字体粗细可以用 font-weight 属性来调节：

```css
font-weight: bold
font-weight: bolder
font-weight: 600
```

### img

图片缩进和阴影：

```css
img {
    border: 0;
    width: 90%;
    height: auto;
    box-shadow:  #080808 0px 0px 10px;
}
```

可以添加图片的注释信息，使用 center 标签居中：

```css
center {
    font-size: 12px;
    color: #777777;
}
```

图片示例如下：

![demo.jpg](https://i.loli.net/2019/01/19/5c42e67f7be09.jpg)

<center class="note">旅行照片</center >

### 动态居中

如果需要把 H2 标签居中，根据内容长度来显示 border 的长度：

```css
h2 {
    /* padding-bottom: .3em; */
    font-size: 1.5em;
    line-height: 1.225;
    border-bottom: 1px solid rgb(185, 185, 185);
    display: table;
    margin: 0 auto;
    padding: 5px;
}
```

效果图如下：

![css_center.png](https://i.loli.net/2019/01/19/5c42e67f3da10.png)



通过简单的排版布局，不得不感叹 CSS 真的难学啊，调来调去的比较耗耐心，以后还是少搞这些外表功夫了，太费脑子。