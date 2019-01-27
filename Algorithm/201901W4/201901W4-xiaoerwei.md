### Leetcode: 01.Two Sum

题目难度：简单

题目描述：

给定一个整数容器，两个数相加等于特定值，输出这两个数的索引
**说明：**

假定只有一个正确答案，不能使用容器中同一个元素两次。

**示例：**

Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].





***





**解答：**

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> backup(nums);
        sort(nums.begin(), nums.end());
        vector<int>::iterator i1 = nums.begin(), i2 = nums.end()-1;
        while ((*i1 + *i2)!= target)
        {
            while ((*i1 + *i2) < target) i1++;
            while ((*i1 + *i2) > target) i2--;
        }
        
        vector<int> res;
        for (unsigned int i = 0; i < nums.size(); i++)
        {
            if (backup[i]==*i1 || backup[i] == *i2)
                res.push_back(i);
        }
        return res;
    }
};
```



