迁移到Cloudflare Pages
#######################

:title: 迁移到Cloudflare Pages
:Date: 2022-06-07
:Modified: 2022-06-07
:Tags: Tech
:Slug: migrate-from-github-pages-to-cloudflare-pages
:Summary: 从Github Pages迁移到Cloudflare Pages，Cloudflare不够给力，但还是香。



缘起
====

就是瞎折腾，想折腾了..

Cloudflare Pages对Python支持还是不太够。
========================================

-  首先是python版本支持不够，参考\ `Build
   configuration <https://developers.cloudflare.com/pages/platform/build-configuration>`__\ ，\ ``2.7, 3.5, 3.7 only``
-  不支持\ ``requirements.txt``\ ，可以写\ ``runtime.txt`` 或
   ``Pipfile``\ ，但是不习惯。
-  费大劲安装了用\ ``Pipfile``\ 安装了\ ``pelican``\ ，发现\ ``pelican``\ 不在环境变量。虽然google一大圈知道在\ ``/opt/buildhome/.local/bin``\ 了，但也太不人性化了。

解决方法嘛，当然是继续用\ ``Github Actions``\ 。
================================================

方法就按下面这么写…

去repo的\ ``settings/secrets/actions``\ 建立几个\ ``secrets``

-  GITHUB_TOKEN：这玩意是全局默认的，不用管。
-  CLOUDFLARE_API_TOKEN：去\ `api-tokens <https://dash.cloudflare.com/profile/api-tokens>`__\ 新建一个Token，权限仅限对
   ``帐户.Cloudflare Pages`` 的 ``编辑`` 权限 即可。
-  CLOUDFLARE_ACCOUNT_ID：就是返回首页后，你的网址
   ``https://dash.cloudflare.com/``\ 后面那串字符。

.. code:: yaml

   # This is a basic workflow to help you get started with Actions

   name: CI

   # Controls when the workflow will run
   on:
     # Triggers the workflow on push or pull request events but only for the "master" branch
     push:
       branches: [ "main" ]


     # Allows you to run this workflow manually from the Actions tab
     workflow_dispatch:

   # A workflow run is made up of one or more jobs that can run sequentially or in parallel
   jobs:
     # This workflow contains a single job called "build"
     build:
       # The type of runner that the job will run on
       runs-on: ubuntu-latest

       # Steps represent a sequence of tasks that will be executed as part of the job
       steps:
         # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
         - uses: actions/checkout@v3


         - name: Setup Python
           uses: actions/setup-python@v3.1.2
           with:
              python-version: 3.9
              cache: 'pip'
        
         - name: Install dependencies
           run: pip install -r requirements.txt
           
         - name: Build
           run: pelican  content -o ./output -s "publishconf.py"

         - name: Cloudflare Pages GitHub Action
           # You may pin to the exact commit or the version.
           # uses: cloudflare/pages-action@752c4fc911d149221a4173136118c3cc250e9409
           uses: cloudflare/pages-action@1.0.0
           with:
             # Cloudflare API Token
             apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
             # Cloudflare Account ID
             accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
             # The name of the Pages project to upload to
             projectName: liantian-log
             # The directory of static assets to upload
             directory: output
             # GitHub Token
             gitHubToken: ${{ secrets.GITHUB_TOKEN }}
         
