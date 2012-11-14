Satay
=====

> A (much better) Python variation of the C++ PorkScript.

Why Satay?
----------

Satay is an extensible game engine library written entirely in Python. Unlike PorkScript, Satay actually works out of the box (with a small amount of implementation as seen in the agame.py example). Also unlike PorkScript, since it is written in Python, Satay is naturally cross-platform.

The main purpose of the Satay game engine is the painless creation of adventure games (games with maps, items, etc.). A user of Satay simply defines a dictionary with their maps and items and another dictionary for game settings. After this, the user simply instantiates a gamemode class with their settings, and proceeds to call the .Run() function on it. This starts the game, and takes care of _everything_ else. As previously noted, a working example of Satay exists on the root of the project: agame.py.

## Stacking ##

Using Python's wonderful `super` method, all functions (including gamemode functions) stack on top of their baser classes. This means that when a gamemode creator wants to have, for example, an RPGTextGame save XP points and other related information into a user save file, they simply add the members they want saved into a object which is passed on to the underlying classes. Each underlying class adds the information they need saved until it finally reaches the BaseGame class, whose job it is to save all the collected information.

This same method works for _every_ function in Satay, allowing for powerful gamemode package extension.

Theory
------

Internally, Satay works with 3 signifigant areas: gamemodes, gamemode functions, and commands.

## Gamemodes ##
Gamemodes are, obviously, different types or modes of games. Gamemodes are defined as packages of two files: a Game module and a Functions module. Functions.py defines the Gamemode Functions for the gamemode, whilst Game.py defines the gamemode class itself. Since gamemodes are classes, and all derive from the BaseGame class, more complex gamemodes may be created by deriving from other gamemodes.

For example, the Satay.TextGame.Game.TextGame class derives from Satay.BaseGame.Game.BaseGame class. Now, we have a gamemode that has textual abilities (takes textual user input, parses and resolves selected objects). If a developer wanted to create a textual RPG, they would create an RPG gamemode class of which derives from TextGame. This way, the developer does not worry about textual abilites, but rather _only_ RPG elements (EXP, STR, etc.). 

On a sidenote (although I have not tested it nor thought about it very much), an RPG mix-in class, which is then derived from (along with TextGame) to create a gamemode, may be another possible way to do this.

## Gamemode Functions ##
Gamemode functions are functions that commands use to alter the game's state. They are contained inside a class which derives from the base FunctionContainer. These functions are then integrated with a gamemode that way these functions may be called directly from the game instance (e.g. Game.Func()). Functions to print text to the screen, or replace an item with another item are examples of gamemode functions.

## Commands ##
Commands are special classes called that take user input, and then use gamemode functions to alter the game. Each command class represents one command. Functions are then defined within each class that represent the different "forms" of that command (akin to function overloading in C++).

In Satay.TextGame, user input is first parsed and then resolved into a list of string conjunctions (e.g. words like "with", "as", "using", etc.) and map/item entities. These are then passed on to a Command class-derivative instanstiation, which automatically runs the command and attempts to find a proper form to run. However, this Command class structure theoretically may be applied to _any_ gamemode type (e.g. 3D, 2D animation, etc.).

How Can I Help?
---------------

The best way to help me would be to fork this project, add more gamemodes, and make pull requests for them. I want Satay to become a large library of easy-to-use and accessible gamemodes and game types. The underlying principle behind Satay is simplicity: simplicty to the point that to use the basic elements of Satay (as in the example script "agame.py") requires _little to no_ knowledge of Python, or even programming. In this way, designers can prototype simple adventure (and perhaps beyond) games in shorter time in true Python fashion.


