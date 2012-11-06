# A test game
from Satay.TextGame.Game import Map, Item, TextGame
from Satay.Base import NumeratedList
from Commands.kill import kill, murder
from Commands.basic import look, go, get, take, drop

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
    ),

    "iTem":Item(
        name="Item",
        desc="A wonderous item for you.",
        nbase="item",
        descriptors=['wonderous'],
        kill_msg={
            '':"My item! NOESSS!!!",
            "iSword":"You killed my item with a sword!?!?",
        },
        kill_newitem="iStone",
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
    "commands":[kill, murder, look, go, get, take, drop],
}

# Start game immediately
if __name__ == "__main__":
    aGame = TextGame(settings)
    aGame.Run()
