利用Python分析股票（五）：使用matplotlib绘合成图（MACD）
########################################################

:Title: 利用Python分析股票（五）：使用matplotlib绘合成图（MACD）
:Date: 2021-09-11 20:56:28
:Modified: 2021-09-11 20:56:28
:tags: Python, Stocks
:Slug: python-analyze-stocks-5
:Summary: MACD的全名是[指数平滑移动平均线]，是股票交易中一种常见的技术分析工具。

首先要了解MACD指标的计算方式
============================

   MACD的全名是\ `指数平滑移动平均线 <https://zh.wikipedia.org/wiki/%E6%8C%87%E6%95%B0%E5%B9%B3%E6%BB%91%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E7%BA%BF>`__\ ，是股票交易中一种常见的技术分析工具，由Gerald
   Appel于1970年代提出，用于研判股票价格变化的强度、方向、能量，以及趋势周期，找出股价支撑与压力，以便把握股票买进和卖出的时机。
   MACD指标由一组曲线与图形组成，通过收盘时股价或指数的快变及慢变的指数移动平均值（EMA）之间的差计算出来。“快”指更短时段的EMA，而“慢”则指较长时段的EMA，最常用的是12及26日EMA。[2]

   MACD指标是由三部分构成的，分别是：差离值（DIF值）、信号线（DEM值，又称MACD值）、柱形图或棒形图（histogram
   / bar graph）。

   差离值（DIF值）：利用收盘价的指数移动平均值（12日／26日）计算出差离值。
   〖公式〗DIF=EMA(close,12)-EMA(close,26)

   信号线（DEM值，又称MACD值）：计算出DIF后，会再画一条“信号线”，通常是DIF的9日指数移动平均值。
   〖公式〗 DEM=EMA(DIF,9)

   柱形图或棒形图（histogram / bar
   graph）：将DIF与DEM的差画成“柱形图”（MACD bar / OSC）。
   〖公式〗OSC=DIF-DEM
   注意，为了反应趋势，这个算法是对的，但实际绘图中，为了曲线和柱状图的比例协调，柱状图的值要乘2

pandas提供的函数\ ``DateFarme.ewm()``\ 计算移动平均，\ `官方文档 <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html>`__\ ，当\ ``adjust``\ 设置为\ ``False``\ 时，将计算简单移动平均

关于移动平均，可参考wiki
`移动平均 <https://zh.wikipedia.org/wiki/%E7%A7%BB%E5%8B%95%E5%B9%B3%E5%9D%87>`__

.. code:: python

   df["exp12"] = df['Close'].ewm(span=12, adjust=False).mean()
   df["exp26"] = df['Close'].ewm(span=26, adjust=False).mean()
   df['DIF'] = df['exp12'] - df['exp26']
   df["DEM"] = df['DIF'].ewm(span=9, adjust=False).mean()
   df['OSC'] = 2*(df['DIF'] - df['DEM'])
   df

.. image:: {static}/images/132967852-d55d40d7-2740-4103-b751-63185a644597.png



其中\ ``macd``\ 值应该是柱状图，为了设置颜色，
再写一个函数，生成颜色列。

.. code:: python



   def macd_color(r):
       return 'red' if r["OSC"] > 0 else 'green'
   df['macd_color'] = df.apply(macd_color, axis=1)  
   df

然后将\ ``dif``\ 和\ ``dea``\ 作为线绘入，\ ``macd``\ 柱状图绘入

.. code:: python

   graph_MACD.plot(np.arange(0, len(df.index)), df['DIF'], 'red', label='DIF') 
   graph_MACD.plot(np.arange(0, len(df.index)), df['DEM'], 'blue', label='DEM') 
   graph_MACD.bar(np.arange(0, len(df.index)), df['OSC'],color=df['macd_color'])
   fig

   graph_MACD.legend(loc='best')    # 设置图例
   graph_MACD.set_ylabel("MACD")    # 设置Y轴标题

.. image:: {static}/images/132967903-a960d91f-9e61-4f8a-88b9-019402d3a53a.png



解读（来自Wiki\ `指数平滑移动平均线 <https://zh.wikipedia.org/wiki/%E6%8C%87%E6%95%B0%E5%B9%B3%E6%BB%91%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E7%BA%BF>`__\ ）
============================================================================================================================================================

MACD其实就是两条指数移动平均线——EMA(12)和EMA(26)——的背离和交叉，EMA(26)可视为MACD的零轴，但是MACD呈现的消息噪声较均线少。

MACD是一种趋势分析指针，不宜同时分析不同的市场环境。以下为三种交易信号：

-  差离值（DIF值）与信号线（DEM值，又称MACD值）相交；
-  差离值与零轴相交；
-  股价与差离值的背离。
   差离值（DIF）形成“快线”，信号线（DEM）形成“慢线”。若股价持续上涨，DIF
   值为正，且愈来愈大；若股价持续下跌，DIF 值为负，且负的程度愈来愈大。

当差离值（DIF）从下而上穿过信号线（DEM），为买进信号；相反若从上而下穿越，为卖出信号。买卖信号可能出现频繁，需要配合其他指针（如：RSI、KD）一同分析。
DIF 值与 MACD
值在0轴在线，代表市场为牛市，若两者皆在0轴线之下，代表市场为熊市。 DIF
值若向上突破 MACD 值及0
轴线，为买进信号，不过若尚未突破0轴，仍不宜买进；DIF 值若向下跌破 MACD
值及0 轴线，为卖出信号，不过若尚未跌破0轴，仍不宜卖出。[6]:278

棒形图（MACD bar / Oscillator，OSC）
的作用是显示出“差离值”与“信号线”的差，同时将两条线的走势具体化，以利判断差离值和信号线交叉形成的买卖信号，例如正在下降的棒形图代表两线的差值朝负的方向走，趋势向下；靠近零轴时，差离值和信号线将相交出现买卖信号。

棒形图会根据正负值分布在零轴（X轴）的上下。棒形图在零轴上方时表示走势较强(牛市)，反之则是走势较弱(熊市)。

差离值自底向上穿过零轴代表市场气氛利好股价，相反由上而下则代表利淡股价。差离值与信号线均在零轴上方时，被称为多头市场，反之，则被称为空头市场。

当股价创新低，但MACD并没有相应创新低（牛市背离），视为利好（利多）消息，股价跌势或将完结。相反，若股价创新高，但MACD并没有相应创新高（熊市背离），视为利淡（利空）消息。同样地，若股价与棒形图不配合，也可作类似结论。

MACD是一种中长线的研判指标。当股市强烈震荡或股价变化巨大（如送配股拆细等）时，可能会给出错误的信号。所以在决定股票操作时，应该谨慎参考其他指标，以及市场状况，不能完全信任差离值的单一研判，避免造成损失。
