#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
For pypi
'''

from setuptools import setup, find_packages

desc = ('Static site generator (SSG) for GIS data publishment as light WebGIS application.')
setup(
    name='gislite',
    version='0.0.4',
    keywords=('WebGIS', 'Static site generator'),
    description=desc,
    long_description=''.join(open('ReadMe.rst').readlines()),
    license='MIT License',

    url='http://gislite.osgeo.cn',
    author='bukun',
    author_email='bukun@osgeo.cn',

    packages=find_packages(
        # include=('torcms',),
        exclude=("tester", "wcs_imgmap", 'static', 'docs', 'dist-site', 'deprecated')),
    include_package_data=True,

    platforms='any',
    zip_safe=True,
    install_requires=['markdown', 'mapproxy', 'pyyaml', 'openpyxl'],

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
)
