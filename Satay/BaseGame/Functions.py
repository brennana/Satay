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

 Functions.py --
   Derives the FunctionContainer class from base
   with standard Satay functions. This class is
   instanced in Game.py.
-------------------------------------------------"""

from ..Base import FunctionContainer

class BaseGameFuncs(FunctionContainer):
    """The function container for Satay functions."""
    def __init__(self, game):
        self.game = game
        super(FunctionContainer, self).__init__()

    def Replace(self, item1, item2):
        """Replace item1 with item2."""
        item1,item2 = self.__toref__(item1,item2)
        if item1 in self.game.inventory:
            self.game.inventory.Take(item1)
            self.game.inventory.Give(item2)
        elif item1 in self.game.__objects__[self.game.curmap].itemlist():
            self.game.__objects__[self.game.curmap].itemlist().Take(item1)
            self.game.__objects__[self.game.curmap].itemlist().Give(item2)

    def ChgMap(self, newmap):
        """Change the current game map to newmap."""
        newmap = self.__toref__(newmap)
        self.game.curmap = newmap

    def RemoveFromMap(self, item):
        """Remove 1 of 'item' from the current map."""
        item = self.__toref__(item)
        self.game.__objects__[self.game.curmap].itemlist().Take(item)

    def AddToMap(self, item):
        """Add 1 of 'item' to the current map."""
        item = self.__toref__(item)
        self.game.__objects__[self.game.curmap].itemlist().Give(item)

    def RemoveFromInventory(self, item):
        """Remove 1 of 'item' from the inventory."""
        item = self.__toref__(item)
        self.game.inventory.Take(item)

    def AddToInventory(self, item):
        """Add 1 of 'item' to the inventory."""
        item = self.__toref__(item)
        self.game.inventory.Give(item)
