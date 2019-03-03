> 最近看了些链表相关的理论，但实际操作时，还是会卡壳，这里记录自己一顿操作后对链表题的理解（一些技巧？）

## 理解指针（引用）

指针，就是C语言中的指针，像`Java/Python`没有指针概念的语言可以用引用代替，实际上可以大致理解成存储对象的内存地址。

对于指针（引用）的理解，引用《数据结构与算法之美》中的一句话：

**将某个变量赋值给指针，实际上就是将这个变量的地址赋值给指针，或者反过来说，指针中存储了这个变量的内存地址，指向了这个变量，通过指针就可以找到这个变量。**

这里举两个例子，像删除节点其实就是改变上一个节点指向的内存地址，改为下下个即可。

```python
node.next = node.next.next
```

不过在新增节点中，需要注意插入操作的先后顺序，如果是像这样操作顺序，会导致**指针丢失**。

```python
node.next = new_node
new_node.next = node.next
```

第一个步时，已将`node`已经指向`new_node`，导致第二步`new_node`又指向`node`，正确操作如下，先定义新节点的指向，再改变旧节点。

```python
new_node.next = node.next
node.next = new_node
```

## 边缘情况

软件开发中，代码在边缘情况下，最容易导致BUG，链表中也不例外。要想链表代码能通过OJ，各种边缘情况是必须要考虑到了。这里列了最参见的4中边缘情况。

- 1. 如果链表为空时，代码是否能正常工作？ 如果链表只包含一个
- 2. 如果链表只包含一个结点时，代码是否能正常工作？
- 3. 如果链表只包含两个结点时，代码是否能正常工作？
- 4. 代码逻辑在处理头结点和尾结点的时候，是否能正常工作？



## 面试中参见的单链表题

最后列了5道面试经常遇到的单链表题

```python
class ListNode(object):
    def __init__(self, x):
      self.val = x
      self.next = None
```

> TIP: 有时候不太理解指针变化可以使用画图举例法，将指针变化通过画图更直观的呈现出来

### 合并两个有序链表

```python
class Solution(object):
    def merge_wwo_lists(self, l1, l2):
        cur = ans = ListNode(0)
        while l1 and l2:
            if l1.val > l2.val:
                cur.next = l2
                l2 = l2.next
            else:
                cur.next = l1
                l1 = l1.next
            cur = cur.next
        cur.next = l1 or l2
        return ans.next
```

### 环形链表

```python
class Solution:
    def has_cycle(self, head: ListNode) -> bool:
        """ 如果是环形链表，一快一慢的双指针最终会相遇 """
        if not head or not head.next:  # 防止head为空或只为一个值
            return False
        fast = head.next  # 快指针
        slow = head       # 慢指针
        while fast != slow:
            if not fast or not fast.next:
                return False
            fast = fast.next.next
            slow = slow.next
        return True
```

### 单链表反转

```python
class Solution(object):
    def reverse_list(self, head):
        cur, ans = head, None
        while cur:
            temp = cur.next
            cur.next = ans
            ans = cur
            cur = temp
            # ans, ans.next, cur = cur, ans, cur.next
        return ans
```

### 链表的中间结点

```python
class Solution:
    def middle_node(self, head):
        fast = slow = head
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
        return slow
```

### 删除链表倒数第 n 个结点

```python
class Solution:
    def remove_nth_from_end(self, head: ListNode, n: int) -> ListNode:
        node = ListNode(0)
        node.next = head
        left = right  = node
        for _ in range(n+1):
            right = right.next
        while right:
            left, right = left.next, right.next
        left.next = left.next.next
        return node.next
```

