# -*- coding: utf-8 -*-
"""
发布程序入口
"""
import os
import shutil
import time

from gislite import sphinx_builder
from gislite.helper import clean_sphinx

sphinx_builder.run()

clean_sphinx('./dist_sphinx/source')
