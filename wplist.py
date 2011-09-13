#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wordpresslib
import os
import sys

from config import *
reload(sys)
sys.setdefaultencoding('utf-8')

wp = wordpresslib.WordPressClient(BLOG_XMLRPC_URI, BLOG_USERNAME, BLOG_PASSWORD)
wp.selectBlog(BLOG_ID)

def print_list(format, command):
    c = 0
    n = 0
    MAX_N = LIST_NUMBER
    for post in wp.getRecentPosts(MAX_N):
        if c > 0:
            c -= 1
            continue
        elif n < MAX_N:
            n += 1
            print format % (post.id, post.post_status, post.title, "!python" + " " + WPCONTROL_PATH + " " + command + " " + str(post.id))
        else:
            break

if __name__ == '__main__':
    main()

