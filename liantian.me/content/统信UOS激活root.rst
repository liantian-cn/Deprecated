统信UOS激活root
##################

:Title: 统信UOS激活root
:Date: 2021-12-09
:Modified: 2021-12-09
:tags: UOS
:Slug: root-uos
:Summary: 自己玩玩UOS的专业版，头个问题就是如何root。（linux竟然需要root也算奇葩）

缘起（怨气）
============

初试UOS发现，root竟然被禁用，启用还需要激活系统（正版激活）…

.. image:: {static}/images/20211209205022.png


使用LiveCD
==========

既然uos用deb包，那么思路很显然会参考debian。先查看内核版本

.. image:: {static}/images/20211209205322.png


内核版本是\ ``4.19.0``\ 那么猜测可以用debian 10的live CD试试破解root.

livecd的地址：\ ``https://cdimage.debian.org/mirror/cdimage/archive/latest-oldstable-live/amd64/iso-hybrid/debian-live-10.11.0-amd64-standard.iso``

livecd的用户名是\ ``user``
密码是\ ``live``\ ，然后可以\ ``sudo passwd root``\ 拿到root。

新建一个目录

::

   mkdir /mnt1

将uos的分区挂载：

::

   mount /dev/sda1 /mnt1/

查询下bash的安装路径

::

   which bash

用chroot

::

   chroot /mnt1/ /usr/bin/bash

修改下面的文件
==============

/etc/pam.d/sudo
---------------

使用#注释掉auth requisite deepin_security_verify.so

::

   # auth requisite deepin_security_verify.so

/etc/pam.d/su
-------------

使用#注释掉auth requisite deepin_security_verify.so

::

   # auth requisite deepin_security_verify.so

试试看
======

::

   sudo passwd root # 修改root的密码
   su - root # 切换到root

.. image:: {static}/images/20211209212341.png

