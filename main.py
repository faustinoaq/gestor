#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestor

Simple web application for publishing content.
"""

from core.views import app

# WSGI interface
application = app.wsgifunc()

# Local server
if __name__ == '__main__':
    app.run()
