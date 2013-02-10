# A test game
from Satay.PorkStyleTextGame.Game import Map, Item, NPC, PorkStyleTextGame as GameMode
from Satay.Base import NumeratedList, Dynamic, DialogMap, Dialog, Response, Action, Condition
from Commands.kill import kill, murder
from Commands.basic import look, go, get, take, drop, inventory, inv, i, save, load, quit
from Commands.talk import talk
from Commands.eat import eat

objects = {
    "mPuddle":Map(
        name="A Puddle",
        desc="You see a nice puddle here.",
        nbase="puddle",
        descriptors=["wet","nice","pleasant"],
        itemlist=NumeratedList(
            iTem=3,
            iStone=2,
            nMan=1,
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

    "iEmerald":Item(
        name="Emerald"
        desc="A green and valuable emerald.",
        nbase="emerald",
        descriptors=['green', 'valuable'],
    ),

    "iChicken":Item(
        name="Chicken",
        desc="Some juicy, cooked chicken.",
        nbase="chicken",
        descriptors=['juicy', 'cooked'],
        eat_edible=True,
    ),

    "nMan":NPC(
        name="A Man",
        desc="An old, aging man.",
        nbase="man",
        descriptors=['old','aging'],
        dialog=DialogMap(
            start=Dialog(
                "Hey there.",
                Response(
                    "Hey.",
                    'a0',
                    Condition("manTalkedPreviously01") == True,
                ),
                Response("Sup.",'a0'),
                Response(
                    "I killed the item with my sword.",
                    'e2',
                    Condition.History.Happened("kill").To("iItem"),
                    Condition.History.Happened("kill").With("iSword")
                ),
            ),
            a0=Dialog(
                "Want some chicken?",
                Response("I like chicken.","a1"),
                Response("I hate chicken.","a2"),
                Response(
                    "That chicken sucked last time.",
                    "a2",
                    Condition.History.Happened("talk").To("nMan"),
                    Condition.History.Happened("eat").To("iChicken"),
                ),
                Response(
                    "I already have some.",
                    "a2",
                    Condition("inventory").Contains("iChicken"),
                ),
            ),
            a1=Dialog(
                "Nice! So do I. Have some!",
                Response("Bye", "e1"),
                action=[
                    Action("AddToInventory")("iChicken"),
                    Action("SetVar")("gotManChicken01", True),
                ],
            ),
            a2=Dialog(
                "Aw, dang.",
                Response("Bye", "e1"),
            ),
            e2=Dialog(
                "Excellent! Take this emerald...",
                action=Action("AddToInventory")("iEmerald"),
                end=True,
            ),
            e1=Dialog(
                "Good bye, then.",
                action=Action("SetVar")("manTalkedPreviously01", True),
                end=True,
            ),
        )
    )
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
    "commands":[kill, murder, talk, look, go, get, take, drop, inventory, inv, i, save, load, quit, eat],
    "variables":{
        "manTalkedPreviously01":False,
        "gotManChicken01":False,
        "chickenEaten":True,
    }
}

# Start game immediately
if __name__ == "__main__":
    aGame = GameMode(settings)
    aGame.Run()
