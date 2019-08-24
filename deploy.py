import subprocess

from cfg import SITE_WS, GIS_BASE

subprocess.run('sudo chown -R bk {}/dist_site'.format(SITE_WS), shell=True)
subprocess.run('sudo chown -R bk {}'.format(GIS_BASE), shell=True)
subprocess.run('cd {} && python3 build_gislite.py'.format(SITE_WS), shell=True)
# subprocess.run()
subprocess.run('sudo chown -R www-data.www-data {}/dist_site'.format(SITE_WS), shell=True)
subprocess.run('sudo chown -R www-data.www-data {}'.format(GIS_BASE), shell=True)
subprocess.run('sudo supervisorctl restart gislite', shell=True)