#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import argparse
import subprocess
import wordpresslib
import os
import sys
import tempfile
from utils import htmlentity2unicode

from config import *

# for vim
sys.path.append("/opt/vim/bin")
sys.path.append("/usr/local/bin")
sys.path.append("/usr/bin")
VIM = "vim"
VIM_ENC = "+e ++enc=utf-8" 


wp = wordpresslib.WordPressClient(BLOG_XMLRPC_URI, BLOG_USERNAME, BLOG_PASSWORD)
wp.selectBlog(BLOG_ID)


def readfile(filepath, charset='utf-8'):
    with open(filepath, "r") as f:
        return f.read().decode(charset)

def create_description(tmp_file, default_description=u"", charset='utf-8'):
    try:
        fh = os.fdopen(tmp_file[0], "w")
        if default_description != "":
            fh.write(default_description.encode(charset))
    except:
        print "ERROR! fdopen"
        return False
    finally:
        fh.close()

    try:
        # edit post description by vim
        subprocess.call([VIM, VIM_ENC, tmp_file[1]])
        if not os.path.exists(tmp_file[1]):
            return False

        description = readfile(tmp_file[1])
        if len(description) == 0:
            return False
    except:
        print "read post file error"
        print sys.exc_info()[0]
        sys.exit()
    finally: 
        os.remove(tmp_file[1])
        
    return description

def split_title(description):
    """
    :return:
        (title, description)
    """
    lines=description.split("\n")
    return (lines[0], "\n".join(lines[2:]))

def split_post(data):
    """
    :return:
        (title, cat, tag, description)
    """
    lines = data.split("\n")
    metalines = []
    for line in lines:
        if line == "":
            break
        metalines.append(line)

    title = metalines[0]
    if len(metalines)>1:
        for line in metalines:
            if line.index("cat:")==0:
                cat = line.split(":")[1].split(",")
            if line.index("tag:")==0:
                tag = line.split(":")[1].split(",")
    
    description = "\n".join(lines[len(metalines)+1:])

    return (title, cat, tag, description)

def main():
    parser = argparse.ArgumentParser(description="post to wordpress")
    parser.add_argument('-v', '--version', action='version', 
                        version='%(prog)s2.0')
    subparsers = parser.add_subparsers(dest='command', 
                                       title='commands', 
                                       help='select command')

    parser_new = subparsers.add_parser('new', help='create new post')
    parser_new.add_argument('post_title', default='', help='post title')
    parser_new.add_argument('-p', '--post_status', 
                            choices=('draft','publish'), 
                            default='draft', help='published status')

    parser_list = subparsers.add_parser('list', help='help')
    parser_list.add_argument('-s', '--start', type=int, 
                             default=0, help='start pos')
    parser_list.add_argument('-n', '--num', type=int, 
                             default=10, help='get number')

    parser_edit = subparsers.add_parser('edit', help='help')
    parser_edit.add_argument('-p', '--post_status', 
                             choices=('draft','publish'), 
                             help='published status')
    parser_edit.add_argument('id', type=int,help='post id')

    parser_delete = subparsers.add_parser('delete', help='help')
    parser_delete.add_argument('id', type=int,help='post id')

    args = parser.parse_args()

    command = args.command

    if command == 'new':
        publish = 0
        if args.post_status == 'publish':
            publish = 1
        post_title = args.post_title
        if post_title == '':
            post_title = 'notitle'

        tmp_file = tempfile.mkstemp(suffix='.html',text=True)
        before = post_title.decode('utf-8') + u"\n\n" + u""
        description = create_description(tmp_file, before)
        if not description or before == description:
            print "canceled"
            sys.exit()

        post_title, description = split_title(description)
        post = wordpresslib.WordPressPost()
        post.title = post_title
        post.description = description
        post.tags = []
        post.categories = []
        id = wp.newPost(post, publish)
        print "success new post id = %d" % (id)

    elif command == 'list':
        c = args.start
        n = 0
        for post in wp.getRecentPosts(args.start + args.num):
            if c > 0:
                c -= 1
                continue
            elif n < args.num:
                n += 1
                print "%5d: %7s: %s" % (post.id, post.post_status, post.title)
            else:
                break
    elif command == 'edit':
        id = args.id
        post = wp.getPost(id)
        scat = "cat:" + ",".join(post.categories)
        stag = "tag:" + post.tags
        post.categories = [cat.id for cat in wp.getPostCategories(id)]
     
        if args.post_status:
            publish_string = args.post_status
        else:
            publish_string = post.post_status

        if publish_string == 'draft':
            publish = 0
        elif publish_string =='publish':
            publish = 1

        tmp_file = tempfile.mkstemp(suffix='.html',text=True)
        before = htmlentity2unicode(post.title) + "\n"
        before += htmlentity2unicode(scat) + "\n"
        before += htmlentity2unicode(stag) + "\n"
        before += "\n" 
        before += htmlentity2unicode(post.description)
        if post.textMore != "":
            before += "<!--more-->" 
            before += htmlentity2unicode(post.textMore)
            
        after = create_description(tmp_file, before)
        if not after or before == after:
            print "canceled"
            sys.exit()

        post_title, cat, tag, description = split_post(after)
        import debug
        post.title = post_title
        post.description = description
        post.textMore = ""
        try:
            wp.editPost(id, post, publish)
        except:
            print "failure edit post id = %d" % (id)
            sys.exit()

        print "success edit post id = %d" % (id)

    elif command == 'delete':
        id = args.id
        try:
            wp.deletePost(id)
        except:
            print "failure delete post id = %d" % (id)
            sys.exit()
            
        print "success delete post id = %d" % (id)

    else:
        print "unknown command"


if __name__ == '__main__':
    main()

