[Fisher–Yates](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)随机置乱算法也被称做高纳德置乱算法，通俗说就是生成一个有限集合的随机排列。Fisher-Yates随机置乱算法是无偏的，所以每个排列都是等可能的，当前使用的Fisher-Yates随机置乱算法是相当有效的，需要的时间正比于要随机置乱的数，不需要额为的存储空间开销。

```
function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1)); // r 从 0 到 i 的随机索引
    [array[i], array[j]] = [array[j], array[i]]; // 交换元素
  }
}
```
