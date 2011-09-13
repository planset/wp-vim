#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wordpresslib

from config import *
from wplist import print_list

wp = wordpresslib.WordPressClient(BLOG_XMLRPC_URI, BLOG_USERNAME, BLOG_PASSWORD)
wp.selectBlog(BLOG_ID)

if __name__ == '__main__':
    print_list("%5d: %7s: %s\t%s", "delete")

