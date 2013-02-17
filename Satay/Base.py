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

 Base.py --
   Contains all the basic classes that make up Satay.
-------------------------------------------------"""

from Exceptions import *
import sqlite3

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
                # Log history
                self.game.history.AddEntry(self.__class__.__name__, list(args))
                # Command was successful, evaluate all post-command events
                for arg in args:
                    if isinstance(arg, EntBase) and "events" in arg:
                        for event in arg.events():
                            event.Evaluate(self.game)
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
    def ExpectType(self, obj, *clses):
        if not any([isinstance(obj, cls) for cls in clses]):
            self.ThrowType()
    def ExpectProperty(self, obj, *props):
        for prop in props:
            if prop not in obj:
                self.ThrowProperty()
    funclist = []
    NoSuitableFormMsg = "Do what now?"
    ConjuctionMsg     = "Learn to English, my friend."
    TypeMsg           = "You cannot do that."
    PropertyMsg       = "You cannot do that."
    ScopeMsg          = "Object is nowhere to be found."

class Event(object):
    """An event of which evaluates a condition and then executes actions."""
    def __init__(self, condition, *actions):
        self.condition = condition
        self.actions = actions
        super(Event, self).__init__()

    def Evaluate(self, game):
        if self.condition(game):
            for action in self.actions:
                action(game)

class Dynamic(dict):
    """A type of dictionary for dynamic properties (key is dynamic ident, value is value)."""
    def __init__(self, default, **dyns):
        dyns[''] = default
        super(Dynamic, self).__init__(**dyns)

class Property(object):
    """Class to hold attr name and value, used for defining module properties
        and for shorthand value retreival."""
    def __init__(self, name, value):
        self.name = name
        if not isinstance(value, Dynamic):
            self.value = Dynamic(value)
        else:
            self.value = value
    def __getitem__(self, item=''):
        try:
            return self.value[item]
        except KeyError:
            return self.value['']
    def __setitem__(self, item, value):
        try:
            self.value[item] = value
        except KeyError:
            self.value[''] = value
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
        if isinstance(props["name"], Dynamic) or isinstance(props["desc"], Dynamic):
            raise EntityError("Neither name nor description may be dynamic!")
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

class Action(object):
    def __init__(self, funcname):
        self.funcname = funcname
    def __call__(self, *args):
        return lambda game: getattr(game, self.funcname)(*args)

class HistoryQuery(object):
    def __init__(self, verb):
        self.verb = verb
    def To(self, obj):
        return lambda game: game.history.Query(self.verb, obj, 0, 1)
    def With(self, obj):
        return lambda game: game.history.Query(self.verb, obj, 1, None)

class Condition(object):
    """Generates lambda functions based on chosen operator."""
    def __init__(self, var):
        self.var = var
    def __eq__(self, other):
        place = self.ResolveSubject(self.var)
        if place != "variables":
            return lambda game: getattr(game, place) == other
        else:
            return lambda game: getattr(game, place)[self.var] == other

    def __lt__(self, other):
        place = self.ResolveSubject(self.var)
        if place != "variables":
            return lambda game: getattr(game, place) < other
        else:
            return lambda game: getattr(game, place)[self.var] < other

    def __gt__(self, other):
        place = self.ResolveSubject(self.var)
        if place != "variables":
            return lambda game: getattr(game, place) > other
        else:
            return lambda game: getattr(game, place)[self.var] > other

    def __ge__(self, other):
        place = self.ResolveSubject(self.var)
        if place != "variables":
            return lambda game: getattr(game, place) >= other
        else:
            return lambda game: getattr(game, place)[self.var] >= other

    def __le__(self, other):
        place = self.ResolveSubject(self.var)
        if place != "variables":
            return lambda game: getattr(game, place) <= other
        else:
            return lambda game: getattr(game, place)[self.var] <= other

    def __ne__(self, other):
        place = self.ResolveSubject(self.var)
        if place != "variables":
            return lambda game: getattr(game, place) != other
        else:
            return lambda game: getattr(game, place)[self.var] != other

    def Contains(self, key):
        place = self.ResolveSubject(self.var)
        if place != "variables":
            return lambda game: key in getattr(game, place)
        else:
            return lambda game: key in getattr(game, place)[self.var]

    def Is(self, other):
        place = self.ResolveSubject(self.var)
        if place != "variables":
            return lambda game: getattr(game, place) is other
        else:
            return lambda game: getattr(game, place)[self.var] is other

    def ResolveSubject(self, subject):
        if subject == "inventory":
            return "inventory"
        else:
            return "variables"
    class history(object):
        """Internal History methods for Condition"""
        @classmethod
        def Happened(cls, verb):
            return HistoryQuery(verb)
    History = history

class Response(object):
    """Represents a user response to an NPC dialog."""
    def __init__(self, response, redirect, *conditions):
        self.response = response
        self.redirect = redirect
        if len(conditions) == 0:
            conditions = [lambda game: True]
        self.conditions = conditions

class Dialog(object):
    """Object that represents a single dialog item (NPC speech and then
        possible respones from the player plus actions the NPC can execute.)"""
    def __init__(self, speech, *responses, **props):
        self.speech = speech
        self.responses = responses
        if "action" in props:
            self.actions = props["action"]
            if not type(self.actions) == list:
                self.actions = [self.actions]
        else:
            self.actions = [lambda game: 0]
        if "end" in props:
            self.end = props["end"]
        else:
            self.end = False

class DialogMap(dict):
    """Object that represents a map of a dialog 
    (i.e. what speech returns what from an NPC and in what order, etc.)"""
    def __init__(self, **dialogs):
        super(DialogMap, self).__init__(dialogs)

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

    @classmethod
    def FromList(cls, lst):
        """Create a NumeratedList from actual list object."""
        d = {}
        for item in lst:
            d[item] = lst.count(item)
        return cls(**d)

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

    def __toent__(self, *args, **kwargs):
        """Resolve EntRefs into the actual entity"""
        if "forcelist" not in kwargs:
            forcelist = False
        else:
            forcelist = kwargs["forcelist"]
        newargs = []
        for arg in args:
            if isinstance(arg, str):
                newargs.append(self.game.__objects__[arg])
            else:
                newargs.append(arg)
        if len(newargs) > 1 or forcelist:
            return newargs
        else:
            return newargs[0]

    def __toref__(self, *args, **kwargs):
        """Convert entites into EntRefs."""
        if "forcelist" not in kwargs:
            forcelist = False
        else:
            forcelist = kwargs["forcelist"]
        newargs = []
        for arg in args:
            if isinstance(arg, EntBase):
                newargs.append(EntRef(arg.id))
            else:
                newargs.append(arg)
        if len(newargs) > 1 or forcelist:
            return newargs
        else:
            return newargs[0]

class History(object):
    """Class for storing an RDB of all game history (executed commands)."""
    def __init__(self, dbConnection):
        self.conn = dbConnection
        self.cursor = self.conn.cursor()

    @classmethod
    def New(cls, objects, commands):
        conn = sqlite3.connect(":memory:")
        conn.executescript("""CREATE  TABLE IF NOT EXISTS COMMAND (
              id INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT UNIQUE,
              name TEXT NOT NULL UNIQUE
              );

            CREATE  TABLE IF NOT EXISTS OBJECT (
              id INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT UNIQUE,
              name TEXT NOT NULL UNIQUE
              );

            CREATE  TABLE IF NOT EXISTS EXECUTED (
              id INTEGER NOT NULL PRIMARY KEY ASC AUTOINCREMENT,
              COMMAND_id INTEGER NOT NULL ,
              CONSTRAINT fk_EXECUTED_COMMAND
                FOREIGN KEY (COMMAND_id )
                REFERENCES COMMAND (id )
                ON DELETE NO ACTION
                ON UPDATE NO ACTION);

            CREATE  TABLE IF NOT EXISTS EXECUTED_has_OBJECT (
              EXECUTED_id INTEGER NOT NULL,
              OBJECT_id INTEGER NOT NULL,
              placement INTEGER NOT NULL,
              CONSTRAINT fk_EXECUTED_has_OBJECT_EXECUTED1
                FOREIGN KEY (EXECUTED_id )
                REFERENCES EXECUTED (id )
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
              CONSTRAINT fk_EXECUTED_has_OBJECT_OBJECT1
                FOREIGN KEY (OBJECT_id )
                REFERENCES OBJECT (id )
                ON DELETE NO ACTION
                ON UPDATE NO ACTION);
            """)
        conn.executemany("INSERT INTO COMMAND (name) VALUES (?)", [(c.__name__,) for c in commands])
        conn.executemany("INSERT INTO OBJECT (name) VALUES (?)", [(k,) for k in objects])
        conn.commit()
        return cls(conn)

    @classmethod
    def Load(cls, dump):
        conn = sqlite3.connect(":memory:")
        conn.executescript(dump)
        conn.commit()
        return cls(conn)

    def Dump(self):
        dump = ""
        for line in self.conn.iterdump():
            dump += line
        return dump

    def AddEntry(self, cmd, args):
        # Remove conjunctions
        count = 0
        for arg in args:
            if not isinstance(arg, EntBase):
                args.pop(count)
            count += 1
        self.cursor.execute("INSERT INTO EXECUTED (COMMAND_id) SELECT id FROM COMMAND WHERE name=? LIMIT 1;", (cmd,))
        # Get the executed id
        self.cursor.execute("SELECT last_insert_rowid()")
        executed = self.cursor.fetchone()[0]
        self.cursor.executemany("INSERT INTO EXECUTED_has_OBJECT (EXECUTED_id, OBJECT_id, placement) SELECT ?, id, ? FROM OBJECT WHERE name=?;", [(executed,c,a.id) for c,a in zip(range(1, len(args)+1), args)])
        self.conn.commit()

    def __parseCSV__(self, table):
        newTable = []
        for row in table:
            newTable.append(row[0].split(','))
        return newTable

    def Query(self, verb, obj, p1=None, p2=None):
        self.cursor.execute("""SELECT group_concat(OBJECT.name) FROM EXECUTED_has_OBJECT 
                                    INNER JOIN OBJECT ON EXECUTED_has_OBJECT.OBJECT_id = OBJECT.id
                                    INNER JOIN EXECUTED ON EXECUTED_has_OBJECT.EXECUTED_id = EXECUTED.id
                                    INNER JOIN COMMAND ON EXECUTED.COMMAND_id = COMMAND.id
                                  WHERE COMMAND.name = ?
                                  GROUP BY EXECUTED.id;""", (verb,))
        table = self.__parseCSV__(self.cursor.fetchall())
        for row in table:
            if obj in row[p1:p2]:
                return True

        return False
        