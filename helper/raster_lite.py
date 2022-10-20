

from pathlib import Path

mfile_tmpl = '''

MAP
NAME "map_dir_sig"
SIZE 300 300
UNITS meters

FONTSET "./fonts/fonts.list"

EXTENT -180 -90 180 90
SHAPEPATH  "/qsvr/geodata/maplet80_tvdi_weather"

PROJECTION
    "init=epsg:4326"
END

SYMBOL
  TYPE ellipse
  POINTS 1 1 END
  NAME "circle"
END

# Background color for the map canvas -- change as desired
IMAGECOLOR 255 255 255
IMAGEQUALITY 95
IMAGETYPE png

#include "/qsvr/geodata/maplet80_tvdi_weather/lyr_aqi.map"

'''

lyr_tmpl = '''
LAYER
    NAME "lyr_{sig}"
    TYPE RASTER
    DATA "{fpath}"
    STATUS ON
    DUMP TRUE
    PROJECTION
        "+proj=longlat +datum=WGS84 +no_defs"
    END
    METADATA
        "ows_title" "meta_{sig}"
        "wms_title" "meta_{sig}"
        "ows_srs" "EPSG:4326 EPSG:3857"
        "wms_srs" "EPSG:4326 EPSG:3857"
        "gml_include_items" "all"
        "wms_include_items" "all"
        "wms_enable_request" "*"
    END
    CLASS
        STYLE
        END
        LABEL
            FONT "simsun"
        END
    END
    PROCESSING "scale=auto"
END
'''

inws = Path('maplet80_tvdi_weather')
with open('mfile_weather2.map', 'w') as mfo:
    mfo.write(mfile_tmpl)
    for wfile in inws.rglob('*.tif'):
        print(wfile.name)
        uu = wfile.stem.split('_')[-1]
        out_mapfile = wfile.parent / f'lyr_{uu}.map'
        with open(out_mapfile, 'w') as fo:
            fo.write(lyr_tmpl.format(sig = uu, fpath = wfile.resolve()))
        mfo.write(
            f'''
            include "{out_mapfile.resolve()}"
            '''
            )
    mfo.write('END')