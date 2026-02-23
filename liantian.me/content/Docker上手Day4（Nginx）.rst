Docker上手Day4（Nginx）
#######################

:title: Docker上手Day4（Nginx）
:Date: 2019-07-09 19:50:19
:Modified: 2019-07-09 19:50:19
:Tags: Tech
:Slug: docker-day-4
:Summary: 在Docker中运行Nginx，注意nginx本身的一些坑。


学习到了奇怪的知识点..

-  日志重定向到 /dev/stdout
-  错误日志重定向到/dev/stderr

然后通过docker logs 查看日志。。

下面是正文…

新建一个Dockerfile

::

   FROM alpine:latest

   RUN  sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
   &&  apk update \
   &&  apk upgrade \ 
   &&  apk add --no-cache nginx \
   &&  rm -rf /var/cache/apk/*   \
   && ln -sf /dev/stdout /var/log/nginx/access.log \
   && ln -sf /dev/stderr /var/log/nginx/error.log \
   && rm -f /etc/nginx/conf.d/default.conf \
   && mkdir -p /config/  \
   && mkdir -p /wwwroot/ \
   && mkdir -p /run/nginx \
   && sed -i 's|include /etc/nginx/conf.d/\*.conf;| include /config/nginx/conf.d/\*.conf;|g' /etc/nginx/nginx.conf


   STOPSIGNAL SIGTERM

   EXPOSE 80

   VOLUME ["/config", "/wwwroot"]
   CMD ["nginx", "-g", "daemon off;"]

这里遇到一个坑

1. 启动报错\ ``nginx: [emerg] open() "/run/nginx/nginx.pid" failed (2: No such file or directory)``\ ，解决方法：加入\ ``mkdir -p /run/nginx \``

编译Dockerfile

::

   docker build --tag nginx:20200509 .

创建配置文件目录

::

   sudo mkdir -p /DATA/config/nginx/conf.d/
   sudo mkdir -p /DATA/wwwroot/

新建配置文件/DATA/config/nginx/conf.d/default.conf

::

   server {
       listen 80 default_server;
       listen [::]:80 default_server;
       root /wwwroot;
       server_name _;
       autoindex on;
       autoindex_localtime on; 

       location / {
           # First attempt to serve request as file, then
           # as directory, then fall back to displaying a 404.
           try_files $uri $uri/ =404;
       }
   }

创建容器

::

   docker create \
     -p 80:80  \
     -v /DATA/config:/config  \
     -v /DATA/wwwroot:/wwwroot  \
     --log-driver local \
     --log-opt max-size=10m \
     --log-opt max-file=3 \
     --log-opt compress=true \
     --restart always \
     --name nginx \
     nginx:20200509 

导出容器

::

   docker export nginx  > nginx.export.tar

清理

::

   docker stop nginx
   docker container rm nginx
   docker image rm nginx:20200509

在生产机导入

::

   docker import nginx.export.1.16.1.tar  nginx:1.16.1

   docker create \
     -p 80:80  \
     -v /DATA/config:/config  \
     -v /DATA/wwwroot:/wwwroot  \
     --log-driver local \
     --log-opt max-size=10m \
     --log-opt max-file=3 \
     --log-opt compress=true \
     --restart always \
     --name nginx \
     nginx:1.16.1 \
     nginx -g 'daemon off;'
