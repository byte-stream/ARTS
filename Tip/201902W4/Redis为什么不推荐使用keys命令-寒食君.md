Redis是单线程的，当使用`keys`命令来获取key，如果数据庞大的话，redis可能会被锁定几秒，对于生产环境来说，这可能会导致灾难。

那如果我需要根据一定的条件来批量查询key，应该怎么做？

你可以自己将key根据分类存在不同的set中，建立索引。这样做貌似还不错，但是有两个问题：

1. 如果key的格式并不规律，这可能导致难以分类，或者分类太多，造成很大的冗余现象。
2. 将这些key存在set中，浪费了宝贵的内存空间。

显然这不是一种“干净”的做法，在2.8版本以后，redis实现了“scan”命令，利用游标来分批查询与返回结果，这样避免了系统长时间阻塞的问题。

scan 命令完整的写法是：


```
SCAN 0 cursor MATCH pattern COUNT count
```

其中cursor是游标，pattern是匹配key的正则表达式，count是一次查询的数量。

![ ](http://upload-images.jianshu.io/upload_images/5889935-d6fedd3273d42f68?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**注意**：count是一次查询的数量，不是一次返回的数量，如果设置的很小，可能会导致查询次数过多，响应时间变慢。

查询以cursor为0开始，也以返回的cursor为0结束。

Shell示例：


![image](http://upload-images.jianshu.io/upload_images/5889935-f7f658b22a86301d?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Java示例：

```
/**
   * 返回匹配的所有key
   */
  public List<String> getKeys(String pattern){
    List<String> keys = new ArrayList<String>();
    try {
      JedisPool pool = jedisPoolWrapper.getJedisPool();
      if (pool != null) {
        try (Jedis jedis = pool.getResource()) {
          ScanParams scanParams = new ScanParams().count(10).match(pattern);
          String cur = SCAN_POINTER_START;
          do {
            ScanResult<String> scanResult = jedis.scan(cur, scanParams);
            cur = scanResult.getStringCursor();
            keys.addAll(scanResult.getResult());
          } while (!cur.equals(SCAN_POINTER_START));
        }
      }
    } catch (Exception e) {
      logger.error("Fail to init counter", e);
    }
    return keys;
  }
```