# 前言

> 前段时间学习了 Solr ，当时学完印象还挺深刻，这没过多久都感觉快忘的差不多了。赶紧写入篇总结来回忆下。



# Solr

Solr 是一个企业级的搜索服务器，用户可以通过 http 请求，向搜索服务器提交 XML 文件，生成索引；也可以通过 Http Get 操作提出查找请求，并得到 XML 格式的返回结果。



## 原理

* 检索
  * 顺序扫描法：对文件按顺序依次查找，这种方式在文件少的情况下速度不错，但文件多的时候就有点差强人意了。
  * 全文检索：对文档内容进行分词，对结果创建索引，通过对索引的搜索来达到查找的目的。

##  使用 SolrJ 管理索引库

* 添加文档

  * 导入 SolrJ 的 jar 包
  * 创建一个 SolrServer，使用 HttpSolrServer 创建对象
  * 创建一个文档对象 SolrInputDocument 对象
  * 向文档中添加域。
  * 把文档添加到索引库
  * 提交

  ``` java
  @Test
  public void testSolrJAdd() throws SolrServerException, IOException {
    // 创建一个SolrServer对象。创建一个HttpSolrServer对象
    // 需要指定solr服务的url
    SolrServer solrServer = new HttpSolrServer("http://101.132.69.111:8080/solr/collection1");
    // 创建一个文档对象SolrInputDocument
    SolrInputDocument document = new SolrInputDocument();
    // 向文档中添加域，必须有id域，域的名称必须在schema.xml中定义
    document.addField("id", "123");
    document.addField("item_title", "红米手机");
    document.addField("item_price", 1000);
    // 把文档对象写入索引库
    solrServer.add(document);
    // 提交
    solrServer.commit();
  }
  ```

* 删除文档

  ```java
  @Test
  public void deleteDocumentByQuery() throws Exception {
    SolrServer solrServer = new HttpSolrServer("http://101.132.69.111:8080/solr/collection1");
    //这边会根据分词去删
    solrServer.deleteByQuery("item_title:红米手机");
    solrServer.commit();
  }
  ```

  

* 查找

  ```java
  @Test
  public void queryDocument() throws Exception {
      // 第一步：创建一个SolrServer对象
      SolrServer solrServer = new HttpSolrServer("http://101.132.69.111:8080/solr/collection1");
      // 第二步：创建一个SolrQuery对象。
      SolrQuery query = new SolrQuery();
      // 第三步：向SolrQuery中添加查询条件、过滤条件。。。
      query.setQuery("*:*");
      // 第四步：执行查询。得到一个Response对象。
      QueryResponse response = solrServer.query(query);
      // 第五步：取查询结果。
      SolrDocumentList solrDocumentList = response.getResults();
      System.out.println("查询结果的总记录数：" + solrDocumentList.getNumFound());
      // 第六步：遍历结果并打印。
      for (SolrDocument solrDocument : solrDocumentList) {
        System.out.println(solrDocument.get("id"));
        System.out.println(solrDocument.get("item_title"));
        System.out.println(solrDocument.get("item_price"));
    	}
  }
  ```

  