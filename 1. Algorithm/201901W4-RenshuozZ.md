### 1. 两数之和


给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

示例:

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9


```js
//暴力算法(O(n^2))
function violence(nums,target){
    for(var i=0;i<nums.length;i++){
        for(var j=i+1;j<nums.length;j++){
            if(nums[i]+nums[j]==target){
                return [i,j];
            }
        }
    } 
    return [0,0];
}
violence( [2, 7, 11, 15],9);
```

```js
//改进算法O(n)
function improvement(nums,target){
    for(var i=0;i<nums.length;i++){
       var index=nums.indexOf(target-nums[i]);
        if(index>=0){
            return [i,index]
        }
    } 
    return [0,0];
}
improvement( [2,3,4] ,6);
```