## LeetCode 3. 无重复字符的最长子串
  
#### 题目描述：  
> 给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。  
 
#### 示例：  

    输入: "abcabcbb"
    输出: 3 
    解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
  
分析思路：  
　　双指针i和j，i为字符串的起始下标，j为字符串的结束下标。通过两个指针，扩大子字符串的长度并通过对j的下一位字符进行比较，直至字符串被遍历完全。   
  
#### 我的代码：  

    class Solution {
    public int lengthOfLongestSubstring(String s) {
        if (null == s)
        return 0;
        int max = 0;
        for (int i = 0, j = i; i < s.length() && j < s.length(); ) {

            int sum = j - i + 1;
            for (j += 1; j < s.length(); ++j) {
                int index = s.substring(i, j).indexOf(s.substring(j, j + 1));

                if (index >= 0) {
                    i += index + 1;
                    break;
                }

                sum++;
            }

            max = Math.max(max, sum);
        }
        return max;
    }
}     
  
运行结果：  

  |    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-12   |通 过  |   54ms    | Java  |
  
#### 优化：  
    public class Solution {
	    public int lengthOfLongestSubstring(String s)     {
		    int ans = 0;
		    int[] vis = new int[257];
		    int len = s.length();
		    int left = -1;
		    Arrays.fill(vis,-1);
		    for(int i = 0; i < len; i++) {
			    if(vis[s.charAt(i)] > left) {
				    left = vis[s.charAt(i)];
			    }
			    ans = Math.max(ans,i - left);
                vis[s.charAt(i)] = i;
		    }
		
		    return ans;
        }
    }

    
  
优化后执行速度：  
    
|    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-12   | 通 过 |   18ms     | Java  |