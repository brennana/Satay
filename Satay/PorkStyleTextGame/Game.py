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

from ..TextGame import Game as TextGame
from ..Exceptions import *
from Functions import *
from ..Base import History

class Map(TextGame.Map):
    """Map entity derivative."""
    def __init__(self, **props):
        super(Map, self).__init__(**props)

class Item(TextGame.Item):
    """Item entity."""
    def __init__(self, **props):
        super(Item, self).__init__(**props)

class NPC(TextGame.NPC):
    """Class representing NPCs (non player characters)."""
    def __init__(self, **props):
        super(NPC, self).__init__(**props)

class PorkStyleTextGame(TextGame.TextGame):
    """Classical Pork-style game."""
    def __init__(self, settings, funcCls=PorkStyleTextGameFuncs):
        super(PorkStyleTextGame, self).__init__(settings, funcCls)
    def __mainloop__(self):
        super(PorkStyleTextGame, self).__mainloop__()
    def Run(self):
        """Run the game."""
        # Print title and author of game as well
        # as specifics for start map, then go into loop
        self.Print(self.title + " by " + self.author)
        self.Print(self.GetCurmap().name())
        self.Print(self.GetCurmap().desc())
        super(PorkStyleTextGame, self).Run()
