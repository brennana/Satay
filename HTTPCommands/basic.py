from Satay.Base import Command
from Satay.HTTPGame.Game import Item, Map, NPC
from Satay.Exceptions import *

class go(Command):
    def form1(self, direction):
        newmap = None
        cmap = self.game.GetCurmap()
        print direction
        if direction == "forward":
            self.ExpectProperty(cmap, 'forward')
            newmap = cmap.forward()
        elif direction == "backward":
            self.ExpectProperty(cmap, 'backward')
            newmap = cmap.backward()
        elif direction == "left":
            self.ExpectProperty(cmap, 'left')
            newmap = cmap.left()
        elif direction == "right":
            self.ExpectProperty(cmap, 'right')
            newmap = cmap.right()
        else:
            self.ThrowType()
        self.game.ChgMap(newmap)

    funclist = [form1]
    NoSuitableFormMsg = "Go where, now?"
    ConjunctionMsg    = "I can't understand you."
    TypeMsg           = "Go where, now?"
    PropertyMsg       = "You cannot go that way."
    ScopeMsg          = "That place is nowhere to be found."