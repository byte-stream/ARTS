# 懒加载
网页开发时，因为服务器加载的数据可能过大，但是用户界面只能显示那么多，所以没必要等待全部加载完才开始显示，这样会显示速度变卡。

懒加载：延迟加载，对网页性能优化的方式，比如当访问一个页面的时候，优先显示可视区域的内容而不是一次性加载所有内容，当需要显示的时候再发送请求，避免打开网页时加载过多资源。

实现方式
方式一 : 使用scrollTop/innerHeight/offsetTop
window.innerHeight：浏览器可视区域高度
document.body.scrollTop || document.documentElement.scrollTop：浏览器滚动条滚过高度
img.offsetTop：元素距文档顶部的高度 

加载条件：
img.offsetTop<window.innerHeight+document.body.scrollTop>

方法二：使用IntersectionObserver方法
基本知识：
var io = new IntersectionObserver(callback, option);
 
//开始观察
io.observe(document.getElementById('example'));
 
//停止观察
io.unobserve(element);
 
// 关闭观察器
io.disconnect();

其中，callback是可见性变化时的回调函数，option是配置对象。这个构造函数的返回值是一个观察器实例。构造函数的返回值是一个观察器实例，实例的observe方法可以指定观察哪个DOM节点。

observer的参数是一个DOM节点对象。如果要观察多个节点，就要多次调用这个方法。
callback函数的参数是一个数组，每个成员都是一个IntersectionObserverEntry对象。