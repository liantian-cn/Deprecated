时隔4年，重装vps记录
######################

:title: 时隔4年，重装vps记录
:Date: 2021-12-25
:Modified: 2021-12-25
:Tags: Tech
:Slug: rebuild-vps
:Summary: v2ray变成了v2fly，iptables变成了ufw，之前的VPS运行了4年没动也是神奇。


操作系统选择Debian 11..上一次安装的Debian 9还有一个月就LTS结束了。

初始化新用户
============

先用root登录到服务器

::

   ssh root@ip_address

创建新用户

::

   adduser username

为新用户增加sudo权限

::

   usermod -aG sudo username

登录新用户到服务器

::

   ssh username@ip_address

为新用户配置ssh证书登录
=======================

生成ssh密钥

::

   ssh-keygen

查看\ ``~/.ssh``\ 目录

::

   ls -l ~/.ssh/

包含\ ``id_rsa``\ 和\ ``id_rsa.pub``\ 两个文件

将公钥\ ``id_rsa.pub``\ 重命名为\ ``authorized_keys``

::

   mv ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys

将私钥\ ``id_rsa``\ 打印后，复制并保存到本地

::

   cat ~/.ssh/id_rsa

删除私钥

::

   rm ~/.ssh/id_rsa

修复文件的权限，不然无法正常工作

::

   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys

尝试使用私钥登录..

为新用户配置免密sudo
====================

尝试切换到\ ``root``

::

   sudo su - root

去掉sudo的密码，编辑\ ``/etc/sudoers``

::

   %sudo   ALL=(ALL:ALL) NOPASSWD: ALL

关掉密码登录ssh和root登录ssh权限
================================

编辑\ ``/etc/ssh/sshd_config``

注释掉 PermitRootLogin yes

::

   #PermitRootLogin yes

修改\ ``PasswordAuthentication``

::

   PasswordAuthentication no

重启ssh服务

::

   systemctl restart sshd.service

更新系统
========

::

   apt update -y && apt upgrade -y

安装设置防火墙
==============

安装\ ``ufw``

::

   apt update
   apt install ufw

查看ufs的应用列表

::

   ufw app list

运行OpenSSH，并激活防火墙。

::

   ufw allow OpenSSH
   ufw enable

查询ufw的状态

::

   ufw status numbered

多余的行号，可用\ ``ufw delete 行号``\ 删掉

安装v2ray
=========

参考:https://www.v2fly.org/guide/install.html

::

   apt install v2ray

-  修改配置文件: ``/etc/v2ray/config.json``
-  重启服务: ``systemctl restart v2ray.service``
-  验证端口开启: ``netstat -an | grep LISTEN``

安装nginx
=========

::

   apt install nginx

   cd /etc/nginx/sites-enabled/
   ln -s ../sites-available/nginx配置

过程中可以关闭ufw便于调试\ ``ufw disable``

配置仅允许cloudflare流量访问nginx
=================================

::

   curl -s https://www.cloudflare.com/ips-v4 -o /tmp/cf_ips

   for cfip in `cat /tmp/cf_ips`; do ufw allow from $cfip to any app WWW comment 'Cloudflare'; done

   curl -s https://www.cloudflare.com/ips-v6 -o /tmp/cf_ips

   for cfip in `cat /tmp/cf_ips`; do ufw allow from $cfip to any app WWW comment 'Cloudflare'; done

查询ufw的状态

::

   ufw status numbered

配置每周自动更新
================

``crontab -e`` 加入

::

   50 19 * * 3  /usr/bin/apt update -q -y >> /var/log/apt/automaticupdates.log
   0 20 * * 3  /usr/bin/apt upgrade -q -y >> /var/log/apt/automaticupdates.log

为nginx配置ssl
==============

::

    openssl genrsa -out null.key 2048

    openssl req \
   -subj "/C=US/ST=NULL/L=NULL/O=NULL/OU=NULL/CN=NULL/emailAddress=NULL@example.com" \
   -new \
   -key null.key \
   -out null.csr

   openssl x509 \
   -req \
   -days 3650 \
   -in null.csr \
   -signkey null.key \
   -out null.crt

   cp null.crt /etc/nginx/
   cp null.key /etc/nginx/

修改对应的nginx站点配置

::

       listen              80;  < -  原本的配置
       listen              443 ssl;
       ssl_certificate     null.crt;
       ssl_certificate_key null.key;

开启防火墙

::

   ufw allow "WWW Secure"
