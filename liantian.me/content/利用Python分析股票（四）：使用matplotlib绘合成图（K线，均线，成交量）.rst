利用Python分析股票（四）：使用matplotlib绘合成图（均线，成交量）
################################################################

:Title: 利用Python分析股票（四）：使用matplotlib绘合成图（均线，成交量）
:Date: 2021-09-11 20:49:02
:Modified: 2021-09-11 20:49:02
:tags: Python, Stocks
:Slug: python-analyze-stocks-4
:Summary: 稍微学习下pandas和matplotlib，就可以方便绘制其他K线图上的指标。

还是先参考之前的文章，读取数据
==============================

.. code:: python

   from django_pandas.io import read_frame
   import pandas as pd

   # 使用read_frame将django orm query转换为pandas.DataFrame
   df = read_frame(stock_hst,fieldnames=['date', 'Open', 'Close',"High","Low","Volume"])
   # 有些字段需要改名，才可以配合mplfinance使用，通过字典，可以一次更改多个字段。
   df.rename(columns={"date":"Date"}, inplace=True)
   # read_frame读到的datetime.Date为字符串，需要使用pandas的方法转换为时间
   df['Date'] = pd.to_datetime(df['Date'])
   # read_frame会将id作为索引，mplfinance需要将日期设置为索引
   df.set_index(["Date"], inplace=True)
   df

.. image:: {static}/images/132950439-3f247575-b137-42bf-a269-b6131e5961bf.png


计算布林线数据
==============

.. code:: python

   df['mid'] = df['Close'].rolling(20).mean()
   df['std'] = df['Close'].rolling(10).std()
   df["top"] = df['mid'] + 2*df['std']
   df["bottom"] = df['mid'] - 2*df['std']
   df

.. image:: {static}/images/132951415-1658adfa-128b-46e1-a5cd-1a5349d47449.png


计算均线
========

.. code:: python

   df['ma3'] = df['Close'].rolling(3).mean()
   df['ma10'] = df['Close'].rolling(10).mean()
   df['ma30'] = df['Close'].rolling(30).mean()
   df

.. image:: {static}/images/132951430-19eea8b5-64bf-40f8-b83f-68510debb299.png


使用mplfinance绘制合成图
========================

mplfinance可以通过设置\ ``addplot``\ 将其他数据附加到k线图上。

.. code:: python

   import mplfinance as mpf

   ap = [ mpf.make_addplot(df[['top','bottom']],ylabel='布林线'),
          mpf.make_addplot(df[['ma3','ma10','ma30']],ylabel='3/10/30均线')
        ]


   #ap_ma = mpf.make_addplot(df[['ma3','ma10','ma30']],ax=graph_KAV,ylabel='3/10/30均线')
   #ap_bl = mpf.make_addplot(df[['top','bottom']],ax=graph_KAV2,ylabel='布林线')

   mpf.plot(df,type='candle',style='yahoo',addplot=ap,xrotation=10)

.. image:: {static}/images/132951618-716f68c5-0a47-4761-9d3a-68a9b42dc524.png

不使用mplfinance的自动K线方案，手动画图
=======================================

创建画板（fig对象），分配四个区域，将分别绘制K线，成交量，MACD图，KDJ图
-----------------------------------------------------------------------

.. code:: python


   import matplotlib.pyplot as plt
   import matplotlib.gridspec as gridspec

   # 新建一个800x600的画图
   fig = plt.figure(figsize=(8,6), dpi=100,facecolor="white") 
   # 创建GridSpec，大小比例3.5：1：1：1
   gs = gridspec.GridSpec(4, 1, left=0.08, bottom=0.15, right=0.99, top=0.96, wspace=None, hspace=0, height_ratios=[3.5,1,1,1])
   graph_KAV = fig.add_subplot(gs[0,:])
   # 四个区域共享X轴
   graph_VOL = fig.add_subplot(gs[1,:],sharex=graph_KAV)
   graph_MACD = fig.add_subplot(gs[2,:],sharex=graph_KAV)
   graph_KDJ = fig.add_subplot(gs[3,:],sharex=graph_KAV)

.. image:: {static}/images/132951504-aff82769-bd1a-4bba-82cb-0e7f5d8f54cb.png

使用mpf的candlestick2_ochl函数绘制基础k线
-----------------------------------------

.. code:: python

   candlestick2_ochl(graph_KAV, df["Open"], df["Close"], df["High"], df["Low"], width=0.5, colorup='r', colordown='g')  # 绘制K线走势
   fig

.. image:: {static}/images/132951703-2aebc21a-5d6e-4cc4-a4c7-922d82f7f785.png


在绘图区域上再绘制均线
----------------------

.. code:: python

   graph_KAV.plot(np.arange(0, len(df.index)), df['ma3'],color='black', label='M3',lw=1.0)
   graph_KAV.plot(np.arange(0, len(df.index)), df['ma10'],color='teal', label='M10',lw=1.0)
   graph_KAV.plot(np.arange(0, len(df.index)), df['ma30'],color='magenta', label='M30',lw=1.0)
   fig

.. image:: {static}/images/132951737-7503ff62-b49e-4165-a062-65f51b32024d.png


设置 图例、标题、Y轴标题
------------------------

.. code:: python

   graph_KAV.legend(loc='best')   # 图例
   graph_KAV.set_title("这里是标题")
   graph_KAV.set_ylabel("价格")   # Y轴描述
   fig

.. image:: {static}/images/132951768-b40c7395-af12-44c1-8b25-ec1a1bc41d56.png


修改X轴刻度，完整填充
---------------------

.. code:: python

   graph_KAV.set_xticks(range(0,len(df.index),7))#X轴刻度设定 每7天标一个日期
   fig

.. image:: {static}/images/132952032-f1e3d373-1e15-48a2-9c8d-cc8da1379453.png


绘制成交量：设置成交量的颜色。
------------------------------

这里展示了，如果通过一个简单的函数，新增一个列并赋值

.. code:: python

   def vol_color(r):
       return 'green' if r["Open"] > r["Close"] else 'red'
   df['vol_color'] = df.apply(vol_color, axis=1)  
   df

.. image:: {static}/images/132952103-80f99391-47b8-49b6-942f-18ef6f518d50.png


绘制成交量
----------

成交量绘制使用\ ``DataFarme.bar``\ 绘制柱状图

.. code:: python

   graph_VOL.bar(np.arange(0, len(df.index)), df['Volume'],color=df['vol_color'])
   fig

.. image:: {static}/images/132952132-c01f3c0d-936a-483c-953a-d69fd23783a1.png

