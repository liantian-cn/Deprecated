利用Python分析股票（二）：pandas 、django 以及 jupyter notebook
#################################################################

:Title: 利用Python分析股票（二）：pandas 、django 以及 jupyter notebook
:Date: 2021-09-11 20:46:16
:Modified: 2021-09-11 20:46:16
:tags: Python, Stocks
:Slug: python-analyze-stocks-2
:Summary: pandas用于数据处理，django借用orm，jupyter用于展示数据。

从\ ``django-orm``\ 到\ ``pandas.DataFrame``
============================================

这里要用到第三方库
`django-pandas <https://github.com/chrisdev/django-pandas>`__

.. code:: python


   # 使用read_frame。
   from django_pandas.io import read_frame

   # 使用django orm读取信息。
   stock_hst = AStockHist.objects.filter(stock_id=code,date__gte=datetime.date(2021, 1, 1)).order_by("date").all()

   # 使用read_frame将django orm query转换为pandas.DataFrame。
   df = read_frame(stock_hst,fieldnames=['date', 'Open', 'Close',"High","Low","Volume"])

   # 为字段改名，以mplfinance等库使用。可以一次更改多个字段。
   df.rename(columns={"date":"Date"}, inplace=True)

   # read_frame读到的datetime.Date为字符串，需要使用pandas的方法转换为时间。
   df['Date'] = pd.to_datetime(df['Date'])

   # read_frame会将主键作为索引，实际往往需要将日期设置为索引。
   df.set_index(["Date"], inplace=True)

从\ ``pandas.DataFrame``\ 到\ ``django-orm``
============================================

其实输入数据库的方法很多，只要通过\ ``DateFrame.iloc[i]``\ 就可以历遍数据集中的行，并写入数据。

.. code:: python


   # 通过akshare抓取某一A股数据为DataFrame（其他抓取方法均类似）
   import akshare as ak
   stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_id, adjust="hfq")


   # 获取数据库内已有的记录，这里将结尾保存为日期的集合，便于后面求交集、差集、并集。

   # 单行写法
   in_db_hst = set([t.strftime('%Y-%m-%d') for t in AStockHist.objects.filter(stock=stock).values_list('date', flat=True)])

   # 多行写法
   qs =  AStockHist.objects.filter(stock=stock).values_list('date', flat=True)
   in_db_hst = []
   for  q in qs:
       in_db_hst.append(q.strftime('%Y-%m-%d'))
   in_db_hst = set(in_db_hst)

   # 获取DateFrame里的日期集合
   cur_hst = set(stock_zh_a_hist_df["日期"].values.tolist())

   # 求差集，得到数据库内没有，需要更新的日期，并根据这个集合过滤此前的DateFrame
   set_need_create_hst = cur_hst - in_db_hst
   need_create_hst = stock_zh_a_hist_df[stock_zh_a_hist_df['日期'].isin(set_need_create_hst)]

   # 批量写入django-orm
   bulk_create_list = []
   for i in range(0, need_create_hst.index.__len__()):
       hst = need_create_hst.iloc[i]
       new_hst = AStockHist(stock = stock,date = datetime.strptime(hst['日期'], '%Y-%m-%d').date())
       new_hst.Open = hst['开盘']
       ......
       ......
       bulk_create_list.append(new_hst)
   AStockHist.objects.bulk_create(bulk_create_list)

在\ ``Jupyter Notebook``\ 中访问\ ``django-orm``
================================================

安装扩展
``django-extensions``\ 后，可使用批处理启动\ ``Jupyter Notebook``

.. code:: batch

   @echo off
   cmd /k "CHCP 65001 & cd /d %~dp0\.env\Scripts & activate & cd /d  %~dp0 & python manage.py shell_plus --notebook & exit 0"
