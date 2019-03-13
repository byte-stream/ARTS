该系列是阅读/翻译 nature 上的论文[《Information flow reveals prediction limits in online social activity》](https://doi.org/10.1038/s41562-018-0510-5)的记录，每周将不定量翻译，也欢迎大家提出建议。

In this work, we applied information-theoretic estimators to study information and information flow in a collection of Twitter user activities. These estimators fully incorporate language data while also accounting for the temporal ordering of user activities. We found that meaningful predictive information about individuals is encoded in their social ties, allowing us to determine fundamental limits of social predictability, independent of actual predictive or machine learning methods. We explored the roles of information recency and social activity patterns, as well as structural network properties such as information homophily between individuals. 

在这次工作中，我们应用信息理论估计来研究一组 Twitter 用户活动中的信息和信息流。这些估计完全包含语言数据，同时还考虑了用户活动的时间顺序。我们发现有关个人的有意义的预测信息被编码在他们的社会关系中，使我们能够确定社会可预测性的基本限制，而独立于实际的预测或机器学习方法。 我们探讨了信息新近度和社交活动模式的作用，以及结构网络属性，例如个体之间的信息同质性。

We gathered a data set of n = 13,905 users, comprising egocentric networks from the Twitter social media platform, and a total of m = 30,852,700 public postings from these users. Each of the n = 927 ego-networks consisted of one user (the ego) and their 15 most frequently mentioned Twitter contacts (the alters), providing us with ego–alter pairs on which to measure information flow. See‘Data collection and filtering’ in the Methods section for full details on the data processing.

我们收集了 n = 13,905 个用户的数据集，包括来自 Twitter 社交媒体平台的自我中心网络，以及来自这些用户的总共 m = 30,852,700 个公开帖子。每个 n = 927 个自我网络由一个用户（自我）和他们最常提到的15个 Twitter联系人 （改变者）组成，为我们测量信息流提供自我-改变者对。 有关数据处理的完整详细信息，请参阅“方法”部分中的“数据收集和过滤”。

