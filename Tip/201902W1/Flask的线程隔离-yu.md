# 20190203-Flask的线程隔离

多线程都会存在线程安全的问题，python 没有办法手动控制每个线程的执行顺序，所以如果多个线程同时修改了一个数据，数据的状态就没有办法确认：
```python
import time
import threading

class A:
    data = 1

obj = A()
obj.data = 2
# 单线程
def worker():
    print("before")
    obj.data = 1
    time.sleep(1)
    print("after")

t = threading.Thread(target=worker)
print("main thread")
t.start()
time.sleep(2)
print(obj.data)
```
倒数第二行等待的时间不一样，最后 obj.data 的数据也会完全不一样。需要线程隔离的方式来保证数据安全。

Flask 中使用字典封装了一个 Local 类来隔离线程，线程内部修改数据不会影响主线程的数据状态：
```python
obj = Local()
obj.data = 2
```
结果无论如何，obj.data 都是主线程的 2。

Flask 还通过 LocalStack 类进一步封装了 Local 通过栈来进一步限制数据处理的灵活性，充分利用了栈先进后出的特性。