#!/bin/env python
from ocg_parser import *
from ct_parser import *
import re

#list of parsers ['filename pattern', 'document instance', 'file type name'] 
parser_map = [
        (re.compile(r'.*\.ct'), CtDocument(CtBlock), ".ct"),
        (re.compile(r'msg_.*\.txt'), OcgDocument(OcgBlock), "ocg msg trace"),
        ]

def error_msg():
    return '<p id="err">Sorry, I can only support %s files, your upload file type is not supported<p/>'%(', '.join(map(lambda p:p[2], parser_map)))

head = '''<!doctype html>
<html>
<link rel=stylesheet type=text/css href=/static/style.css>
<title>after colorized</title>
<body>
'''
tail = "</body></html>"
        

def render_msg(filename, msg):
    doc = None
    for r in parser_map:
        if r[0].match(filename) is None:
            continue
        doc = r[1]
    try:
        body = doc.transform(msg)
        return (200, head+ body +tail)
    except Exception,e:
        print e
        return (501, head + error_msg() +tail)

def render_msg2(filename, msg):
    doc = None
    for r in parser_map:
        if r[0].match(filename) is None:
            continue
        doc = r[1]
    try:
        body = doc.transform(msg)
        return (200, doc.blocks)
    except Exception,e:
        print e
        return (501, error_msg())
