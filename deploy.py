'''
发布 WebGIS.
'''
from fabric import Connection

from cfg import mach, SITE_WS, GIS_BASE_REMOTE



def main():

    print("{}@{}".format(mach['u'], mach['h']))
    c = Connection("{}@{}".format(mach['u'], mach['h']), port=11022, connect_kwargs={"password": mach['p']})

    c.run('sudo chown -R bk {}/dist_site'.format(SITE_WS))
    c.run('sudo chown -R bk {}'.format(GIS_BASE_REMOTE))

    with c.cd(SITE_WS):
        c.run('git pull')
        c.run('python3 build_gislite.py')

    c.run('sudo chown -R www-data.www-data {}/dist_site'.format(SITE_WS))
    c.run('sudo chown -R www-data.www-data {}'.format(GIS_BASE_REMOTE))


if __name__ == '__main__':
    main()
