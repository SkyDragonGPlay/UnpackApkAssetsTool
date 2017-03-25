# -*- coding: UTF-8 -*-

import os
from xml.dom.minidom import parse
import xml.dom.minidom

def xmlParseTest():
    if not os.path.isfile('movies.xml'):
        print 'movies.xml not exist'
        return

    DOMTree = xml.dom.minidom.parse("movies.xml")

    collection = DOMTree.documentElement
    if(collection.hasAttribute("shelf")):
        print "Root element : %s" % collection.getAttribute("shelf")

    movies = collection.getElementsByTagName("movie")

    for movie in movies:
        print '************Movie************'
        if movie.hasAttribute('title'):
            print "Title: %s" % movie.getAttribute("title")

        type = movie.getElementsByTagName('type')[0]
        print 'Type: %s' % type.childNodes[0].data

        format = movie.getElementsByTagName('format')[0]
        print 'Format: %s' % format.childNodes[0].data

        rating = movie.getElementsByTagName('rating')[0]
        print 'Rating: %s' % rating.childNodes[0].data

        description = movie.getElementsByTagName('description')[0]
        print 'Description: %s' % description.childNodes[0].data








