# -*- coding: utf-8 -*-

'''
3. Running with python3, with markdown module.
'''
# pylint: disable=invalid-name
# pylint: disable=unused-variable
import os
import shutil
import markdown

import gislite.helper as helper

from config import GIS_BASE, TILE_SVR

# pwd = os.getcwd()

src_ws = GIS_BASE
tpl_ws = os.path.join(os.getcwd(), 'static')
dst_ws = os.path.join(os.getcwd(), 'dist_site')

if os.path.exists(dst_ws):
    pass
else:
    os.mkdir(dst_ws)


def markdown2html(markdown_text):
    '''
    Convert markdown text to HTML. with extensions.
    '''
    html = markdown.markdown(
        markdown_text,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
            'markdown.extensions.meta'
        ]
    )
    han_biaodians = ['。', '，', '；', '、', '！', '？']
    for han_biaodian in han_biaodians:
        html = html.replace(han_biaodian + '\n', han_biaodian)
    return html


def format_nav(list_main):
    '''
    格式化菜单导航栏
    '''
    a_nav = '''<li class="dropdown">
        <a href="{nav_slug}.html" class="dropdown-toggle" data-toggle="dropdown">
         {nav_title} <b class="caret"></b></a>
        <ul class="dropdown-menu">{nav_arr}</ul></li>'''
    a_md = '<li><a href="{slug}.html">{title}</a></li>\n'

    out_str = ''

    for idx_list, the_list in enumerate(list_main):
        sub_str = ''
        for idx_link, the_link in enumerate(the_list['list_md']):
            a_md_f = a_md.format(slug=the_link['slug'], title=the_link['title'])
            sub_str = sub_str + a_md_f

        a_nav_f = a_nav.format(
            nav_arr=sub_str,
            nav_slug=the_list['list_md'][0]['slug'],
            nav_title=the_list['title']
        )
        out_str = out_str + a_nav_f

    return out_str


def format_leftnav(list_main, mname):
    '''
    格式化左侧导航栏
    '''
    a_nav = '''<li>
<a href="#configSetting{idx}" class="nav-header collapsed" data-toggle="collapse">
<i class="glyphicon glyphicon-th-list"></i>
{nav_title}
<span class="pull-right glyphicon  glyphicon-chevron-toggle"></span>
</a>
<ul id="configSetting{idx}" class=" secondmenu collapse  {ul_class}">{nav_arr}</ul>
</li>
'''
    a_md = '''<li style="padding:8px 0;overflow: hidden; 
text-overflow:ellipsis; white-space: nowrap;">
<a href="{slug}.html">{title}</a></li>'''

    out_str = ''
    idx = 1
    for idx_list, the_list in enumerate(list_main):
        sub_str = ''

        ul_class = ''
        for idx_link, the_link in enumerate(the_list['list_md']):
            a_md_f = a_md.format(slug=the_link['slug'], title=the_link['title'])
            sub_str = sub_str + a_md_f

        if the_list['title'] == mname:
            ul_class = 'in'

        a_nav_f = a_nav.format(
            nav_arr=sub_str,
            nav_slug=the_list['list_md'][0]['slug'],
            nav_title=the_list['title'],
            idx=idx,
            ul_class=ul_class
        )
        idx = idx + 1
        out_str = out_str + a_nav_f

    return out_str


def format_cntnav(cnt_arr):
    '''
    格式化内容导航栏
    '''
    tpl = '''<li {sig}><a href="#{index}">{title}</a></li>'''
    out_str = ''
    for idx, title in enumerate(cnt_arr):
        if idx == 0:
            the_str = tpl.format(index=title['key'], title=title['val'], sig='class="active"')
        else:
            the_str = tpl.format(index=title['key'], title=title['val'], sig='')
        out_str = out_str + the_str
    return out_str


def gen_html_pages():
    '''
    根据输入的 MarkDown 文件，生成 HTML 结果。
    '''

    the_dirs = os.listdir(src_ws)
    the_dirs.sort()

    for idx_dir, the_dir in enumerate(the_dirs):
        wroot = os.path.join(src_ws, the_dir)
        if os.path.isdir(wroot) and 'maplet' in wroot:
            gen_html_pages2(wroot)
        else:
            continue


def gen_html_pages2(wroot):
    # 处理 HTML 文件
    _, the_dir = os.path.split(wroot)
    list_main = fetch_structure()
    nav_formated = format_nav(list_main)
    md_files = [x for x in os.listdir(wroot) if x.endswith('.xlsx') and x.startswith('meta_')]
    for idx_file, md_file in enumerate(md_files):
        name_before, name_after = os.path.split(the_dir)
        midx, mname, mslug = name_after.split('_')
        lqian, lhou = os.path.splitext(md_file)
        left_nav = format_leftnav(list_main, mname)
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
        out_html_file = os.path.join(dst_ws, file_slug + '.html')
        jinja2_file = 'templates/lyr.jinja2'
        jinja2_file = '/'.join(jinja2_file.split('/')[1:])

        if '_grp' in md_file:
            #  处理。
            helper.render_html(
                'lyrgrp.jinja2',
                out_html_file,
                nav=nav_formated,
                layers=helper.lyr_list(os.path.join(wroot, md_file)),
                IP=TILE_SVR,
                left_nav=left_nav,
                title=lname,
                mname=mname
            )
        elif '[' in md_file:
            dispose_serial_file(md_file, wroot, mslug, lslug, jinja2_file, left_nav, mname,
                                nav=nav_formated)
        else:
            helper.render_html(
                jinja2_file,
                out_html_file,
                nav=nav_formated,
                lyr_name=file_slug,
                IP=TILE_SVR,
                left_nav=left_nav,
                title=lname,
                mname=mname
            )


def dispose_serial_file(png, wroot, mslug, lslug, jinja2_file, left_nav, mname, nav=None):
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


def gen_html_index():
    '''
    生成首页 index.html
    '''
    list_main = fetch_structure()
    nav_formated = format_nav(list_main)
    left_nav = format_leftnav(list_main, '')
    index_in = 'index.jinja2'
    index_out = os.path.join(dst_ws, 'index.html')

    helper.render_html(index_in, index_out, nav=nav_formated, left_nav=left_nav)


def dispose_serial_structure(file_path, wroot):
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


def fetch_structure():
    '''
    对网站目录、文件进行遍历；
    以列表形式，返回网站的目录结构。
    '''
    the_dirs = os.listdir(src_ws)

    list_main = []
    the_dirs.sort()
    for the_dir in the_dirs:
        if the_dir in ['symbols', 'fonts']:
            continue
        xx_dir = os.path.join(src_ws, the_dir)

        if os.path.isdir(xx_dir) and 'maplet' in xx_dir:
            pass
        else:
            continue

        wroot = os.path.join(src_ws, the_dir)

        the_files = os.listdir(wroot)
        the_files = [x for x in the_files if x.endswith('.xlsx') and x.startswith('meta_')]

        for xlsfile in the_files:
            if '[' in xlsfile:
                serial_arr = dispose_serial_structure(xlsfile, os.path.join(src_ws, the_dir))
                the_files.remove(xlsfile)
                the_files = the_files + serial_arr

        the_files.sort()

        dir_idx, dir_title, dir_slug = the_dir.split('_')

        list_md = []
        for wfile in the_files:

            lqian, lhou = os.path.splitext(wfile)
            file_path = lqian.split('_')
            if len(file_path) > 2:
                lidx, lname, lslug = file_path
            else:
                lidx, lslug = file_path
                lname = file_path[-1]

            the_file = os.path.join(wroot, wfile)

            md_dic = {}
            # with open(the_file) as fin:
            #     cnt_arr = []
            #     for cnt in fin.readlines():
            #         if cnt.strip().startswith(';'):
            #             tkey, tval = cnt.strip().strip(';').split(':')
            #
            #             md_dic[tkey.strip().lower()] = tval.strip()
            #         else:
            #             cnt_arr.append(cnt)

            if wfile.endswith('jinja2'):
                the_title = helper.get_html_title(the_file)
                md_dic['title'] = the_title
            #  with category
            # file_name = dir_slug + '_' + lslug + '.html'

            # Only layer slug
            file_name = lslug + '.html'

            title_h = md_dic['title'] if 'title' in md_dic else lname
            list_md.append({'slug': os.path.splitext(file_name)[0],
                            'file_name': lname,
                            'title': title_h})

        list_main.append(
            {
                'slug': dir_slug,
                'title': dir_title,
                'list_md': list_md
            }
        )

    return list_main


def copy_static_files():
    for wroot, wdirs, wfiles in os.walk(src_ws):

        for wfile in wfiles:
            _, houzhui = os.path.splitext(wfile)
            if houzhui.lower() in ['.jpg', '.png', '.jpeg']:
                infile = os.path.join(wroot, wfile)
                # outfile = dst_ws + infile[len(src_ws) : ]
                outfile = os.path.join(dst_ws, wfile)

                shutil.copy(infile, outfile)

    for file_name in os.listdir(tpl_ws):

        inbb = os.path.join(tpl_ws, file_name)

        outbb = os.path.join(dst_ws, file_name)

        if os.path.isdir(inbb):
            if os.path.exists(outbb):
                shutil.rmtree(outbb)
            shutil.copytree(inbb, outbb)
        else:
            shutil.copy(inbb, outbb)


def run():
    gen_html_index()
    gen_html_pages()
    copy_static_files()


if __name__ == '__main__':
    run()
