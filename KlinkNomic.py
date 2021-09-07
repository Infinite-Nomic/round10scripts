import math
from tkinter import *
from collections import deque
import re

CB = Tk()

print("1 Tax  2 Sort")
whichprogram = input()
if int(whichprogram) == 1:
    # grabs table data from clipboard, will crash if you dont have table data in it though bc im an expert programmer
    clipboardData = CB.clipboard_get()
    clipboardList = clipboardData.splitlines()
    listClean = [x for x in clipboardList if x != "|-"]
    longestName = 0

    def cleanInventory(unclean):
        split = unclean.split("||")
        clean =[y.strip("|").strip() for y in split]
        return  clean

    for x in listClean:
        name = cleanInventory(x)[0]
        if len(name) > longestName: longestName = len(name)

    for x in listClean:
        InvClean = cleanInventory(x)
        PlayerName = InvClean[0]
        NameBuffer = " "
        ChipValue = int(InvClean[1])
        TaxValue = 0
        TrungValue = 0  # placeholder
        TrungMatch = re.search("(\d+) Trung", InvClean[2])
        if TrungMatch != None:
            TrungValue = int(TrungMatch.group(1))
        WealthValue = ChipValue + (TrungValue * 20)

        def Buffer(value):
            buff = " " * (4 - len(str(value)))
            return " " + str(value) + buff + "| "

        if WealthValue >= 320: #the first tax increment kicks in at 320 currently
            TaxValue = math.floor(((TrungValue * 20) + ChipValue - 300) / 20) * 5
            if TaxValue >= 100: # the hardcap on tax is 100 currently
                TaxValue = 100

        if len(PlayerName) < longestName:
            NameBuffer = " " * (1+longestName - len(PlayerName))

        print(PlayerName + NameBuffer + "| Wealth:" + Buffer(WealthValue) + "Chips:" + Buffer(ChipValue) + "Trungs:" + Buffer(TrungValue) + "Tax:" + Buffer(TaxValue) + "Gain:" + Buffer(100 - TaxValue))

elif int(whichprogram) == 2:

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

    #this one requires you paste it and i have no idea why since i lit have clipboard shit earlier?? need to fix
    carddetails = input("Paste suit/rank/tarot ranks with the sets separated by |\n").split("|")

    suits = deque([suitdict[int(x.strip("[").strip().strip("]"))] for x in carddetails[0].split(",")])
    regularranks = deque([rankdict[int(y.strip().strip("]").strip("["))] for y in carddetails[1].split(",")])
    tarotranks = deque([tarotdict[int(z.strip().strip("]").strip("["))] for z in carddetails[2].split(",")])

    assembledCards = deque([])

    while len(suits) > 0:
        if suits[0] == "Tarot":
            assembledCards.append(tarotranks.popleft() + "[" + suits.popleft() +"]")
        else:
            assembledCards.append(regularranks.popleft() + " of " + suits.popleft())

    for x, value in enumerate(range(int(len(assembledCards)/3))):
        print("Lot " + str(value+1) + ": " + assembledCards.popleft() + ", " + assembledCards.popleft() + ", "  + assembledCards.popleft())
