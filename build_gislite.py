# -*- coding: utf-8 -*-
"""
发布程序入口
"""
import os
import shutil
import time

from gislite import layer_builder
from gislite import tile_builder
from gislite import site_builder
from gislite import sphinx_builder


from config import TILE_SVR

STR_RUN_WCS_TMPL = '''#!/bin/bash
# mapproxy-util create -t base-config wcs_imgmap
# /usr/lib/python3-mapproxy/mapproxy-util serve-develop ./mapproxy.yaml -b 0.0.0.0:{port}
# ~/.local/bin/mapproxy-util serve-develop ./mapproxy.yaml -b 0.0.0.0:{port}
# mapproxy-util serve-develop ./mapproxy.yaml -b 0.0.0.0:{port}
/usr/lib/python3-mapproxy/mapproxy-util serve-develop ./mapproxy.yaml -b 0.0.0.0:{port}
'''

mapserver_ip = '127.0.0.1'
out_yaml_file = 'out_mapproxy.yaml'

start_time = time.time()

###########################################################

print('generating mapfiles ...')
layer_builder.run_it()
print('generating mapproxy yaml ...')
tile_builder.gen_yaml_file(mapserver_ip, out_yaml_file)
print('building for website ...')
site_builder.run_it()
print('building for Sphinx ...')
sphinx_builder.run_it()

###########################################################
wcs_cache_dir = 'wcs_imgmap/cache_data'
if os.path.exists(wcs_cache_dir):
    shutil.rmtree(wcs_cache_dir)
else:
    os.makedirs(wcs_cache_dir)
shutil.move(out_yaml_file, './wcs_imgmap/mapproxy.yaml')


def gen_run_mapproxy_sh():
    ###########################################################
    # 生成运行 MapProxy 的脚本
    STR_RUN_WCS = STR_RUN_WCS_TMPL.format(port=TILE_SVR.split(':')[-1])
    with open('./wcs_imgmap/run_mapproxy.sh', 'w') as fo:
        fo.write(STR_RUN_WCS)


gen_run_mapproxy_sh()

end_time = time.time()

# 保存时间戳到文件。此文件用来判断要新处理的XLSX文件。
with open('mts.log', 'w') as fo:
    fo.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))

print('Running time: ', end_time - start_time)
