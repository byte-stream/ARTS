在第九节里 winter 通过一篇 [外国CSS标准文献](https://www.w3.org/TR/css-syntax-3/ ) 引出了他的主要观点。

> `CSS` 的 顶层样式表 由两种规则组成的规则列表构成，一种被称为 at-rule，也就是 **at 规则**，另一种是 qualified rule，也就是 **普通规则**。 

## at 规则

at-rule 由一个 @ 关键字和后续的一个区块组成，如果没有区块，则以分号结束。

- @charset
- @import
- @media
- @page
- @counter-style
- @keyframes
- @fontface
- @supports
- @namespace

## 普通规则

普通规则则是我们熟悉的 **选择器** 和 **声明列表** 组成

- 普通规则
  - 选择器
  - 声明列表
    - 属性
    - 值
      - 值的类型
      - 函数



### 选择器

- complex-selector
    - combinator（连接）
        - 空格
        - `>`
        - `+`
        - `~`
        - `||`
    - compound-selector（单个元素）
        - type-selector
        - subclass-selector
            - id
            - class
            - attribute
            - pseudo-class
        - pseudo-element

选择器连接：空格、大于号、波浪线、双竖线

选择器类型：id、class、元素、伪类和属性

### 声明列表

#### 1、声明变量值

> 实际就是 `CSS` 的变量值

``` CSS
/* 根元素，可以存放变量值 */ 
:root {
    --main-color: #fff;
}

body {
    /* 使用 var 来使用变量值 */
    color: var(--main-color);
}
```

#### 2、变量值类型

> 经常使用到的地方就是初始值、宽高、计算值、伪类的 `content` 值、URL值等，类似于预编译语言Less和Sass使用

- `CSS` 范围的关键字：initial，unset，inherit，定义为初始值、继承。

- 字符串：content
- URL/图片URL
- 整数或实数
- 纬度：带单位的整数或实数
- 百分比/颜色/图片/ 2D 位置
- 函数的值

```css
/* 例子 */

/* 根元素 */
:root {
    --initial-content: "你好";
    --initial-url: url(../img/);
    --initial-width: 20;
    /* 带单位时，不能用字符串 */
    --initial-width: 20px;
    --color: #fff;
    --BgColor: #ccc;
}
```

#### 3、变量值的类型限制

- 字符串可以与字符拼接
```CSS
body {
    --bar: 'hello';
    --foo: var(--bar)' world';
}
```

- 变量值是数值，不能与数值单位直接连用

```css
.foo {
    --gap: 20;
    /* 无效 */
    margin-top: var(--gap)px;
}

/* 使用calc()函数连接 */

.foo {
    --gap: 20;
    margin-top: calc(var(--gap)* 1px);
}
```

- 变量带有单位，则不能写成字符串

```css
/* 无效 */
.foo {
    --foo: '20px';
    font-size: var(--foo)
}

/* 有效 */
.foo {
    --foo: 20px;
    font-size: var(--foo)
}
```
### 计算型函数

- `calc()` 可以说是一个计算器，我们可以在里面运行我们的计算表达式。且可以计算各种单位的数值

```css
div {
    width: calc(100%/3 - 2*1em - 2*1px);
}
```

- `max()`、`min()`、`clamp()` 最大值、最小值和范围值

- `attr()` 获取属性值

```
.tooltip:after{
  content:attr(data-tooltip);  
}

<div class="tooltip" data-tooltip="提示" data-direction="down">down</div>
```

- [transform 的一系列图形旋转](http://www.w3school.com.cn/cssref/pr_transform.asp)

- [filter 的一系列滤镜变化](https://developer.mozilla.org/zh-CN/docs/Web/CSS/filter)

- linear-gradient() & radial-gradient() 线性渐变和径向渐变

### 总结

CSS 从学习以来就是以多而复杂著称，winter这次教程则是让我们 **从整体上去掌握内容，再去定位到单个细节** 这对于我们学习 CSS 有非常重要的提示作用。



再分享一本张鑫旭老师出版的《CSS世界》，希望能加深你的学习。

链接：https://pan.baidu.com/s/1gwKQeKU2uDAPK0Gbvoj8OA 
提取码：971z 