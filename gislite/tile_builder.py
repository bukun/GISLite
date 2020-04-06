# -*- coding:utf-8 -*-

'''
2. create YAML file  for MapProxy.
'''

import os
import yaml

import gislite.helper as helper
from gislite.const import TPL_MAPPROXY

from config import GIS_BASE


def dispose_serial_file(file_name, mapserver_ip, mapproxy_mold, wroot):
    """
    处理系列文件的方法
    """

    data_apth = ''
    for meta in helper.xlsx2dict(os.path.join(wroot, file_name)):
        for key in meta:
            if key == 'data':
                data_apth = meta[key]

    if '[' in data_apth:

        meta_q = data_apth.index('[')
        meta_h = data_apth.index(']')
        sig_q = data_apth[:meta_q]
        sig_h = data_apth[meta_h + 1:]

        for wwfile in os.listdir(wroot):
            if wwfile.startswith(sig_q) and wwfile.endswith(sig_h):
                the_sig = wwfile[meta_q: meta_h - 1]

                gdata = file_name.replace('[sig]', the_sig)
                gen_imagery4d(gdata, mapserver_ip, mapproxy_mold, wroot)


def run(mapserver_ip, out_yaml_file):
    '''
    Generate YAML file.
    '''
    mapproxy_tmpl = yaml.load(TPL_MAPPROXY)

    for wroot, _, wfiles in os.walk(GIS_BASE):
        if 'maplet' in wroot:
            pass
        else:
            continue
        for file_name in wfiles:
            if file_name.startswith('meta_') and file_name.endswith('.xlsx'):
                if '_mul' in file_name:
                    gen_mul_lyr(file_name, mapproxy_tmpl, wroot)
                elif '_grp' in file_name:
                    pass
                elif '[' in file_name:
                    dispose_serial_file(
                        file_name, mapserver_ip, mapproxy_tmpl, wroot
                    )
                else:
                    gen_imagery4d(
                        file_name, mapserver_ip, mapproxy_tmpl, wroot
                    )
            else:
                continue

    with open(out_yaml_file, 'w') as fo:
        yaml.dump(mapproxy_tmpl, fo, encoding='utf-8', allow_unicode=True)


def gen_mul_lyr(file_name, mapproxy_mold, wroot):
    '''
    处理多图层。
    '''
    lqian, _ = os.path.splitext(file_name)
    tmp_arr = lqian.split('_')
    if len(tmp_arr) > 2:
        lidx, lname, lslug = tmp_arr
    else:
        lidx, lslug = tmp_arr


    the_file = os.path.join(wroot, file_name)
    lyr_list = helper.lyr_list(the_file)

    sig = 'maplet_{}'.format(lslug)

    mapproxy_mold['caches'][sig] = {}
    mapproxy_mold['caches'][sig]['grids'] = ['webmercator']
    mapproxy_mold['caches'][sig]['sources'] = lyr_list
    new_dic = {'name': sig, 'title': sig, 'sources': [sig]}
    mapproxy_mold['layers'].append(new_dic)


def gen_imagery4d(file_name, mapserver_ip, mapproxy_tmpl, wroot):
    '''
    对图层进行处理，
    相关信息补充到传入的变量中。
    '''
    lqian, _ = os.path.splitext(file_name)
    file_dir = lqian.split('_')
    if len(file_dir) > 2:
        lidx, lname, lslug = file_dir
    else:
        lidx, lslug = file_dir

    mqian, mhou = os.path.split(wroot)
    _, _, mslug = mhou.split('_')
    fc_map_file = os.path.join(mqian, 'mfile_{}.map'.format(mslug))

    sig = 'maplet_{}'.format(lslug)  # 使用唯一 ID.
    mapproxy_tmpl['sources'][sig] = {}
    mapproxy_tmpl['sources'][sig]['type'] = 'wms'
    mapproxy_tmpl['sources'][sig]['image'] = {'transparent_color_tolerance': 0,
                                              'transparent_color': '#ffffff'}
    mapproxy_tmpl['sources'][sig]['req'] = {}
    mapproxy_tmpl['sources'][sig]['req']['url'] = 'http://{0}/cgi-bin/mapserv?map={1}'.format(
        mapserver_ip, fc_map_file)
    mapproxy_tmpl['sources'][sig]['req']['layers'] = 'lyr_{}'.format(lslug)
    mapproxy_tmpl['caches'][sig] = {}
    mapproxy_tmpl['caches'][sig]['grids'] = ['webmercator']
    mapproxy_tmpl['caches'][sig]['sources'] = [sig]
    new_dic = {'name': sig, 'title': sig, 'sources': [sig]}
    mapproxy_tmpl['layers'].append(new_dic)


if __name__ == '__main__':
    mapserver_ip = '127.0.0.1'
    out_yaml_file = 'out_mapproxy.yaml'
    run(mapserver_ip, out_yaml_file)
