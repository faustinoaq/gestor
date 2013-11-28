#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestor URLs

Test Regex

    >>> import re

Check date Regex

    >>> date = re.match(dateregex, "2012-12-30")
    >>> date.groups()
    ('2012', '12', '3')

Invalid date

    >>> date = re.match(dateregex, "3abY-34-0.566")
    >>> type(date)
    <type 'NoneType'>
    >>> date = re.match(dateregex, "2012-45-99")
    >>> type(date)
    <type 'NoneType'>
"""

# Regex for date format YYYY-MM-DD
dateregex = r"(20[0-9][0-9])-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])/?"

# url = ('path', 'class', 'path', 'class')
urls = (
    r'/?', 'Index',
    r'/login/?', 'Login',
    r'/logout/?', 'Logout',
    r'/search/?', 'Search',
    r'/user/(.*)/?', 'User',
    r'/date/'+dateregex, 'Date',
    r'/post/?', 'PostAll',
    r'/post/new/?', 'PostNew',
    r'/post/draft/?', 'PostDraft',
    r'/post/(.*)/(\d+)/?', 'PostOne',
    r'/post/(\d+)/edit/?', 'PostEdit',
    r'/post/(\d+)/delete/?', 'PostDelete',
    r'/comment/(\d+)/delete/?', 'CommentDelete',
    r'/tag/?', 'TagAll',
    r'/tag/(.*)/(\d+)/?', 'TagOne',
    r'/tag/(\d+)/edit/?', 'TagEdit',
)
