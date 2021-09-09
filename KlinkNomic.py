import math
from collections import deque
if __name__ == '__main__':
    from tkinter import *
    CB = Tk()
    CB.withdraw()

import re

class PlayingCard:
    def __init__(self):
        self.suitnum = 0
        self.ranknum = 0
        self.suit = ""
        self.rank = ""
        self.color = ""
        self.tradition = ""

    suit_alpha = {
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
    invsuit_alpha = {v: k for k, v in suit_alpha.items()}

    rank_alpha =   {
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
    invrank_alpha = {v: k for k, v in rank_alpha.items()}

    card_suits = {
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

    card_ranks = {
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

    card_colors = {
        1: "Green",
        2: "Red",
        3: "Gold",
        4: "Black",
        5: "Green",
        6: "Red",
        7: "Gold",
        8: "Black",
        9: "Green",
        10: "Red",
        11: "Gold",
        12: "Black",
        13: "Special"

    }

    card_traditions = {
        1: "German",
        2: "French",
        3: "Spanish",
        4: "Spanish / French",
        5: "German / Swiss",
        6: "Swiss",
        7: "German / Swiss",
        8: "Spanish",
        9: "Swiss",
        10: "French / German",
        11: "Spanish",
        12: "French",
        13: "Tarot"
    }

    def interpret(self):
        try:
            self.suit = self.card_suits[int(self.suitnum)]
            self.suitnum = int(self.suitnum)
            self.color = self.card_colors[int(self.suitnum)]
            self.tradition = self.card_traditions[int(self.suitnum)]
        except ValueError:
            self.suit = self.card_suits[self.suit_alpha[self.suitnum]]
            self.suitnum = int(self.suit_alpha[self.suitnum])
            self.color = self.card_colors[self.suitnum]
            self.tradition = self.card_traditions[self.suitnum]

        try:
            self.rank = self.card_ranks[int(self.ranknum)]
            self.ranknum = int(self.ranknum)
        except ValueError:
            self.rank = self.card_ranks[self.rank_alpha[self.ranknum]]
            self.ranknum = int(self.rank_alpha[self.ranknum])

class TarotCard:
    tarot_ranks = {
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
    invtarot_ranks = {v: k for k, v in tarot_ranks.items()}

    def __init__(self):
        self.ranknum = ""
        self.rank = ""
    def interpret(self):
        self.rank = self.tarot_ranks[int(self.ranknum)]

def testfunction():
    print(PlayingCard.invrank_alpha[28])

def clipboard():
    return CB.clipboard_get()

def createplayerlist(rawdata):
    rawList = rawdata.splitlines()
    playerlist = [x for x in rawList if x != "|-"]
    return playerlist

def cleaninventory(unclean):
    split = unclean.split("||")
    clean = [y.strip("|").strip() for y in split]
    return clean

def processtaxes(rawdata):
    #make sure the wiki table is in your clipboard starting with the first player
    print("1: All Players | 2: Players with tax < 100")
    whichmode = input()
    try:
        int(whichmode)
    except ValueError:
        whichmode = 1

    listClean = createplayerlist(rawdata)
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

def processdiceroles(rawdata):

    #Separate the three sets of rolls with | and copy it into your clipboard
    rawdicerolls = rawdata
    carddetails = rawdicerolls.split("|")
    suits = deque([PlayingCard.card_suits[int(x.strip("[").strip().strip("]"))] for x in carddetails[0].split(",")])
    regularranks = deque([PlayingCard.card_ranks[int(y.strip().strip("]").strip("["))] for y in carddetails[1].split(",")])
    tarotranks = deque([TarotCard.tarot_ranks[int(z.strip().strip("]").strip("["))] for z in carddetails[2].split(",")])

    assembledCards = deque([])

    while len(suits) > 0:
        if suits[0] == "Tarot":
            assembledCards.append(tarotranks.popleft() + "[" + suits.popleft() + "]")
        else:
            assembledCards.append(regularranks.popleft() + " of " + suits.popleft())

    for x, value in enumerate(range(int(len(assembledCards) / 3))):
        print("Lot " + str(
            value + 1) + ": " + assembledCards.popleft() + ", " + assembledCards.popleft() + ", " + assembledCards.popleft())



def preprocess(rawdata):
    print("1: Sort by Rank | 2: Sort by Suit | 3: Sort by Color | 4: Sort by Tradition |  ! after num to output wiki "
          "format")
    rawinput = input()
    whichsort = rawinput[0]

    try:
        whichsort = int(whichsort)
    except ValueError:
        whichsort = 1

    try:
        outputformat = rawinput[1]
    except ValueError:
        outputformat = None
    except IndexError:
        outputformat = None

    processhand(rawdata,whichsort,outputformat)


def processhand(rawdata,sortstyle,outputformat):
    GetPlayers = createplayerlist(rawdata)

    #
    # print("1: Sort by Rank | 2: Sort by Suit | 3: Sort by Color | 4: Sort by Tradition |  ! after num to output wiki "
    #       "format")
    # rawinput = input()
    # whichsort = rawinput[0]
    #
    # try:
    #     whichsort = int(whichsort)
    # except ValueError:
    #     whichsort = 1
    #
    # try:
    #     outputformat = rawinput[1]
    # except ValueError:
    #     outputformat = None
    # except IndexError:
    #     outputformat = None

    
    for x in GetPlayers:
        CurrentPlayer = cleaninventory(x)
        def sortby():
            CurrentHand = [z.strip("{").strip("}").strip() for z in CurrentPlayer[3].split(" ") if z]
            HandDetails =[]
            TarotSleeve = []


            for B in CurrentHand:
                cardtype = B.find("Card")
                if cardtype > -1: # add tarot to this
                    HandDetails.append(PlayingCard())
                    HandDetails[-1].ranknum = B[5]
                    HandDetails[-1].suitnum = B[7:]
                    HandDetails[-1].interpret()
                else:
                    TarotSleeve.append(TarotCard())
                    TarotSleeve[-1].ranknum = B[6:]
                    TarotSleeve[-1].interpret()

            if sortstyle == 1:
                HandDetails.sort(key=lambda x: x.suitnum)
                HandDetails.sort(key=lambda x: x.ranknum)
            elif sortstyle == 2:
                HandDetails.sort(key=lambda x: x.ranknum)
                HandDetails.sort(key=lambda x: x.suitnum)
            elif sortstyle == 3:
                # Make this add color to the final display
                HandDetails.sort(key=lambda x: x.ranknum)
                HandDetails.sort(key=lambda x: x.color)
            elif sortstyle == 4:
                # Make this add tradition to the final display
                HandDetails.sort(key=lambda x: x.ranknum)
                HandDetails.sort(key=lambda x: x.tradition)

            if outputformat == None:
                HandPrint = CurrentPlayer[0] + ": "
            elif outputformat == "!":
                HandPrint = "|-\n| " + CurrentPlayer[0] + " || " + CurrentPlayer[1] + " || " + CurrentPlayer[2] + " || "


            for x in HandDetails:
                # add ability to print wiki formatted for rank / suit
                if outputformat == None:
                    HandPrint += x.rank + " " + x.suit
                    if sortstyle == 3:
                        HandPrint += " [" + x.color + "]"
                    elif sortstyle == 4:
                        HandPrint += " [" + str(x.tradition) + "]"
                    HandPrint += ", "
                elif outputformat == "!":
                    HandPrint += "{{Card|"
                    try:
                        RankText = PlayingCard.invrank_alpha[x.ranknum]
                    except KeyError:
                        RankText = str(x.ranknum)
                    HandPrint += RankText + "|"
                    try:
                        SuitText = PlayingCard.invsuit_alpha[x.suitnum]
                    except KeyError:
                        SuitText = "Error, sorry :("
                    HandPrint += SuitText + "}} "


            if len(TarotSleeve) > 0:
                if outputformat == None:
                    HandPrint += "Tarot Cards: "
                for z in TarotSleeve:
                    if outputformat == None:
                        HandPrint += "[" + z.rank + "]"
                    elif outputformat == "!":
                        HandPrint += "{{Tarot|"
                        TarotText = z.ranknum
                        HandPrint += TarotText + "}} "

            print(HandPrint)

        try:
            if CurrentPlayer[3] != "-":
                sortby()
        except IndexError:
            print("Make sure you copy the wiki table")
            return

if __name__ == '__main__':
    while True:
        print("1: Tax | 2: Sort | 3: Hand")
        whichprogram = input()
        try:
            int(whichprogram)
        except ValueError:
            whichprogram = 0

        if int(whichprogram) == 1:
            processtaxes(clipboard())
            input()
        elif int(whichprogram) == 2:
            processdiceroles(clipboard())
            input()
        elif int(whichprogram) == 3:
            preprocess(clipboard())
            input()
        elif int(whichprogram) == 4:
            testfunction()
            input()
        else:
            print("Thats not an option")
