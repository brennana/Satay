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
   Dervives the FunctionContainer class from base
   with standard Satay functions. This class is
   instanced in Game.py.
-------------------------------------------------"""

from ..BaseGame import Functions
from ..Exceptions import StopGame

class TextGameFuncs(Functions.BaseGameFuncs):
    """The function container for Satay functions."""
    def __init__(self, game):
        super(TextGameFuncs, self).__init__(game)

    def Print(self, message):
        """Print a Message to Game Screen."""
        print(message)

    def RequestInput(self, prompt):
        """Request some user input with given prompt."""
        return raw_input(prompt)

    def EndGame(self, msg):
        """End the current game with a message (such as Game Over) and quit."""
        self.game.Print(msg)
        self.game.QuitGame()

    def QuitGame(self):
        """Quit the current game."""
        raise StopGame
