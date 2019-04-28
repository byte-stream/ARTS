#  算法
# leetcode 
## desc
> 92.Reverse Linked List II 
Reverse a linked list from position m to n. Do it in one-pass.

EXAMPLE:
```
Input: 1->2->3->4->5->NULL, m = 2, n = 4
Output: 1->4->3->2->5->NULL
```
## Solution:
```
class Solution {

    private boolean stop;
    private ListNode left;

    public void recurseAndReverse(ListNode right, int m, int n) {

        if (n == 1) {
            return;
        }


        right = right.next;

       
        if (m > 1) {
            this.left = this.left.next;
        }

 
        this.recurseAndReverse(right, m - 1, n - 1);

        if (this.left == right || right.next == this.left) {
            this.stop = true;            
        }

     
        if (!this.stop) {
            int t = this.left.val;
            this.left.val = right.val;
            right.val = t;

            this.left = this.left.next;
        }
    }

    public ListNode reverseBetween(ListNode head, int m, int n) {
        this.left = head;
        this.stop = false;
        this.recurseAndReverse(head, m, n);
        return head;
    }
}
```
