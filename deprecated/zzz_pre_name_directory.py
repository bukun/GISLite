# -*- coding:cp936 -*-

#
import os
import sys
import arcpy
import random


def get_uu4d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 3)
    return ('v' + ''.join(slice))


def get_sig_arr(inws):
    '''
    得到所有的地图的sig列表
    '''
    now_arr = []
    for wroot, wdirs, wfiles in os.walk(inws):
        for wfile in wfiles:
            # hou_lower = os.path.splitext(wfile)[1].lower()
            (qian, hou) = os.path.splitext(wfile)
            if hou.lower() in ['.jpg', '.bmp', '.tif', '.png']:

                # print(qian)
                sig_arr = qian.split('_')
                if len(sig_arr) > 1:

                    sig = sig_arr[-1]
                    if len(sig) == 5 and sig[0] == 'v':
                        now_arr.append(sig[1:])
                    else:
                        continue
                else:
                    continue
    return now_arr


if __name__ == '__main__':
    inws = r'c:\opt\mapws\ydyl'
    now_arr = get_sig_arr(inws)

    print('For files: ')
    for wroot, wdirs, wfiles in os.walk(inws):
        for wfile in wfiles:
            if wfile.endswith('.shp'):
                pass
            else:
                continue
            (qian, hou) = os.path.splitext(wfile)
            new_sig = get_uu4d()
            while new_sig in now_arr:
                new_sig = get_uu4d()
            if qian.endswith('_tt'):
                now_arr.append(new_sig)
                raw_path = os.path.join(wroot, wfile)
                new_path = os.path.join(wroot, ''.join([qian[:-2], 'v', new_sig, hou]))
                print(raw_path)
                print(new_path)
                # 这里必须使用arcpy对数据集进行重命名
                arcpy.Rename_management(in_data=raw_path, out_data=new_path, data_type="ShapeFile")
                # os.rename(raw_path, new_path)
