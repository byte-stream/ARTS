## 给 hexo 添加瀑布式相册

参考链接：<https://me.idealli.com/post/73ad4183.html>

但是原文贴出的代码中有 bug，并且有一些配置没有说明，在这里全面总结一下。

大部分内容引用自原博，添加内容会做说明。

昨天突发奇想给博客写了个相册页面，使用腾讯云cos作为相册的存储桶，使用api在线获取相册里面的存储桶里的照片并且实时生成相册内容。之前也有看过一些人做的相册页面，但是对于我来说，还是感觉不方便。网上的大多是在本地项目文件夹存放照片，然后更改一系列的主题文件来实现相册页面。

比如这位制作的[Hexo NexT 博客增加瀑布流相册页面](https://blog.dongleizhang.com/posts/3720dafc/)，然而他做的过程已经算是比较简洁了，没有改动太多主题配置。但是这种相册，每次添加新照片的时候，还是需要手动在相册页面添加相应的图片链接与代码。

所以我想能不能做一个直接后台上传图片，不用再改动代码的静态博客的相册页面呢，就像一个动态博客一样，或者像 qq 相册那样，只需要上传照片就可以了。

答案是可以的，机智的我使用了腾讯云的cos存储桶作为相册后台，调用cos存储桶的xml文件api在线获取图片链接，再使用JavaScript代码动态生成相册内容。

步骤如下：

### 创建腾讯云 cos 存储桶

搜索腾讯云，注册账号登陆，在云产品中选择对象存储，新建一个存储桶。就OK了。![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/给-hexo-添加瀑布式相册/1555401694589.png)

### 跨域访问 cors 设置

在基础配置中找到cors设置![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/给-hexo-添加瀑布式相册/1555401902258.png)

操作选择 GET，来源 Origin 填写你的域名，带 http 或者 https，其他默认不要填，如下图![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/给-hexo-添加瀑布式相册/1555401947976.png)

然后记住这个地方**访问域名**，这里就是我们动态生成相册，获取链接时需要用到的 xml 链接，下面要用到![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/给-hexo-添加瀑布式相册/1555402065533.png)

### 配置权限

不进行这一步，你永远取不到 xml。

![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/给-hexo-添加瀑布式相册/1555402171216.png)![](https://bucket-1258741719.cos.ap-beijing.myqcloud.com/给-hexo-添加瀑布式相册/1555402320582.png)

将箭头所知的地方改为 Allow。

至此，腾讯云 COS 部署完成。

### hexo 本地配置

在本地项目新建一个相册页面

```shell
hexo new page photos
```

编辑 \source\photos\ 路径下的`index.md`文件，写入以下代码

记得在下面的代码中填写 xmllink 的值，也就是上面提到的你的存储桶访问域名

代码和原版略有出入，修正了一些 bug。

```javascript
<style type="text/css">
	.main-inner{
		width: 100%;
	}
	.main {
    padding-bottom: 150px;
    margin-top: 0px;
    background: #121212;
	}
	.main-inner{
		margin-top: unset;
	}
	.page-post-detail .post-meta{
		display: none;
	}
	body {
		background-image: unset;
		background-attachment: unset;
		background-size: 100%;
		/*background-position: top left;*/
	}
	.header{
		background: rgba(28, 25, 25, 0.6);
		border-bottom: unset;
	}
	.menu .menu-item a{
		    font-weight: 300;
    		color: #e6eaed;
	}

	.imgbox{
	 width: 100%;
	 overflow: hidden;
	 height: 250px;
	 border-right: 1px solid #bcbcbc;
	}
	.box{
		visibility: visible;
		overflow: auto;
		zoom: 1;
	}
	.box li{
	float: left;
	width: 25%;
	position: relative;
	overflow: hidden;
	text-align: center;
	list-style: none;
	margin: 0;
	/*display: inline;*/
	padding: 0;
	height: 360px;
	}
	.box li span{
	display: block;
	padding: 4% 7% 10% 7%;
	min-height: 80px;
	background: #fff;
	color: #fff;
	font-size: 16px;
	background: #121212;
	font-weight: 600;
	line-height: 26px;
	-webkit-box-sizing: border-box;
	box-sizing: border-box;
	}

	img.imgitem{
		padding: unset;
		padding: unset;
		border: unset;
		position: relative;
		padding: 0px;
		height: auto;
		width: 100%;
	}

	div#comments.comments.v {
	border: 0px;
	margin: auto !important;
	margin-top: unset;
	margin-left: unset;
	margin-right: unset;
	width: 60%;
	padding-top: 50px;
}

div#posts.posts-expand {
    border: unset;
    padding: unset;
    margin-bottom: 10px;
}
.posts-expand .post-body img{
	padding: 0px !important;
}
.box p{
	display: block;
    background: #121212;
    color: #fff;
    font-size: 12px;
    font-family: 'SwisMedium';
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    text-align: center;
}

.box span strong{
	background: rgba(0,0,0,0.4);
	padding: 20px;
}

.posts-expand .post-title {
	display: none;
}
.title{
    display: inline-block;
    vertical-align: middle;
    background: url(https://image.idealli.com/bg11.jpg);
    font: 85px/250px 'ChaletComprimeMilanSixty';
    background-position: left bottom !important;
    color: #fff;
    background-size: 100% auto !important;
	-webkit-background-size: cover;
	-moz-background-size: cover;
	-o-background-size: cover;
    width: 100%;
    text-align: center;
    border: unset;
    height: 700px;
    cursor: unset !important;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
}
.btn-more-posts{
	display: inline-block;
    vertical-align: middle;
    font: 85px/250px 'ChaletComprimeMilanSixty';
    color: #000;
    width: 100%;
    text-align: center;
    border: unset;
    height: 400px;
    background-color: #121212;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
}

@media (max-width: 767px){
	.box li {
    width: 100%;
}
.title {
    height: 200px;
}

.box span {
    min-height: 80px;
    border-right: unset;
    font-size: 17px;
}
.box p{
    border-right: unset;
    font-size: 12px;

}
.posts-expand {
    margin: unset;
}
	div#comments.comments.v {
    width: 96%;
    padding-top: 50px;
}


}

@media (min-width: 1600px){
	.container .main-inner{
		width: 100%;
	}
}

.footer{
	background-color: #121212 !important;
}
.v * {
    color: #f4f4f4 !important;
}

.v .vwrap .vmark .valert .vcode {
    background: #00050b !important;
}

</style>

<div id="box" class="box"></div>


<script type="text/javascript">

if (window.XMLHttpRequest)
{// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
}
else
{// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}

var xmllink="yourlink"
//访问域名链接就是我上面提到的那个访问域名xml链接

xmlhttp.open("GET",xmllink,false);
xmlhttp.send();
xmlDoc=xmlhttp.responseXML;

var urls=xmlDoc.getElementsByTagName('Key');
var date=xmlDoc.getElementsByTagName('LastModified');
var wid=250;
var showNum=12; //每个相册一次展示多少照片
if ((window.innerWidth)>1200) {wid=(window.innerWidth*3)/18;}
var box=document.getElementById('box');
var i=0;

var content=new Array();
var tmp=0;
var kkk=-1;
for (var t = 0; t < urls.length ; t++) {
	var bucket=urls[t].innerHTML;
	var length=bucket.indexOf('/');
	if(length===bucket.length-1){
		kkk++;
		content[kkk]=new Array();
		content[kkk][0]={'url':bucket,'date':date[t].innerHTML.substring(0,10)};
		tmp=1;
	}
	else {
		content[kkk][tmp++]={'url':bucket.substring(length+1),'date':date[t].innerHTML.substring(0,10)};
	}
}

for (var i = 0; i < content.length; i++) {
	var conBox=document.createElement("div");
	conBox.id='conBox'+i;
	box.appendChild(conBox);
	var item=document.createElement("div");
	var title=content[i][0].url;
	item.innerHTML="<button class=title style=background:url("+xmllink+'/'+title+"cover.jpg"+");><span style=display:inline;><strong style=color:#f0f3f6; >"+title.substring(0,title.length-1)+"</strong></span></button>";
	conBox.appendChild(item);

	for (var j = 1; j < content[i].length && j < showNum+1; j++) {
		var con=content[i][j].url;
		var item=document.createElement("li");
		item.innerHTML="<div class=imgbox id=imgbox style=height:"+wid+"px;><img class=imgitem src="+xmllink+'/'+title+con+" alt="+con+"></div><span>"+con.substring(0,con.length-4)+"</span><p>上传于"+content[i][j].date+"</p>";
		conBox.appendChild(item);
	}
	if(content[i].length > showNum){
		var moreItem=document.createElement("button");
		moreItem.className="btn-more-posts";
		moreItem.id="more"+i;
		moreItem.value=showNum+1;
		let cur=i;
		moreItem.onclick= function (){
			moreClick(this,cur,content[cur],content[cur][0].url);
		}
		moreItem.innerHTML="<span style=display:inline;><strong style=color:#f0f3f6;>加载更多</strong></span>";
		conBox.appendChild(moreItem);
	}
}

function moreClick(obj,cur,cont,title){
	var parent=obj.parentNode;
	parent.removeChild(obj);
	var j=obj.value;
	var begin=j;
	for ( ; j < cont.length && j < Number(showNum) + Number(begin); j++) {
		console.log( Number(showNum) + Number(begin));
		var con=cont[j].url;
		var item=document.createElement("li");
		item.innerHTML="<div class=imgbox id=imgbox style=height:"+wid+"px;><img class=imgitem src="+xmllink+'/'+title+con+" alt="+con+"></div><span>"+con.substring(0,con.length-4)+"</span><p>上传于"+cont[j].date+"</p>";
		parent.appendChild(item);
	}
	if(cont.length > j){
		obj.value=j;
		parent.appendChild(obj);
	}
}

</script>
```

然后刷新 hexo 渲染

```
hexo clean
hexo d -g
```

再往cos存储桶里上传照片，就可以了！效果如下
重要的是以后更新照片都不用改动代码。往腾讯云cos上传照片就好了，而且腾讯云页提供了很多工具可以再本地命令行上传照片，非常方便，感兴趣可以自行百度。
