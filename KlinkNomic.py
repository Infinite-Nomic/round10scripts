import math
from tkinter import *
import re

CB = Tk()

print("1.Tax  2.Sort")
whichprogram = input()
if int(whichprogram) == 1:
    clipboardData = CB.clipboard_get()
    clipboardList = clipboardData.splitlines()
    listClean = [x for x in clipboardList if x != "|-"]
    longestName = 0

    for x in listClean:
        slicePoint = re.search("(\|\|)", x).span()
        print(slicePoint)
        if slicePoint[0] - 1 > longestName:
            longestName = slicePoint[0] - 3

    for x in listClean:
        slicePoint = re.search("(\|\|).*?(\|\|)", x).span()

        ChipValue = int(x[slicePoint[0] + 3:slicePoint[1] - 3])
        TrungValue = 0  # placeholder
        WealthValue = ChipValue + (TrungValue * 20)

        playerName = x[2:slicePoint[0] - 1]

        taxBuffer = ""
        wealthBuffer = ""
        trungBuffer = ""
        chipBuffer = ""

        if WealthValue >= 320:
            taxValue = math.floor(((TrungValue * 20) + ChipValue - 300) / 20) * 5
        else:
            taxValue = 0

        if taxValue >= 100:
            taxValue = 100
        elif taxValue > 9:
            taxBuffer = " "
        else:
            taxBuffer = "  "

        if WealthValue < 10:
            wealthBuffer = "  "
        elif WealthValue < 100:
            wealthBuffer = " "

        while len(playerName) < longestName:
            playerName += " "

        print(playerName + " | Wealth: " + str(WealthValue) + wealthBuffer + " | Chips: " + str(
            ChipValue) + " | Trungs: " + str(TrungValue) + " | Tax: " + str(taxValue) + taxBuffer + " | Gain: " + str(
            100 - taxValue))
elif int(whichprogram) == 2:
    carddetails = input("Paste suit/rank/tarot ranks with the sets separated by |\n").split("|")
    suits = [x.strip("[").strip().strip("]") for x in carddetails[0].split(",")]
    regularranks = [y.strip().strip("]").strip("[") for y in carddetails[1].split(",")]
    tarotranks = [z.strip().strip("]").strip("[") for z in carddetails[2].split(",")]

    regrankplace = 0
    tarotrankplace = 0
    cardSuitandRank = []
    readableCard = []

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
        3: "The High Priestess ",
        4: "The Empress ",
        5: "The Emperor ",
        6: "The Hierophant ",
        7: "The Lovers ",
        8: "The Chariot ",
        9: "Justice",
        10: "The Hermit ",
        11: "Wheel of Fortune ",
        12: "Strength",
        13: "The Hanged Man ",
        14: "Death",
        15: "Temperance",
        16: "The Devil ",
        17: "The Tower ",
        18: "The Star ",
        19: "The Moon ",
        20: "The Sun ",
        21: "Judgement ",
        22: "The World "
    }

    for x in suits:
        if int(x) != 13:
            cardSuitandRank.append(x + " " + regularranks[regrankplace])
            readableCard.append("[" + rankdict[int(regularranks[regrankplace])] + "] " + suitdict[int(x)])
            regrankplace += 1
        else:
            cardSuitandRank.append(x + " " + tarotranks[tarotrankplace])
            readableCard.append("[" + tarotdict[int(tarotranks[tarotrankplace])] + "] " + suitdict[int(x)])
            tarotrankplace += 1

    lotdivider = 2
    lotnumber = 1
    # this should be enumerate i think
    for x in readableCard:
        if lotdivider == 2:
            print("\nLot " + str(lotnumber) + ":\n" + x)
            lotdivider = 0
            lotnumber += 1

        else:
            print(x)
            lotdivider += 1
