'''
Running locally. For Development.
'''

import subprocess

from cfg import SITE_WS, GIS_BASE, USER

subprocess.run('sudo chown -R {} {}/dist_site/*'.format(USER, SITE_WS), shell=True)
subprocess.run('sudo chown -R {} {}/dist_site'.format(USER, SITE_WS), shell=True)
subprocess.run('sudo chown -R {} {}/*'.format(USER, GIS_BASE), shell=True)
subprocess.run('cd {} && python3 build_gislite.py'.format(SITE_WS), shell=True)
subprocess.run('sudo chown -R www-data.www-data {}/dist_site'.format(SITE_WS), shell=True)
subprocess.run('sudo chown -R www-data.www-data {}'.format(GIS_BASE), shell=True)

# subprocess.run('sudo supervisorctl restart gislite', shell=True)
