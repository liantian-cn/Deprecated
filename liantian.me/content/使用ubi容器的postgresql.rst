使用ubi容器的postgresql
#########################

:title: 使用ubi容器的postgresql
:Date: 2021-06-27 20:18:30
:Modified: 2021-06-27 20:18:30
:Tags: Tech
:Slug: ubi-postgresql
:Summary: ubi是Red Hat Universal Base Image的缩写，使用ubi镜像，还是蛮适合生产的。


先登陆到RH

::

   # subscription-manager register
   Registering to: subscription.rhsm.redhat.com:443/subscription
   Username: ********
   Password: **********

   # podman login registry.redhat.io

新建数据库运行路径，并设置权限

::

   mkdir -p /data/psql/datebase
   mkdir -p /data/psql/log
   chown -R 26:26 /data/psql/

制作一个Dockerfile

::

   FROM registry.redhat.io/ubi8/ubi
   RUN yum -y install bash-completion nano net-tools iputils && \
       yum -y module enable postgresql:12 && \
       yum -y module install postgresql  && \
       yum clean all
   RUN usermod -a -G root postgres && \
       mkdir -p /var/lib/pgsql/data && \
       chown -R postgres:postgres /var/lib/pgsql/data && \
       chmod 777 /var/lib/pgsql/data
       
   USER 26
   VOLUME ["/var/lib/pgsql/data"]
   EXPOSE 5432
   STOPSIGNAL SIGINT

   CMD ["postgres","-D","/var/lib/pgsql/data"]

使用buildah构建image

::

   buildah bud -t psql:$(date +%Y%m%d%H%M%S) .

初始化数据库（以后升级不再需要）

::

   podman run --rm -it \
   -p 5432:5432 \
   -v /data/psql/log:/var/log \
   -v /data/psql/datebase:/var/lib/pgsql/data \
   localhost/psql:20210627192640 \
   /bin/bash


   # 进入容器后执行
   initdb -D /var/lib/pgsql/data

新建并运行容器

::

   podman create  \
   -p 5432:5432 \
   -v /data/psql/log:/var/log \
   -v /data/psql/datebase:/var/lib/pgsql/data \
   --name=PostgreSQL  \
   localhost/psql:20210627192640


   podman start PostgreSQL
