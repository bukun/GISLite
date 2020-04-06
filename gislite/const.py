'''
MAP Object template in Mapfile.
'''





TPL_MAP = '''
MAP
NAME "{fc_name}"
SIZE 300 300
UNITS meters

FONTSET "./fonts/fonts.list"

EXTENT {fc_extent}
SHAPEPATH  "{basedir}"

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

{fc_includes}

END
'''

'''
LAYER Object template in Mapfile.
'''



TPL_LAYER = '''
LAYER
    NAME 'land'
    TYPE POLYGON
    DATA 'data'
    STATUS ON
    DUMP true

    # MAXSCALEDENOM 2500000
    # LABELITEM 'RNAME'


    PROJECTION
    "init=epsg:4326"
    END


    METADATA
    'ows_title' ""
    'wms_title' ''
    'ows_srs'  'EPSG:4326 EPSG:3857'
    'wms_srs' 'EPSG:4326 EPSG:3857'
    "gml_include_items"   "all"
    "wms_include_items"   "all"
    "wms_enable_request" "*"
    END
    CLASS
    end
END
'''

'''
CLASS Object template in Mapfile.
'''


TPL_CLASS = '''
CLASS
    STYLE
                
    END
    label
        FONT "simsun"
    end
END
'''

'''
MapProxy config file template.
'''


TPL_MAPPROXY = '''
services:
  demo:
  tms:
    use_grid_names: true
    # origin for /tiles service
    origin: 'nw'
  kml:
      use_grid_names: true
  wmts:
  wms:
    md:
      title: MapProxy WMS Proxy
      abstract: This is a minimal MapProxy example.
layers:
  - name: osm
    title: Omniscale OSM WMS - osm.omniscale.net
    sources: [osm_cache]

caches:
  osm_cache:
    grids: [webmercator]
    sources: [osm_wms]

sources:
  osm_wms:
    type: wms
    req:
      # use of this source is only permitted for testing
      url: http://osm.omniscale.net/proxy/service?
      layers: osm

grids:
    webmercator:
        base: GLOBAL_WEBMERCATOR

globals:
'''
COLOR_INDEX = (
    '00000000', '00FFFFFF', '00FF0000', '0000FF00', '000000FF',
    '00FFFF00', '00FF00FF', '0000FFFF', '00000000', '00FFFFFF',
    '00FF0000', '0000FF00', '000000FF', '00FFFF00', '00FF00FF',
    '0000FFFF', '00800000', '00008000', '00000080', '00808000',
    '00800080', '00008080', '00C0C0C0', '00808080', '009999FF',
    '00993366', '00FFFFCC', '00CCFFFF', '00660066', '00FF8080',
    '000066CC', '00CCCCFF', '00000080', '00FF00FF', '00FFFF00',
    '0000FFFF', '00800080', '00800000', '00008080', '000000FF',
    '0000CCFF', '00CCFFFF', '00CCFFCC', '00FFFF99', '0099CCFF',
    '00FF99CC', '00CC99FF', '00FFCC99', '003366FF', '0033CCCC',
    '0099CC00', '00FFCC00', '00FF9900', '00FF6600', '00666699',
    '00969696', '00003366', '00339966', '00003300', '00333300',
    '00993300', '00993366', '00333399', '00333333',
    'System Foreground', 'System Background'
)