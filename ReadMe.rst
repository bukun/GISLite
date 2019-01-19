Introduction of GISLite
===============================

In English
-------------------------------------

Static site generator (SSG) for GIS data publishment as light WebGIS application.

Example: http://lyr.osgeo.cn/

说明
---------------------------------------

使用静态网站形式对GIS数据进行发布。

演示网站： http://lyr.osgeo.cn/

基于 MapServer 的服务器端GIS数据图层发布管理系统。
目的是用于解决发布较多数量的地图时的数据更新、样式修改，以及不同样式组合应用的问题。
尽量实现数据源唯一，使用 XLSX 文件定义样式。
主要实现GIS数据图层的发布，但也实现了多源数据发布为单个地图切片，以及多个图层发布为图层分组的功能。

- 基于MapServer、MapProxy
- 使用开放电子表格格式 XLSX 定义样式
- 可用于团队地理信息数据快速发布管理


运行方式
--------------------------

::

    run_gislite.py

相关网站
---------------------------------

-  http://pygis.osgeo.cn/  《Python与开源GIS》，使用 Python 读取与处理 GIS数据 的工具。
-  http://webgis.osgeo.cn/  对 MapServer， MapProxy， Leaflet 的基本介绍。

MapProxy使用
-------------------------

使用了 MapProxy 生成地图切片。下面是脚本运行的方式。

::

    mapproxy-util serve-develop ./mapproxy.yaml -b 0.0.0.0:8011
    ~/.local/bin/mapproxy-util serve-develop ./out_mapproxy.yaml -b 0.0.0.0:8011
    mapproxy-util create -t base-config wcs_imgmap
    ~/.local/bin/mapproxy-util create -t base-con