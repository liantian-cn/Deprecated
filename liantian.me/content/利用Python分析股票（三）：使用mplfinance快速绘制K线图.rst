利用Python分析股票（三）：使用mplfinance快速绘制K线图
######################################################

:Title: 利用Python分析股票（三）：使用mplfinance快速绘制K线图
:Date: 2021-09-11 20:46:55
:Modified: 2021-09-11 20:46:55
:tags: Python, Stocks
:Slug: python-analyze-stocks-3
:Summary: mplfinance是商业图表的专业工具，很强大，可以快速绘制k线图。


mplfinance是绘制K线图的快速工具，足够强大，但也有局限性。
=========================================================

1. 先根据上一篇文章，将数据提取出来。
-------------------------------------

.. code:: python

   # 使用read_frame将django orm query转换为pandas.DataFrame
   df = read_frame(stock_hst,fieldnames=['date', 'Open', 'Close',"High","Low","Volume"])
   # 有些字段需要改名，才可以配合mplfinance使用，通过字典，可以一次更改多个字段。
   # mplfinance要求列名强制为  Open | Close | High | Low | Volume ，索引为 Date 
   df.rename(columns={"date":"Date"}, inplace=True)
   # read_frame读到的datetime.Date为字符串，需要使用pandas的方法转换为时间
   df['Date'] = pd.to_datetime(df['Date'])
   # read_frame会将id作为索引，mplfinance需要将日期设置为索引
   df.set_index(["Date"], inplace=True)
   df

数据集效果如下

.. image:: {static}/images/132950439-3f247575-b137-42bf-a269-b6131e5961bf.png



2. 均线使用10、20、60日，画一个\ ``candle``\ 图，\ ``candle``\ 是主图线条的样式..
---------------------------------------------------------------------------------

.. code:: python

   import matplotlib

   import pandas as pd

   import mplfinance as mpf

   mpf.plot(df, type='candle',mav=(10,20,60), volume=True)

.. image:: {static}/images/132950550-158a757b-df1d-4764-9d77-277e16cf593b.png


3. 其他样式包括
---------------

.. code:: python

   mpf.plot(df, type='ohlc',mav=(10,20,60), volume=True)

.. image:: {static}/images/132950575-3a17c08d-4aa0-4237-a9ef-29b2a569637a.png



