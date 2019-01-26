# 算法练习

### 题目：输入一个链表，输出该链表中倒数第 k 个结点。

> 思路：定义一快一慢两个指针，快指针走 K 步，然后慢指针开始走，快指针到尾时，慢指针就找到了倒数第 K 个切点。

```java
public ListNode FindKthToTail(ListNode head, int k) {
    if(head == null || k <= 0) {
        return null;
    }
    ListNode fast = head;
    ListNode slow = head;
    while(k-- > 1) {
        if(fast.next != null) {
            fast = fast.next;
        }
        else null;
    }
    while(fast.next != null) {
        fast = fast.next;
        slow = slow.next;
    }
    return slow;
}
```
