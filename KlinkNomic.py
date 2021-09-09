import math
from tkinter import *
from collections import deque
import re

CB = Tk()

suitdict = {
    1: "Leaves",
    2: "Diamonds",
    3: "Cups",
    4: "Clubs",
    5: "Acorns",
    6: "Roses",
    7: "Bells",
    8: "Swords",
    9: "Shields",
    10: "Hearts",
    11: "Coins",
    12: "Spades",
    13: "Tarot"
}

rankdict = {
    1: "Ace",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "11",
    12: "12",
    13: "13",
    14: "Unter Knave",
    15: "Ober Knave",
    16: "Knight",
    17: "Bishop",
    18: "Rook",
    19: "Queen",
    20: "King"
}


tarotdict = {
    1: "The Fool",
    2: "The Magician",
    3: "The High Priestess",
    4: "The Empress",
    5: "The Emperor",
    6: "The Hierophant",
    7: "The Lovers",
    8: "The Chariot",
    9: "Justice",
    10: "The Hermit",
    11: "Wheel of Fortune",
    12: "Strength",
    13: "The Hanged Man",
    14: "Death",
    15: "Temperance",
    16: "The Devil",
    17: "The Tower",
    18: "The Star",
    19: "The Moon",
    20: "The Sun",
    21: "Judgement",
    22: "The World"
}


def createplayerlist():
    clipboardData = CB.clipboard_get()
    clipboardList = clipboardData.splitlines()
    playerlist = [x for x in clipboardList if x != "|-"]
    return playerlist

def cleaninventory(unclean):
    split = unclean.split("||")
    clean = [y.strip("|").strip() for y in split]
    return clean

def processtaxes():
    #make sure the wiki table is in your clipboard starting with thhe first player
    print("1: All Players | 2: Players with tax < 100")
    whichmode = input()
    try:
        int(whichmode)
    except ValueError:
        whichmode = 1

    listClean = createplayerlist()
    longestName = 0
    if len(listClean) <= 1:
        print("Make sure you have the wiki table in your clipboard")
        return

    for x in listClean:
        name = cleaninventory(x)[0]
        if len(name) > longestName: longestName = len(name)

    for x in listClean:
        InvClean = cleaninventory(x)
        PlayerName = InvClean[0]
        NameBuffer = " "
        ChipValue = int(InvClean[1])
        TaxValue = 0
        TrungValue = 0  # placeholder
        TrungMatch = re.search("(\d+) Trung", InvClean[2])
        if TrungMatch != None:
            TrungValue = int(TrungMatch.group(1))
        WealthValue = ChipValue + (TrungValue * 20)

        def buffer(value):
            buff = " " * (4 - len(str(value)))
            return " " + str(value) + buff + "| "

        if WealthValue >= 320:  # the first tax increment kicks in at 320 currently
            TaxValue = math.floor(((TrungValue * 20) + ChipValue - 300) / 20) * 5
            if TaxValue >= 100:  # the hardcap on tax is 100 currently
                TaxValue = 100
        NewChipValue = ChipValue + (100-TaxValue)
        if len(PlayerName) < longestName:
            NameBuffer = " " * (1 + longestName - len(PlayerName))

        if int(whichmode) == 1:
            print(PlayerName + NameBuffer + "| New Chips:" + buffer(NewChipValue) + "Wealth:" + buffer(WealthValue) + "Chips:" + buffer(
                ChipValue) + "Trungs:" + buffer(TrungValue) + "Tax:" + buffer(TaxValue) + "Gain:" + buffer(100 - TaxValue))
        elif int(whichmode) == 2 and TaxValue < 100:
            print(PlayerName + NameBuffer + "| New Chips:" + buffer(NewChipValue) + "Wealth:" + buffer(WealthValue) + "Chips:" + buffer(
                ChipValue) + "Trungs:" + buffer(TrungValue) + "Tax:" + buffer(TaxValue) + "Gain:" + buffer(100 - TaxValue))
    sys.exit()

def processdiceroles():

    #Separate the three sets of rolls with | and copy it into your clipboard
    clipboardData = CB.clipboard_get()
    carddetails = clipboardData.split("|")
    suits = deque([suitdict[int(x.strip("[").strip().strip("]"))] for x in carddetails[0].split(",")])
    regularranks = deque([rankdict[int(y.strip().strip("]").strip("["))] for y in carddetails[1].split(",")])
    tarotranks = deque([tarotdict[int(z.strip().strip("]").strip("["))] for z in carddetails[2].split(",")])

    assembledCards = deque([])

    while len(suits) > 0:
        if suits[0] == "Tarot":
            assembledCards.append(tarotranks.popleft() + "[" + suits.popleft() + "]")
        else:
            assembledCards.append(regularranks.popleft() + " of " + suits.popleft())

    for x, value in enumerate(range(int(len(assembledCards) / 3))):
        print("Lot " + str(
            value + 1) + ": " + assembledCards.popleft() + ", " + assembledCards.popleft() + ", " + assembledCards.popleft())
    sys.exit()

def processhand():
    GetPlayers = createplayerlist()

    print("1: Sort by Rank | 2: Sort by Suit")
    whichsort = input()
    try:
        whichsort = int(whichsort)
    except ValueError:
        whichsort = 1

    wikirankdict = {
        "A": 1,
        "T": 10,
        "E": 11,
        "D": 12,
        "H": 13,
        "U": 14,
        "O": 15,
        "N": 16,
        "B": 17,
        "R": 18,
        "Q": 19,
        "K": 20
    }

    wikisuitdict = {
        "L": 1,
        "D": 2,
        "Cp": 3,
        "C": 4,
        "A": 5,
        "R": 6,
        "B": 7,
        "Sw": 8,
        "Sh": 9,
        "H": 10,
        "Cn": 11,
        "S": 12
    }


    for x in GetPlayers:
        CurrentPlayer = cleaninventory(x)
        def sortby():
            CurrentHand = [z.strip("{").strip("}") for z in CurrentPlayer[3].split(" ") if z]
            HandDetails = []
            TarotSleeve = []


            for z in CurrentHand:
                cardtype = z.find("Card")
                if cardtype > -1: # Activates if its a card
                    cardrank = z[5]  # Rank
                    cardsuit = wikisuitdict[z[7:]] # Suit converted into a number

                    try:
                        cardrank = int(cardrank)
                    except ValueError:
                        # if it cant int the rank, feeds it thru partial dictionary above to get the equivalent number
                        cardrank = wikirankdict[cardrank]

                    if len(HandDetails) == 0: #makes sure theres a card to compare to
                        HandDetails.append({"Rank":cardrank,"Suit":cardsuit})
                        continue


                    if whichsort == 1:
                        sorter = "Rank"
                        valueholder = cardrank
                    elif whichsort == 2:
                        sorter = "Suit"
                        valueholder = cardsuit

                    Added = False
                    for x in range(len(HandDetails)):
                        if valueholder <= HandDetails[x][sorter]:
                            HandDetails.insert(x,{"Rank":cardrank,"Suit":cardsuit})
                            Added = True
                            break
                    if Added == False:
                        HandDetails.append({"Rank": cardrank, "Suit": cardsuit})
                else:
                    #print("This is a Tarot")
                    cardrank = int(z[6:])
                    TarotSleeve.append(tarotdict[cardrank])
                    pass
            for x in HandDetails:
                print(rankdict[x["Rank"]] + " of " + suitdict[x["Suit"]])

            print("\nTarot Cards:")

            for x in TarotSleeve:
                print(x)
            return

        if CurrentPlayer[3] != "-":
            sortby()
#            print(CurrentPlayer[0] + " " + CurrentPlayer[3])
    sys.exit()

while True:
    print("1: Tax | 2: Sort | 3: Hand")
    whichprogram = input()
    try:
        int(whichprogram)
    except ValueError:
        whichprogram = 0

    if int(whichprogram) == 1:
        processtaxes()
    elif int(whichprogram) == 2:
        processdiceroles()
    elif int(whichprogram) == 3:
        processhand()
    else:
        print("Thats not an option")
