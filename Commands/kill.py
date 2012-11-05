# Lil' test command script
from Satay.Base import Command
from Satay.BaseGame.Game import Map, Item
from Satay.Exceptions import *

# Create commands
class kill(Command):
    def form1(self, item1):
        self.ExpectType(item1, Item)
        self.ExpectProperty(item1, ['kill_msg','kill_newitem'])
        if self.game.CheckScope(item1):
            self.game.Print(item1.kill_msg())
            self.game.Replace(item1, item1.kill_newitem())
        else:
            self.ThrowScope()

    def form2(self, item1, cWith, item2):
        if cWith not in ['with','using']:
            self.ThrowConjunction()
        self.game.Print(item1.kill_msg(item2))
        self.game.Replace(item1, item1.kill_newitem(item2))

    funclist = [form1,form2]
    NoSuitableFormMsg = "No function found for args given!"
    ConjunctionMsg    = "Learn to English, my friend."
    TypeMsg           = "You cannot kill like this!"
    PropertyMsg       = "You cannot kill this!"
    ScopeMsg          = "Object is nowhere to be found."

# Another name for kill
class murder(kill):
    pass
