# -*- coding: utf-8 -*-

'''
Replacement for site_builder. Using Sphinx to generate website.
'''

import os
import gislite.helper as helper

from config import GIS_BASE

# tpl_ws = os.path.join(os.getcwd(), 'static')
SPHINX_SRC = os.path.join(os.getcwd(), 'dist_sphinx/source')

if os.path.exists(SPHINX_SRC):
    pass
else:
    os.makedirs(SPHINX_SRC)


def generate_chfile(chdir, title):
    '''
    Generate rst file for chapter.
    '''
    chfile = os.path.join(chdir, 'chapter.rst')

    with open(chfile, 'w') as fileo:
        fileo.write('''{title}
=============================================

{title}
        
'''.format(title=title))


def gen_html_pages2(wroot, idx_dir=0):
    '''
    处理 HTML 文件
    '''

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

        outdir = os.path.join(SPHINX_SRC, 'ch{}-'.format(str(idx_dir).zfill(2)) + mslug)

        if os.path.exists(outdir):
            pass
        else:
            os.mkdir(outdir)

        generate_chfile(outdir, mname)

        if '_grp' in md_file:
            layers = helper.lyr_list(os.path.join(wroot, md_file))

            out_html_file = os.path.join(
                outdir,
                'sec{}-'.format(str(idx_file + 1).zfill(2)) + file_slug + '.rst'
            )
            with open(out_html_file, 'w') as fo:
                fo.write('''{lname}
==========================================

{mname}——{lname} 。

.. raw:: html

  <div id="map_kd1" data-maplet="{file_slug}" data-title="{lname}"></div>
   


'''.format(mname=mname, lname=lname, file_slug=','.join(layers)))

        elif '[' in md_file:
            dispose_serial_file(wroot, md_file, lname, lslug, mname, outdir)
        else:
            out_html_file = os.path.join(
                outdir,
                'sec{}-'.format(str(idx_file + 1).zfill(2)) + file_slug + '.rst'
            )
            with open(out_html_file, 'w') as fo:
                fo.write('''{lname}
==========================================

{mname}——{lname} 。

.. raw:: html

  <div id="map_kd1" data-maplet="maplet_{file_slug}" data-title="{lname}"></div>
   


'''.format(mname=mname, lname=lname, file_slug=file_slug))


def dispose_serial_file(wroot, mdfile, lname, lslug, mname, outdir):
    '''
    处理满足条件的序列数据
    '''
    png = mdfile

    rrxlsx_file = os.path.join(wroot, png)

    data_apth, h_place, q_place = parse_serial_filename(rrxlsx_file)
    sig_q = data_apth[:q_place]
    sig_h = data_apth[h_place + 1:]

    idx_file = 0
    for wwfile in os.listdir(wroot):

        if wwfile.startswith(sig_q) and wwfile.endswith(sig_h):
            the_sig = wwfile[q_place: h_place - 1]

            npng = png.replace('[sig]', the_sig)
            print(npng)
            file_slug = '{}'.format(lslug.replace('[sig]', the_sig))

            file_name = 'sec{}-'.format(str(idx_file + 1).zfill(2)) + file_slug + '.rst'

            out_html_file = os.path.join(outdir, file_name)
            idx_file = idx_file + 1
            print(out_html_file)

            with open(out_html_file, 'w') as fo:
                fo.write('''{lname}{sig}
==========================================

{mname}——{lname}{sig} 。

.. raw:: html

  <div id="map_kd1" data-maplet="maplet_{file_slug}" data-title="{lname}{sig}"></div>
   


'''.format(mname=mname, lname=lname[: lname.index('[')], file_slug=file_slug, sig=the_sig))


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

    q_place = data_apth.index('[')
    h_place = data_apth.index(']')
    return data_apth, h_place, q_place


def run():
    '''
    根据输入的 MarkDown 文件，生成 HTML 结果。
    '''

    the_dirs = os.listdir(GIS_BASE)
    the_dirs = [x for x in the_dirs if os.path.isdir(os.path.join(GIS_BASE, x)) and 'maplet' in x]
    the_dirs.sort()

    for idx_dir, the_dir in enumerate(the_dirs):
        wroot = os.path.join(GIS_BASE, the_dir)
        if os.path.isdir(wroot) and 'maplet' in wroot:
            gen_html_pages2(wroot, idx_dir=idx_dir + 1)
        else:
            continue


if __name__ == '__main__':
    run()
