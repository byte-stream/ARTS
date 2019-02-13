## LeetCode 2. 两数之和
  
#### 题目描述：  
> 给出两个 非空 的链表用来表示两个非负的整数。其中，它们各自的位数是按照 逆序 的方式存储的，并且它们的每个节点只能存储 一位 数字。
如果，我们将这两个数相加起来，则会返回一个新的链表来表示它们的和。
您可以假设除了数字 0 之外，这两个数都不会以 0 开头。  
 
#### 示例：  

    输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
    输出：7 -> 0 -> 8
    原因：342 + 465 = 807
  
分析思路：  
　　两个链表存储输入的数字，一个新链表输出结果。可以用两个链表从头开始，每两个数值相加，添加一个新节点到新链表后面。需要考虑两个数相加时产生的进位，以及最高位的进位。   
  
#### 我的代码：  

    /**
    * Definition for singly-linked list.
    * public class ListNode {
    *     int val;
    *     ListNode next;
    *     ListNode(int x) { val = x; }
    * }
    */
    class Solution {
        public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
            if (l1 == null && l2 == null) {
                return null;
            }
            if (l1 == null) {
                return l2;
            }
            if (l2 == null) {
                return l1;
            }
            ListNode result = new ListNode(0);
            ListNode temp = result;
            while (true) {
                if (l1 != null) {
                    temp.val = temp.val + l1.val;
                    l1 = l1.next;
                }
                if (l2 != null) {
                    temp.val = temp.val + l2.val;
                    l2 = l2.next;
                }
                temp.next = new ListNode(temp.val / 10);
                //进位判断
                temp.val = temp.val % 10;
                if (l1 == null && l2 == null) {
                    temp.next = (temp.next.val==0?null:temp.next);
                    break;
             }
                temp = temp.next;
            }
            return result;
        }
    }     
  
运行结果：  

  |    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-02   |通 过  |   54ms    | Java  |
  
#### 优化：  
    class Solution {
        public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
            int carryOver = 0;
            ListNode firstRetNode = new ListNode(0);
            ListNode tempL1 = l1 , tempL2 = l2, childRetNode,  parentRetNode = firstRetNode ;
            int value1,value2, remainder;
            while(true){
                if(tempL1 != null){
                    value1 = tempL1.val;
                    tempL1 = tempL1.next;
                }else{
                    value1 = 0;
                }
                if(tempL2 != null){
                    value2 = tempL2.val;
                    tempL2 = tempL2.next;
                }else{
                    value2 = 0;
                }
                remainder =  (carryOver + value1 + value2)%10;
                carryOver = (carryOver + value1 + value2)/10;
                childRetNode = new ListNode(remainder);
                parentRetNode.next = childRetNode;
                parentRetNode = childRetNode;
            
                if(tempL1 == null && tempL2 == null){
                    break;
                }
            }
            if(carryOver!=0){
                parentRetNode.next = new ListNode(carryOver);
            }
            return firstRetNode.next;
        }
    }

    
  
优化后执行速度：  
    
|    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-02   | 通 过 |   22ms     | Java  |