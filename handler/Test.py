# !/usr/bin/python
#  -*- coding: utf-8 -*-
import SimpleHandler
from xml.sax import parse
"""
测试
"""
xmlfile = "/home/sghipr/PycharmProjects/useXml/test/website.xml"
handler = SimpleHandler.MyHandler("/home/sghipr/PycharmProjects/useXml")
parse(xmlfile, handler)
