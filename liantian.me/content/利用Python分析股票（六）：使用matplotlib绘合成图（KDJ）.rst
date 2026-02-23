利用Python分析股票（六）：使用matplotlib绘合成图（KDJ）
########################################################

:Title: 利用Python分析股票（六）：使用matplotlib绘合成图（KDJ）
:Date: 2021-09-12 20:58:01
:Modified: 2021-09-12 20:58:01
:tags: Python, Stocks
:Slug: python-analyze-stocks-6
:Summary: KDJ中的KD是随机指标（Stochastic Oscillator），原名 %K and %D


首先要了解KDJ指标的计算方式
===========================

   KDJ中的KD是\ `随机指标 <https://zh.wikipedia.org/wiki/%E9%9A%8F%E6%9C%BA%E6%8C%87%E6%A0%87>`__\ ，随机指标（Stochastic
   Oscillator，KD），原名 %K and
   %D（%K&%D）又称为KD指标，是技术分析中的一种动量分析方法，采用超买和超卖的概念，由乔治·莱恩（George
   C.
   Lane）在1950年代推广使用。指标借由比较收盘价格和价格的波动范围，预测价格趋势何时逆转。“随机”一词是指价格在一段时间内相对于其波动范围的位置。

   当股价趋势上涨时，当日收盘价会倾向接近当日价格波动的最高价；
   当股价趋势下跌时，当日收盘价会倾向接近当日价格波动的最低价。

   公式：参考Wiki
   `随机指标 <https://zh.wikipedia.org/wiki/%E9%9A%8F%E6%9C%BA%E6%8C%87%E6%A0%87>`__

   J指標的計算公式為：J = 3×K –
   2×D。從使用角度來看，J的實質是反映K值和D值的乖離程度，它的範圍上可超過100，下可低於0。
   最早的KDJ指標只有K線和D線兩條線，那個時候也被稱為KD指標，隨着分析技術的發展，KD指標逐漸演變成KDJ指標，引入J指標後，能提高KDJ指標預判行情的能力。

计算RSV，这里学习到DataFrame如何填充Nan字段
-------------------------------------------

.. code:: python

   df['MinLow'] = df['Low'].rolling(9, min_periods=9).min()
   df['MinLow'].fillna(value = df['Low'].expanding().min(), inplace = True)     #  填充Nan字段
   df['MaxHigh'] = df['High'].rolling(9, min_periods=9).max()
   df['MaxHigh'].fillna(value = df['High'].expanding().max(), inplace = True)   #  填充Nan字段
   df['RSV'] = (df['Close'] - df['MinLow']) / (df['MaxHigh'] - df['MinLow']) * 100
   df

.. image:: {static}/images/132991805-a74d50c1-cad3-42c9-91ec-1ebb3dfb334d.png


计算D和K值，这里通过历遍循环来计算K和D，这个方法之前MACD图中没有使用。
----------------------------------------------------------------------

.. code:: python


   for i in range(len(df)):
       if i==0:     # 第一天
           df.at[i,'K']=50
           df.at[i,'D']=50
       if i>0:
           df.at[i,'K']=df.iloc[i-1]['K']*2/3 + 1/3*df.iloc[i]['RSV']
           df.at[i,'D']=df.iloc[i-1]['D']*2/3 + 1/3*df.iloc[i]['K']
       df.at[i,'J']=3*df.iloc[i]['K']-2*df.iloc[i]['D']
   df

.. image:: {static}/images/132991818-6d9d5220-baf7-495a-af71-7c0c97a4253a.png


绘图… 这个参考前面的文章。

.. code:: python

   graph_KDJ.plot(df.index, df['K'], 'blue', label='K') 
   graph_KDJ.plot(df.index, df['D'], 'green', label='D') 
   graph_KDJ.plot(df.index, df['J'], 'purple', label='J') 

   graph_KDJ.legend(loc='best')
   graph_KDJ.set_ylabel("KDJ")
   graph_KDJ.set_xticks(range(0,len(df.index),7))
   fig

.. image:: {static}/images/132991894-1570b98f-8bff-4a86-a1f1-c389e5586ffd.png


最后，我们修改X轴的显示 - 将坐标轴修改为时间 - 适当倾斜 - 小号字体

.. code:: python

   graph_KAV.set_xticklabels([df["Date"][index] for index in graph_KAV.get_xticks()])  # 标签设置为日期

   for label in graph_KDJ.xaxis.get_ticklabels():
       label.set_rotation(45)
       label.set_fontsize(10)  # 设置标签字体
   fig

.. image:: {static}/images/132991941-30c4808d-5084-4b6d-936a-9af2db475d0f.png
