import os
import sqlite3
import cherrypy
import chess_html

class chess_tournament(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def open_match(self, match_code):
        try:
            conn = sqlite3.connect('tournament_register.db')
            cursor = conn.execute(
                'SELECT tournament_index, tournament_path \
                FROM tournament_register \
                WHERE match_code_root="' + match_code + '";'
            );
            count = 0
            for row in cursor:
                count += 1
                if row[0] == 1:
                    vv = chess_html.setup_tournament()
                    return vv
                else:
                    return "Path: " + row[1]
            if count == 0:
                return "0234" 
        except Exception as err:
            return "ERROR: " + str(err)
cherrypy.quickstart(chess_tournament())
