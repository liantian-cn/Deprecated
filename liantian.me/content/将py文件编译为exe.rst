使用cython将py文件编译为exe
#############################


:Title: 使用cython将py文件编译为exe
:Date: 2022-08-02
:Modified: 2022-08-02
:tags: Python
:Slug: making-an-executable-in-cython
:Summary: 有时候cython比pyinstaller更方便，比如用来做windows服务啥的。


首先，使用\ ``embed``\ 参数生成文件main.c

::

   cython main.py --embed -3

然后编译它：

::

   call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64

   cl main.c /I C:\Python39\include /link C:\Python39\libs\python39.lib

然后检查依赖 |sshot-1|

.. |sshot-1| image:: {static}/images/sshot-1.png
