# -*- coding: utf-8 -*-

'''
1. Parse XLSX file, and generate Mapfile for layers.
'''
import os
import mappyfile

import gislite.const
import gislite.helper as helper
from config import GIS_BASE

MTS = helper.get_mts()


def is_lyr_def(xlsfile):
    '''
    if the xlsx file is used to define layer.
    NOT for Multiple layers, or group layers.
    '''
    if xlsfile.endswith('.xlsx'):
        if '_mul' in xlsfile or '_grp' in xlsfile:
            return False
        else:
            return True
    else:
        return False


def do_for_map_category(category_dir):
    '''
    按分类进行处理，生成总的 Mapfile.
    这个分类的文件夹名称，以 ``maplet`` 开头。
    '''
    # 得到路径与文件夹的名称
    mqian, mhou = os.path.split(category_dir)

    # 对文件夹名称进行切分，得到 索引顺序, 名称, slug
    _, _, mslug = mhou.split('_')

    fc_inc = ''
    for wroot, wdirs, wfiles in os.walk(category_dir):
        for wfile in wfiles:
            if is_lyr_def(wfile):
                # 只对 XLSX 定义的图层进行处理
                for lyr_name in get_lyrs_name(category_dir, wfile, wroot):
                    fc_inc = fc_inc + 'include "{}"\n'.format(lyr_name)

    fc_map_file = os.path.join(mqian, 'mfile_{}.map'.format(mslug))

    with open(fc_map_file, 'w') as fo2:
        tmp_str = gislite.const.TPL_MAP.format(
            basedir=category_dir,
            fc_name='map_dir_sig', fc_includes=fc_inc,
            fc_extent='{x_min} {y_min} {x_max} {y_max}'.format(
                x_min=-180,
                x_max=180,
                y_min=-90,
                y_max=90)
        )
        fo2.write(tmp_str)


def get_lyrs_name(category_dir, xlsxfile_name, wroot):
    '''
    在分类的文件夹下，得到所有图层的名称。
    '''
    rrxlsx_file = os.path.join(wroot, xlsxfile_name)
    print(rrxlsx_file)

    map_mata = helper.xlsx2dict(rrxlsx_file)

    data_path = ''
    for mata in map_mata:
        for key in mata:
            if key == 'data':
                data_path = mata[key]
    lyrs_file = []
    if '[' in data_path:
        # print('-' * 40)

        print(data_path)
        q_place = data_path.index('[')
        h_place = data_path.index(']')
        sig_q = data_path[:q_place]
        sig_h = data_path[h_place + 1:]

        for wwfile in os.listdir(wroot):
            if wwfile.startswith(sig_q) and wwfile.endswith(sig_h):
                print(wwfile)

                the_sig = wwfile[q_place: h_place - 1]
                shp = os.path.join(wroot, wwfile)

                lyr_file = generate_lyr_mapfile(
                    category_dir,
                    map_mata,
                    shp,
                    xlsxfile_name,
                    sig=the_sig
                )
                lyrs_file.append(lyr_file)

    else:
        shp = os.path.join(wroot, data_path)

        lyr_file = generate_lyr_mapfile(
            category_dir,
            map_mata,
            shp,
            xlsxfile_name
        )
        lyrs_file.append(lyr_file)

    return lyrs_file


def generate_lyr_mapfile(category_dir, map_mata, shp, wfile, sig=None):
    '''
    生成图层的 Mapfile.
    '''
    mqian, mhou = os.path.splitext(wfile)
    file_name = mqian.split('_')
    if len(file_name) > 2:
        midx, mname, mslug = file_name
    else:
        midx, mslug = file_name
    new_layer = mappyfile.loads(gislite.const.TPL_LAYER)
    shp_info = helper.get_epsg_code(shp)
    # print(shp)
    # qian, hou = os.path.split(shp)
    # shpfile_name, shpfile_ext = os.path.splitext(hou)
    # lyr_name = 'lyr_' + shpfile_name + '.map'
    if sig:
        lyr_name = 'lyr_' + mslug.replace('[sig]', sig) + '.map'
    else:
        lyr_name = 'lyr_' + mslug + '.map'
    lyr_file = os.path.join(category_dir, lyr_name)
    # if t_mts > MTS:
    if True:

        if shp_info['geom_type'].lower() in ['linestring', 'multilinestring']:
            lyr_type = 'line'
        elif shp_info['geom_type'].lower() in ['multipolygon']:
            lyr_type = 'polygon'
        else:
            lyr_type = shp_info['geom_type']
        new_layer['type'] = lyr_type
        new_layer['data'] = [shp]
        # new_layer['name'] = os.path.splitext(wfile)[0]
        if sig:
            new_layer['name'] = 'lyr_{}'.format(mslug.replace('[sig]', sig))
        else:
            new_layer['name'] = 'lyr_{}'.format(mslug)
        new_layer['metadata']['ows_title'] = os.path.splitext(wfile)[0]
        new_layer['metadata']['wms_title'] = os.path.splitext(wfile)[0]
        new_layer['PROJECTION'] = "{}".format(shp_info['proj4_code'])

        new_layer['processing'] = []
        for idx, cl in enumerate(map_mata):

            cls = mappyfile.loads(gislite.const.TPL_CLASS)
            for key in cl:
                if key.lower() == 'classitem':
                    new_layer['classitem'] = cl[key]
                elif key.lower() == 'labelitem':
                    new_layer['labelitem'] = cl[key]
                elif key.lower() == 'data':
                    new_layer['data'] = [shp]
                elif key.lower() == 'labelminscaledenom':
                    new_layer['labelminscaledenom'] = cl[key]
                elif key.lower() == 'labelmaxscaledenom':
                    new_layer['labelmaxscaledenom'] = cl[key]
                elif key.lower() == 'encoding':
                    new_layer['encoding'] = cl[key]
                elif key.lower() == 'processing':
                    #  对于影像的单独处理
                    new_layer['processing'].append(cl[key])
                elif key.lower() == 'class':
                    pass
                elif key.lower() == 'expression' and type(cl[key]) == type(1):
                    '''
                    注意，即使是使用数值作为条件，也需要添加引号。故需转换为字符串。
                    '''
                    cls[key] = str(cl[key])
                elif key.lower() == 'style':
                    for subkey in cl[key]:
                        cls['styles'][0][subkey] = cl[key][subkey]

                elif key.lower() == 'label':
                    for subkey in cl[key]:
                        cls['labels'][0][subkey] = cl[key][subkey]
                else:
                    cls[key] = cl[key]

            new_layer["classes"].insert(0, cls)
        # 去掉原来的。
        new_layer['classes'].pop()
        new_layer['classes'].pop()
        # print(help(new_layer['classes']))

        with open(lyr_file, 'w') as fo:
            fo.write(mappyfile.dumps(new_layer, indent=1, spacer="    "))
    return lyr_file


def run():
    """
    程序入口
    """
    for wroot, wdirs, wfile in os.walk(GIS_BASE):
        for wdir in wdirs:
            if wdir.startswith('maplet'):
                do_for_map_category(os.path.join(wroot, wdir))


if __name__ == '__main__':
    run()
