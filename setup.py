# -*- coding: utf-8 -*-
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['iCake.py']
# DATA_FILES = ['file/postcode.csv',
#               'file/postcode_full.csv',
#               'file/orderandcakedata.csv',
#               'file/orderandcakedata_copy.csv',
#               'file/dispatchers.csv',
#               'file/dispatchers_copy.csv',
#               'file/log.txt',
#               'file/cake_size.csv',
#               'file/cake_type.csv',
#               'file/cake_inner.csv',
#               'file/cake_shapes.csv']

DATA_FILES = ['file']
OPTIONS = {'argv_emulation': True,
           'packages': ['googlemaps']}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
