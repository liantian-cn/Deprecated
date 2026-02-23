在Linux系统中实现RunOnce功能
#############################

:title: 在Linux系统中实现RunOnce功能
:Date: 2022-03-01 19:51:13
:Modified: 2022-03-01 19:51:13
:Tags: UOS, Tech
:Slug: windows-runonce-in-linux
:Summary: 简单来说...就是靠crontab的@reboot功能，实现在linux下次开机自动运行一次的效果。


原理
====

简单来说…就是靠crontab的@reboot功能，实现在linux下次开机自动运行一次的效果。

操作
====

``/usr/local/bin/runonce``\ 的文件内容
--------------------------------------

::

   #!/bin/sh

   for file in /etc/local/runonce.d/*

   do
       if [ ! -f "$file" ]
       then
           continue
       fi
       "$file"
       mv "$file" "/etc/local/runonce.d/ran/$(basename $file).$(date +%Y%m%dT%H%M%S)"
       logger -t runonce -p local3.info "$file"

   done

``/etc/cron.d/runonce``\ 的文件内容
-----------------------------------

::

   @reboot root /usr/local/bin/runonce

其他操作
--------

-  新建\ ``/etc/local/runonce.d/ran/``\ 目录
-  修改权限：

   -  ``chown root:root /usr/local/bin/runonce``
   -  ``chmod +x /usr/local/bin/runonce``
   -  ``chown root:root -R /etc/local/runonce.d/``
   -  ``chown root:root -R /etc/cron.d/runonce``
