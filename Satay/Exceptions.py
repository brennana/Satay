"""-------------------------------------------------
Satay Game Engine Copyright (C) 2012 Andy Brennan

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR APARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTIONOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Satay on GitHub: https://github.com/Valdez42/Satay

 Exceptions.py --
   Defines all exceptions for Satay.
-------------------------------------------------"""

class SettingsError(Exception):
    """Error in game settings"""
    pass

class EntityError(Exception):
    """Error creating entity"""
    pass

class PropertyError(Exception):
    """Error accessing property"""
    pass

class AmbiguityError(Exception):
    """Error resolving noun"""
    pass

class CommandError(Exception):
    """Error executing command"""
    pass

class CommandPropertyError(CommandError, PropertyError):
    """Error with command argument properties"""
    pass

class CommandTypeError(CommandError):
    """Error with command argument type"""
    pass

class CommandConjunctionError(CommandError):
    """Error with conjunctions (e.g. with, for, etc.) between commands"""
    pass

class CommandNoSuitableFormError(CommandError):
    """Error finding a suitable command form from args given"""
    pass

class CommandScopeError(CommandError):
    """Error finding entity in inv/curmap scopes"""
    pass
