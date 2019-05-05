## Leetcode 

> Leetcode 876


### 解法1：

```
class Solution {
        public ListNode middleNode(ListNode head) {
            ListNode slow = head,fast = head;
            while(fast !=null && fast.next !=null) {
                slow = slow.next;
                fast = fast.next.next;
            }
            return slow;
        }
    }

    public class ListNode {
        int val;
        ListNode next;
        ListNode(int x) { val = x; }
    }
```




