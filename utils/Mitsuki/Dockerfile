FROM shadowsocksr-libev:latest

RUN  sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories  \
&&  apk update \
&& apk add --no-cache bash  bash-doc bash-completion nano \
&& apk add --no-cache python3 supervisor py3-pip py3-setuptools py3-flask py3-psutil py3-requests \
&& pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
&& rm -rf /var/cache/apk/* \
&& pip3 install  --no-cache-dir peewee  \
&& pip3 install  --no-cache-dir  --upgrade pip \
&& ln -s /usr/bin/python3 /usr/bin/python



RUN apk add --no-cache openssh tzdata   \
&& cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
&& ssh-keygen -t dsa -P "" -f /etc/ssh/ssh_host_dsa_key \
&& ssh-keygen -t rsa -P "" -f /etc/ssh/ssh_host_rsa_key  \
&& ssh-keygen -t ecdsa -P "" -f /etc/ssh/ssh_host_ecdsa_key  \
&& ssh-keygen -t ed25519 -P "" -f /etc/ssh/ssh_host_ed25519_key  \
&& echo "root:admin" | chpasswd



RUN rm /etc/supervisord.conf && mkdir /etc/supervisor.d/ 

COPY docker/supervisord.conf /etc/

COPY docker/fetch_url.ini /etc/supervisor.d/
COPY docker/monitor.ini /etc/supervisor.d/
COPY docker/ssrun.ini /etc/supervisor.d/
COPY docker/webserver.ini /etc/supervisor.d/

RUN mkdir /Mitsuki

COPY . /Mitsuki

EXPOSE 22 1080 8000 

CMD ["/usr/bin/supervisord"]