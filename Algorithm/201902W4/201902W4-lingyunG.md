## Leetcode 

### 难度： 简单

### 描述：

> 给定一个数组和目标值，要求找出数组中两个相加之后等于目标值的两个数，并将它们的在数组中的索引返回。假定答案只有一个。


### 示例：

### 解法1：

```
class Solution {  
    public int[] twoSum(int[] nums, int target) {
        for(int i =0; i<nums.length;i++){
            for(int j=i+1;j<nums.length;j++) {
                if(nums[i]+nums[j]==targer) {
                    return new int[]{i,j};
                }
            }
        }
    }
}
```

时间复杂度：O(n^2)


