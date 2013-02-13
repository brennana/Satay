from Satay.Base import Command
from Satay.TextGame.Game import Item, Map
from Satay.Exceptions import *

class eat(Command):
    def form1(self, item):
        self.ExpectType(item, Item)
        self.ExpectProperty(item, "eat_edible")
        if not self.game.CheckScope(item):
            self.ThrowScope()
        if not item.eat_edible:
            self.ThrowProperty()
        self.game.RemoveFromInventory(item)
        if "eat_message" not in item:
            self.game.Print("Eaten.")
        else:
            self.game.Print(item.eat_message())

    def form2(self, item, cWith, utensil):
        self.ExpectType(item, Item)
        self.ExpectType(utensil, Item)
        if not self.game.CheckScope(item, utensil):
            self.ThrowScope()
        if not item.eat_edible:
            self.ThrowProperty()
        if cWith not in ['with','using']:
            self.ThrowConjunction()
        self.game.RemoveFromInventory(item)
        if "eat_message" not in item:
            self.game.Print("Eaten.")
        else:
            self.game.Print(item.eat_message(utensil))

    funclist=[form1, form2]
    NoSuitableFormMsg = "Eat what?"
    ConjunctionMsg    = "Learn to English, my friend."
    TypeMsg           = "You cannot eat this!"
    PropertyMsg       = "You cannot eat this!"
    ScopeMsg          = "That item is nowhere to be found."
