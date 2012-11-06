# Some important, basic commands for use in a TextGame
from Satay.Base import Command
from Satay.TextGame.Game import Item, Map
from Satay.Exceptions import *

class look(Command):
    def form1(self):
        self.game.Print(self.game.GetCurmap().name())
        self.game.Print(self.game.GetCurmap().desc())
    def form2(self, obj):
        self.ExpectType(obj, Item, Map)
        if self.game.CheckScope(obj):
            self.game.Print(obj.name())
            self.game.Print(obj.desc())
        else:
            self.ThrowScope()
    funclist = [form1, form2]
    NoSuitableFormMsg = "Look at what, now?"
    ConjunctionMsg    = "I can't understand you."
    TypeMsg           = "Look at what, now?"
    ScopeMsg          = "Object is nowhere to be found."

class go(Command):
    def form1(self, direction):
        newmap = None
        cmap = self.game.GetCurmap()
        if direction in ['n', 'north']:
            self.ExpectProperty(cmap, 'n')
            newmap = cmap.n()
        elif direction in ['e', 'east']:
            self.ExpectProperty(cmap, 'e')
            newmap = cmap.e()
        elif direction in ['w', 'west']:
            self.ExpectProperty(cmap, 'w')
            newmap = cmap.w()
        elif direction in ['s', 'south']:
            self.ExpectProperty(cmap, 's')
            newmap = cmap.s()
        elif direction in ['u', 'up']:
            self.ExpectProperty(cmap, 'u')
            newmap = cmap.u()
        elif direction in ['d', 'down']:
            self.ExpectProperty(cmap, 'd')
            newmap = cmap.d()
        else:
            self.ThrowType()
        self.game.ChgMap(newmap)
        # Print the new map's name and desc
        self.game.Print(self.game.GetCurmap().name())
        self.game.Print(self.game.GetCurmap().desc())

    funclist = [form1]
    NoSuitableFormMsg = "Go where now?"
    ConjunctionMsg    = "I can't understand you."
    TypeMsg           = "Go where, now?"
    PropertyMsg       = "You cannot go that way."
    ScopeMsg          = "That place is nowhere to be found."

class take(Command):
    def form1(self, item):
        self.ExpectType(item, Item)
        if self.game.CheckMapScope(item):
            self.game.RemoveFromMap(item)
            self.game.AddToInventory(item)
            self.game.Print("Taken.")
        else:
            self.ThrowScope()

    funclist = [form1]
    NoSuitableFormMsg = "Take what, now?"
    ConjunctionMsg    = "I can't understand you."
    TypeMsg           = "Take what, now?"
    PropertyMsg       = "You cannot take that."
    ScopeMsg          = "That item is nowhere to be found."

class get(take):
    pass

class drop(Command):
    def form1(self, item):
        self.ExpectType(item, Item)
        if self.game.CheckInvScope(item):
            self.game.AddToMap(item)
            self.game.RemoveFromInventory()
            self.game.Print("Dropped.")
        else:
            self.ThrowScope()

    funclist = [form1]
    NoSuitableFormMsg = "Drop what, now?"
    ConjunctionMsg    = "I can't understand you."
    TypeMsg           = "Drop what, now?"
    PropertyMsg       = "You cannot drop that."
    ScopeMsg          = "That item is not in your inventory."
