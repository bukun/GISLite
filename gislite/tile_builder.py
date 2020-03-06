# -*- coding:utf-8 -*-

'''
2. create YAML file  for MapProxy.
'''

import os
import yaml

from config import GIS_BASE
import gislite.helper as helper
from gislite.helper import TPL_MAPPROXY


# pylint: disable=invalid-name
# pylint: disable=unused-variable
# 针对未使用的变量进行忽略

# raw_yaml = ''
# # if os.path.exists('/home/bk/wcs_maplet/mapproxy.yaml'):
# #     raw_yaml = '/home/bk/wcs_maplet/mapproxy.yaml'
# # else:
# #     pass


def chuli_serial_file(file_name, mapserver_ip, mapproxy_mold, wroot):
    """
    处理一系列文件的方法
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

                # shp = os.path.join(wroot, wwfile)
                npng = file_name.replace('[sig]', the_sig)
                gen_imagery4d(npng, mapserver_ip, mapproxy_mold, wroot)


def gen_yaml_file(mapserver_ip, out_yaml_file):
    '''
    Generate YAML file.
    '''

    mapproxy_mold = yaml.load(TPL_MAPPROXY)

    for wroot, wdirs, wfiles in os.walk(GIS_BASE):
        if 'maplet' in wroot:
            pass
        else:
            continue
        for file_name in wfiles:
            if file_name.startswith('meta_') and file_name.endswith('.xlsx'):
                if '_mul' in file_name:
                    gen_mul_lyr(file_name, mapproxy_mold, wroot)
                elif '_grp' in file_name:
                    pass
                elif '[' in file_name:
                    chuli_serial_file(file_name, mapserver_ip, mapproxy_mold, wroot)
                else:
                    gen_imagery4d(file_name, mapserver_ip, mapproxy_mold, wroot)

            else:
                continue

    with  open(out_yaml_file, 'w') as fo:
        yaml.dump(mapproxy_mold, fo, encoding='utf-8', allow_unicode=True)


def gen_mul_lyr(file_name, mapproxy_mold, wroot):
    '''
    处理多图层。
    '''
    lqian, lhou = os.path.splitext(file_name)
    xxuu = lqian.split('_')
    if len(xxuu) > 2:
        lidx, lname, lslug = xxuu
    else:
        lidx, lslug = xxuu
        # lname = xxuu[-1]

    mqian, mhou = os.path.split(wroot)
    # midx, mname, mslug = mhou.split('_')

    the_file = os.path.join(wroot, file_name)
    lyr_list = helper.lyr_list(the_file)
    # (lyr_name, lyr_ext) = os.path.splitext(png)
    # lyr_name_arr = lyr_name.split('_')
    # the_name = '_'.join(lyr_name_arr[1:])
    # sig = 'maplet_' + the_name

    # with category
    # sig = 'maplet_{}_{}'.format(mslug, lslug)
    # with uid.
    sig = 'maplet_{}'.format(lslug)

    mapproxy_mold['caches'][sig] = {}
    mapproxy_mold['caches'][sig]['grids'] = ['webmercator']
    mapproxy_mold['caches'][sig]['sources'] = lyr_list
    new_dic = {'name': sig, 'title': sig, 'sources': [sig]}
    mapproxy_mold['layers'].append(new_dic)


def gen_imagery4d(file_name, mapserver_ip, mapproxy_mold, wroot):
    '''
    对图层进行处理，
    相关信息补充到传入的变量中。
    '''
    lqian, lhou = os.path.splitext(file_name)
    file_dir = lqian.split('_')
    if len(file_dir) > 2:
        lidx, lname, lslug = file_dir
    else:
        lidx, lslug = file_dir
        # lname = xxuu[-1]

    mqian, mhou = os.path.split(wroot)
    midx, mname, mslug = mhou.split('_')
    fc_map_file = os.path.join(mqian, 'mfile_{}.map'.format(mslug))

    # (lyr_name, lyr_ext) = os.path.splitext(png)
    # lyr_name_arr = lyr_name.split('_')
    # the_name = '_'.join(lyr_name_arr[1:])

    # sig = 'maplet_{}_{}'.format(mslug, lslug)  # 使用分类的 slug
    sig = 'maplet_{}'.format(lslug)  # 使用唯一 ID.
    # fo.write(tmpl.format('maplet_' + sig))
    mapproxy_mold['sources'][sig] = {}
    mapproxy_mold['sources'][sig]['type'] = 'wms'
    mapproxy_mold['sources'][sig]['image'] = {'transparent_color_tolerance': 0,
                                              'transparent_color': '#ffffff'}
    mapproxy_mold['sources'][sig]['req'] = {}
    mapproxy_mold['sources'][sig]['req']['url'] = 'http://{0}/cgi-bin/mapserv?map={1}'.format(
        mapserver_ip, fc_map_file)
    mapproxy_mold['sources'][sig]['req']['layers'] = 'lyr_{}'.format(lslug)
    mapproxy_mold['caches'][sig] = {}
    mapproxy_mold['caches'][sig]['grids'] = ['webmercator']
    mapproxy_mold['caches'][sig]['sources'] = [sig]
    new_dic = {'name': sig, 'title': sig, 'sources': [sig]}
    mapproxy_mold['layers'].append(new_dic)


if __name__ == '__main__':
    mapserver_IP = '127.0.0.1'

    # mapserver_ip = '159.226.123.26' 也可以将IP设置为自己的IP
    out_yaml_file = 'out_mapproxy.yaml'

    gen_yaml_file(mapserver_IP, out_yaml_file)
