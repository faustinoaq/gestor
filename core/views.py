#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Handler
"""

import gettext

if not gettext:
    def textget(text):
        return text
    _ = textget

import web
from markdown import Markdown

import settings
from . import models
from . import helpers
from .db import db
from .urls import urls
from .render import jinja_env, render

# Templates Translation
gettext.install('messages', settings.i18n, unicode=True)
lang = gettext.translation('messages', settings.i18n,
                           languages=[settings.lang])
lang.install(True)


app = web.application(urls, globals())


def encoding():
    """
    Add encoding UTF-8 to Response Headers.
    """
    web.header('Content-type', "text/html; charset=utf-8")

# Add hook to app
app.add_processor(web.loadhook(encoding))

# Create store for sessions
store = web.session.DBStore(db, 'sessions')

# Manage sessions for app
session = web.session.Session(app, store, {'user': ''})

# Markdown
md = Markdown(output_format='html5')

# Markdown with escape HTML
md_safe = Markdown(output_format='html5', safe_mode="escape")

# Remove extra spaces
jinja_env.trim_blocks = True

# Globals variables
jinja_env.globals.update(
    _=_,  # gettext
    md=md.convert,
    session=session,
    md_safe=md_safe.convert,
    gen=helpers.gen,
    md5=helpers.md5,
    slug=helpers.slug,
    names=helpers.names,
    more=helpers.textmark,
    datestr=helpers.datestr,
    exist=models.tag.exist,
    counter=models.count.comments,
    admin=settings.users,
    footer=settings.footer,
    lang=settings.lang[:2],
    static=settings.static,
    sitetitle=settings.title,
    sitedescription=settings.description,
)

# Error pages
app.badrequest = web.badrequest
if not settings.debug:
    def notfound():
        """Error 404"""
        return web.notfound(render('404.html'))

    def internalerror():
        """Error 500"""
        return web.internalerror(render('500.html'))

    def badrequest():
        """Error 400"""
        return web.badrequest(render('400.html'))

    app.internalerror = internalerror
    app.notfound = notfound
    app.badrequest = badrequest


def logged(function):
    """
    Decorator for check login.
    """
    def GET(*args, **kwargs):
        if session.get('logged_in'):
            return function(*args, **kwargs)
        raise web.seeother('/login')
    return GET


class Index:

    def GET(self):
        raise web.seeother('/post')


class Login:
    """
    Sign in a user.
    """

    def GET(self):
        """
        Login form.
        """
        session_id = web.cookies().get('webpy_session_id')
        if session.get('logged_in'):
            raise web.seeother('/')
        return render('login.html', token=session_id)

    def POST(self):
        session_id = web.cookies().get('webpy_session_id')
        i = web.input(token='')
        # I think that avoid CSRF attacks
        if session_id == i.token:
            user = i.user
            password = helpers.md5(i.password)
            if user in settings.users and settings.users[user] == password:
                session.logged_in = True
                session.user = user
                raise web.seeother('/')
            return render('login.html', error='error', token=session_id)
        raise app.badrequest()


class Logout:
    """
    Sign out a user.
    """

    @logged
    def GET(self):
        session.logged_in = False
        session.user = ""
        raise web.seeother('/')


class Date:
    """
    Posts by date.
    """

    def GET(self, day, month, year):
        date = "{0}-{1}-{2}".format(day, month, year)
        i = web.input(p=1)
        limit = settings.limit
        count = models.count.date(date)
        offset, pages, page = helpers.paginate(i.p, limit, count)
        posts = models.post.date(date, offset, limit)
        return render('date.html', posts=posts, date=date, page=page,
                      pages=pages, count=count)


class User:
    """
    Posts by user.
    """

    def GET(self, user):
        if models.count.userpost(user) or user in settings.users:
            i = web.input(p=1)
            limit = settings.limit
            count = models.count.userpost(user)
            offset, pages, page = helpers.paginate(i.p, limit, count)
            posts = models.post.user(user, offset, limit)
            return render('user.html', posts=posts, user=user, page=page,
                          pages=pages, count=count)
        raise app.notfound()


class Search:
    """
    Posts by search.
    """

    def GET(self):
        i = web.input(s="", p=1)
        if helpers.validate(i.s):
            limit = settings.limit
            count = models.count.search(i.s)
            offset, pages, page = helpers.paginate(i.p, limit, count)
            posts = models.post.search(i.s, offset, limit)
            return render('search.html', posts=posts, search=i.s,
                          page=page, pages=pages, count=count)
        raise web.seeother('/')


class PostAll:
    """
    All posts.
    """

    def GET(self):
        i = web.input(p=1)
        limit = settings.limit
        count = models.count.posts(checked='checked')
        offset, pages, page = helpers.paginate(i.p, limit, count)
        posts = models.post.all(offset, limit, 'checked')
        return render('posts.html', posts=posts, page=page,
                      pages=pages, count=count)


class PostDraft:
    """
    All drafts.
    """

    @logged
    def GET(self):
        i = web.input(p=1)
        limit = settings.limit
        count = models.count.posts()
        offset, pages, page = helpers.paginate(i.p, limit, count)
        posts = models.post.all(offset, limit)
        return render('postdraft.html', posts=posts, page=page,
                      pages=pages, count=count)


class PostOne:
    """
    Gets a post with your comments.
    """

    def GET(self, slug, post_id):
        """
        This method use post_id for check if post exist and
        build the correct path.
        """
        post = models.post.one(post_id)
        if post:
            if post.published or session.get('logged_in'):
                title = helpers.slug(post.title)
                if title == slug:
                    comments = models.comment.all(post_id)
                    return render('post.html', post=post, comments=comments)
                raise web.seeother('/post/{0}/{1}'.format(title, post_id))
            raise web.seeother('/login')
        raise app.notfound()

    def POST(self, slug, post_id):
        i = web.input()
        if helpers.validate(i.name, i.email, i.comment):
            models.comment.new(i.name, i.email, i.comment, i.web, post_id)
            last = models.comment.last(post_id)
            raise web.seeother('/post/{0}/{1}#c{2}'.format(slug,
                                                           post_id, last))
        raise web.seeother('/post/{0}/{1}#n'.format(slug, post_id))


class PostNew:
    """
    Create a Posts.
    """

    @logged
    def GET(self):
        return render('postnew.html')

    @logged
    def POST(self):
        i = web.input(published="", comment="")
        if helpers.validate(i.title, i.content, i.tags):
            tags = helpers.ids(i.tags)
            Id = models.post.new(i.title, i.content, tags,
                                 i.autor, i.published, i.comment)
            slug = helpers.slug(i.title)
            raise web.seeother('/post/{1}/{0}'.format(Id, slug))
        return render('postnew.html', title=i.title, comment=i.comment,
                      tags=i.tags, published=i.published, autor=i.autor,
                      content=i.content)


class PostEdit:
    """
    Update a Post.
    """

    @logged
    def GET(self, post_id):
        post = models.post.one(post_id)
        return render('postedit.html', post=post)

    @logged
    def POST(self, post_id):
        i = web.input(id=post_id, published="", comment="")
        if helpers.validate(i.title, i.content, i.tags):
            tags = helpers.ids(i.tags)
            models.post.edit(post_id, i.title, i.content,
                             tags, i.autor, i.published, i.comment)
            slug = helpers.slug(i.title)
            raise web.seeother('/post/{1}/{0}'.format(post_id, slug))
        return render('postedit.html', post=i)


class TagAll:
    """
    All tags.
    """

    def __init__(self):
        """
        Clean unused tags.
        """
        models.tag.clean()

    def GET(self):
        i = web.input(p=1)
        limit = settings.limit
        count = models.count.tags()
        offset, pages, page = helpers.paginate(i.p, limit, count)
        tags = models.tag.all(offset, limit)
        return render('tags.html', tags=tags, page=page, pages=pages)


class TagOne:
    """
    Posts by tag.
    """

    def GET(self, tag_name, tag_id):
        """
        This method use tag_id for check if tag exist.
        """
        tag = models.tag.one(tag_id)
        if tag:
            if tag.name == tag_name or helpers.slug(tag.name) == tag_name:
                i = web.input(p=1)
                limit = settings.limit
                count = models.count.tag(tag_id)
                offset, pages, page = helpers.paginate(i.p, limit, count)
                posts = models.post.tag(tag_id, offset, limit)
                return render('tag.html', tag=tag, posts=posts, page=page,
                              pages=pages, count=count)
            raise web.seeother('/tag/{0}/{1}'.format(helpers.slug(tag.name),
                                                     tag_id))
        raise app.notfound()


class TagEdit:
    """
    Update a tag.
    """

    @logged
    def GET(self, tag_id):
        i = web.input(p=1)
        tag = models.tag.one(tag_id)
        return render('tagedit.html', tag=tag, page=i.p)

    @logged
    def POST(self, tag_id):
        i = web.input()
        if helpers.validate(i.name):
            models.tag.edit(tag_id, i.name)
            raise web.seeother('/tag?p={0}'.format(i.p))
        raise web.seeother('/tag/{0}/edit?p={1}'.format(tag_id, i.p))


class PostDelete:
    """
    Delete a post.
    """

    @logged
    def GET(self, post_id):
        models.post.delete(post_id)
        raise web.seeother('/post')


class CommentDelete:
    """
    Delete a comment.
    """

    @logged
    def DELETE(self, comment_id):
        """
        I can use method DELETE because I use Ajax
        for delete comments.
        """
        try:
            models.comment.delete(comment_id)
        except:
            raise web.notfound()
