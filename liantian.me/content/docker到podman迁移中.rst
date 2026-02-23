Docker上手Day X（迁移到podman）
###############################

:title: Docker上手Day X（迁移到podman）
:Date: 2021-05-10 20:03:33
:Modified: 2021-05-10 20:03:33
:Tags: Tech
:Slug: docker-day-x
:Summary: Podman 原来是CRI-O项目的一部分。Podman 的使用体验和Docker 类似


安装：

::

   yum module install -y container-tools

登录RH账号：

::

   podman login registry.redhat.io

拉取最小镜像：

::

   podman pull registry.redhat.io/ubi8/ubi-minimal

运行一个叫\ ``mybash``\ 的容器，启动bash

::

   podman run --name=mybash -it registry.redhat.io/ubi8/ubi-minimal /bin/bash

再次启动\ ``mybash``

::

   podman start -ai mybash

制作一个开发环境，新建Dockerfile

::

   FROM registry.redhat.io/ubi8/ubi-init

   RUN dnf install bash-completion nano  --nodocs
   RUN rm -f /etc/localtime
   RUN cp  /usr/share/zoneinfo/Asia/Shanghai /etc/localtime



   ############################################################
   # 安装 SSH
   ############################################################

   RUN dnf install openssh-server passwd --nodocs
   RUN ssh-keygen -t dsa -P "" -f /etc/ssh/ssh_host_dsa_key  <<< y
   RUN ssh-keygen -t rsa -P "" -f /etc/ssh/ssh_host_rsa_key   <<< y
   RUN ssh-keygen -t ecdsa -P "" -f /etc/ssh/ssh_host_ecdsa_key   <<< y
   RUN ssh-keygen -t ed25519 -P "" -f /etc/ssh/ssh_host_ed25519_key   <<< y
   RUN echo "root:root" | chpasswd
   RUN systemctl enable sshd


   ############################################################
   # 安装 Python , 同时安装pip，设置为清华源。
   ############################################################

   RUN dnf install -y python38 python38-psycopg2 python38-PyMySQL python38-jinja2 python38-numpy python38-requests python38-scipy python38-setuptools python38-pip
   RUN dnf clean all
   RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   RUN pip3 install --no-cache-dir django django-debug-toolbar django-rq django-redis 

   EXPOSE 22 8000 8080 

启动这个开发环境

::

   buildah bud -t devenv .
   podman run    -p 8080:8080 -p 8000:8000 -p 31022:22 -name DevENV localhost/devenv
