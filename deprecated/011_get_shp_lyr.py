# '''
# 对 Shapefile 进行遍历，生成 Mapfile.
# '''
# import os
# import mappyfile
#
# import helper
# from config import img_base
#
#
# #
# # def get_tmpl(map_dir='', fea_type=1):
# #     tmpl_name = 'tmpl_lyr.map'
# #     if fea_type == 2:
# #         tmpl_name = 'tmpl_point_lyr.map'
# #
# #     return tmpl_name
#
#
# def map_map(map_dir):
#     # map_dir_sig = os.path.split(map_dir)[1]
#
#     # shp_dir = os.path.join(map_dir, 'data')
#     # shps = glob.iglob('{0}/{1}'.format(shp_dir, '*.tif'))
#
#     mqian, mhou = os.path.split(map_dir)
#
#     midx, mslug, mname = mhou.split('_')
#
#     fc_inc = ''
#     for wroot, wdirs, wfiles in os.walk(map_dir):
#         for wfile in wfiles:
#             if wfile.endswith('.shp'):
#                 pass
#             else:
#                 continue
#             # ext = None
#             # lyr_name = get_lyr_map(map_dir, wfile, wroot)
#             lyr_name = get_lyr_mapfile(map_dir, wfile, wroot)
#
#             fc_inc = fc_inc + 'include "{}"\n'.format(lyr_name)
#
#     # fc_map_file = os.path.join(map_dir, 'mapfile.map')
#
#     fc_map_file2 = os.path.join(mqian, 'mfile_{}.map'.format(mslug))
#     with open(fc_map_file2, 'w') as fo2:
#         tmp_str = open('tmpl_mapfile.map').read().format(
#             basedir=map_dir,
#             fc_name='map_dir_sig', fc_includes=fc_inc,
#             fc_extent='{x_min} {y_min} {x_max} {y_max}'.format(
#                 x_min=-180,
#                 x_max=180,
#                 y_min=-90,
#                 y_max=90)
#         )
#         fo2.write(tmp_str)
#
#
# def get_lyr_mapfile(map_dir, wfile, wroot):
#     # mapfile = mappyfile.open("basic_mapfile.map")
#     #
#     # update the map name
#     # mapfile["name"] = "MyNewMap"
#     new_layer_string = """
# LAYER
#     NAME 'land'
#     TYPE POLYGON
#     DATA '../data/vector/naturalearth/ne_110m_land'
#
#     METADATA
#     'ows_title' ""
#     'wms_title' ''
#     'ows_srs'  'EPSG:4326 EPSG:3857'
#     'wms_srs' 'EPSG:4326 EPSG:3857'
#     "gml_include_items"   "all"
#     "wms_include_items"   "all"
#     "wms_enable_request" "GetMap GetFeatureInfo GetCapabilities"
#     END
#     CLASS
#     end
# END
# """
#
#     new_class_string = """
#     CLASS
#         STYLE
#             COLOR 107 208 107
#             OUTLINECOLOR 2 2 2
#             WIDTH 1
#         END
#         label
#
#         end
#     END
#     """
#
#     # layers = mapfile["layers"]
#     new_layer = mappyfile.loads(new_layer_string)
#     # print(mappyfile.dumps(new_layer['class']))
#
#     # layers.insert(0, new_layer) # insert the new layer at any index in the Mapfile
#     # for l in layers:
#     #     print("{} {}".format(l["name"], l["type"]))
#     # print(mappyfile.dumps(mapfile, indent=1, spacer="\t"))
#     # mapfile = mappyfile.open("xx_out.map")
#     shp = os.path.join(wroot, wfile)
#     shp_info = helper.get_epsg_code(shp)
#     # print(shp)
#     qian, hou = os.path.split(shp)
#     shpfile_name, shpfile_ext = os.path.splitext(hou)
#     lyr_name = 'lyr_' + shpfile_name + '.map'
#     # if shp_info['geom_type'].lower() == 'point':
#     #     fea_type = 2
#     # else:
#     #     fea_type = 1
#     lyr_file = os.path.join(map_dir, lyr_name)
#     xlsx_file = os.path.join(
#         map_dir,
#         'meta_' + shpfile_name + '.xlsx')
#     print(shp_info)
#     if os.path.exists(xlsx_file):
#         pass
#     elif shp_info['geom_type'].lower() == 'point':
#         xlsx_file = 'meta_point.xlsx'
#     elif shp_info['geom_type'].lower() == 'linestring':
#         xlsx_file = 'meta_line.xlsx'
#     elif shp_info['geom_type'].lower() == 'polygon':
#         xlsx_file = 'meta_poly.xlsx'
#     xlsx_file = 'meta_poly.xlsx'
#     map_mata = helper.xlsx2dict(xlsx_file)
#
#     lyr_type = 'line' if shp_info['geom_type'].lower() in [ 'linestring', 'multilinestring'] else shp_info['geom_type']
#     new_layer['type'] = lyr_type
#     new_layer['data'] = shp
#     new_layer['name'] = os.path.splitext(wfile)[0]
#     new_layer['metadata']['ows_title'] = os.path.splitext(wfile)[0]
#     new_layer['metadata']['wms_title'] = os.path.splitext(wfile)[0]
#
#     for idx, cl in enumerate(map_mata):
#
#         print('=' * 30)
#         print(idx)
#         print(cl)
#         cls = mappyfile.loads(new_class_string)
#         for key in cl:
#             print(key)
#             if key == 'classitem':
#                 new_layer['classitem'] = cl[key]
#
#             elif key == 'labelitem':
#                 new_layer['labelitem'] = cl[key]
#
#
#             elif key == 'class':
#                 pass
#
#             elif key == 'style':
#                 for subkey in cl[key]:
#                     cls['styles'][0][subkey] = cl[key][subkey]
#
#             elif key == 'label':
#                 for subkey in cl[key]:
#                     print('x' * 10)
#                     print(cl[key][subkey])
#                     cls['labels'][0][subkey] = cl[key][subkey]
#             else:
#                 cls[key] = cl[key]
#
#         # new_layer['classes'].append(cls)
#         new_layer["classes"].insert(0, cls)
#
#     # 去掉原来的。
#     new_layer['classes'].pop()
#     # print(help(new_layer['classes']))
#
#     with open(lyr_file, 'w') as fo:
#         fo.write(mappyfile.dumps(new_layer, indent=1, spacer="    "))
#
#     # pprint(new_layer)
#
#     # print(yaml.dump(new_layer))
#     return lyr_file
#
#
# if __name__ == '__main__':
#
#     for wroot, wdirs, wfile in os.walk(img_base):
#         for wdir in wdirs:
#             if wdir.startswith('maplet'):
#                 print(wdir)
#                 map_map(os.path.join(wroot, wdir))
