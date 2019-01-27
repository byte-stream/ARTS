# leetcode1：两数之和

题目描述：

给定一个整数数组 `nums` 和一个目标值 `target`，请你在该数组中找出和为目标值的那 **两个** 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。



**示例:**

```
给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
```

**题解-Java**

~~~java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        //暴力算法，两个循环遍历
        int index1=0;
        int index2=0;
        for(int i=0;i<nums.length;i++){
            for(int j=i+1;j<nums.length;j++){
                if(nums[i]+nums[j]==target){
                    index1=i;
                    index2=j;
                }
            }
        }
        int[] result={index1,index2};
        return result;
    }
}
~~~

执行用时: 61 ms

**题解-Python**

~~~python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        n = len(nums)
        index1 = 0
        index2 = 0
        for i in range(n):
            for j in range(i+1,n):
                if nums[i]+nums[j] == target:
                    index1 = i
                    index2 = j
                    break
        
        return [index1,index2]
~~~

执行用时: 4496 ms。

==Python编码效率高，但计算速度慢==



