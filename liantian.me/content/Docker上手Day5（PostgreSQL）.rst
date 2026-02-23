Docker上手Day5（PostgreSQL）
############################

:title: Docker上手Day5（PostgreSQL）
:Date: 2019-07-13
:Modified: 2019-07-13
:Tags: Tech
:Slug: docker-day-5
:Summary: 奇怪的知识点: import/export的缺点，cmd和entrypoint的区别

今天学习到的奇怪的知识点：

-  export/import 丢失的信息比较多：env entrypoint cmd全会丢
-  cmd和entrypoint的区别。cmd设计被用来容易覆盖。entrypoint不容易。

开搞 下载官方镜像，打包tar，清理

::

   docker create --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword  postgres:9.6-alpine
   docker export some-postgres  > postgres.export.9.6.17.tar
   docker container rm some-postgres

回到无网生产机..
创建docker时的密码是可以修改的。修改后这个环境变量就没用了。

::

   docker import postgres.export.9.6.17.tar  postgres:9.6.17
   sudo mkdir -p /DATA/database/psql9.6/

   docker create \
       --name some-postgres \
       -e LANG=en_US.utf8 \
       -e PGDATA=/var/lib/postgresql/data \
       -e POSTGRES_PASSWORD=mysecretpassword \
       -v /DATA/database/psql9.6:/var/lib/postgresql/data \
       -p 5432:5432  \
       --entrypoint "docker-entrypoint.sh" \
       postgres:9.6.17 \
       postgres

使用docker，新建用户，新建数据库

::

   docker exec -it some-postgres sh
   su - postgres

   createuser liantian
   createdb -O liantian liantian
   psql 
   alter user liantian with encrypted password '123456';
