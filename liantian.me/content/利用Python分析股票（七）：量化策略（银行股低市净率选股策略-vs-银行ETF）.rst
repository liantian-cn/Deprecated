利用Python分析股票（七）：量化策略
###################################

:Title: 利用Python分析股票（七）：量化策略
:Date: 2021-09-20 20:59:00
:Modified: 2021-09-20 20:59:00
:tags: Python, Stocks
:Slug: python-analyze-stocks-7
:Summary: （银行股低市净率选股策略 vs 银行ETF） 这是一个亏本的模拟。

.. code:: python

   from jqdata import *

   def initialize(context):
       # 设定中证银行指数作为基准
       set_benchmark('399986.XSHE')
       # 开启动态复权模式(真实价格)
       set_option('use_real_price', True)
       # 过滤掉order系列API产生的比error级别低的log
       log.set_level('order', 'error')

       ### 股票相关设定 ###
       # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
       set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')

       run_weekly(choose_stock, weekday=3, time='before_open') #选股
       run_weekly(weekly, weekday=3, time='open')
       
       g.count = 1


   def choose_stock(context):
       # 得到中证银行指数的成分股
       g.stocks = get_index_stocks('399986.XSHE')

       # 查询股票的市净率，并按照市净率升序排序
       if len(g.stocks) > 0:
           g.df = get_fundamentals(
               query(
                 valuation.code,
                 valuation.pubDate,
                  valuation.pb_ratio,
               ).filter(
                   valuation.code.in_(g.stocks)
               ).order_by(
                   valuation.pb_ratio.asc()
               )
           )

           # 找出最低市净率的一只股票
           g.code = g.df['code'][0]

   def weekly(context):
       print("第{count}次交易，日期{date}".format(count=g.count,date=context.current_dt.isoweekday()))
       if g.count == 1:
           order_value('512800.XSHG',context.portfolio.starting_cash)
       else:
           # 先卖出etf
           order_value('512800.XSHG',-100000)
           # 剩余金额买入最低市值的股票
           order_value(g.code,context.portfolio.available_cash)
           
       g.count += 1

实际上并没有跑赢银行ETF
=======================

因为2020年底，银行股出现分化，民生银行，华夏银行、交通银行等都在刷新市净的历史新低

.. image:: {static}/images/133973818-65af3ad6-e5c2-44d4-a4d6-5d28d3686708.png
