#### 装饰者模式

​	

​	之前学习JAVAIO时对于文本字符串操作经常写以下代码，当时使用这种方式只是图方便，没有仔细想过为什么这样可以做到直接读取整行字符串。直到后来学了装饰者模式，才慢慢有点了解。

```
// 代码1
InputStream is = new FileInputStream(filePath);
BufferedReader reader = new BufferedReader(new InputStreamReader(is));
String line = reader.readLine(); // 读取第一行!

// 代码2
InputStream is = new FileInputStream("filePath");
BufferedInputStream bi = new BufferedInputStream(is);
LineNumberInputStream ls = new LineNumberInputStream(bi);
```

 

​	装饰者模式是一种能将功能动态的附加到对象上，能提供比继承更有弹性的替代方案。符合对扩展开放对修改关闭原则。

​	在装饰者模式中：

 - 装饰者和被装饰者对象拥有同一个超类型
 - 可以用一个或多个装饰者包装一个对象
 - 由于装饰者与被装饰者拥有相同超类型，所以在需要原始对象(被装饰者)时，都可以用装饰者来代替它
 - 装饰者可以在被装饰者委托的行为前后加上自己想要的行为，达到装饰目的
 - 对象可以在任何时候被修饰，并且不限制修饰的数量

<img src="https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/1.png" style="width:200px height:300px" />

​	上图对应代码2，FileInputStream为原始对象(被装饰者)，BufferedInputStream和LineNumberInputStream为装饰者，当调用LineNumberInputStream对象的read()方法时，BufferedInputStream和FileInputStream类的read()方法将被依次调用，然后再逐层返回，有点类似递归。

​	这种调用方式间接使用了组合而非继承来组装对象的关联，对应与has-a而非is-a。

![](<https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/zhuangshi.png>)

​	上图对应于代码1，在Stream类别中展示了装饰者模式的对应框架，具体组件和抽象装饰者都同一由抽象组件派生，其中抽象装饰者定义了所有装饰者装饰者所必须实现的接口。间接的，具体装饰者与具体组件都拥有同一超类型。

​	其中比较不同的是Reader，所以Reader也拥有对应的FilterReader，但是它的作用和FilerInputStream不太一样，它并不充当抽象装饰者，而是通过适配器适配到Reader类别的具体组件(也许由于java只支持单继承)，而BufferedReader也属于装饰者，所以就出现了代码1中一层套一层的写法。

​	弄懂了这个基本框架后，也可以自己实现一个具体装饰者对组件进行再包装。

```
// 装饰者，将读取文件内容转大写
public class UppercaseInputStream extends FilterInputStream {

    public UppercaseInputStream(InputStream in) {
        super(in);
    }

    @Override
    public int read(byte[] b, int off, int len) throws IOException {
        int read = super.read(b, off, len);
        for (int i = off; i < off + len; i++) {
            b[i] = (byte) Character.toUpperCase(b[i]);
        }
        return read;
    }

    @Override
    public int read() throws IOException {
        int read = super.read();
        return (read == -1 ? read : Character.toUpperCase(read));
    }
}
```

```
public static void main(String[] args) throws IOException {
        // 原始对象
        InputStream is = new FileInputStream("test.txt");
        // 装饰者
        BufferedInputStream bs = new BufferedInputStream(is);
        UppercaseInputStream ui = new UppercaseInputStream(bs);
        int c;
        while ((c = ui.read() )!= -1) {
            System.out.print((char)c);
        }
        ui.close();
    }
```

​	总结：装饰者模式使用组合而非继承，使得类设计更有弹性。但这就要求使用前需要知道有哪些装饰者可以使用，因为实例化原始对象后，还要将其包装进装饰者中(如果需要装饰者的功能的话)，这将带来一定的代码复杂性。

​	在编写代码的过程中，如果代码使用到了装饰者模式，而自己又不知道的话，将很难用好它。