"""-------------------------------------------------
Satay Game Engine Copyright (C) 2012 Andy Brennan

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR APARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
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

from Base import *
from Exceptions import *

# Game variables
__commands__ = []
__objects__ = {}
settings = dict()

# Player variables
curmap = None
inventory = None

# Game Functions
def PPrint(message):
    """Print a Message to Game Screen."""
    print(message)

def PReplace(item1, item2):
    """Replace item1 with item2."""
    global inventory
    global __objects__
    global curmap
    if item1 in inventory:
        inventory.Take(item1)
        inventory.Give(item2)
    elif item1 in __objects__[curmap].itemlist():
        print "here"
        __objects__[curmap].itemlist().Take(item1)
        __objects__[curmap].itemlist().Give(item2)


def PChgMap(newmap):
    """Change the current game map to newmap."""
    global curmap
    curmap = newmap

def PRemoveFromMap(item):
    """Remove 1 of 'item' from the current map."""
    global __objects__
    global curmap
    __objects__[curmap].itemlist().Take(item)

def PAddToInventory(item):
    """Add 1 of 'item' to the inventory."""
    pass


# Main input loop for game
def __mainloop__():
    # Print opening line, then go into loop
    PPrint(settings["title"] + " by " + settings["author"])
    while 1:
        PPrint(__objects__[curmap].name())
        PPrint(__objects__[curmap].desc())
        cmd = raw_input("> ")
        if cmd == 'quit':
            break
        try:
            pcmd = __parse__(cmd)
        except AmbiguityError as ex:
            PPrint(ex.message)
            continue
        # Nothing passed by user
        if len(pcmd) <= 0:
            continue
        called = False
        for command in __commands__:
            if command.__name__ == pcmd[0]:
                try:
                    command(pcmd[1:])
                except CommandError as ex:
                    PPrint(ex.message)
                called = True
                break
            else:
                continue
        if not called:
            PPrint("Hmm?")

# Parses user input for Command class
def __parse__(line):
    args = []
    posf = 0
    posb = 0
    for char in line:
        posb = posb + 1
        if char == " " or posb == len(line):
            args.append(line[posf:posb].strip().lower())
            posf = posb
    return __resolve__(args)

# Resolves argument list into list of entities and conjunctions (strings)
# Rules for priority:
#   * A described noun (e.g. green rock) trumps regular nouns (e.g. rock).
#   * Above holds true for all cases--the more specific, the higher its priority
#       (e.g. "green smelly rock" trumps "green rock" trumps "rock").
#   * Conjunctions do not describe nouns.
#   * First argument is always the command--therefore, skip it.
#   * If the noun described is ambiguous, then do nothing.
# Method:
#   Iterate over our list of args, and attempt to find a noun, then find all words
#   preceeding that noun and check them against those nouns' adjective lists.
#   The rules above dictate what a block of strings will be translated into.
#   Non-translated strings are conjunctions.
def __resolve__(args):
    # Adjective position marker
    adjp = 0
    usradj = []
    nouns = {k:(v.nbase(),v.descriptors()) for k,v in __objects__.items()}
    for arg in args[1:]:
        if arg in [t[0] for t in nouns.values()]:
            candidates = {}
            #Found a noun! Now backtrack and examine adjectives to the last noun/command
            # and compare against adjectives in each possible nouns
            for ID, nountuple in nouns.items():
                if nountuple[0] != arg:
                    continue
                # There ARE adjs the user gave that do NOT describe our object.
                adjcmp = set(usradj) - set(nountuple[1])
                if len(adjcmp) > 0:
                    continue
                else:
                    candidates[len(adjcmp)] = ID
            amts = candidates.keys()
            amts.sort(reverse=True)
            if len(amts) <= 0:
                continue
            # Ambiguity in user's described noun
            if amts.count(amts[0]) > 1:
                raise AmbiguityError("Which one are you talking about?")
            args[adjp+1:len(usradj)+adjp+2] = [__objects__[candidates[amts[0]]]]
            print args
            adjp += 1

        elif arg in sum([tup[1] for tup in nouns.values()],[]):
            usradj.append(arg)
        else:
            usradj = []
            adjp += 1
    return args

def __setids__(objs):
    newObjs = {}
    for objID, obj in objs.items():
        obj.id = objID
        newObjs[objID] = obj
    return newObjs

def CheckScope(ent):
    """Check if a entity is in the current scope (curmap or inventory)"""
    return ent.id in inventory or ent.id in __objects__[curmap].itemlist()

class Map(EntBase):
    """Class representing map entity (places the player and items inhabit)"""
    pass

class Item(EntBase):
    """Class representing item entity (things the player interacts with)"""
    pass

def RegisterCommands(*args):
    """Register commands with the game."""
    global __commands__
    __commands__ += args

def Initialize():
    """Start the game."""
    if "title" not in settings:
        settings["title"] = "Untitled"
    if "author" not in settings:
        settings["author"] = "Anonymous"
    if "items" in settings:
        global inventory
        inventory = settings["items"]
    if "objects" not in settings:
        raise SettingsError("No maps/items defined!")
    else:
        global __objects__
        __objects__ = __setids__(settings["objects"])
    if not all(["nbase" in w and "descriptors" in w for w in settings["objects"].values()]):
        raise SettingsError("Missing name conventions (nbase and descriptors)!")
    try:
        global curmap
        curmap = settings['start']
    except KeyError:
        raise SettingsError("No startmap defined!")
    __mainloop__()
