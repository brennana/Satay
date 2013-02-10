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
import cPickle

class Map(EntBase):
    """Class representing map entity (places the player and items inhabit)"""
    def __init__(self, **props):
        if "itemlist" not in props:
            raise EntityError("Missing itemlist in map!")
        super(Map, self).__init__(**props)


class Item(EntBase):
    """Class representing item entity (things the player interacts with)"""
    def __init__(self, **props):
        super(Item, self).__init__(**props)

class NPC(EntBase):
    """Class representing NPCs (non player characters)."""
    def __init__(self, **props):
        if "dialog" not in props:
            raise EntityError("Missing dialog map in NPC!")
        if not isinstance(props["dialog"], DialogMap):
            raise EntityError("Dialog map must be of type 'DialogMap'!")
        super(NPC, self).__init__(**props)


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
        if "commands" not in settings:
            raise SettingsError("No commands defined for game!")
        if "variables" in settings:
            if type(settings["variables"]) != dict:
                raise SettingsError("Game variables must be a dictionary!")
            self.variables = settings["variables"]
        else:
            self.variables = dict()
        self.title = settings["title"]
        self.author = settings["author"]
        self.__objects__ =  self.__setids__(settings["objects"])
        self.__commands__ = settings["commands"]
        self.curmap = settings['start']
        self.caller = funcCls(self)
        self.history = History.New(self.__objects__, self.__commands__)
        super(BaseGame, self).__init__()

    def __getattr__(self, attr):
        return self.caller.__getattribute__(attr)

    def __setids__(self, objs):
        newObjs = {}
        for objID, obj in objs.items():
            obj.id = objID
            newObjs[EntRef(objID)] = obj
        return newObjs

    def __lOpen__(self, fname):
        """Unpickle loaddata from fname as file."""
        try:
            f = open(fname, 'r')
        except IOError:
            raise LoadGameError("Could not open file!")
        else:
            loaddata = cPickle.load(f)
        finally:
            f.close()
        return loaddata

    def __sOpen__(self, fname, savedata):
        """Open fname as file and pickle savedata."""
        try:
            f = open(fname, 'w')
        except IOError:
            raise SaveGameError("Could not create save file!")
        else:
            # Dump with protocol 2 (for efficiency)
            cPickle.dump(savedata, f)
        finally:
            f.close()

    def Save(self, fname, savedata={}):
        """Save a game."""
        savedata["inventory"] = self.inventory
        savedata["curmap"] = self.curmap
        savedata["variables"] = self.variables
        savedata["history"] = self.history.Dump()
        itemlists = {}
        for ID, obj in self.__objects__.items():
            if isinstance(obj, Map):
                itemlists[ID] = list(obj.itemlist())
        savedata["itemlists"] = itemlists
        self.__sOpen__(fname, savedata)

    def Load(self, fname, loaddata=None):
        """Load a game."""
        if loaddata is None:
            loaddata = self.__lOpen__(fname)

        if len(set(["inventory", "curmap", "itemlists", "history", "variables"]) - set(loaddata)) != 0:
            raise LoadGameError("Missing data in savefile!")

        for ID, itemlist in loaddata["itemlists"].items():
            self.__objects__[ID].itemlist[''] = NumeratedList.FromList(itemlist)
        self.curmap = loaddata["curmap"]
        self.inventory = loaddata["inventory"]
        self.variables = loaddata["variables"]
        self.history = History.Load(loaddata["history"])

    def InsertHistory(self, command, *args):
        pass

    def GetCurmap(self):
        return self.__objects__[self.curmap]

    def CheckScope(self, *ents):
        """Check if an entity is in the current scope (curmap or inventory)"""
        return all([a.id in self.inventory or a.id in self.GetCurmap().itemlist() for a in ents])

    def CheckMapScope(self, *ents):
        """Check if entities are in the curmap scope."""
        return all([a.id in self.GetCurmap().itemlist() for a in ents])

    def CheckInvScope(self, *ents):
        """Check if entities are in the inventory scope."""
        return all([a.id in self.inventory for a in ents])
