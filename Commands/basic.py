# Some important, basic commands for use in a TextGame
from Satay.Base import Command
from Satay.TextGame.Game import Item, Map
from Satay.Exceptions import *
import time
import os

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
    NoSuitableFormMsg = "Go where, now?"
    ConjunctionMsg    = "I can't understand you."
    TypeMsg           = "Go where, now?"
    PropertyMsg       = "You cannot go that way."
    ScopeMsg          = "That place is nowhere to be found."

class take(Command):
    def form1(self, item):
        self.ExpectType(item, Item)
        if self.game.CheckMapScope(item):
            try:
                self.ExpectProperty(item, 'untakeable')
            except CommandPropertyError:
                pass
            else:
                if item.untakeable == True:
                    self.ThrowProperty()
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
            self.game.RemoveFromInventory(item)
            self.game.Print("Dropped.")
        else:
            self.ThrowScope()

    funclist = [form1]
    NoSuitableFormMsg = "Drop what, now?"
    ConjunctionMsg    = "I can't understand you."
    TypeMsg           = "Drop what, now?"
    PropertyMsg       = "You cannot drop that."
    ScopeMsg          = "That item is not in your inventory."

class save(Command):
    def form1(self):
        fname = "Genericsave_"+str(int(time.time()))+".sav"
        try:
            self.game.SaveGame(fname)
        except SaveGameError:
            raise CommandError("Could not save game!")
        self.game.Print("Saved.")

    def form2(self, fname):
        self.ExpectType(fname, str)
        fname = fname.strip('"\'')+".sav"
        try:
            self.game.SaveGame(fname)
        except SaveGameError:
            raise CommandError("Could not save game!")
        self.game.Print("Saved.")

    funclist = [form1, form2]
    NoSuitableFormMsg = "Save what, now?"
    TypeMsg           = "That's not a filename. (Try quotes!)"

class load(Command):
    def form1(self):
        ls = os.listdir('./')
        candidates = []
        for f in ls:
            if f.startswith("Genericsave_") and f.endswith(".sav"):
                candidates.append(int(f[12:-4]))
        candidates.sort(reverse=True)
        try:
            self.game.LoadGame("Genericsave_"+str(candidates[0])+".sav")
        except LoadGameError:
            raise CommandError("Could not load game!")
        self.game.Print("Loaded.")

    def form2(self, fname):
        self.ExpectType(fname, str)
        fname = fname.strip('"\'')+".sav"
        try:
            self.game.LoadGame(fname)
        except LoadGameError:
            raise CommandError("Could not load game!")
        self.game.Print("Loaded.")

    funclist = [form1, form2]
    NoSuitableFormMsg = "Load what, now?"
    TypeMsg           = "That's not a filename. (Try quotes!)"

class quit(Command):
    def form1(self):
        self.game.QuitGame()

    funclist = [form1]
    NoSuitableFormMsg = "Just type 'quit'."

class inventory(Command):
    def form1(self):
        for pair in self.game.GetInventory().items():
            if pair[1] > 0:
                self.game.Print("%r \t %r" % pair)
    funclist = [form1]
    NoSuitableFormMsg = "Just say 'inventory'."
    ConjunctionMsg    = "I can't understand you."

class inv(inventory):
    NoSuitableFormMsg = "Just say 'inv'."

class i(inventory):
    NoSuitableFormMsg = "Just say 'i'."
