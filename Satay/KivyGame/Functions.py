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

 Functions.py --
   Dervives the FunctionContainer class from base
   with standard Satay functions. This class is
   instanced in Game.py.
-------------------------------------------------"""

from ..BaseGame import Functions

class KivyGameFuncs(Functions.BaseGameFuncs):
    """The function container for Satay functions."""
    def __init__(self, game):
        super(KivyGameFuncs, self).__init__(game)
