## Leetcode 

### 难度： 中度

### 描述：

> 给定一个字符串，返回没有重复的最大长度的子串


### 解法1：

```
class Solution {  
   public int lengthOfLongestSubstring(String s) {

        int n = s.length();
        int ans = 0;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j <= n; j++)
                if (allUnique(s, i, j)) ans = Math.max(ans, j - i);
        return ans;
    }

    public boolean allUnique(String s, int start, int end) {

        Set<Character> set = new HashSet<>();
        for (int i = start; i < end; i++) {
            Character ch = s.charAt(i);
            if (set.contains(ch)) return false;
            set.add(ch);
        }
        return true;
    }
}
```

时间复杂度：O(n^3)
空间复杂度：O（max(m,n))


