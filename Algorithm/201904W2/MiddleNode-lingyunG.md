## Leetcode 

### 难度： 简单

### 描述： 返回一个list的中间节点，如果有两个中间结点，取第二个

> Leetcode 876


### 解法1：

```
class Solution {  
    public class ListNode {
      int val;
      ListNode next;
      ListNode(int x) { val = x; }
    }

    public ListNode middleNode(ListNode head) {
        ListNode slow = head,fast = head;
        while(fast !=null && fast.next !=null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }
}
```

时间复杂度：O(N)
空间复杂度：O（1）


