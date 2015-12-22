#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Andrew Tsai'
SITENAME = "TH's Notes"
SITEURL = ''
#SITEURL = 'tsaith.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
'''
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)
'''

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Plugins
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.youtube', 'liquid_tags.include_code',
           'liquid_tags.notebook','render_math','googleplus_comments',
           'liquid_tags.flickr', 'pelican_gist']
 
# For notebooks
NOTEBOOK_DIR = 'notebooks'
        

# Flickr images
FLICKR_API_KEY = '69a5ee09fe685cf9c3c304118b219549'

DIRECT_TEMPLATES = ['index', 'categories', 'authors', 'archives']

# Theme
THEME = "../pelican-themes/pelican-bootstrap3"

# Social widget
SOCIAL = (('Github', 'https://github.com/tsaith'),
          ('Twitter', 'https://twitter.com/tsunghuatsai'),
          ('Linkedin', 'https://linkedin.com/in/tsunghua'),)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
