## 命令模式

> 将请求封装成对象，以便使用不同的请求、队列或者日志来参数化其他对象。命令模式也支持可撤销的操作。

​	在大学里，辅导员经常会发一些公告或文件在班长群里，然后再由班长转发或执行，很多通知班长仅需要在第一时间转发到班群即可。

![](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/sadas.png)

​	如上图，班长工作大部分是接收辅导员的通知再将通知转给同学，而且大多数情况下不需要关心文件或通知内容(有时候还是需要关心一下的)，只需要将通知从班委群转到班级群即可。

​	对应的命令模式：

![](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/edede.png)

​	首先客户端需要创建一个命令对象，并将命令对象存储在调用者中，一个命令加载到调用者后，该命令可以被使用后丢弃(如：班长通知五一放假注意安全)，也可以重复使用(如：班长发布奖学金公示，需要重复发送确认)。

**定义：**一个命令对象通过在特定接收者上绑定一组动作来封装一个请求。命令对象将动作和接收者包装进了对象中，这个对象只暴露一个execute()方法，当方法被调用时，接收者会执行命令封装的动作。在使用者看来，并不需要接收者进行了哪些动作，只知道调用一下execute()方法，目的就可以达到。

```java
/**
 * 通知
 */
public interface Command {

    void execute();
}

```
先定义一个命令接口，所有命令实现此接口。
```java
/**
 * 一群可爱的学生
 */
public class Students {

    /**
     * 开班会
     */
    public void meeting(){
        System.out.println("教学楼四楼开班会....");
    }

    /**
     * 参加讲座
     */
    public void attendLecture(){
        System.out.println("讲堂群参加讲座....");
    }

    /**
     * 提交材料
     */
    public void submitMaterial(){
        System.out.println("提交材料....");
    }
    //............

}
```
这里简单的定义一个学生群体，作为命令接收者。
```java
/**
 * 开会通知
 */
public class MeetCommand implements Command{

    private Students students;

    public MeetCommand(Students students) {
        this.students = students;
    }

    @Override
    public void execute() {
        students.meeting();
    }
}

```
如果想要实现这个命令就需要将接收者传入命令，这里学生群体还可以扩展修改为其他班级学生，因为一个辅导员所下发通知是相同的。
```java
/**
 * 讲座通知
 */
public class LectureCommand implements Command{

    private Students students;

    public LectureCommand(Students students) {
        this.students = students;
    }

    @Override
    public void execute() {
        students.attendLecture();
    }
}

```

```java
/**
 * 提交材料通知
 */
public class SubmitMaterialCommand implements Command{

    private Students students;

    public SubmitMaterialCommand(Students students) {
        this.students = students;
    }

    @Override
    public void execute() {
        students.submitMaterial();
    }
}
```

```java
/**
 * 班长(调用者)
 */
public class Monitor {

    Command command;

    public Monitor() {}

    public void setCommand(Command command) {
        this.command = command;
    }

    // 发布通知
    public void releasingNotice(){
        command.execute();
    }
}
```

```java
/**
 * 辅导员(客户)
 */
public class Counsellor {

    public static void main(String[] args) {
        // 一班
        Monitor monitorOne = new Monitor();
        Students studentsOne = new Students();
        LectureCommand lectureCommandOne = new LectureCommand(studentsOne);
        // 二班
        Monitor monitorTwo = new Monitor();
        Students studentsTwo = new Students();
        LectureCommand lectureCommandTwo = new LectureCommand(studentsTwo);

        MeetCommand meetCommandTwo = new MeetCommand(studentsTwo);

        // 一班听讲座
        monitorOne.setCommand(lectureCommandOne);
        monitorOne.releasingNotice();

        // 二班听讲座，听完留下来看班会
        monitorTwo.setCommand(lectureCommandTwo);
        monitorTwo.releasingNotice();
        monitorTwo.setCommand(meetCommandTwo);
        monitorTwo.releasingNotice();
    }

}
```

如上，客户端创建调用者和接收者并把命令传递给调用者，在调用者看来每次得到命令后只需要execute一下就行了。后面无论什么通知，需要实现Command，就可以是一个正常通知。命令对象只提供execute方法，当方法被调用时，接收者就可以进行行为动作，达到请求目的。通过命令对象调用者和接收者之前可以达到**间接解耦**。

辅导员一组通知（命令）对象，然后将其发布到班长群，每一个通知（命令）对象都封装了一次具体通知。班长则接收一组通知，当辅导员通知发布后调用发布通知方法，间接调用execute。

![](https://artsmd.oss-cn-hangzhou.aliyuncs.com/arts/wqewe.png)

上述的实现，命令的执行需要依赖于接收者，但有时候命令对象会实现更多逻辑，甚至直接去完成一个请求。但这样接收者和调用者的**解耦程度**不如之前，而且接收者也不能动态变更，相当于限制了很多灵活性。

##### 命令模式其他用途

1. 队列：

   ​	在Java线程池中，线程的调度基于生产者消费者模式，所以往往在内部会实现一个阻塞队列。可以在一端添加任务，另一端消费任务。同时任务和工作队列之前是解耦的，无论传入什么任务给线程池，工作队列只负责取出任务，执行execute()方法，下一个.........。

2. 保留日志：

   ​	Redis是现在常用的缓存数据库，读写快的一个原因是数据不走磁盘，都是基于内存读写。虽然都是基于内存，但同样提供持久化方案。其中一种叫AOF，相对于RDB来说它是以执行命令逐条追加的方式来持久化的。所以类似Redis，在开发过程中，命令模式也可用于逐条持久化，因为很多应用在进行数据修改后不是立即持久化到磁盘中，而是先放入内存，等待时机写入磁盘，所以数据变更没发快速存储。如果在使用命令模式时，执行完请求将其持久化到磁盘，那么在将来某一时刻即使宕机，只要从磁盘中取出命令逐条执行就行(Redis的AOF也是这样恢复的)。

##### 总结

- 命令模式将发出请求对象、与执行请求对象通过命令进行解耦
- 调用者通过命令对象的execute便可以通知接收者
- 调用者的命令对象可以动态变更
- 接收者也可以同时接收多个命令然后一起调用
- 调用者可以直接实现请求而不转发给接收者