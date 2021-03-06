"""-------------------------------------------------
Satay Game Engine Copyright (C) 2013 Andy Brennan

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Satay on GitHub: https://github.com/Valdez42/Satay

 Game.py --
   Game module for use in game creation.
   Here, game settings are set, commands are registered,
   and the game is actually played.
-------------------------------------------------"""

from ..BaseGame import Game as BaseGame
from ..Exceptions import *
from Functions import *

import BaseHTTPServer
import mimetypes
import json
import uuid

class Map(BaseGame.Map):
    """Class representing map entity (places the player and items inhabit)"""
    def __init__(self, **props):
        super(Map, self).__init__(**props)

class Item(BaseGame.Item):
    """Class representing item entity (things the player interacts with)"""
    def __init__(self, **props):
        super(Item, self).__init__(**props)

class NPC(BaseGame.NPC):
    """Class representing NPCs (non player characters)."""
    def __init__(self, **props):
        super(NPC, self).__init__(**props)

class HTTPGameHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """HTTP handler for a Satay game."""
    def do_GET(self):
        """Serve a GET request."""
        res = self.send_head()
        print self.wfile.write(res)

    def send_head(self):
        request = self.decode_literals(self.path).split("?")
        path = request[0].split('/')
        additional = []
        if(len(request) == 2):
            additional = request[1].split('&')
        elif(len(request) == 1):
            pass
        else:
            return self.create_error(404)
  
        try:
            if path[1] == "game":
                ctype = "text/html"
                if len(path) == 2:
                    response = self.open_file(self.server_root+self.build_path(path)+"/index.html")
                else:
                    response = self.open_file(self.server_root+self.build_path(path))
            elif path[1] == "assets":
                ctype = self.guess_type(self.path)
                response = self.open_file(self.server_root+'/assets/'+self.build_path(path[2:]))
            elif path[1] == "properties":
                ctype = "application/json"
                dyn = path[4] if len(path) > 4 else ''

                try:
                    response = '{"value":%r}' % getattr(self.game.__objects__[path[2]], path[3])(dyn)
                    response = response.replace("'", '"')
                except PropertyError:
                    return self.create_error(404)
            elif path[1] == "dataonly":
                # User requested data only
                ctype = "application/json"
                game = self.aquire_client_session()
                return json.dumps(self.gather_data(game, additional, {"status":True, "message":None}))
            elif path[1] == "session":
                # Create new session for client
                ctype = "text/html"
                session = self.session.CreateSession()
                response = "<!DOCTYPE html><html><head><title>Session Created</title></head><body></body></html>"
            else:
                # A command was sent to the server. Execute and send json data.
                
                game = self.aquire_client_session()
                ctype = "application/json"
                dict_response = {"status":None, "message":None, "gameData":{}}
                # User requested for data only
                if path[1] == "data":
                    dict_response["status"] = True
                else:
                    for command in game.__commands__:
                        if command.__name__ == path[1]:
                            try:
                                command(game, path[2:])
                            except CommandError as ex:
                                dict_response["status"] = False
                                dict_response["message"] = ex.message
                            else:
                                dict_response["status"] = True
                                dict_response = self.gather_data(additional, dict_response)

                return json.dumps(dict_response)
        except IOError:
            return self.create_error(404)
        else:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            try:
                self.send_header("Set-Cookie", 'satay_session='+session)
            except NameError:
                pass
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            return response

    def open_file(self, path):
        with open(path, "rb") as asset:
            return asset.read()

    def gather_data(self, game, additional, dict_response={}):
        print additional
        dict_response["gameData"] = game.GetData()
        if len(additional) > 0:
            for addition in additional:
                try:
                    addition = addition.split('=')
                    if addition[0] == 'curmap':
                        obj = game.curmap
                    else:
                        obj = addition[0]
                    for selection in addition[1].replace(' ', '').split(","):
                        prop_full = selection.split(':')
                        prop = prop_full[0]
                        dyn = prop_full[1] if len(prop_full) == 2 else ''
                        dyn_str = '_'+dyn if dyn != '' else ''
                        dict_response["gameData"][addition[0]+"_"+prop+dyn_str] = getattr(game.__objects__[obj], prop)(dyn)
                except (PropertyError, KeyError):
                    dict_response[addition[0]+"_"+prop+dyn_str] = None
        return dict_response

    def decode_literals(self, path):
        for code, literal in self.literals.items():
            path = path.replace(code, literal)
        return path

    def aquire_client_session(self):
        sessionID = self.parse_cookie(self.headers.getheader('Cookie'))["satay_session"]
        game = self.session.GetSession(sessionID)
        print game
        return game

    def parse_cookie(self, cookies):
        cookie_dict = {}
        cookie_list = cookies.split(";")
        for cookie in cookie_list:
            pair = cookie.strip().split('=')
            cookie_dict[pair[0]] = pair[1]
        return cookie_dict

    def create_error(self, error_code):
        try:
            response = self.open_file(self.server_root+"/errors/"+str(error_code)+".html")
        except IOError:
            response = "<!DOCTYPE html><html><head><title>%s Error</title></head><body><h1>Unhanded %s Error Occurred</h1></body></html>" % (error_code, error_code)

        self.send_response(error_code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        return response

    def guess_type(self, path):
        ext = "." + path.rpartition('.')[2].lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    def build_path(self, lpath):
        built = ""
        for piece in lpath:
            built += piece + '/'
        return built[:-1]

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })
    literals = {
        "%3A":":",
        "%3B":";",
        "%2C":",",
        "%20":" ",
        "+":" ",
    }
    server_version = "Satay/0.1"

class SessionHandler(object):
    """Base class for handling an HTTP session"""
    def __init__(self):
        super(SessionHandler, self).__init__()
        self.sessions = {}
    def GetSession(self, sessionID):
        return self.sessions[sessionID]
    def LoadSession(self, sessionID):
        game = HTTPGame()
        game.Load(sessionID)
        self.sessions[sessionID] = game
    def CreateSession(self):
        sessionID = self.GenerateID()
        game = HTTPGame()
        self.sessions[sessionID] = game
        return sessionID
    def GenerateID(self):
        return uuid.uuid4().hex


class HTTPGame(BaseGame.BaseGame):
    """HTTP-based game with Satay."""
    def __init__(self, settings=None, funcCls=HTTPGameFuncs):
        if settings is None:
            settings = self.gameSettings
        super(HTTPGame, self).__init__(settings, funcCls)

    def GetData(self):
        """Get important game data for json dumping."""
        data = {}
        data["inventory"] = dict(self.inventory)
        data["curmap"] = self.curmap
        data["variables"] = self.variables
        return data

    @classmethod
    def Run(cls, root, settings, ip="localhost", port=80, sessionHandler=SessionHandler, httpHandler=HTTPGameHandler):
        """Run the game."""
        try:
            #httpHandler.game = self
            HTTPGameHandler.server_root = root
            HTTPGameHandler.session = sessionHandler()
            cls.httpd = BaseHTTPServer.HTTPServer((ip, port), httpHandler)
            cls.port = port
            cls.ip = ip
            cls.gameSettings = settings
            print("Serving "+settings["title"]+" by "+settings["author"]+" at port " + str(port))
            cls.httpd.serve_forever()
        except KeyboardInterrupt:
            cls.httpd.shutdown()
        # Server shutdown
        print("Server shutdown.")

    httpd = None
    port = None
    ip = None
    gameSettings = None