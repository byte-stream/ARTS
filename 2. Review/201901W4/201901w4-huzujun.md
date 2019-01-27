# 个性化推荐系统的概述与样例实现

https://github.com/PaddlePaddle/book/blob/develop/05.recommender_system/README.md



种类：

1. 协同过滤推荐（Collaborative Filtering Recommendation） 该方法是应用最广泛的技术之一，**通过收集和分析用户的历史行为、活动和偏好推荐**。该方法的一个关键优势是它不依赖于机器去分析物品的内容特征，因此它无需理解物品本身也能够准确地推荐诸如电影之类的复杂物品；缺点是对于没有任何行为的新用户存在冷启动的问题，同时也存在用户与商品之间的交互数据不够多造成的稀疏问题。
2. 基于内容过滤推荐(Content-based Filtering Recommendation)：该方法**利用商品的内容描述，抽象出有意义的特征，通过计算用户的兴趣和商品描述之间的相似度，来给用户做推荐**。优点是简单直接，不需要依据其他用户对商品的评价，而是通过商品属性进行商品相似度度量，从而推荐给用户所感兴趣商品的相似商品；缺点是对于没有任何行为的新用户同样存在冷启动的问题。
3. 组合推荐(Hybrid Recommendation)：多种方法结合

####  融合推荐模型概览

在融合推荐模型的电影个性化推荐系统中：

1. 首先，使用用户特征和电影特征作为神经网络的输入，其中：
   - 用户特征融合了四个属性信息，分别是用户ID、性别、职业和年龄。
   - 电影特征融合了三个属性信息，分别是电影ID、电影类型ID和电影名称。
2. 对用户特征，将用户ID映射为维度大小为256的向量表示，输入全连接层，并对其他三个属性也做类似的处理。然后将四个属性的特征表示分别全连接并相加。
3. 对电影特征，将电影ID以类似用户ID的方式进行处理，电影类型ID以向量的形式直接输入全连接层，电影名称用文本卷积神经网络得到其定长向量表示。然后将三个属性的特征表示分别全连接并相加。
4. 得到用户和电影的向量表示后，计算二者的余弦相似度作为个性化推荐系统的打分。最后，用该相似度打分和用户真实打分的差异的平方作为该回归模型的损失函数。

[![img](https://github.com/PaddlePaddle/book/raw/develop/05.recommender_system/image/rec_regression_network.png?raw=true)](https://github.com/PaddlePaddle/book/blob/develop/05.recommender_system/image/rec_regression_network.png?raw=true)

## 后记

读这篇文章的目的性倒很强，将为大学生服务外包竞赛中的项目实现一个推荐系统，不过比电影推荐要复杂一些。