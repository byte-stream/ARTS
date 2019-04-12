#### leetcode
#### 15. 三数之和

> 给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？找出所有满足条件且不重复的三元组。

> 注意：答案中不可以包含重复的三元组。

例如, 给定数组 nums = [-1, 0, 1, 2, -1, -4]，

满足要求的三元组集合为：
```
[
  [-1, 0, 1],
  [-1, -1, 2]
]
```
java版
```
	class Solution {
  public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if(nums.length < 3) {
            return result;
        }
        Arrays.sort(nums);

        for (int i = 0; i < nums.length - 2; i++){
            if(i == 0 || (i > 0 && nums[i] != nums[i - 1])) { // 过滤重复数据
                int l = i + 1, r = nums.length - 1, sum = 0 - nums[i];
                while (l < r){
                    if(sum == nums[l] + nums[r]) {
                        List<Integer> temp = new ArrayList<>();
                        temp.add(nums[i]);
                        temp.add(nums[l]);
                        temp.add(nums[r]);
                        result.add(temp);
                        while (l < r && nums[l] == nums[l + 1]) { // 过滤重复数据
                            l++;
                        }
                        while (l < r && nums[r] == nums[r - 1]) { // 过滤重复数据
                            r--;
                        }
                        l++;
                        r--;
                    }else if(sum > nums[l] + nums[r]) {
                        while (l < r && nums[l] == nums[l + 1]) { // 过滤重复数据
                            l++;
                        }
                        l++;
                    }else {
                        while (l < r && nums[r] == nums[r - 1]) { // 过滤重复数据
                            r--;
                        }
                        r--;
                    }
                }
            }
        }
        return result;
    }
}
```