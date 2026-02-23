使用ubi容器的mariadb
########################

:title: 使用ubi容器的mariadb
:Date: 2021-06-27 20:19:06
:Modified: 2021-06-27 20:19:06
:Tags: Tech
:Slug: ubi-mariadb
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

   mkdir -p /data/mariadb/datebase
   mkdir -p /data/mariadb/log
   chown -R 27:27 /data/mariadb/

制作一个Dockerfile

::

   FROM registry.redhat.io/ubi8/ubi
   RUN yum -y install bash-completion nano net-tools iputils && \
       yum -y module enable mariadb:10.3  && \
       yum -y module install mariadb   && \
       yum clean all
   RUN usermod -a -G root mysql && \
       mkdir -p /var/lib/mysql && \
       chown -R mysql:mysql /var/lib/mysql && \
       chmod 777 /var/lib/mysql
       
   USER 27
   VOLUME ["/var/lib/mysql","/var/log/mariadb/"]
   EXPOSE 3306
   STOPSIGNAL SIGINT

   CMD ["/usr/libexec/mysqld","--basedir=/usr","--datadir=/var/lib/mysql","--plugin-dir=/usr/lib64/mariadb/plugin","--log-error=/var/log/mariadb/mariadb.log"]

使用buildah构建image

::

   buildah bud -t mariadb:$(date +%Y%m%d%H%M%S) .

初始化数据库（以后升级不再需要）

::

   podman run --rm -it \
   -p 3306:3306 \
   -v /data/mariadb/log:/var/log/mariadb \
   -v /data/mariadb/datebase:/var/lib/mysql \
   -u=root \
   localhost/mariadb:20210627221353 \
   /bin/bash


   # 进入容器后执行
   mysql_install_db
   chown -R mysql:mysql /var/lib/mysql
   mysqld_safe
   /usr/bin/mysql_secure_installation

新建并运行容器

::

   podman create  \
   -p 3306:3306 \
   -v /data/mariadb/log:/var/log/mariadb \
   -v /data/mariadb/datebase:/var/lib/mysql \
   --name=MariaDB  \
   localhost/mariadb:20210627221353


   podman start MariaDB

建立数据库开通远程访问

::

   podman exec -it MariaDB bash
   mysql -u root -p

   CREATE DATABASE db_name DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
   CREATE OR REPLACE USER db_user IDENTIFIED BY 'password';

   GRANT ALL PRIVILEGES ON db_name.* TO 'db_user'@'远程ip' IDENTIFIED BY 'password' WITH GRANT OPTION;
   FLUSH PRIVILEGES;
