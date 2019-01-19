#!/bin/bash

# mapproxy-util create -t base-config wcs_imgmap

python3 012_gen_xlsx_lyr.py
python3 020_gen_mapproxy.py
rm -rf  wcs_imgmap/cache_data
cp -f out_mapproxy.yaml  ./wcs_imgmap/mapproxy.yaml

python3 030_build_site.py
