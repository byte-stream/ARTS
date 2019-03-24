# 84. Largest Rectangle in Histogram
Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the area of largest rectangle in the histogram.

![](https://assets.leetcode.com/uploads/2018/10/12/histogram.png)

Above is a histogram where width of each bar is 1, given height = [2,1,5,6,2,3].

![](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/10/12/histogram_area.png)

The largest rectangle is shown in the shaded area, which has area = 10 unit.

Example:

Input: [2,1,5,6,2,3]
Output: 10

思路

> 1. 可以使用暴力，但python会超市，时间复杂度为O(n^2)
> 
> 2. 使用栈来完成O(n)的算法，当第 i 个长方形比第 i-1 个 低时，低 i-1 个长方形高出的部分无法进入计算，我们维护一个始终递增的栈来保证尽可能全面的截取长方形，在维护栈的时候获取弹出栈的长方形可截取的最大面积，最后弹出所有长方形，算得最大的面积。

```python
class Solution(object):
    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        # 添加0是为了最后弹出sack中所有的值
        heights.append(0)
        # 保存索引值，维护长方形高度递增的一个栈
        stack = [-1]
        ans = 0
        for i in range(len(heights)):
            while heights[i] < heights[stack[-1]]:
                # 维护栈，算得弹出的长方形能截得的最大面积
                h = heights[stack.pop()]
                # 因为栈是递增的，我们算面积是获取的宽也是往后计算
                w = i - 1 - stack[-1]
                ans = max(ans, h * w)
            stack.append(i)
        heights.pop()
        return ans
```