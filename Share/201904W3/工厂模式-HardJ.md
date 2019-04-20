## 工厂模式

​	很多时候当我们创建对象时经常会造成对象与某个具体实现“耦合”的问题。而如果能通过依赖接口，而再运行时动态决定要创建的具体对象，将降低系统的耦合度，使系统更容易扩展与维护。针对接口编程可以减少很多不必要的麻烦，而工厂模式正是用来做这件事的。

​	工厂模式进一步细分为：简单工厂模式、工厂方法模式、抽象工厂模式，三种模式有各自的优缺点，也有一定的关联。

#### 	简单工厂模式

​	简单工厂模式其实不是一种具体设计模式，更像是一种编程习惯，它将创建对象的处理细节抽取出来，然后通过提供一个共有接口按照传入的指定产品描述生产出具体的产品。

```java
// 简单工厂
public class SimpleFactory {

    public MilkTea getMilkTea(String type) {
        MilkTea milkTea = null;
        if("rose".equals(type)) {// 玫瑰奶茶
            milkTea = new RoseMilkTea();
        }else if("taro".equals(type)) {// 香芋奶茶
            milkTea = new TaroMilkTea();
        }else if("strawberry".equals(type)) {// 草莓奶茶
            milkTea = new TaroMilkTea();
        }
        return milkTea;
    }
}

// 奶茶店
public class MilkTeaStore {

    SimpleFactory simpleFactory;

    public MilkTeaStore(SimpleFactory simpleFactory) {
        this.simpleFactory = simpleFactory;
    }

    public MilkTea orderMilkTea(String type) {
        MilkTea milkTea = null;
        milkTea = simpleFactory.getMilkTea(type);
        // 准备
        milkTea.prepare();
        // 放材料
        milkTea.material();
        // 加水
        milkTea.water();
        // 打包
        milkTea.packaged();
        return milkTea;
    }
}
```

​	通过简单工厂模式可以将创建对象统一放到一个地方，在需要使用对象的地方，通过工厂提供的获取接口动态的获取需要的对象。使用方与对象达到解耦效果，但这种方式并不符合开闭原则，如果需要新增不同类型的对象就需要修改工厂中获取对象的方法，进而影响原有的功能。

#### 	工厂方法模式

​	工厂方法模式定义了一个获取对象的接口，具体获取方式由子类决定。使得对象的创建被延迟到了子类进行。符合开闭原则。

```java
// 商店标准
public abstract class MilkTeaStore {

    public MilkTea orderMilkTea(String type) {
        MilkTea milkTea = null;

        // 获取奶茶
        milkTea = getMilkTea(type);
        // 准备
        milkTea.prepare();
        // 放材料
        milkTea.material();
        // 加水
        milkTea.water();
        // 打包
        milkTea.packaged();
        return milkTea;
    }

    abstract MilkTea getMilkTea(String type);
}

// 一号奶茶店
public class MilkTeaStoreOne extends MilkTeaStore {

    @Override
    MilkTea getMilkTea(String type) {
        MilkTea milkTea = null;
        if("rose".equals(type)) {// 玫瑰奶茶
            milkTea = new RoseMilkTea();
        }else if("taro".equals(type)) {// 香芋奶茶
            milkTea = new TaroMilkTea();
        }else if("strawberry".equals(type)) {// 草莓奶茶
            milkTea = new TaroMilkTea();
        }
        return milkTea;
    }
}

// 二号奶茶店
public class MilkTeaStoreTwo extends MilkTeaStore {

    @Override
    MilkTea getMilkTea(String type) {
        MilkTea milkTea = null;
        if("rose".equals(type)) {// 玫瑰奶茶
            milkTea = new RoseMilkTea();
        }else if("taro".equals(type)) {// 香芋奶茶
            milkTea = new TaroMilkTea();
        }else if("strawberry".equals(type)) {// 草莓奶茶
            milkTea = new TaroMilkTea();
        }
        return milkTea;
    }
}

// 奶茶
public abstract class MilkTea {

    protected String name;

    protected String material;

    // 准备
    void prepare() {
        System.out.println("准备制作:" + name);
    }

    // 加水
    void water(){
        System.out.println("加水......");
    }

    // 加原料
    void material(){
        System.out.println("添加原料:" + material);
    }

    // 包装
    void packaged() {
        System.out.println("包装.....");
    }

}


/**
 * 玫瑰奶茶
 */
public class RoseMilkTea extends MilkTea{

    public RoseMilkTea() {
        name = "玫瑰奶茶";
        material = "玫瑰花";
    }
}

/**
 * 草莓奶茶
 */
public class StrawberryMilkTea extends MilkTea{

    public StrawberryMilkTea() {
        name = "草莓奶茶";
        material = "草莓";
    }
}

/**
 * 香芋奶茶
 */
public class TaroMilkTea extends MilkTea{

    public TaroMilkTea() {
        name = "香芋奶茶";
        material = "香芋";
    }
}

// test
 public static void main(String[] args) {
       	MilkTeaStore store = new MilkTeaStoreOne();
        MilkTea milkTea = store.orderMilkTea("草莓");
        milkTea.prepare();
        milkTea.material();
        milkTea.water();
        milkTea.packaged();
    }

```

​	在上例中，工厂方法是个抽象接口，并且必须返回一个产品。并且将产品的创建与后续使用步骤分离，产品创建延迟到子类中进行（有点类似于Thread类，线程的一种实现方式是构造一个实现Runnable的类将它传入Thread。此时，线程执行任务与线程动作分离，使每个类行为更加专注）。对于工厂方法来说，相当于创建了一个框架，具体的创建让子类自行实现。

​	另外，工厂方法相比简单工厂创建对象更加有弹性，遵守了开闭原则，如果想新添加产品(奶茶种类)或者改变产品(奶茶店)的实现，直接添加新的具体产品类和具体工厂类即可，保证了不会改变原有实现。但每次修改都增加实现使得类越来越多，增加编辑器编译成本。

#### 抽象工厂模式

​	抽象工厂模式用于提供一个接口，用于创建相关或依赖对象的家族（产品族），而不需要明确指定具体类。在开闭原则上，从动态创建产品族的维度来说是遵守的，但从新增加产品的维度来说开闭原则还是被破坏了。

​	如下代码，虽然制作一份奶茶的基本步骤是准备、加水、加原料、包装，但如果奶茶店已在各省开了分店，一位出差的程序员到了出差省份后买到了的草莓奶茶，感觉味道不错，但回到原来工作省份后去了同一家奶茶店分店却被告知没这款口味奶茶。类似情况经常发生，销量会受到一定影响。所以，奶茶店主店必须保证各地的奶茶分店种类统一。(这里的所有种类就是产品族)。

​	而且对于各个地方由于原料差异，所做的草莓奶茶可能不同，用了不用地方的生产原料。

​	抽象产品：

```java
/**
 * 玫瑰奶茶
 */
public abstract class RoseMilkTea {
    protected String name;
    // 准备
    void prepare() {
        System.out.println("准备制作:" + name);
    }
    // 加水
    void water(){
        System.out.println("加水......");
    }

    // 加原料
    abstract void material();

    // 包装
    void packaged() {
        System.out.println("包装.....");
    }
}

/**
 * 草莓奶茶
 */
public abstract class StrawberryMilkTea extends MilkTea{
    protected String name;
    // 准备
    void prepare() {
        System.out.println("准备制作:" + name);
    }
    // 加水
    void water(){
        System.out.println("加水......");
    }
    
    // 加原料
    abstract void material();

    // 包装
    void packaged() {
        System.out.println("包装.....");
    }
}
```

​	具体产品：

```java
public class FuJianRoseMilkTea extends RoseMilkTea {
  	public FuJianRoseMilkTea() {
        name = "玫瑰奶茶福建分店";
    }
    @Override
    void material() {
        System.out.println("我所使用的玫瑰产自福建....");
    }
}

public class ShangHaiMilkTea extends RoseMilkTea {
 	public ShangHaiMilkTea() {
        name = "玫瑰奶茶上海分店";
    }
    @Override
    void material() {
        System.out.println("我所使用的玫瑰产自上海....");
    }
}

public class FuJianStrawberryMilkTea extends StrawberryMilkTea{
	public FuJianStrawberryMilkTea() {
        name = "草莓奶茶福建分店";
    }
    @Override
    void material() {
        System.out.println("我所使用的草莓产自福建....");
    }
}

public class ShangHaiStrawberryMilkTea extends StrawberryMilkTea{
	public ShangHaiStrawberryMilkTea() {
        name = "玫瑰奶茶上海分店";
    }
    @Override
    void material() {
        System.out.println("我所使用的草莓产自上海....");
    }
}

```

​	抽象工厂:

```java
public abstract class MilkTeaStore {

    private String place = "???";

    abstract RoseMilkTea getRoseMilkTea();
    abstract StrawberryMilkTea getStrawberryMilkTea();

    @Override
    public String toString() {
        return "奶茶店所在地：" + place;
    }
}
```

​	具体工厂:

```java
public class FuJianMilkTeaStore extends MilkTeaStore{

    public FuJianMilkTeaStore() {
        place = "福建";
    }

    @Override
    RoseMilkTea getRoseMilkTea() {
        return new FuJianRoseMilkTea();
    }

    @Override
    StrawberryMilkTea getStrawberryMilkTea() {
        return new FuJianStrawberryMilkTea();
    }
}

public class ShangHaiMilkTeaStore extends MilkTeaStore{

    public ShangHaiMilkTeaStore() {
        place = "上海";
    }

    @Override
    RoseMilkTea getRoseMilkTea() {
        return new ShangHaiMilkTea();
    }

    @Override
    StrawberryMilkTea getStrawberryMilkTea() {
        return new ShangHaiStrawberryMilkTea();
    }
}

```

​	Test

```java
// 顾客
public class Customer {

	// 奶茶店
    private MilkTeaStore milkTeaStore;

    public Customer(MilkTeaStore milkTeaStore) {
        this.milkTeaStore = milkTeaStore;
    }

	// 买奶茶
    void purchase() {
        StrawberryMilkTea strawberryMilkTea = milkTeaStore.getStrawberryMilkTea();
        System.out.println(strawberryMilkTea.name);
        strawberryMilkTea.material();
    }

}
```

​	如上测试代码，现在顾客不需要关注到底哪个城市的奶茶分店可以获取到草莓奶茶，只要是一个店并且能得到该产品就行，通过milkTeaStore.getStrawberryMilkTea();会返回所在区域的草莓奶茶。如果各个地方除了原料不同外对应其他步骤也不同，就可以覆盖同一奶茶接口的模板实现。

抽象工厂中的开闭原则
![image](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/2.png)

​	根据上图，对于增加产品族(各个地方的分店)来说，抽象工厂很好的支持了开闭原则，仅需要提供三个接口实现（玫瑰奶茶、草莓奶茶、奶茶店）就可以增加对应产品族（对应分店）。但如果有个需求（推出新品香芋奶茶/玫瑰奶茶下架）是想改产品族中的某个产品，这时就必须修改所有工厂的实现了，并且新增产品接口。所以，抽象工厂从某种程度上来说是支持开闭原则的，但从另一个程度来说并不支持。

#### 	三种工厂模式

- 简单工厂

  将创建对象的整体逻辑移动到一个工厂类中，所有产品都是平级的。如果新增加产品，则必须修改工厂，不符合开闭原则。

- 工厂方法

  符合开闭原则，新增产品不是在已有的工厂中修改，而是新增加工厂和产品。但这会导致每一次修改都引入非常多类，增加系统复杂性。

- 抽象工厂

  从某种程度上支持开闭原则，对于新增产品族，仅需添加对应实现工厂和产品实现。对于修改产品族，则需要将所有工厂都进行修改，并添加新产品接口。

- 关系

  - 抽象工厂、工厂方法

    抽象工厂中每一个接口方法都类似工厂方法，所以当抽象工厂只有一个接口时，抽象工厂类似于工厂方法。对于抽象工厂和工厂方法都能将创建对象移到子类，但抽象方法是将一组相关产品集合起来。工厂方法能够使调用方依赖接口而不需要依赖具体实现。

  - 工厂方法、简单工厂

    工厂方法的子类看起来和简单工厂类似，都是处理创建对象的逻辑。而工厂方法更多的是提供一个框架，具体的创建对象逻辑让子类自行实现，简单工厂则是直接将创建对象逻辑封装起来。所以，简单工厂并不具备工厂方法的可扩展性，如果要修改工厂，工厂方法不需要修改原有实现，而简单工厂需要修改原有实现以适应新需求。

  - 共性

    三种工厂模式都能够将创建对象与对象的使用分离，隐藏对象创建细节，增加了一定的灵活性，使系统更靠近单一职责设计原则。
