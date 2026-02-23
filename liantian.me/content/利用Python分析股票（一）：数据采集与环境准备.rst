利用Python分析股票（一）：数据采集与环境准备
#############################################

:Title: 利用Python分析股票（一）：数据采集与环境准备
:Date: 2021-09-11 20:20:23
:Modified: 2021-09-11 20:20:23
:tags: Python, Stocks
:Slug: python-analyze-stocks-1
:Summary: 最常用的数据采集工具Tushare，最方便的环境Anaconda。


数据采集
========

通过公开的数据接口抓取信息
--------------------------

自己造爬虫轮子，不推荐

-  腾讯：http://qt.gtimg.cn
-  东方财富：http://quote.eastmoney.com
-  新浪：http://hq.sinajs.cn

包装好的开源库
--------------

开源版本都是通过requests、pandas、numpy等库，对腾讯、新浪、东财接口的再封装，使用便捷。免费的缺点就是缺乏实时数据、数据有反爬虫的频次限制、没有历史财务指标数据。

-  Tushare：https://tushare.pro/
-  Akshare：https://github.com/jindaxiang/akshare
-  BaoStock：http://baostock.com/

一些小厂的实时数据
------------------

-  好灵数据：h0.cn

类似的可能还有很多，但是我没用过，这些数据大多需要通过自写爬虫，配合api-key使用。

优点：收费较低。 缺点：稳定性较差，没有成熟的封装好的苦。

大厂数据
--------

往往包含历史财务数据，实时数据到L2级别，同时都有完善的接口，适配java/python等。缺点：贵

-  万得资讯
-  同花顺

如果在金融企业，已购买万得的情况下，可以联系客户经理，申请试用账号用于研发。

环境准备
========

64位的OS和Python
----------------

-  64位并不是强制要求，但是强烈推荐，因为部分第三方库缺少32位的预编译版本。比如\ `py-mini-racer <https://pypi.org/project/py-mini-racer/#files>`__

Anaconda
--------

-  Anaconda是一个用于科学计算的Python发行版，对于不数据python第三方库的安装和编译的同学，这是最简单的选择。

-  使用\ `清华Anaconda源 <https://mirror.tuna.tsinghua.edu.cn/help/anaconda/>`__\ 是改善国内anaconda使用速度的方法。

-  对于Python老手，不使用anaconda也是个好主意。因为conda和pip还是会产生一些冲突。导致conda
   update失败。

-  conda-forge
   是anaconda的社区版本，anaconda存在一些商业授权问题，conda-forge则规避了这些问题。适合商业环境下使用，并且conda-forge的库更丰富。
   安装conda-forge的好办法是使用\ `MiniForge <https://github.com/conda-forge/miniforge>`__\ ，并修改\ ``.condarc``\ 文件如下使用清华源。

   ::

      channels: [https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/]
      show_channel_urls: true

安装必要的第三方库
------------------

不管使用原版Python，还是Anaconda，或conda-forge，都需要这些库：

-  ipython
-  jupyter
-  notebook
-  matplotlib
-  numpy
-  Pillow
-  mplfinance

另外还需要：

-  自己习惯的数据库访问库，或者把数据都保存成csv
-  自己习惯的orm

如果喜欢使用Django，那么还需要：

-  django-extensions
-  django-pandas
