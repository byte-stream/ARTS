## Leetcode 

### 难度： 中度

### 描述：

> 给定两个非负整数，将它们的数字逆序排列并存放进每个list里面，将这两个数相加，并把它们的结果逆序排列


### 示例：
    Input: (2->4->3) + (5->6->4)
	Output: 7->0->8
	Explanation: 342 + 465 = 807

### 解法1：

```
class Solution {  
   public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummyHead = new ListNode(0);
        ListNode p = l1, q = l2, curr = dummyHead;
        int carry = 0;
        while (p != null || q != null) {
        int x = (p != null) ? p.val : 0;
        int y = (q != null) ? q.val : 0;
        int sum = carry + x + y;
        carry = sum / 10;
        curr.next = new ListNode(sum % 10);
        curr = curr.next;
        if (p != null) p = p.next;
        if (q != null) q = q.next;
    }
    if (carry > 0) {
        curr.next = new ListNode(carry);
    }
    return dummyHead.next;
    }
}
```

时间复杂度：O(max(m,n))
空间复杂度：O（max(m,n))


