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

 Base.py --
   Contains all the basic classes that make up Satay.
-------------------------------------------------"""

from Exceptions import *

class Command(object):
    """Base Command Class -- All commands derive from here."""
    def __init__(self, game, args):
        self.game = game
        self.__defer__(*args)
    def __defer__(self, *args):
        """Defer arguments to each function until a suitable match is found"""
        called = False
        for func in self.funclist:
            try:
                func(self,*args)
            except TypeError:
                continue
            else:
                called = True
                break
        if not called:
            self.ThrowNoSuitableForm()
    def ThrowNoSuitableForm(self, hint=''):
        raise CommandNoSuitableFormError(self.NoSuitableFormMsg+'\n'+hint)
    def ThrowConjunction(self, hint=''):
        raise CommandConjunctionError(self.ConjunctionMsg+'\n'+hint)
    def ThrowType(self, hint=''):
        raise CommandTypeError(self.TypeMsg+'\n'+hint)
    def ThrowProperty(self, hint=''):
        raise CommandPropertyError(self.PropertyMsg+'\n'+hint)
    def ThrowScope(self, hint=''):
        raise CommandScopeError(self.ScopeMsg+'\n'+hint)
    def ExpectType(self, obj, cls):
        if not isinstance(obj, cls):
            self.ThrowType()
    def ExpectProperty(self, obj, props):
        if type(props) != list:
            props = list(props)
        for prop in props:
            if prop not in obj:
                self.ThrowProperty()
    funclist = []
    NoSuitableFormMsg = "Do what now?"
    ConjuctionMsg     = "Learn to English, my friend."
    TypeMsg           = "You cannot do that."
    PropertyMsg       = "You cannot do that."
    ScopeMsg          = "Object is nowhere to be found."

class Property(object):
    """Class to hold attr name and value, used for defining module properties
        and for shorthand value retreival."""
    def __init__(self, name, value):
        self.name = name
        if type(value) != dict:
            self.value = {'':value}
        else:
            self.value = value
    def __getitem__(self, item=''):
        try:
            return self.value[item]
        except KeyError:
            return self.value['']
    def __repr__(self):
        return self.value['']
    def __call__(self, attr=''):
        if type(attr) != str:
            attr = attr.id
        return self[attr]

class EntBase(object):
    """Entity base class. Objects such as Maps and Items derive from this."""
    def __init__(self, **props):
        self.__props__ = {}
        if "name" not in props or "desc" not in props:
            raise EntityError("Name and/or description not defined!")
        if type(props["name"]) == dict or type(props["desc"]) == dict:
            raise EntityError("Name nor description may be dynamic!")
        for prop in props:
            self.__props__[prop] = Property(prop, props[prop])
    def __getattr__(self, attr):
        try:
            return self.__props__[attr]
        except KeyError:
            raise PropertyError("%r property does not exist!" % attr)
    def __contains__(self, attr):
        return attr in self.__props__
    def __repr__(self):
        return self.name()
    def __str__(self):
        return self.name()

class NumeratedListIter(object):
    """Iterator object for NumeratedList"""
    def __init__(self, lst):
        self.lst = lst
        self.subiter = 0
        self.cur = 0
        self.keys = lst.keys()
    def __iter__(self):
        return self
    def next(self):
        self.subiter += 1
        if self.subiter-1 >= self.lst[self.keys[self.cur]]:
            self.cur += 1
            self.subiter = 1
        if self.cur > len(self.lst)-1:
            raise StopIteration
        else:
            return self.keys[self.cur]

class NumeratedList(dict):
    """A type of dictionary that acts as a list.
        It stores any type key, and an integer type value representing how
        many of 'key' are in the NumeratedList."""
    def __init__(self, **items):
        for v in items.values():
            if type(v) != int:
                raise TypeError("NumeratedList requires integer keys!")
        super(NumeratedList, self).__init__(items)
    def __iter__(self):
        return NumeratedListIter(self)
    def __contains__(self, obj):
        if super(NumeratedList, self).__contains__(obj):
            return self[obj] > 0
        else:
            return False
    def Give(self, item, amt=1):
        if item not in self:
            self[item] = amt
        else:
            self[item] += amt
    def Take(self, item, amt=1):
        if (self[item] - amt) < 0:
            raise NumeratedListError("Cannot take "+str(amt)+" more of that!")
        else:
            self[item] -= amt
        return self[item]

class EntRef(str):
    """A string-deriving reference for entities (maps, items, etc.)"""
    def __init__(self, string):
        super(EntRef, self).__init__(string)

class FunctionContainer(object):
    """Class for containing and calling Satay functions (Print, Replace, etc.)"""
    def __init__(self):
        super(FunctionContainer, self).__init__()

    def __toent__(self, *args):
        """Resolve EntRefs into the actual entity"""
        newargs = []
        for arg in args:
            if isinstance(arg, EntRef):
                newargs.append(self.game.__objects__[arg])
            else:
                newargs.append(arg)
        if len(newargs) > 1:
            return newargs
        else:
            return newargs[0]

    def __toref__(self, *args):
        """Convert entites into EntRefs."""
        newargs = []
        for arg in args:
            if isinstance(arg, EntBase):
                newargs.append(EntRef(arg.id))
            else:
                newargs.append(arg)
        if len(newargs) > 1:
            return newargs
        else:
            return newargs[0]

