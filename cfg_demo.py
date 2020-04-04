########################################################
# 服务器端配置 #
TILE_SVR = '192.168.56.1:8011'
# Path for GIS data.
GIS_BASE = '/home/bk/opt/geodemo'

## 服务器的工作空间
SITE_WS = '/home/bk/github/GISLite'

# User name
USER = 'bk'

###########################################################
# 远程部署使用，客户端定义. 不使用远程部署可以不用定义
machines = {
    'aliyun3': {'u': 'bk',
                'h': '192.168.56.1',
                'p': '',
                'ws': 'workspace'},
}

mach = machines['aliyun3']
