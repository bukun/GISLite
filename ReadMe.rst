Introduction of GISLite
===============================

In English
-------------------------------------

Static site generator (SSG) for GIS data publishment as light WebGIS application.

Example: http://www.osgeo.cn/gislite

说明
---------------------------------------

基于开源GIS技术开发，使用静态网站形式对GIS数据进行发布。

演示网站： http://www.osgeo.cn/gislite

基于 MapServer 的服务器端GIS数据图层发布管理系统。
目的是用于解决发布较多数量的地图时的数据更新、样式修改，以及不同样式组合应用的问题。
尽量实现数据源唯一，使用 XLSX 文件定义样式。
主要实现GIS数据图层的发布，但也实现了多源数据发布为单个地图切片，以及多个图层发布为图层分组的功能。

- 基于MapServer、MapProxy
- 使用开放电子表格格式 XLSX 定义样式
- 可用于团队地理信息数据快速发布管理

使用技术
-------------------------------------

- MapServer
- MapProxy
- LeafletJS
- Python 3
- Jinja2

运行方式
--------------------------

::

    run_gislite.py

或

::

    python3 run_gislite.py

相关网站
---------------------------------

-  http://www.osgeo.cn/pygis/  《Python与开源GIS》，使用 Python 读取与处理 GIS数据 的工具。
-  http://www.osgeo.cn/webgis/  涉及到 MapServer， MapProxy， Leaflet 的在线 WebGIS 教学网站 。

运行环境安装
-----------------------------------------

开发与测试运行于 Debian Stretch / Ubuntu 18.04 。 在管理员权限下安装运行环境：

::

    apt install -y apache2 php libapache2-mod-fcgid cgi-mapserver mapserver-bin libapache2-mod-php
    apt install -y python3-openpyxl python3-mapproxy
    apt install -y build-essential  python3-gdal python3-pip
    pip3 install mapproxy

另外，需要GIS数据，路径由 ``cfg.py`` 中的 ``GIS_BASE``指定。

程序需要的资源，都在 ``cfg.py`` 中定义。 ``TILE_SVR`` 是 MapProxy 服务地址。

MapProxy使用
-------------------------

使用了 MapProxy 生成地图切片。下面是脚本运行的方式。

首先建立子项目：

::

    ~/.local/bin/mapproxy-util create -t base-config wcs_imgmap

或

::

    mapproxy-util create -t base-config wcs_imgmap

然后运行：

::

    ~/.local/bin/mapproxy-util serve-develop ./out_mapproxy.yaml -b 0.0.0.0:8011

或

::

    # mapproxy-util serve-develop ./mapproxy.yaml -b 0.0.0.0:8011



