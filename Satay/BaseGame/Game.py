"""-------------------------------------------------
Satay Game Engine Copyright (C) 2012 Andy Brennan

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

from ..Base import *
from ..Exceptions import *
from Functions import *

class Map(EntBase):
    """Class representing map entity (places the player and items inhabit)"""
    pass

class Item(EntBase):
    """Class representing item entity (things the player interacts with)"""
    pass

class BaseGame(object):
    """Base class for any kind of game."""
    def __init__(self, settings, funcCls=BaseGameFuncs):
        if "title" not in settings:
            settings["title"] = "Untitled"
        if "author" not in settings:
            settings["author"] = "Anonymous"
        if "objects" not in settings:
            raise SettingsError("No maps/items defined!")
        if "start" not in settings:
            raise SettingsError("No startmap defined!")
        if "items" in settings:
            self.inventory = settings["items"]
        else:
            self.inventory = NumeratedList()
        self.title = settings["title"]
        self.author = settings["author"]
        self.__objects__ =  self.__setids__(settings["objects"])
        self.curmap = settings['start']
        self.caller = funcCls(self)
        super(BaseGame, self).__init__()

    def __getattr__(self, attr):
        return self.caller.__getattribute__(attr)

    def __mainloop__(self):
        pass

    def __setids__(self, objs):
        newObjs = {}
        for objID, obj in objs.items():
            obj.id = objID
            newObjs[EntRef(objID)] = obj
        return newObjs

    def GetCurmap(self):
        return self.__objects__[self.curmap]

    def CheckScope(self, *ents):
        """Check if a entity is in the current scope (curmap or inventory)"""
        return all([a.id in self.inventory or a.id in self.GetCurmap().itemlist() for a in ents])

    def CheckMapScope(self, *ents):
        """Check if entities are in the curmap scope."""
        return all([a.id in self.GetCurmap().itemlist() for a in ents])

    def CheckInvScope(self, *ents):
        """Check if entities are in the inventory scope."""
        return all([a.id in self.inventory for a in ents])
