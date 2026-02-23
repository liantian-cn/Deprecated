使用脚本设置wmi的访问权限
#########################

:Title: 使用脚本设置wmi的访问权限
:Date: 2022-06-23
:Modified: 2022-06-23
:tags: Windows
:Slug: wmi-access-setting-via-script
:Summary: 合理设置wmi的访问权限，有利于安全的，同时也可以通过wmi赋予普通用户一些权限。


如何设置WMI权限
===============

``compmgmt.msc``\ 进入\ ``Computer Management`` ->
``WMI Control``\ ，然后右键->\ ``Properties``

在\ ``Security``\ 标签，可以设置每个路径的权限。

如何导出wmi权限
===============

参考资料
https://docs.microsoft.com/en-us/windows/win32/wmisdk/–systemsecurity-getsd

输入命令，可以导出权限安全描述符(security descriptor)

::

   wmic /namespace:\\root\CIMV2  /output:sd.txt path __systemsecurity call getSD

sd.txt的内容大概如下

::

   Executing (__systemsecurity)->getSD()
   Method execution successful.
   Out Parameters:
   instance of __PARAMETERS
   {
   ReturnValue = 0;
   SD = {1, 0, 4, 129, 160, 0, 0, 0, 176, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 2, 0, 140, 0, 6, 0, 0, 0, 0, 0, 24, 0, 33, 0, 2, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 46, 2, 0, 0, 0, 0, 24, 0, 33, 0, 2, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 47, 2, 0, 0, 0, 18, 24, 0, 63, 0, 6, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0, 0, 18, 20, 0, 19, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 5, 20, 0, 0, 0, 0, 18, 20, 0, 19, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 5, 19, 0, 0, 0, 0, 18, 20, 0, 19, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 5, 11, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0};
   };

这其中SD={}內文字內容就是二进制保存的安全描述符

导入wmi权限
===========

参考资料
https://docs.microsoft.com/en-us/windows/win32/wmisdk/–systemsecurity-setsd

新建一个\ ``.vbs``\ 文件，内容如下。

::

   strSD = array(1, 0, 4, 129, 160, 0, 0, 0, 176, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 2, 0, 140, 0, 6, 0, 0, 0, 0, 0, 24, 0, 33, 0, 2, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 46, 2, 0, 0, 0, 0, 24, 0, 33, 0, 2, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 47, 2, 0, 0, 0, 18, 24, 0, 63, 0, 6, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0, 0, 18, 20, 0, 19, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 5, 20, 0, 0, 0, 0, 18, 20, 0, 19, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 5, 19, 0, 0, 0, 0, 18, 20, 0, 19, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 5, 11, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0, 1, 2, 0, 0, 0, 0, 0, 5, 32, 0, 0, 0, 32, 2, 0, 0)
   set namespace = createobject(“wbemscripting.swbemlocator").connectserver(,"root\CIMV2″)
   set security = namespace.get(“__systemsecurity=@")
   nStatus = security.setsd(strSD)

就可以通过这个vbs导入安全描述符(security descriptor)
