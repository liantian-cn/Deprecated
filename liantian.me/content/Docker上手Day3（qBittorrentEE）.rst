Docker上手Day3（qBittorrentEE）
################################

:title: Docker上手Day3（qBittorrentEE）
:Date: 2019-07-03 19:41:50
:Modified: 2019-07-03 19:41:50
:Tags: Tech
:Slug: docker-day-3
:Summary: 在Docker中运行qBittorrentEE，这次设计如何使用一个容器编译，另一个容器运行。


安装Docker
==========

参考\ `https://mirror.tuna.tsinghua.edu.cn/help/docker-ce/ <url>`__

加源、傻瓜安装 ``apt-get install docker-ce``

**赋予当前用户用docker的权限**

``sudo usermod -aG docker $USER``

需要重启docker服务，重登user生效。

两个dockerfile
==============

**Dockerfile**

::

   FROM alpine:latest

   ENV TZ=Asia/Shanghai
   COPY ./qbittorrent /

   RUN  sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
   &&  apk update \
   &&  apk upgrade \ 
   &&  apk add --no-cache ca-certificates tzdata python3 bash nano openssl \
   &&  rm -rf /var/cache/apk/*   \
   &&  chmod a+x  /usr/local/bin/qbittorrent-nox   \
   &&  mkdir -p ~/.config/qBittorrent/ssl \
   &&  cd ~/.config/qBittorrent/ssl  \
   &&  openssl req -new -newkey rsa:4096 -x509 -nodes -days 7300 -subj "/C=CC/ST=ST/L=LL/O=Dis/CN=qbittorrent.home.local" -out server.crt -keyout server.key  \
   &&  echo "[Preferences]" >> /root/.config/qBittorrent/qBittorrent.conf \
   &&  echo "Bittorrent\AutoUpdateTrackers=true" >> /root/.config/qBittorrent/qBittorrent.conf \
   &&  echo "Bittorrent\CustomizeTrackersListUrl=https://trackerslist.com/all.txt" >> /root/.config/qBittorrent/qBittorrent.conf \
   &&  echo "WebUI\Port=8080" >> /root/.config/qBittorrent/qBittorrent.conf \
   &&  echo "WebUI\HTTPS\CertificatePath=/root/.config/qBittorrent/ssl/server.crt" >> /root/.config/qBittorrent/qBittorrent.conf \
   &&  echo "WebUI\HTTPS\KeyPath=/root/.config/qBittorrent/ssl/server.key" >> /root/.config/qBittorrent/qBittorrent.conf \
   &&  echo "WebUI\HTTPS\Enabled=false" >> /root/.config/qBittorrent/qBittorrent.conf 


   VOLUME /DATA

   EXPOSE 8080 8443 9068  9068/udp


   CMD [ "/usr/local/bin/qbittorrent-nox" ]

Dockerfile.build

::

   FROM alpine:latest
   WORKDIR /root/

   RUN  sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories                                   \
   &&   apk update                                                                                                               \
   &&   apk upgrade                                                                                                              \
   &&   apk add --no-cache  ca-certificates make g++ gcc qt5-qtsvg-dev boost-dev qt5-qttools-dev file wget unzip tar                 

   # 墙内下不动，改为拷贝                                                                                                        
   # RUN   wget https://github.com/arvidn/libtorrent/releases/download/libtorrent_1_2_7/libtorrent-rasterbar-1.2.7.tar.gz          
   # RUN   wget https://github.com/c0re100/qBittorrent-Enhanced-Edition/archive/release-4.2.5.11.zip       
   COPY libtorrent-rasterbar-1.2.7.tar.gz   .
   COPY qBittorrent-Enhanced-Edition-release-4.2.5.11.zip .

   RUN  cd /root                                                                                                                 \
   &&   tar  -zxvf  libtorrent-rasterbar-1.2.7.tar.gz                                                                           \
   &&   cd  libtorrent-rasterbar-1.2.7                                                                                           \
   &&   ./configure  --host=x86_64-alpine-linux-musl                                                                             \
   &&   make -j$(nproc) install-strip                                                                                                       


   RUN  cd /root                                                                                                              \
   &&   unzip qBittorrent-Enhanced-Edition-release-4.2.5.11.zip                                                                 \
   &&   cd qBittorrent-Enhanced-Edition-release-4.2.5.11/                                                                        \
   &&   ./configure   --disable-gui --host=x86_64-alpine-linux-musl                                                              \
   &&   make -j$(nproc) install                                                                                                             

   RUN  ldd /usr/local/bin/qbittorrent-nox   |cut -d ">" -f 2|grep lib|cut -d "(" -f 1|xargs tar -chvf /root/qbittorrent.tar   \
   &&   mkdir /qbittorrent                                                                                                       \
   &&   tar  -xvf /root/qbittorrent.tar   -C  /qbittorrent                                                                    \
   &&   cp --parents /usr/local/bin/qbittorrent-nox  /qbittorrent                                                                

脚本

::

   docker build --no-cache -t qbittorrentee:build . -f Dockerfile.build
   docker create --name extract qbittorrentee:build
   docker cp extract:/qbittorrent  .
   docker rm -f extract

   docker build --no-cache -t qbittorrentee:4.2.5.11 .


   docker create -p 8080:8080  -p 8443:8443 -p 9068:9068  -p 9068:9068/udp  -v /DATA:/DATA  --restart always --name qBittorrentEE qbittorrentee:4.2.5.11 /usr/local/bin/qbittorrent-nox

   docker start qBittorrentEE


   docker stop qBittorrentEE
   docker rm qBittorrentEE
   docker rmi  qbittorrentee:4.2.5.11


   docker export qBittorrentEE  > qBittorrentEE.export.4.2.5.11.tar

   docker import qBittorrentEE.export.4.2.5.11.tar qbittorrentee:4.2.5.11

   docker create -p 8080:8080  -p 8443:8443 -p 9068:9068  -p 9068:9068/udp  -v /DATA:/DATA  --restart always --name qBittorrentEE qbittorrentee:4.2.5.11 /usr/local/bin/qbittorrent-nox
