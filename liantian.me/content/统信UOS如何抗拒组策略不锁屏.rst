统信UOS如何抗拒组策略不锁屏
############################

:Title: 统信UOS如何抗拒组策略不锁屏
:Date: 2022-06-15
:Modified: 2022-06-15
:tags: UOS
:Slug: how-to-disable-lock-screen-policy-in-uos
:Summary: 在windows下，只需要定时移动指针，就可以不锁屏，但是这个方法在UOS下是无效的..


本质上UOS的组策略是由管控服务器下发的一组组脚本。并且定期刷新这些脚本，实现组策略的功能。

当然，管控服务器是商业版UOS的私有功能，并非开源组件，可以搜索\ ``udcp``\ 获得更多线索，实际分析过程中。可以通过观察日志，监控路径包含\ ``udcp``\ 的文件生成，获得更多线索。

如何抗拒组策略不锁屏
====================

通过观察日志，会发现，定时锁屏策略就是通过每次刷新策略时执行gsettings命令设置锁屏时间实现的，那么只需要反其道而行之，定时设置锁屏时间为0即可。

即：设法定期执行下面的命令

.. code:: bash


   gsettings set com.deepin.dde.power line-power-screen-black-delay 0
   gsettings set com.deepin.dde.power line-power-lock-delay 0
   gsettings set com.deepin.dde.power sleep-lock false
   gsettings set com.deepin.dde.power screen-black-lock false

实现的方法有很多，自行发挥即可。
