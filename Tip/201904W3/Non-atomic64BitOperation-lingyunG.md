The Java Memory Model requires fetch and store operations to be atomic,but for nonvolatile long and double 
variables, the JVM is permitted to treat a 64‐bit read or write as two separate 32‐bit operations.

因为在并发场景中使用long 和 double 型变量时候要把它声明为volatile类型。