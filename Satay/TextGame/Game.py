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

class TextGame(BaseGame.BaseGame):
    """Text-based game with Satay."""
    def __init__(self, settings, funcCls=TextGameFuncs):
        if not all(["nbase" in w and "descriptors" in w for w in settings["objects"].values()]):
            raise SettingsError("Missing name conventions (nbase and descriptors)!")
        if "enableScopeChecking" not in settings:
            self.enableScopeChecking = True
        else:
            self.enableScopeChecking = settings["enableScopeChecking"]
        super(TextGame, self).__init__(settings, funcCls)

    def __mainloop__(self):
        """Represents one cycle for the game."""
        #Print the current map's name and desc.
        cmd = raw_input("> ")
        try:
            pcmd = self.__parse__(cmd)
        except AmbiguityError as ex:
            self.Print(ex.message)
            return
        # Nothing passed by user
        if len(pcmd) <= 0:
            return
        called = False
        for command in self.__commands__:
            if command.__name__ == pcmd[0]:
                try:
                    command(self, pcmd[1:])
                except CommandError as ex:
                    self.Print(ex.message)
                called = True
                break
            else:
                continue
        if not called:
            self.Print("Hmm?")

    def __parse__(self, line):
        """Parses user input for Command class"""
        args = []
        posf = 0
        posb = 0
        for char in line:
            posb = posb + 1
            if char == " " or posb == len(line):
                args.append(line[posf:posb].strip().lower())
                posf = posb
        return self.__resolve__(args)

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
    def __resolve__(self, args):
        # Adjective position marker
        adjp = 0
        usradj = []
        nouns = {k:(v.nbase(),v.descriptors()) for k,v in self.__objects__.items()}
        for arg in args[1:]:
            if arg in [t[0] for t in nouns.values()]:
                candidates = []
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
                        candidates.append((len(adjcmp), ID))

                # Remove candidates not in scope if requested
                if self.enableScopeChecking:
                    for candidate in candidates:
                        if not self.CheckScope(candidate[1]):
                            candidates.remove(candidate)

                amts = [t[0] for t in candidates]
                amts.sort(reverse=True)
                if len(amts) <= 0:
                    continue
                # Ambiguity in user's described noun
                if amts.count(amts[0]) > 1:
                    raise AmbiguityError("Which one are you talking about?")
                chosenID = [tup[1] if tup[0] == amts[0] else None for tup in candidates]
                chosenID.sort(reverse=True)
                args[adjp+1:len(usradj)+adjp+2] = [self.__objects__[chosenID[0]]]
                adjp += 1

            elif arg in sum([tup[1] for tup in nouns.values()],[]):
                usradj.append(arg)
            else:
                usradj = []
                adjp += 1
        return args

    def Run(self):
        """Run the game."""
        while 1:
            try:
                self.__mainloop__()
            except StopGame:
                break
        # Game has ended
        self.Print("Thanks for playing!")
