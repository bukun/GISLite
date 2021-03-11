'''
Merge YAML files used for MapProxy.
合并 MapProxy 中使用的 YAML.
'''

import ruamel.yaml
import os

yaml = ruamel.yaml.YAML()

def get_yaml_data(yaml_file):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    data = yaml.load(file_data)
    return data
current_path = os.path.abspath(".")

yamls = [x for x in os.listdir() if x.startswith('x') and x.endswith('.yaml')]

dic_a = get_yaml_data(yamls[0])

for yaml_path in yamls[1:] :
    dic_b = get_yaml_data('xx_mapproxy.yaml')

    for key in ['caches', 'globals', 'grids', 'services', 'sources']:
        print(key)
        if dic_b.get(key):
            pass
        else:
            continue
        for i in dic_b[key]:
            # print i,data1['resources'][i]
            dic_a[key].update({i:dic_b[key][i]})

    for key in ['layers']:
        for val in dic_b[key]:
            dic_a[key].append(val)

with open('mapproxy.yaml', 'w') as fo:
    # fo.write(yaml.dump(new_dic))
    yaml.dump(dic_a, fo)
