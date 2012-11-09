# A test game
from Satay.PorkStyleTextGame.Game import Map, Item, PorkStyleTextGame as GameMode
from Satay.Base import NumeratedList, Dynamic
from Commands.kill import kill, murder
from Commands.basic import look, go, get, take, drop, inventory, inv, i, save, load, quit

objects = {
    "mPuddle":Map(
        name="A Puddle",
        desc="You see a nice puddle here.",
        nbase="puddle",
        descriptors=["wet","nice","pleasant"],
        itemlist=NumeratedList(
            iTem=3,
            iStone=2,
        ),
        s="mHeree",
    ),

    "mHeree":Map(
        name="Heree",
        desc="At the Wall.",
        nbase="heree",
        descriptors=[],
        n="mPuddle",
        itemlist=NumeratedList(
            iStone=2,
            iSword=1,
        ),
    ),

    "iTem":Item(
        name="Item",
        desc="A wonderous item for you.",
        nbase="item",
        descriptors=['wonderous'],
        kill_msg=Dynamic(
            "My item! NOESSS!!!",
            iSword="You killed my item with a sword!?!?",
        ),
        kill_newitem=Dynamic(
            "iStone",
            iSword="iPebble"
        ),
    ),

    "iPebble":Item(
        name="Pebble",
        desc="A small gray pebble.",
        nbase="pebble",
        descriptors=["small", "gray"],
    ),

    "iStone":Item(
        name="Stone",
        desc="A boring gray stone.",
        nbase="stone",
        descriptors=['boring','gray'],
    ),

    "iSword":Item(
        name="Sword",
        desc="A sharp, shiny sword.",
        nbase="sword",
        descriptors=['sharp','shiny'],
    ),
}

settings = {
    "start":"mPuddle",
    "title":"A Game",
    "author":"Andy Brennan",
    "items":NumeratedList(
        iTem=3,
        iSword=1,
    ),
    "objects":objects,
    "commands":[kill, murder, look, go, get, take, drop, inventory, inv, i, save, load, quit],
}

# Start game immediately
if __name__ == "__main__":
    aGame = GameMode(settings)
    aGame.Run()
