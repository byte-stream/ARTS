## LeetCode 6.  Z 字形变换
  
#### 题目描述：  
> 将一个给定字符串根据给定的行数，以从上往下、从左到右进行 Z 字形排列。
比如输入字符串为 "LEETCODEISHIRING" 行数为 3 时，排列如下： 
>  
    L   C   I   R
    E T O E S I I G
    E   D   H   N
       
>  
> 之后，你的输出需要从左往右逐行读取，产生出一个新的字符串，比如："LCIRETOESIIGEDHN"。
> 
> 请你实现这个将字符串进行指定行数变换的函数：  
  
    string convert(string s, int numRows);  
    
#### 示例：  

    输入: s = "LEETCODEISHIRING", numRows = 3
    输出: "LCIRETOESIIGEDHN"
  
分析思路：  
　　其实题意更应该说是N字形变换0...0，从左到右迭代 ss，将每个字符添加到合适的行。只有当我们向上移动到最上面或向下移动到最下面时，当前方向才会发生改变。需要构建一个StringBuilder列表来输出整个变换的结果。 
  
#### 我的代码：  

    class Solution {
    public String convert(String s, int numRows) {
        if(numRows == 1) {
            return s;
        }
        List<StringBuilder> rows = new ArrayList<>();
        for(int i = 0; i < Math.min(numRows, s.length()); i++) {
            rows.add(new StringBuilder());  
        }
        int curRow = 0;
        boolean turnAway = false;
        for(char c : s.toCharArray()) {
            rows.get(curRow).append(c);
            if(curRow == 0 || curRow == numRows -1) {
                turnAway = !turnAway;
            }
            if(turnAway) {
                    curRow++;
                }else {
                
                    curRow--;
                }
            }
        
            StringBuilder result = new StringBuilder();
            for(StringBuilder row :rows) {
                result.append(row);
            }
            return result.toString();
        }
    }

  
运行结果：  

|    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-13   |通 过  |   74ms    | Java  |
  
#### 优化：  
    class Solution {
        public String convert(String s, int numRows) {
            if (s == null || s.length() <= numRows || numRows == 1) return s;
	            StringBuilder sb = new StringBuilder();
	            //gap为字符间隔
	            int gap = 2 * (numRows - 1), len = s.length();
	            for (int i = 0; i < numRows; i++) {
	                for (int j = 0; i + j * gap < len; j++) {
	                    sb.append(s.charAt(i + j * gap));
	                    //在非首尾行下
	                    if (i > 0 && i < numRows - 1 && (j + 1) * gap - i < len) {
	                        sb.append(s.charAt((j + 1) * gap - i));
	                    }
	                }
	            }
	       return sb.toString();
        }
    }

    
  
优化后执行速度：  
    
|    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-13   | 通 过 |   21ms    | Java  |