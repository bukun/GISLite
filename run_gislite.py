
import os
import shutil

from gislite import gen_xlsx_lyr
from gislite import gen_mapproxy
from gislite import build_site

gen_xlsx_lyr.run_it()

mapserver_ip = '127.0.0.1'

# mapserver_ip = '159.226.123.26'
out_yaml_file = 'out_mapproxy.yaml'
# mapfile_ws = '/opt/mapdisk/mapws'
gen_mapproxy.gen_by_ip(mapserver_ip, out_yaml_file)

build_site.run_it()

wcs_cache_dir = 'wcs_imgmap/cache_data'
if os.path.exists(wcs_cache_dir):
    shutil.rmtree(wcs_cache_dir)
shutil.move(out_yaml_file, './wcs_imgmap/mapproxy.yaml')
