# -*- coding: utf-8 -*-

'''
3. Running with python3, with markdown module.
'''
# pylint: disable=invalid-name
# pylint: disable=unused-variable
import os
import shutil
import markdown

# import gislite.helper as helper

from config import GIS_BASE, TILE_SVR

# pwd = os.getcwd()

src_ws = GIS_BASE
tpl_ws = os.path.join(os.getcwd(), 'static')
dst_ws = os.path.join(os.getcwd(), 'dist_sphinx/source')

if os.path.exists(dst_ws):
    pass
else:
    os.mkdir(dst_ws)


def generate_chfile(chdir, title):
    chfile = os.path.join(chdir, 'chapter.rst')

    with open(chfile, 'w') as fo:
        fo.write('''{title}
=============================================

{title}
        
'''.format(title=title))


def gen_html_pages2(wroot, idx_dir=0):
    # 处理 HTML 文件
    _, the_dir = os.path.split(wroot)

    # nav_formated = format_nav(list_main)
    md_files = [x for x in os.listdir(wroot) if x.endswith('.xlsx') and x.startswith('meta_')]
    for idx_file, md_file in enumerate(md_files):
        name_before, name_after = os.path.split(the_dir)
        midx, mname, mslug = name_after.split('_')
        lqian, lhou = os.path.splitext(md_file)

        file_dirs = lqian.split('_')
        if len(file_dirs) > 2:
            lidx, lname, lslug = file_dirs
        else:
            lidx, lslug = file_dirs
            lname = file_dirs[-1]

        #  对分组(grp)的XLSX进行处理。
        # dir_idx, dir_slug, dir_title = the_dir.split('_')
        # 使用分类 slug
        # file_slug = '{}_{}'.format(mslug, lslug)
        #  使用唯一ID
        file_slug = '{}'.format(lslug)

        outdir = os.path.join(dst_ws, 'ch0{}-'.format(idx_dir) + mslug)

        generate_chfile(outdir, mname)

        if os.path.exists(outdir):
            pass
        else:
            os.mkdir(outdir)

        if '[' in md_file:
            file_slug = 'aa'
        out_html_file = os.path.join(outdir, 'sec0{}-'.format(idx_file + 1) + file_slug + '.rst')

        # if '_grp' in md_file:
        #     pass
        #
        # elif '[' in md_file:
        #     #
        #     pass
        # else:

        with open(out_html_file, 'w') as fo:
            fo.write('''{}——{}
==========================================

Contents.

.. raw:: html

  <div id="map_kd1" data-maplet="maplet_{}"></div>
   


'''.format(mname, lname, file_slug))


def chuli_serial_file(png, wroot, mslug, lslug, jinja2_file, left_nav, mname, nav=None):
    '''
    处理满足条件的序列数据
    '''

    rrxlsx_file = os.path.join(wroot, png)

    data_apth, h_place, q_place = parse_serial_filename(rrxlsx_file)
    sig_q = data_apth[:q_place]
    sig_h = data_apth[h_place + 1:]

    for wwfile in os.listdir(wroot):
        if wwfile.startswith(sig_q) and wwfile.endswith(sig_h):
            the_sig = wwfile[q_place: h_place - 1]

            npng = png.replace('[sig]', the_sig)
            print(npng)
            file_slug = '{}'.format(lslug.replace('[sig]', the_sig))
            file_name = file_slug + '.html'
            out_html_file = os.path.join(dst_ws, file_name)
            helper.render_html(
                jinja2_file,
                out_html_file,
                nav=nav,
                left_nav=left_nav,
                title=mslug + the_sig,
                mname=mname,
                lyr_name=file_slug,
                IP=TILE_SVR
            )


def parse_serial_filename(rrxlsx_file):
    '''
    对于批量的使用变量的，获取路径，以及位置。
    '''
    map_mata = helper.xlsx2dict(rrxlsx_file)
    data_apth = ''
    for mata in map_mata:
        for key in mata:
            if key == 'data':
                data_apth = mata[key]
    print('-' * 40)
    print(data_apth)
    q_place = data_apth.index('[')
    h_place = data_apth.index(']')
    return data_apth, h_place, q_place


def chuli_serial_structure(file_path, wroot):
    '''
    Deal with serial structure.
    '''
    out_arr = []

    rrxlsx_file = os.path.join(wroot, file_path)

    data_apth, h_place, q_place = parse_serial_filename(rrxlsx_file)
    sig_q = data_apth[:q_place]
    sig_h = data_apth[h_place + 1:]

    for wwfile in os.listdir(wroot):
        if wwfile.startswith(sig_q) and wwfile.endswith(sig_h):
            the_sig = wwfile[q_place: h_place - 1]
            out_arr.append(file_path.replace('[sig]', the_sig))
    return out_arr


def run_it():
    '''
    根据输入的 MarkDown 文件，生成 HTML 结果。
    '''

    the_dirs = os.listdir(src_ws)
    the_dirs = [x for x in the_dirs if os.path.isdir(os.path.join(src_ws, x)) and 'maplet' in x]
    the_dirs.sort()

    for idx_dir, the_dir in enumerate(the_dirs):
        wroot = os.path.join(src_ws, the_dir)
        if os.path.isdir(wroot) and 'maplet' in wroot:
            gen_html_pages2(wroot, idx_dir=idx_dir + 1)
        else:
            continue


if __name__ == '__main__':
    run_it()
