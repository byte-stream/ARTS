## Leetcode 

> Leetcode 


### 解法1：

```
class Solution {
    public ListNode swapPairs(ListNode head) {

        if (head == null || head.next == null) return head;
        ListNode dummy = new ListNode(-1);
        dummy.next = head;
        ListNode odd = head, even = head.next, tmp = dummy;

        while (true) {
            ListNode sav = even.next;
            //twist two nodes
            tmp.next = even;
            even.next = odd;
            odd.next = sav;
            //set pointer in right position
            if (odd.next == null || even.next.next.next == null) break;
            odd = odd.next;
            even = even.next.next.next;
            tmp = tmp.next.next;
        }

        return dummy.next;
    }

    public class ListNode {

        int val;
        ListNode next;

        ListNode(int x) {

            val = x;
        }
    }
}
```




