Docker上手Day1（alpine-bash）
#############################

:title: Docker上手Day1（alpine-bash）
:Date: 2019-06-29 20:19:46
:Modified: 2019-06-29 20:19:46
:Tags: Tech
:Slug: docker-day-1
:Summary: 在Docker中运行bash，这是从虚拟机转向Docker的基础。

-  新建一个DockerFile，内容如下

.. code:: bash

   FROM alpine:latest

   RUN  sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \
   apk update && \
   apk upgrade  && \
   apk add --no-cache bash bash-doc bash-completion

   CMD ["/bin/bash"]

生成这个镜像文件

.. code:: bash

   buildah bud -t alpine-bash:latest .

执行这个镜像，\ ``--rm``\ 将在退出时删除。

.. code:: bash


   podman run --rm -it alpine-bash
