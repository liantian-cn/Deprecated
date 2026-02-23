redhat升级OpenSSH
##################

:title: redhat升级OpenSSH
:Date: 2021-12-04 19:04:50
:Modified: 2021-12-04 19:04:50
:Tags: Tech
:Slug: redhat-update-openssh
:Summary: 不知道为啥，国内漏扫软件都认openssh大量中危，而redhat官方却认为是小问题..


Redhat 7.x
==========

创建工作目录

::

   mkdir -pv /root/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

安装依赖

::

   yum update
   cat /etc/redhat-release
   yum -y install rpm-build gcc zlib-devel openssl-devel perl-devel pam-devel wget nano yum-utils
   yumdownloader openssl-devel --resolve --destdir=../SRPMS

下载安装包

::

   cd /root/rpmbuild/SOURCES
   wget -O openssh-8.8p1.tar.gz https://openbsd.hk/pub/OpenBSD/OpenSSH/portable/openssh-8.8p1.tar.gz
   wget -O x11-ssh-askpass-1.2.4.1.tar.gz https://src.fedoraproject.org/repo/pkgs/openssh/x11-ssh-asss-1.2.4.1.tar.gz/8f2e41f3f7eaa8543a2440454637f3c3/x11-ssh-askpass-1.2.4.1.tar.gz

解压

::

   tar xf openssh-8.8p1.tar.gz

复制\ ``spec``\ 文件

::

   cp openssh-8.8p1/contrib/redhat/openssh.spec   ../SPECS

修改\ ``openssh.spec``

::

   %global no_x11_askpass 1 
   %global no_gnome_askpass 1
   注释掉#BuildRequires: openssl-devel < 1.1 

编译

::

   rpmbuild -ba openssh.spec

在生产环境安装

::

   # 先备份
   cp -r /etc/ssh /etc/ssh.bak/
   cp -r /etc/pam.d/ /etc/pam.d.bak/
   ls -l /etc/ssh.bak/

   # 安装包
   rpm -Uvh openssh-*.rpm

   # 善后
   rm -rf /etc/ssh/ssh_host_*
   mv /etc/pam.d/sshd{,.old_$(date '+%s')}
   cp /etc/pam.d.bak/sshd /etc/pam.d/sshd

   echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
