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

from ..TextGame import Functions

class PorkStyleTextGameFuncs(Functions.TextGameFuncs):
    """Function container"""
    def __init__(self, game):
        super(PorkStyleTextGameFuncs, self).__init__(game)
    def Print(self, message):
        """Print message to game screen."""
        super(PorkStyleTextGameFuncs, self).Print(str(message).strip() + "\n")
