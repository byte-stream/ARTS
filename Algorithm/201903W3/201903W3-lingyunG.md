## Leetcode 

### 难度： 中度

### 描述：

> 如何判断一个链表有环


### 解法1：

```
class Solution {  
    public boolean hasCycle(ListNode head) {

        if (head == null || head.next == null) {
            return false;
        }
        ListNode slow = head;
        ListNode fast = head.next;
        while (slow != fast) {
            if (fast == null || fast.next == null) {
                return false;
            }
            slow = slow.next;
            fast = fast.next.next;
        }
        return true;
    }

    class ListNode {

        int val;
        ListNode next;

        ListNode(int x) {

            val = x;
            next = null;
        }
    }
}
```

时间复杂度：O(n)
空间复杂度：O（1）


