该系列是阅读/翻译 nature 上的论文[《Information flow reveals prediction limits in online social activity》](https://doi.org/10.1038/s41562-018-0510-5)的记录，每周将不定量翻译，也欢迎大家提出建议。

Information theory has a long history of estimating the mathematical information content of text ^22–25^. Notably, information is present not just in the words of the text, but also in their order of appearance. Thus, we applied a nonparametric entropy estimator that incorporates the full-sequence structure of the text^25^. This estimator has been proved to converge asymptotically to the true entropy rate for stationary processes and has been applied to human mobility data^26^. See ‘Measuring the flow of predictive information’ and ‘Estimator convergence on our data’ in the Methods section for further details on the entropy estimators and their convergence rates on these data.

信息论在评估文本的数学信息内容方面有着悠久的历史。值得注意的是，信息不仅存在于文本的文字中，而且存在于它们的出现顺序中。因此，我们应用了一个包含了文本的全序列结构的无参数熵估计器。该估计器已被证明渐近收敛于静止过程的真熵率，并已应用于人类移动数据。有关熵估计量及其对这些数据的收敛速度的更多详细信息，请参阅“方法”部分中的“测量预测信息流量”和“我们数据上的估算器收敛”。



We focused on four aspects of information flow over social networks, exploring both content and timing of messages:(1) the extent to which information is encoded through language into an individual’s social ties, (2) the importance of recency to information flow between individuals, (3) the role of tie strength between individuals in the flow of information, and (4) the relationship between structural network properties, such as homophily and information. We first examined the information content of the egos themselves. Their text  streams were relatively well clustered around h of ~6.6 bits, with most falling between 5.5 and 8 bits (Fig. 1b). Equivalently, this corresponds to a perplexity range of ~45–256 words, which is far smaller than the typical user’s ~5,000-word vocabulary, and a mean predictability of ~53%, which is quite high for predicting a given word out of ~5,000 possible words on average (for example, choosing words uniformly at random corresponds to a predictability of 0.02%). We found this typical value of information comparable to other sources of written text, but social media texts were more broadly distributed around the mean—individuals were more likely to be either highly predictable or highly unpredictable than formally written text (see Supplementary Note 1.4).

我们关注社交网络上信息流的四个方面，探索消息的内容和时间：(1) 信息通过语言编码到个人社会关系中的程度，(2)新近度对个人之间信息流动的重要性，(3)在信息流动中个人之间的关系强度的作用和(4)结构网络属性之间的关系，如同性恋和信息。我们首先检查了自我的信息内容。它们的文本流相对较好地聚集在约 6.6bit的 h 周围，大多数落在 5.5 到 8 位之间。同样地，这对应于 \~45-256 个单词的困惑范围，远小于典型用户的\~5,000 个单词的词汇量，并且平均可预测性为 ~53％，这对于预测给定的单词来说是非常高的平均 ~5,000个可能的单词(例如，随机均匀选择单词对应的可预测性为 0.02％)。我们发现这种信息的典型价值可与其他书面文本来源相媲美，但社交媒体文本更广泛地分布在平均值 - 个体更可能是高度可预测的或高度不可预测的正式书面文本（参见补充说明1.4）。



