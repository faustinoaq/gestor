#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create tables in database with SQLAlchemy
"""

import web

# SQLAlchemy modules
from sqlalchemy import create_engine, engine
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, String, CHAR, TIMESTAMP, TEXT
from sqlalchemy.sql import text

# Dict of database settings
from settings import database

# Add sqlite case
if database['dbn'] == 'sqlite':
    db = web.database(dbn='sqlite', db=database['db'])
    system = create_engine('sqlite:///'+database['db'], echo=True)
else:
    # Create objects of database
    db = web.database(**database)
    # Create database URL
    # dialect+driver://username:password@host:port/database
    dbURL = engine.url.URL(drivername=database['dbn'],
        username=database['user'],
        password=database['pw'],
        host=database['host'],
        port=database['port'],
        database=database['db'],
        query=None)
    # Create SQLAlchemy engine with dbURL and print log
    system = create_engine(dbURL, echo=True)

metadata = MetaData(bind=system)

# Create Tables
# For queries to database use web.database

# Create table posts
posts = Table('posts', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', TEXT()),
    Column('content', TEXT()),
    Column('tags', TEXT()),
    Column('autor', TEXT()),
    Column('published', String(10)),
    Column('comment', String(10)),
    Column('date', String(25)),
)

# Create table comments
comments = Table('comments', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', TEXT()),
    Column('email', TEXT()),
    Column('comment', TEXT()),
    Column('web', TEXT()),
    Column('post', Integer),
    Column('date', String(25)),
)

# Create table tags
tags = Table('tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', TEXT()),
)

# Create table sessions
sessions = Table('sessions', metadata,
    Column('session_id', CHAR(128), primary_key=True, nullable=False),
    Column('atime', TIMESTAMP(), server_default=text('current_timestamp')),
    Column('data', TEXT()),
)

# Create all tables in database
metadata.create_all()
