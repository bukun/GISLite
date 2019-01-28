## 基于 MapServer 的服务器端GIS数据图层发布管理系统。

目的是用于解决发布较多数量的地图时的数据更新、样式修改，以及不同样式组合应用的问题。

尽量实现数据源唯一，使用 XLSX 文件定义样式。

主要实现GIS数据图层的发布，但也实现了多源数据发布为单个地图切片，以及多个图层发布为图层分组的功能。

- 基于MapServer、MapProxy
- 使用开放电子表格格式 XLSX 定义样式
- 可用于团队地理信息数据快速发布管理

## 本网站采用静态网站生成器制作

近年来，作为传统动态网站基础架构的替代方案，现代静态网站生成器日渐盛行。

许多导致静态网站失败的限制已不复存在。现在，每周都会有新的静态网站生成器发布。

简单来说,静态网站生成器就是一个由轻量的标记语言以及模版语言和元数据以及CSS预处理器加上可以编译成JavaScript的语言构成的用来生成静态HTML,CSS和JS文件的程序。



### 静态网站的优点


#### 访问速度快

即使是最为优化的动态网站，其性能也无法同静态网站相比。并且，对于动态网站而言，缓存失效非常难以恢复，尤其是需要充分利用CDN的分布式缓存。静态网站所有内容都储存在html里面，不需要后台服务器对内容进行渲染，避免了查询数据库等操作，而且可以充分利用缓存和CDN

#### 非常安全

动态网站容易遭受蠕虫攻击。据保守估计，超过70%的WordPress部署容易因为已知漏洞遭受攻击（超过23%的Web网站以WordPress为基础构建）。网站安全两大威胁SQL注入和XSS（cross-site scritpting）攻击，静态站点都可以很好的避免

#### 易于部署

没有后端要求，想部署在哪儿就部署在哪儿。服务器端配置简单。只需要一个web server（apache、nginx）。

#### 利于版本控制

静态网站是由静态文件组成，所以非常容易使用Git等工具进行版本控制，非常容易维护。


## 运行方式

 
### MapProxy使用

使用了 MapProxy 生成地图切片。下面是脚本运行的方式。

mapproxy-util serve-develop ./mapproxy.yaml -b 0.0.0.0:8011
~/.local/bin/mapproxy-util serve-develop ./out_mapproxy.yaml -b 0.0.0.0:8011
mapproxy-util create -t base-config wcs_imgmap
~/.local/bin/mapproxy-util create -t base-con

### 搭建简易HTTP服务 
 
/gislite/目录下运行一下代码
 
python3 -m http.server 8080

### 生成静态页面

python3 run_gislite.py
 
#### 以上步骤成功运行后，浏览器输入 http://127.0.0.1：8080 访问即可。 