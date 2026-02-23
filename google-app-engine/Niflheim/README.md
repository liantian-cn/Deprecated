### Niflheim : 一个简单的基于GAE的单用户博客程序
![Powered by Google App Engine](https://cloud.google.com/appengine/images/appengine-silver-120x30.gif)

对于博客程序，试图在简单（托管）和复杂（自建）之间找到一个平衡，所以制作了这个程序。
基于App Engine的优点：简单，不需要维护基础设施。高度可定制化，无广告，可绑定域名。

### feature

- 基于 [Python Standard Environment](https://cloud.google.com/appengine/docs/standard/python/ "Google App Engine Python Standard Environment")
- 可见即所得的使用 [Markdown](https://python-markdown.github.io "Markdown") 语法书写博客。
- 使用 [Disqus](https://disqus.com/admin/ "Disqus") 评论系统
- 支援上传图片到[Google Cloud Storage](https://cloud.google.com/storage/ "google cloud storage")
- 简洁并使用方便的后台界面。
- 易于改造的前台模板，默认模板copy自[Typecho](https://github.com/typecho/typecho "Typecho")
- 便利化的设计：
	- 基于Google翻译的Slug生成。
	- 在文章编辑页面上传文档。
	- 缓存设计，优化GAE配额。


### 截图

**文章编辑界面**

![](https://lh3.googleusercontent.com/g-JSj_Q5wTh6YqbxZJkiL-xsWklFr7GgL5iUvPGoaUJaFp9jkgXxG5Cf0MV_S1GRMhwGD7pzY8QW_5DP5_XecWyogkBnfA=s600)

**后台设置**

![](https://lh3.googleusercontent.com/4N1rNM0KOBuq4y5aF3UGkR0EcMvfeKCv1qVqgPLgvu_QJoCoLmmWgyZLBCQzszydpp6x172RGJt-Ph9g2ml7NZE9kEw_=s600)

**首页页面**

![](https://lh3.googleusercontent.com/XZKaLkH4k-jqyKQKd7DxfPQiuEvikof_tXsuxCrT1de0RUOP7O2x8HTD0rucw1oQb7YvUw-Gc6BZQsVc0_qikQI6p24=s600)

### Todo

- pingback功能的实现。
- tag的展现。


### 命名

尼福尔海姆（Niflheim）。在北欧神话中，其义为“雾之国”（Mist-home）。是个终年充满浓雾，寒冷的地区。

万年没人看，很适合这个名字。


