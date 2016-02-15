#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Database Queries
"""

import time

from .db import db

class Date:
    # Date format for column date
    date = time.strftime('%Y-%m-%d')

date = Date().date


class Posts:

    def __init__(self):
        """
        Used for Count class
        """
        self.what = '*'

    def one(self, Id):
        """
        Get a post according to id.
        """
        try:
            return db.select('posts', where='id=$Id', vars=locals())[0]
        except IndexError:
            return False

    def all(self, offset=0, limit=10, checked="", order="id DESC"):
        """
        Gets many publications depending of limit, offset and checked.
        """
        if self.what != "*":
            order, offset, limit = None, None, None
        posts = db.select('posts', what=self.what,
                          offset=offset, limit=limit, order=order,
                          vars=locals(), where='published=$checked')
        if self.what == 'count(*) as count':
            return posts[0].count
        return posts

    posts = all

    def search(self, query="", offset=0, limit=10):
        """
        Search a word or a sentence into title or content and return
        the posts that match.
        """
        query = unicode(query).encode('UTF-8')
        query = db.select('posts', what=self.what,
                          offset=offset, limit=limit, vars=locals(),
                          where="""(title like '%{0}%' or
                                    content like '%{0}%') and
                                    published='checked'
                                    """.format(query))
        if self.what == 'count(*) as count':
            return query[0].count
        return query

    def date(self, date="", offset=0, limit=10, order="id DESC"):
        """
        Return posts that match with date.
        """
        if self.what != "*":
            order, offset, limit = None, None, None
        date = db.select('posts', what=self.what,
                         offset=offset, limit=limit, order=order,
                         vars=locals(),
                         where="""date=$date and
                                  published='checked'""")
        if self.what == 'count(*) as count':
            return date[0].count
        return date

    def user(self, user="", offset=0, limit=10, order="id DESC"):
        """
        Return posts that match with user.
        """
        if self.what != "*":
            order, offset, limit = None, None, None
        user = db.select('posts', what=self.what,
                         offset=offset, limit=limit, order=order,
                         vars=locals(),
                         where="""autor=$user and
                                  published='checked'""")
        if self.what == 'count(*) as count':
            return user[0].count
        return user

    userpost = user

    def new(self, title, content, tags, autor, published, comment):
        """
        Create a post and return postid.
        """
        return db.insert('posts', title=title, content=content, tags=tags, date=date,
                  autor=autor, published=published, comment=comment)

    def edit(self, Id, title, content, tags, autor, published, comment):
        """
        Update a post.
        """
        db.update('posts', title=title, content=content, tags=tags,
                  autor=autor, published=published, comment=comment,
                  vars=locals(), where='id=$Id')

    def delete(self, Id):
        """
        Delete a post with your comments.
        """
        db.delete('comments', vars=locals(), where='post=$Id')
        db.delete('posts', vars=locals(), where='id=$Id')

    def tag(self, Id=0, offset=0, limit=10, order="id DESC"):
        """
        Return posts that match with tagid.
        """
        if self.what != "*":
            order, offset, limit = None, None, None
        tagp = db.select('posts', what=self.what,
                         offset=offset, limit=limit, order=order,
                         vars=locals(),
                         where="""(tags='{0}' or
                                   tags like '{0},%' or
                                   tags like '%, {0},%' or
                                   tags like '%, {0}') and
                                   published='checked'
                                   """.format(Id))
        if self.what == 'count(*) as count':
            return tagp[0].count
        return tagp


class Tags:

    def __init__(self):
        self.what = '*'

    def nameid(self, Id):
        """
        Return Storage Object with tagname and tagid.
        """
        return db.select('tags', vars=locals(), where='id=$Id')[0]

    def name(self, Id):
        """
        Return tagname according tagid.
        """
        tag = db.select('tags', what='name', vars=locals(), where='id=$Id')[0]
        return tag.name

    def key(self, name):
        """
        Return tagid according tagname.
        """
        tag = db.select('tags', what='id',
                        vars=locals(), where='name=$name')[0]
        return tag.id

    def all(self, offset=0, limit=10, order="tags.name ASC"):
        """
        Return all tags.
        """
        if self.what != "*":
            order, offset, limit = None, None, None
        tags = db.select('tags', what=self.what,
                         offset=offset, limit=limit, order=order)
        if self.what == 'count(*) as count':
            return tags[0].count
        return tags

    tags = all

    def one(self, Id):
        """
        Return a tag.
        """
        try:
            return db.select('tags', vars=locals(), where='id=$Id')[0]
        except IndexError:
            return False

    def new(self, name):
        """
        Create a tag.
        """
        db.insert('tags', name=name)

    def edit(self, Id, name):
        """
        Update a tag.
        """
        db.update('tags', name=name, vars=locals(), where='id=$Id')

    def delete(self, Id):
        """
        Delete a tag.
        """
        db.delete('tags', vars=locals(), where='id=$Id')

    def exist(self, Id):
        """
        Check if exist a tag.
        """
        posts = db.select('posts', what="count(1) as count", limit=1,
                          where="""tags='{0}' or
                                   tags like '{0},%' or
                                   tags like '%, {0},%' or
                                   tags like '%, {0}' """.format(Id),
                          vars=locals())[0]
        return posts.count

    def clean(self):
        """
        Delete tags unused.
        """
        tags = db.select('tags')
        for tag in tags:
            if not self.exist(tag.id):
                self.delete(tag.id)


class Comments:

    def __init__(self):
        self.what = '*'

    def all(self, Id, order="id ASC"):
        """
        Get all comments.
        """
        if self.what != "*":
            order = None
        comments = db.select('comments', what=self.what,
                             order=order, vars=locals(), where='post=$Id')
        if self.what == 'count(*) as count':
            return comments[0].count
        return comments

    comments = all

    def new(self, name, email, comment, web, post):
        """
        Create a comment.
        """
        db.insert('comments', name=name, email=email,
                  comment=comment, web=web, post=post, date=date)

    def delete(self, Id):
        """
        Delete a comment.
        """
        db.delete('comments', where='id=$Id', vars=locals())

    def last(self, Id):
        """
        Get last comment.
        """
        last = db.select('comments', what='max(id) as id',
                         vars=locals(), where='post=$Id')[0]
        return last.id


class Counts(Posts, Tags, Comments):

    def __init__(self):
        """
        Add count queries. 
        """
        self.what = 'count(*) as count'

# Class instances
post = Posts()
tag = Tags()
comment = Comments()
count = Counts()
