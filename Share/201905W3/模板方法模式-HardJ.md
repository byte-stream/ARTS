### 模板方法模式：

#### 	定义：

​	在一个方法中定义一个算法的骨架，而将一些步骤延迟到子类中。模板方法使得子类可以在不改变算法结构的情况下，重新定义算法的某些步骤。

​	这个模式创建了一个算法的模板。其中模板相当于一个方法，这个方法将算法定义成一系列的步骤，其中的任何步骤都可以使抽象的，由子类负责实现。这可以确保算法的结构不变，同时由子类提供部分实现。![](<https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/2wewq.png>)

#### 使用模板方法排序：

```java
public static void sort(Object[] a) {
    // 两个入口最终都用到了compareTo()方法
    if (LegacyMergeSort.userRequested)
		// 旧的排序算法
        legacyMergeSort(a);
    else
        ComparableTimSort.sort(a, 0, a.length, null, 0, 0);
}

private static void legacyMergeSort(Object[] a) {
    Object[] aux = a.clone();
    mergeSort(aux, a, 0, a.length, 0);
}

// 类似于一个模板方法
private static void mergeSort(Object[] src, Object[] dest, int low, int high, int off) {
    int length = high - low;
    // 是否使用插入排序
    if (length < INSERTIONSORT_THRESHOLD) {
        for (int i=low; i<high; i++)
            for (int j=i; j>low &&
                 // 需要实现compareTo方法，使模板方法可以调用方法实现
                 ((Comparable) dest[j-1]).compareTo(dest[j])>0; j--)
                // 一个具体的方法，已经在数组中定义 
                swap(dest, j, j-1);
        return;
    }
    // 数量大于INSERTIONSORT_THRESHOLD使用归并排序
    int destLow  = low;
    int destHigh = high;
    low  += off;
    high += off;
    int mid = (low + high) >>> 1;
    mergeSort(dest, src, low, mid, -off);
    mergeSort(dest, src, mid, high, -off);
    if (((Comparable)src[mid-1]).compareTo(src[mid]) <= 0) {
        System.arraycopy(src, low, dest, destLow, length);
        return;
    }
    for(int i = destLow, p = low, q = mid; i < destHigh; i++) {
        if (q >= high || p < mid && ((Comparable)src[p]).compareTo(src[q])<=0)
            dest[i] = src[p++];
        else
            dest[i] = src[q++];
    }
}
```

#### compareTo()：

​	compareTo这个方法将比较两个对象，然后将返回比较结果(大于、小于、等于)。sort()只要知道这两个对象的大小，就可以进行排序。

​	比较学生身高：

```java
public class Student implements Comparable{

    private int height;

    private int age;

    private String name;

    public Student(int height, int age, String name) {
        this.height = height;
        this.age = age;
        this.name = name;
    }

    @Override
    public String toString() {
        return "Student{" +
                "height=" + height +
                ", age=" + age +
                '}';
    }

    @Override
    public int compareTo(Object o) {
        Student temp = (Student) o;
        int x = this.height;
        int y = temp.height;
        return (x < y) ? -1 : ((x == y) ? 0 : 1);
    }
}
```

​	测试:

```java
 public static void main(String[] args) {
     	// 初始化一个学生数组
        Student[] students = new Student[]{
          new Student(178, 20, "小明"),
          new Student(176, 18, "小王")
        };
        System.out.println("排序前：");
        System.out.println(Arrays.toString(students));
     	// 调用模板方法,sort控制算法、定义算法框架，sort依赖一个Comparable类提供compareTo方法实现。
        Arrays.sort(students);
        System.out.println("排序后：");
        System.out.println(Arrays.toString(students));
    }
```

#### 模板方法模式与策略模式：

​	策略模式使用了对象组合，而模板方法模式在排序应用中使用的也是对象组合。但是，在策略模式中，所组合的类实现了整个算法。数组所实现的排序算法并不完整，它需要一个类填补compareTo()方法的实现，所以排序更像是模板方法。模板方法中子类决定如果实现算法中的某些步骤，策略模式中封装可互换的行为，然后通过委托决定要使用哪个行为。

#### 总结：

 	1. 模板方法定义了算法的步骤，把某些步骤的实现延迟到了子类。
 	2. 模板方法模式为我们提供了一个代码复用的重要技巧。
 	3. 模板方法的抽象类可以定义具体方法、抽象方法和钩子方法(子类可以选择实现或不实现)。
 	4. 为了防止子类改变模板方法中的算法，可以将模板方法声明为final。
 	5. 策略模式和模板方法都封装了算法，一个使用组合，一个使用继承。

​	