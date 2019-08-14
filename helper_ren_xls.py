
import os
import sys

import shutil
inws = '/home/bk/ws/geodata/'

# for wroot, wdirs, wfiles in os.walk(inws):
#     for wfile in wfiles:
#         if wfile.lower().endswith('.xlsx'):
#             the_infile = os.path.join(wroot, wfile)
#             print('=' * 10)
#             print(wfile)
#             fname, fzhui = os.path.splitext(wfile)
#             (qian, zhong, hou) = fname.split('_')
#             # print((qian, zhong, hou))
#
#             outfile = '_'.join((qian, hou, zhong)) + fzhui
#
#             the_outfile = os.path.join(wroot, outfile)
#             print(outfile)
#             print(the_infile)
#             print(the_outfile)
#
#             shutil.move(the_infile, the_outfile)

# for wroot, wdirs, wfiles in os.walk(inws):
#     for wdir in wdirs:
#         if wdir.startswith('maplet'):
#             print('=' * 30)
#             print(wdir)
#
#             (qian, zhong, hou) = wdir.split('_')
#             outdir = '_'.join((qian, hou, zhong))
#             the_indir = os.path.join(wroot, wdir)
#             the_outdir = os.path.join(wroot, outdir)
#             print(the_indir)
#             print(the_outdir)
#
#             shutil.move(the_indir, the_outdir)