## LeetCode 1. 两数之和
  
#### 题目描述：  
> 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。  
>你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。  
 
#### 示例：  

    给定 nums = [2, 7, 11, 15], target = 9

    因为 nums[0] + nums[1] = 2 + 7 = 9 所以返回 [0, 1]  
  
分析思路：  
　　数组双指针遍历，确定第一个值然后寻找复符合题意的另外一个值。   
  
#### 我的代码：  

    class Solution {
        public int[] twoSum(int[] nums, int target) {
            if(nums != null || nums.length < 2) {
                return null;
            }
            int []result = new int [2];
            for(int i = 0; i < nums.length; i++) {
                for(int j = nums.length - 1; j > i; j--) {
                    if(target == nums[i] + nums[j]) {
                        result[0] = i;
                        result[1] = j;
                        return result；
                    }
                }
            }
            return null;
        }  
    }  
  
运行结果：  

  |    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-01-21   |通 过  |   84ms    | Java  |
  
#### 优化：  
    class Solution {
        public int[] twoSum(int[] nums, int target) {
            if (nums != null) {  
                // 因为Hashmap仅提供通过key获得value,故  
                // HashMap value放置与nums[index]匹配的数值,key放置index；，故  
                // 在下面循环时每一次查询map中的value是否有相等的值，有即相互匹配  
                // 其思想在于用index的value表示数组中的该数据，map中的key与之匹配，并在数组中寻找匹配值  
                HashMap<Integer, Integer> num_map = new HashMap<>();  
                for (int i = 0; i < nums.length; i++) {  
                    if (num_map.containsKey(nums[i])) {  
                        int index = num_map.get(nums[i]);  
                        int[] result = { index, i };  
                        return result;  
                    } else {  
                        num_map.put(target - nums[i], i);  
                    }  
                }  
            }  
            return null;
        }
    }  
    
  
优化后执行速度：  
    
|    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-01-21   | 通 过 |   8ms     | Java  |