# A test game
from Satay.HTTPGame.Game import Map, Item, NPC, HTTPGame as GameMode
from Satay.Base import NumeratedList, Dynamic, DialogMap, Dialog, Response, Action, Condition, Event
from HTTPCommands.basic import go

objects = {
    "mPuddle":Map(
        name="A Puddle",
        desc="You see a nice puddle here.",
        imgsrc="/assets/img/puddle.png",
        itemlist=NumeratedList(
            iEmerald=1,
        ),
        forward=Dynamic(
            "mHeree",
            iPebble="mHouse",
        ),
    ),

    "mHeree":Map(
        name="Heree",
        desc="At the Wall.",
        imgsrc="/assets/img/wall.png",
        itemlist=NumeratedList(
        ),
        backward="mPuddle",
        right="mHouse",
    ),

    "mHouse":Map(
        name="A House",
        desc="A ramshackle old house.",
        imgsrc="/assets/img/house.png",
        itemlist=NumeratedList(
            iStone=3,
        ),
        left="mHeree",
    ),

    "iTem":Item(
        name="Item",
        desc="A wonderous item for you.",
    ),

    "iPebble":Item(
        name="Pebble",
        desc="A small gray pebble.",
    ),

    "iStone":Item(
        name="Stone",
        desc="A boring gray stone.",
    ),

    "iSword":Item(
        name="Sword",
        desc="A sharp, shiny sword.",
    ),

    "iFork":Item(
        name="Fork",
        desc="A shiny, silver fork. It's quite pointy!",
    ),

    "iChickenFork":Item(
        name="Chicken Stuck to Fork",
        desc="Some awful chicken glued to a now dirty fork.",
    ),

    "iEmerald":Item(
        name="Emerald",
        desc="A green and valuable emerald.",
    ),

    "iChicken":Item(
        name="Chicken",
        desc="Some juicy, cooked chicken.",
    ),
}

settings = {
    "start":"mPuddle",
    "title":"A Web Game",
    "author":"Andy Brennan",
    "root":"./webroot",
    "port":8080,
    "items":NumeratedList(
        iTem=3,
        iSword=1,
        iFork=1,
    ),
    "objects":objects,
    "commands":[go],
    "variables":{

    }
}

# Start game immediately
if __name__ == "__main__":
    aGame = GameMode(settings)
    aGame.Run()
