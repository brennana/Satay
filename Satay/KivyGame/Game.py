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

 Game.py --
   Game module for use in game creation.
   Here, game settings are set, commands are registered,
   and the game is actually played.
-------------------------------------------------"""

from ..BaseGame import Game as BaseGame
from ..Exceptions import *
from Functions import *

import kivy
kivy.require("1.4.1")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty


class Map(BaseGame.Map):
    """Class representing map entity (places the player and items inhabit)"""
    def __init__(self, **props):
        super(Map, self).__init__(**props)

class Item(BaseGame.Item):
    """Class representing item entity (things the player interacts with)"""
    def __init__(self, **props):
        super(Item, self).__init__(**props)


class MapWidget(Widget):
    """Kivy widget that contains a Satay.Base.EntItem map derivative."""
    itsmap = StringProperty(None)

class ItemListWidget(Widget):
    """Kivy widget that contains Satay.Base.EntItem item derivatives (itemlist)."""
    itsitems = ObjectProperty(None)

class SatayWidget(Widget):
    """The Main game widget."""
    def __init__(self, satayGame):
        self.satay = satayGame
        super(SatayWidget, self).__init__()

Factory.register("MapWidget", MapWidget)
Factory.register("ItemListWidget", ItemListWidget)
Factory.register("SatayWidget", SatayWidget)

class SatayApp(App):
    """The basic Kivy application class."""
    def __init__(self,satayGame,**kwargs):
        self.satay = satayGame
        super(SatayApp,self).__init__(**kwargs)
    def build(self):
        return SatayWidget(self.satay)

class KivyGame(BaseGame.BaseGame):
    """Basic game using Kivy."""
    def __init__(self, settings, funcCls=KivyGameFuncs, kivyAppCls=SatayApp):
        self.AppCls = kivyAppCls
        super(KivyGame, self).__init__(settings, funcCls)

    def Run(self):
        self.AppCls(self).run()
