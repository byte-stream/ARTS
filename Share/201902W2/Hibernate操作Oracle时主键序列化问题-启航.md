## Hibernate操作Oracle时主键序列化问题

Oracle数据库建表，主键自增，保存数据的时候，报could not get next sequence value 异常。

**解决方法**：

```
CREATE SEQUENCE SEQ_BT_PASSWORD
minvalue 1
maxvalue 9999999999999999999999999999
start with 1
increment by 1
cache 20;
```

**排查异常步骤**：

在数据库中运行如下语句，如果有value值，则说明sequence 没问题

` select SEQ_BT_PASSWORD.nextval from dual` 

但是我现在遇到了另一个问题，步长设定为1 的情况下， 他自增是2 

尝试过执行如下语句

` drop SEQUENCE SEQ_BT_PASSWORD`

并重新建立SEQUENCE

但是问题还是没解决。。。知道的麻烦指点一下，谢谢

