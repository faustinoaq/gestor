#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helpers functions
"""

import time
import locale
import hashlib
from re import search, sub
from unicodedata import normalize

import settings
from . import models


def gen(count, single, plural):
    """
    Relates the amount and number of the noun.

        >>> gen(0, 'car', 'cars')
        u'0 cars'
        >>> gen(1, 'car', 'cars')
        u'1 car'
        >>> gen(2, 'car', 'cars')
        u'2 cars'

    You could also use ngettext, but no now.
    """
    if count == 1:
        return u'{0} {1}'.format(count, single)
    else:
        return u'{0} {1}'.format(count, plural)


def paginate(page, limit, count):
    """
    Calculate the offset and pages variables and
    check if page is a valid value.

        >>> paginate('cats', 5, 10)
        (0, 2, 1)
        >>> paginate(3, 5, 1)
        (0, 1, 1)
        >>> paginate(2, 10, 23)
        (10, 3, 2)
        >>> paginate(200, 20, 40)
        (20, 2, 2)

    Return 0 posts and templates no render nothing.

        >>> paginate(2, 10, 0)
        (10, 0, 2)
    """
    try:
        # For invalid values
        page = int(page)
    except:
        page = 1
    offset = (page - 1) * limit
    pages = count / limit
    if count % limit > 0:
        pages += 1
    if page > pages and pages > 0:
        page = pages
        offset = (page - 1) * limit
    return offset, pages, page


def md5(string):
    """
    Encrypt a string with MD5, used for password and Gravatar.

        >>> md5('')
        'd41d8cd98f00b204e9800998ecf8427e'
        >>> md5('admin')
        '21232f297a57a5a743894a0e4a801fc3'
    """
    string = string.encode('UTF-8')
    return hashlib.md5(string).hexdigest()


def validate(*args):
    """
    Check NOT NULL values in forms.

        >>> validate('a', 'b', 'c')
        True
        >>> validate('a a', 'b b', 'c c')
        True
        >>> validate('a', '', 'c')
        False
        >>> validate('a', ' ', 'c')
        False
        >>> validate('a', '    ', '    ')
        False
        >>> validate('', '', '')
        False
    """
    for var in args:
        if not search('\S', var):
            return False
            break
    return True


def slug(text):
    """
    Convert string to slug.

        >>> slug(u'Crazy Cats 2')
        'crazy-cats-2'
        >>> slug(u'Cat && Baby')
        'cat--baby'
        >>> slug(u'BeauTifuL   TreEs')
        'beautiful---trees'
        >>> slug(u'The story of Pi: a wonderful adventure')
        'the-story-of-pi-a-wonderful-adventure'
        >>> slug(u'Coffee = Drug')
        'coffee--drug'
    """
    text = text.lower()
    text = normalize("NFKD", text)
    text = sub(r"\s", "-", text)
    text = text.encode('ASCII', 'ignore')
    text = sub("[^a-z0-9-_]", "", text)
    return text


def ids(tags):
    """
    Get a ids group of a tag group.
    Here I can use many-to-many in database, but I don't have
    knowledge about this.

        >>> ids('cats, cows, dogs, rabbits')
        '1, 2, 3, 4'
        >>> ids('cats, dogs')
        '1, 3'
        >>> ids('other')
        '5'
    """
    tags = tags.split(', ')
    # Order tags and removes duplicates.
    tags = set(tags)
    tags = sorted(tags)
    ids = []
    for tag in tags:
        try:
            key = models.tag.key(tag)
            ids.append(str(key))
        except:
            models.tag.new(tag)
            key = models.tag.key(tag)
            ids.append(str(key))
    return ', '.join(ids)


def names(Ids, aslist=''):
    """
    Based on the above tests.
    Get tags name from ids group.

        >>> names('1, 2')
        u'cats, cows'

    You can also get an object Storage.

        >>> names('1, 2', 'list')
        [<Storage {'id': 1, 'name': u'cats'}>, <Storage {'id': 2, 'name': u'cows'}>]

    On error returns the same.

        >>> names('cats, cows')
        'cats, cows'
    """
    try:
        ids = Ids.split(', ')
        names = []
        if aslist == 'list':
            for Id in ids:
                key = models.tag.nameid(Id)
                names.append(key)
            return names
        for Id in ids:
            key = models.tag.name(Id)
            names.append(key)
        return ', '.join(names)
    except:
        # For some strange errors
        return Ids


def datestr(date):
    """
    Date Format based on input.

        >>> datestr('2013-10-23')
        'Oct 23, 2013'
    """
    try:
        locale.setlocale(locale.LC_ALL, settings.lang)
    except:
        pass
    # Timestamp is based on input
    # time.strptime('2013-10-23', '%Y-%m-%d')
    # time.strptime('10-23-2013', '%m-%d-%Y')
    # time.strptime('2013-10', '%Y-%m')
    timestamp = time.strptime(date, '%Y-%m-%d')
    return time.strftime(settings.date, timestamp)


def textmark(string, mark=""):
    """
    Excerpt of content

        >>> textmark('<p>Hello</p><!----><p>World</p>')
        '<p>Hello</p>'
        >>> textmark('<p>Hello</p><!--ex--><p>World</p>', 'ex')
        '<p>Hello</p>'
        >>> textmark('<p>Hello</p><!----><p>World</p><!--test-->', 'test')
        '<p>Hello</p><!----><p>World</p>'
    """
    mark = "<!--{0}-->".format(mark)
    if mark in string:
        index = string.index(mark)
        return string[0:index]
    return ""
