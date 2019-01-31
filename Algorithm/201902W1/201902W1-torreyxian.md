# 算法练习

### 输入两棵二叉树A、B,判断 B 是不是 A 的子结构。

> 思路：若根节点相等，利用递归比较他们的子树是否相等，若根节点不相等，则利用递归分别在左右子树中查找。

```java
public boolean HasSubtree(TreeNode root1, TreeNode root2) {
    boolean result = false;
    
    if(root1!=null && root2!=null) {
        if(root1.val == root2.val) {
            result = doesTreeHaveTree2(root1, root2);
        }
        if(!result) {
            return HasSubtree(root1.left, root2) || HashSubtree(root1.right,root2);
        }
    }
    
    return result;
}
```