from Satay.Base import Command
from Satay.TextGame.Game import Item, Map, NPC
from Satay.Exceptions import *

class talk(Command):
    def form1(self, npc1):
        self.game.Print(npc1)
        self.ExpectType(npc1, NPC)
        if self.game.CheckScope(npc1):
            # Here we enter and traverse dialog tree from start to end
            tree = npc1.dialog()
            curpos = "start"
            redirected = True
            while True:
                self.game.Print(tree[curpos].speech)
                if redirected:
                    for action in tree[curpos].actions:
                        action(self.game)
                redirected = False
                if tree[curpos].end == True:
                    break
                num = 0
                for response in tree[curpos].responses:
                    if not all([func(self.game) for func in response.conditions]):
                        continue
                    num += 1
                    self.game.Print(str(num)+') '+response.response)
                try:
                    sel = int(self.game.RequestInput("(Choose Response)>> "))
                except ValueError, e:
                    self.game.Print("Selection must be a number.")
                    continue
                if sel not in range(1,num+1):
                    self.game.Print("Improper selection.")
                    continue
                curpos = tree[curpos].responses[sel-1].redirect
                redirected = True
    funclist=[form1]
    NoSuitableFormMsg = "Talk to who?"
    ConjunctionMsg    = "Learn to English, my friend."
    TypeMsg           = "You cannot talk like this!"
    PropertyMsg       = "You cannot talk to this!"
    ScopeMsg          = "Person is nowhere to be found."
