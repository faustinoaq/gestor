#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestor Settings
"""

import os
import web

# Set True for dev and False for deploy

debug = True

# Used to translate the templates with gettext
# The lang should be available in the i18n dir
# Some OS require UTF-8 at the end
# lang = 'en_US.UTF-8'

lang = 'en_US'

# Amount of posts and tags per page

limit = 5

# Set your title, description and footer
# You can use Markdown in the footer

title = u"Gestor"

description = u"A simple webapp for publishing content"

footer = u"The username and password is **admin**"

# Dictionary with username and password encrypted with MD5
# The default username and password is admin
# You can use hashlib to encrypt the password
# >>> hashlib.md5('admin').hexdigest()

users = {
    'admin': '21232f297a57a5a743894a0e4a801fc3',
}

# Date Format
# %b month ['Jan', ... , 'Dec']
# %B month ['January', ... , 'December']
# %d day [01,31]
# %j day [001,366]
# %m month [01,12]
# %y year [00,99]
# %Y year [2000,2099]
# 'Jan 1, 1970'

date = u'%b %d, %Y'

# Database settings
# Support sqlite, mysql and postgres
# postgres require psycopg2
# mysql require MySQL-python

database = {
    'dbn':  'sqlite',
    'db':   'data.db',
    'user': '',
    'pw':   '',
    'host': '',
    'port': 3306,
}

# Static folder
# You must specify the directory on your web server
static = '/static'

# Translation dir
i18n = os.path.join(os.path.dirname(__file__), 'i18n')

# Templates dir
templates = os.path.join(os.path.dirname(__file__), 'templates')

# Absolute path of sqlite file
if database['dbn'] == 'sqlite':
    database['db'] = os.path.join(os.path.dirname(__file__), database['db'])

# Set web.py to debug value
web.config.debug = debug
