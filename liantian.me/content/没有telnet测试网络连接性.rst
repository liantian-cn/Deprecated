不使用telnet测试网络连通性
############################

:title: 不使用telnet测试网络连通性
:Date: 2022-07-08
:Modified: 2022-07-08
:tags: Tech
:Slug: test-network-connect-without-telnet
:Summary: telnet已经不是rh8/9默认安装的了，那么如何测试网络呢？


用/dev/tcp
==========

::


   cat < /dev/tcp/8.8.8.8/443

用ncat
======

::

   nc -zv 8.8.8.8 443

用curl / wget
=============

::

   wget http://8.8.8.8:443
   curl -H http://8.8.8.8:443
