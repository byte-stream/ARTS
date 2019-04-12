#### Spring事务

前不久遇到一个问题，查询数据出现NullPointerException，跟踪代码后发现根据id从数据库查询出来**数据为空**，
之前的代码没有对操作对象进行非空判断，而在这段代码之前的一段代码中有对该**数据入库**，两段代码**id**一致。

此时决定不可思议，因为数据库(mysql)默认隔离级别为可重复读，而按照可重复读的定义，一个事务启动后，能看到所有
提交的结果，其他事务的更新对它不可见。但由于在这个隔离级别下，Mysql利用多版本实现当前事务的一致性视图，在这
个视图下，当前事务自己更新的数据对于自己来说还是可见。

##### Mysql四种隔离级别

. | 脏读|不可重复读|幻读
---|--- |--- |---
read uncommitted:读未提交 | × | × | ×
read committed：读已提交(oracle) | √ | × | ×
repeatable read：可重复读(mysql) | √ | √ | × 
serializable：串行化  | √ | √ | √

后来经过调试，发现第二个取操作重启启动了一个线程池，在线程池中进行取操作，也就是说第二个操作重新启动了一个线程。由于数据库连接池使用了线程封闭技术(不用处理共享数据带来的线程安全性问题，因为连接并没有被共享)，JDBC规范里没有要求从数据库连接池中取出的Connection，必须是线程安全的，通过线程封闭技术保证Connection归还给连接池之前这个连接不会被分配给其他线程。所以，可以明确一点，**两次操作是在两个数据库连接下进行的**。

可以得出结论，在第一段代码执行的过程中调用了第二段代码。而此时，第一段代码由于后续还有未完成的操作，所以事务没有立即提交。在可重复读级别下，另外一个事务对于第一段代码中的**数据入库**是不可见的。所以当第二段代码拿着还有入库的id进行查询时，只能出现NullPointerException。

```

class A {

       @Autowired
       private B b;
       
    @Transactional
    public void code1() {
        // 调用code3新增数据1
        b.code3();


        code2();
        // ....后续还有一堆操作
    }


    public void code2() {
        ExecutorService exec = Executors.newFixedThreadPool(1);
        Callable<String> call = () -> {
            // 查询数据1
            return "1";
        };
        Future<String> future = exec.submit(call);

    }

   }
    class B {
        // 新增数据1
        public void code3(){

        }   
    }
```

#### 解决方案

​	由于使用Spring框架，Spring框架通过AOP对方法进行前后事务处理。而在Spring中定义了7种传播行为，其中一种是**PROPAGATION_REQUIRED_NEW**(表示当前方法必须运行在它自己的事务中。一个新的事务将被启动。如果存在当前事务，在该方法执行期间，当前事务会被挂起)。

​	发现这种传播行为正好能解决问题，在新增数据1时，将当前执行事务挂起，重新启动一个事务，执行完并提交。这样由于其他事务都处于重复读隔离级别下，所以对其他事务都可见，从而解决问题。

​	由于Spring在后面版本中提供了注解，所以加个注解就能解决上述问题。

```
@Transactional(rollbackFor = Exception.class, propagation = Propagation.REQUIRES_NEW)
```



修改后的代码

```

   class A {

       @Autowired
       private B b;

    @Transactional
    public void code1() {
        // 调用code3新增数据1
        b.code3();


        code2();
        // ....后续还有一堆操作
    }


    public void code2() {
        ExecutorService exec = Executors.newFixedThreadPool(1);
        Callable<String> call = () -> {
            // 查询数据1
            return "1";
        };
        Future<String> future = exec.submit(call);

    }

   }
   
    class B {
       
        // 新增数据1
        @Transactional(rollbackFor = Exception.class, propagation = Propagation.REQUIRES_NEW)
        public void code3(){

        }
    }
```

