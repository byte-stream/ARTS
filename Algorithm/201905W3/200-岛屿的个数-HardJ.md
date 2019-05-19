200. #### 岛屿的个数

给定一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，计算岛屿的数量。一个岛被水包围，并且它是通过水平方向或垂直方向上相邻的陆地连接而成的。你可以假设网格的四个边均被水包围。

**示例 1:**

```java
输入:
11110
11010
11000
00000

输出: 1
```

**示例 2:**

```java
输入:
11000
11000
00100
00011

输出: 3
```

**解：**

```java
class Solution {
    public int numIslands(char[][] grid) {
        int result = 0;
        if(grid.length <= 0 || grid[0].length <= 0){
            return result;
        }
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                // 通过dfs将1周围数字都改为0
                if(grid[i][j] == '1'){
                    result ++;
                    dfs(grid, i, j);
                }

            }
        }
        return result;
    }
    
     private void dfs(char[][] grid, int i, int j){
        if(i >= grid.length || j >= grid[0].length || i < 0 || j < 0){
            return;
        }
        if(grid[i][j] == '1'){
            grid[i][j] = '0';
            dfs(grid, i - 1, j);
            dfs(grid, i + 1, j );
            dfs(grid, i, j -1);
            dfs(grid, i, j + 1);
        }
    }
}
```

