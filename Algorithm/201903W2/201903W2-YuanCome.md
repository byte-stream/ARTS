## LeetCode 43. 字符串相乘
  
#### 题目描述：  
> 给定两个以字符串形式表示的非负整数 num1 和 num2，返回 num1 和 num2 的乘积，它们的乘积也表示为字符串形式。
    
#### 示例1：  

    输入: num1 = "2", num2 = "3"
    输出: "6"   
      
#### 示例2:  

    输入: num1 = "123", num2 = "456"
    输出: "56088"
    
#### 说明：  
  
    num1 和 num2 的长度小于110。
    num1 和 num2 只包含数字 0-9。
    num1 和 num2 均不以零开头，除非是数字 0 本身。
    不能使用任何标准库的大数类型（比如 BigInteger）或直接将输入转换为整数来处理。  
      

分析思路：  
　　根据题意很可能乘积会比 int 类型的数字范围要大，用 long 似乎也不太合适，但是可以想到每两个 0 - 9 的数字乘积最大为 81，此时可以使用 int 来完成。接下来是如何分解问题的时候 String 可以拆分成 char，利用 ASCII 码减 '0'，求得每个 char 对应的数字。最后利用 StringBuilder 的 append 方法进行合并，转换成 String。
  
#### 我的代码：  

    class Solution {
        public String multiply(String num1, String num2) {
            if ("0".equals(num1) || "0".equals(num2)) {
                return "0";
            }
            int length1 = num1.length();
            int length2 = num2.length();
            int[] result = new int[length1 + length2];
            for (int i = 0; i < num1.length(); i++) {
                for (int j = 0; j < num2.length(); j++) {
                    int tem = (num1.charAt(length1 - 1 - i) - '0') * (num2.charAt(length2 - 1 - j) - '0');
                    int l = 1;
                    do {
                        //加上temp
                        result[length1 + length2 - i - j - l] += tem;
                        //tem保存进位
                        tem = result[length1 + length2 - i - j - l] / 10;
                        //求模去掉进位
                        result[length1 + length2 - i - j - l] %= 10;
                        //在下一轮把进位保存到result数组的前一位中
                        l++;
                    } while (tem > 0);
                }

            }
            StringBuilder sb = new StringBuilder();
            int i = 0;
            //去掉前面为0的元素
            while (result[i] == 0) {
                i++;
            }
            //拼接到StringBuilder上转换成String
            while (i < (length1 + length2)) {
                //使用 i++ 可以不用再添加一句 i++ 使 i 增1；
                sb.append(result[i++]);
            }
            return sb.toString();
        } 
    }

  
运行结果：  

|    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-26   |通 过  |   40ms    | Java  |
  
#### 优化：  

    class Solution {
        public String multiply(String num1, String num2) {
		    if(num1.isEmpty() || num2.isEmpty() 
            ||(num1.length() == 1 && num1.charAt(0) == '0') 
            || (num2.length() == 1 && num2.charAt(0) == '0'))
			    return "0";
		    int len1 = num1.length();
		    int len2 = num2.length();
		    int[] ans = new int[len1 + len2 + 1];
		    for(int i = 0 ; i < len1;i++) {
			    int a = num1.charAt(i) - '0';
			    for(int j = 0; j < len2; j++) {
				    int b = num2.charAt(j) - '0';
				    ans[len1 + len2 - i - j - 2] += a * b ;
			    }
		    }
		    StringBuffer res = new StringBuffer();		
		    for(int i = 0; i < len1 + len2   ;i++) {
			    res.append(ans[i] % 10);
			    ans[i + 1] += ans[i] / 10;
		    }
		    String result = res.reverse().toString();
		    if(result.startsWith("0"))
			    result = result.substring(1, len1 + len2);
		    return result;
	    }  
    }

    
  
优化后执行速度：  
    
|    提交时间  | 状 态 |  执行时间 | 语 言 |
| ----------   | ---   | -------   | ----  |
| 2019-02-26   | 通 过 |   11ms    | Java  |