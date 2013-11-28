#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Adaptation of Jinja2 Templates to Gestor.
"""

from jinja2 import Environment, FileSystemLoader

import settings

# Jinja2 Extensions as htmljinjacompressor, pygments, etc.
extensions = []

# Load the templates from directory specified in settings
jinja_env = Environment(loader=FileSystemLoader(settings.templates),
                        extensions=extensions)


def render(template, **context):
    """
    Render the template with globals vars.
    """
    return jinja_env.get_template(template).render(context)
