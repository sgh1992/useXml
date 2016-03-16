# !/usr/bin/python
#  -*- coding: utf-8 -*-

from xml.sax.handler import  ContentHandler
from xml.sax import parse
import os
class HeadLineHandler(ContentHandler):
    """
    主要是根据对应的事件处理器来解析xml文件.
    主要是处理H1的头标题.
    只是一个demo,尝试!
  """
    def __init__(self, headLines):
        self.headLines = headLines
        self.data = []
        self.headFlag = False

    def startDocument(self):
        print "<html><head>...</head><body>"

    def endDocument(self):
        print "</body></html>"

    def startElement(self, name, attrs):
        if name == 'h1':
            self.headFlag = True

    def endElement(self, name):
        if name == 'h1':
            if self.headFlag:
                text = ''.join(self.data)
                self.headLines.append(text)
                self.headFlag = False
                self.data = []

    def characters(self, content):
        if self.headFlag:
            self.data.append(content)


class dispatch:
    """
    中间件，调度器.
    注意理解这种设计模式.
    """
    def __init__(self):
        pass

    def startElement(self, name, attrs):
        """

        :param name:实际上是指当前元素的名称.
        :param attrs: 实际上指的元素内的各个键值对.
        :return:
        """
        self.disptach("start", name, attrs)

    def endElement(self, name):
        self.disptach("end", name, None)

    def disptach(self, prefix, name, attrs):
        mn = prefix + name.capitalize()
        dn = "default" + prefix.capitalize()
        method = getattr(self, mn, None)  # 注意getattr的使用,它只是判定对象内是否存在这个方法，并不实际调用这个方法,所以可以不用传递参数.
        if callable(method):
            args = ()
        else:
            # 如果对象中不存在对应的方法,則使用其默认的方法.
            method = getattr(self, dn, None)
            args = name,
        if prefix == 'start':
            args += attrs,

        if callable(method):
            method(*args)  # 真正开始利用这个方法.


class MyHandler(dispatch, ContentHandler):
    def __init__(self, directionary):
        self.dirctionary = [directionary]
        self.passthrough = False
        self.out = None

    def startDirectory(self, attrs):
        self.dirctionary.append(attrs['name'])
        self.ensuredirectory()

    def endDirectory(self):
        self.dirctionary.pop()

    def ensuredirectory(self):
        dirName = os.path.join(*self.dirctionary)
        if not os.path.isdir(dirName):
            os.mkdir(dirName)
        return dirName

    def defaultStart(self, name, attrs):
        if self.passthrough:
            # html文件中需要用到这种符号吗.实际上是需要的,由于它可能是html文件中所需要的元素.
            self.out.write("<" + name + " ")
            for key, value in attrs.items():
                self.out.write(key + "=" + value + " ")
            self.out.write(" >")
            self.out.write("\n")

    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write("</")
            self.out.write(name)
            self.out.write(">")
            self.out.write("\n")

    def startPage(self, attrs):

        self.out = open(os.path.join(self.ensuredirectory(), attrs['name'] + ".html"), 'w')
        self.passthrough = True
        self.writeStartFoot(attrs['title'])
        self.out.write("\n")

    def endPage(self):
        self.writeEndFoot()
        self.passthrough = False
        self.out.close()

    def writeEndFoot(self):
        self.out.write("</body></html>")
        self.out.write("\n")

    def writeStartFoot(self,title):
        self.out.write("<html><head><title>\n")
        self.out.write(title)
        self.out.write("</title></head>\n")
        self.out.write("<body>")

    def characters(self, content):
        if self.passthrough:
            self.out.write(content)