import os
import sqlite3
import cherrypy



class chess_tournament(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def open_match(self, match_code):
        return open('index_error.html') 

cherrypy.quickstart(chess_tournament())
