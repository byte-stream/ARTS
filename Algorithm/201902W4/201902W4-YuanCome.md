## LeetCode 5. 最长回文子串
  
#### 题目描述：  
> 给定一个字符串 `s`，找到 `s` 中最长的回文子串。你可以假设 `s` 的最大长度为 1000。  
 
#### 示例：  

    输入: "babad"
    输出: "bab"
    注意: "aba" 也是一个有效答案。
  
分析思路：  
　　回文子串，考虑中点两侧镜像对称，有奇数和偶数两种情况。则一共有2n-1个中心点，n为字符串长度。   
  
#### 我的代码：  

    class Solution {
        public String longestPalindrome(String s) {
            if (s == null || s.length() < 1) return "";
            int end = 0;
            int start =0;
            for(int i = 0; i < s.length(); i++) {
                //奇数情况下
                int length1 = findPalindromeLongth(s, i, i);
                //偶数情况下
                int length2 = findPalindromeLongth(s, i, i+1);
                int length = Math.max(length1, length2);
                if(length > (end - start)) {
                    //获取子字符串的起始下标和结束下标，i为中点下标
                    start = i - (length-1)/2;
                    end = i + length/2;
                }
            }
            //注意substring方法第二个参数所指的下标不包含在子字符串内。
            return s.substring(start, end+1);

        }
        private int findPalindromeLongth(String s, int left, int right) {
            int L = left;
            int R = right;
            while(L >= 0 && R < s.length() && s.charAt(L) == s.charAt(R)) {
                L--;
                R++;
            }
            return R - L -1;
        }
    }
  
运行结果：  

  |    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-12   |通 过  |   13ms    | Java  |
  
#### 优化：  
    class Solution {
    public String longestPalindrome(String s) {
        int n = s.length();

        int [] range = new int[2];
        for(int i = 0;i<n;i++){
            i = helper(s, range, i);
        }

        return s.substring(range[0],range[1]);
    }

    public int helper(String s,int [] range, int i){
        int lo = i; int hi=i;
        while (hi<s.length()-1 && s.charAt(hi) == s.charAt(hi+1)){
            hi++;
        }

        int ret = hi;
        while (lo>0 && hi<s.length()-1 && s.charAt(lo-1)== s.charAt(hi+1)){
            lo--;
            hi++;
        }

        if(hi-lo +1 > range[1]-range[0]){
            range[0] = lo;
            range[1] = hi+1;
        }

        return ret;
    }
}

    
  
优化后执行速度：  
    
|    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-12   | 通 过 |   12ms     | Java  |