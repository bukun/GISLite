import mappyfile


def get_lyr_mapfile():
    # mapfile = mappyfile.open("basic_mapfile.map")
    #
    # update the map name
    # mapfile["name"] = "MyNewMap"
    new_layer_string = """
LAYER
    NAME 'land'
    TYPE POLYGON
    DATA '../data/vector/naturalearth/ne_110m_land'
    CLASS
        STYLE
            COLOR 107 208 107
            OUTLINECOLOR 2 2 2
            WIDTH 1
        END
    END
END
"""
    # layers = mapfile["layers"]
    new_layer = mappyfile.loads(new_layer_string)
    # print(mappyfile.dumps(new_layer['class']))
    classes = new_layer["classes"]
    new_layer['name'] = 'the_lyr_name'
    for c in classes:
        print('aa')
        print(mappyfile.dumps(c['styles'][0]))

        for x in c['styles']:
            print(x['color'])
            x['color'] = [1, 1, 1]
    # layers.insert(0, new_layer) # insert the new layer at any index in the Mapfile
    # for l in layers:
    #     print("{} {}".format(l["name"], l["type"]))
    # print(mappyfile.dumps(mapfile, indent=1, spacer="\t"))
    # mapfile = mappyfile.open("xx_out.map")
    print(mappyfile.dumps(new_layer, indent=1, spacer="    "))


get_lyr_mapfile()
