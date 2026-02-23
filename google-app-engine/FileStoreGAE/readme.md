# File Store on GAE
![Powered by Google App Engine](https://cloud.google.com/appengine/images/appengine-noborder-120x30.gif)
### 用途

* 适合低负载的个人Blog的图床/网盘。
* 简单的缩略图预览及文件上床功能。
* 同时适合存储小体积的文件附件。

### 特性

* 使用DataStore存储文件
* 使用memcache进行优化，数据库不是瓶颈，可跑满每日流量。
* 针对cloudflare等反向代理CDN进行优化，实际流量比每日限额略高。
* 使用Flask。
* 前端使用bootstrap+masonry瀑布流。
* 简单的单页面管理，支持分页，每页最多预览项可修改`PER_PAGE`。
* 删除有确认提示，避免误删。
* 在浏览页面，图片显示缩略图，其他文件根据mime显示图标。
* 简单生成markdown便于插入博客文本。


### 部署

修改`app.yaml`内的`application: static-liantian-me`字段后，使用`appcfg.py`上传即可。


### 授权和其他

开源协议：The Unlicense，可以任意使用。

不介意造访：[LIANTIAN'S LOG](https://liantian.me/)


### 预览：


![](https://github.com/liantian-cn/FileStoreGAE/raw/master/snipaste_20170325_230443.png)
