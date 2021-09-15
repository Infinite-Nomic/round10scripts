import math
from collections import deque

if __name__ == '__main__':
    from tkinter import *

    CB = Tk()
    CB.withdraw()
    from playwright.sync_api import sync_playwright

import re


class PlayingCard:
    def __init__(self):
        self.suit_num = 0
        self.rank_num = 0
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
    #Creates inverted dictionary
    invsuit_alpha = {v: k for k, v in suit_alpha.items()}

    rank_alpha = {
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
    
    #Creates inverted dictionary
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
        # 1: "Green",
        # 2: "Red",
        # 3: "Gold",
        # 4: "Black",
        # 5: "Green",
        # 6: "Red",
        # 7: "Gold",
        # 8: "Black",
        # 9: "Green",
        # 10: "Red",
        # 11: "Gold",
        # 12: "Black",
        # 13: "Special"
        1: "Green",
        5: "Green",
        9: "Green",
        2: "Red",
        6: "Red",
        10: "Red",
        3: "Gold",
        7: "Gold",
        11: "Gold",
        4: "Black",
        8: "Black",
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
    
    #Uses the suit num and rank num to populate the rest of the info for a card
    def interpret(self):
        try:
            self.suit = self.card_suits[int(self.suit_num)]
            self.suit_num = int(self.suit_num)
            self.color = self.card_colors[int(self.suit_num)]
            self.tradition = self.card_traditions[int(self.suit_num)]
        except ValueError:
            self.suit = self.card_suits[self.suit_alpha[self.suit_num]]
            self.suit_num = int(self.suit_alpha[self.suit_num])
            self.color = self.card_colors[self.suit_num]
            self.tradition = self.card_traditions[self.suit_num]

        try:
            self.rank = self.card_ranks[int(self.rank_num)]
            self.rank_num = int(self.rank_num)
        except ValueError:
            self.rank = self.card_ranks[self.rank_alpha[self.rank_num]]
            self.rank_num = int(self.rank_alpha[self.rank_num])


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
    
    #inverted dictionary
    invtarot_ranks = {v: k for k, v in tarot_ranks.items()}

    def __init__(self):
        self.ranknum = ""
        self.rank = ""
    
    #uses raw rank to get rank name
    def interpret(self):
        self.rank = self.tarot_ranks[int(self.ranknum)]

#Uses playwright to get the table info from the wiki
def grab_table():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://infinitenomic.miraheze.org/w/index.php?title=Round_10/Gamestate&action=edit&section=5")
        hold_table = str(page.inner_html("id=wpTextbox1"))
        browser.close()
        return hold_table


def test_function():
    process_taxes(grab_table())


def clipboard():
    return CB.clipboard_get()


def create_player_list(raw_data):
    raw_list = raw_data.splitlines()
    player_list = [x for x in raw_list if x != '|-'
                   and x != ''
                   and x != '== Players =='
                   and x != '{| class="wikitable sortable"'
                   and x != "|}"
                   and x != '! Player !! Chips !! Inventory !! Cards']
    return player_list


def clean_inventory(unclean):
    split = unclean.split("||")
    clean = [y.strip("|").strip() for y in split]
    return clean


def process_taxes(raw_data):
    # make sure the wiki table is in your clipboard if youre not using the wiki
    print("1: All Players | 2: Players with tax < 100")
    which_mode = input()
    try:
        int(which_mode)
    except ValueError:
        which_mode = 1

    list_clean = create_player_list(raw_data)
    longest_name = 0
    if len(list_clean) <= 1:
        print("Make sure you have the wiki table in your clipboard")
        return

    for x in list_clean:
        name = clean_inventory(x)[0]
        if len(name) > longest_name:
            longest_name = len(name)

    for x in list_clean:
        inv_clean = clean_inventory(x)
        player_name = inv_clean[0]
        name_buffer = " "
        chip_value = int(inv_clean[1])
        tax_value = 0
        trung_value = 0  
        trung_match = re.search("(\d+) Trung", inv_clean[2])
        if trung_match is not None:
            trung_value = int(trung_match.group(1))
        wealth_value = chip_value + (trung_value * 20)

        def buffer(value):
            buff = " " * (4 - len(str(value)))
            return " " + str(value) + buff + "| "

        if wealth_value >= 320:  # the first tax increment kicks in at 320 currently
            tax_value = math.floor(((trung_value * 20) + chip_value - 300) / 20) * 5
            if tax_value >= 100:  # the hard cap on tax is 100 currently
                tax_value = 100
        new_chip_value = chip_value + (100 - tax_value)

        if len(player_name) < longest_name:
            name_buffer = " " * (1 + longest_name - len(player_name))

        def print_inventory():
            print(player_name + name_buffer 
                  + "| New Chips:" + buffer(new_chip_value) 
                  + "Wealth:" + buffer(wealth_value) 
                  + "Chips:" + buffer(chip_value) 
                  + "Trungs:" + buffer(trung_value) 
                  + "Tax:" + buffer(tax_value) 
                  + "Gain:" + buffer(100 - tax_value))

        if int(which_mode) == 1:
            print_inventory()
        elif int(which_mode) == 2 and tax_value < 100:
            print_inventory()


def process_dice_roles(raw_data):
    # Separate the three sets of rolls with | and copy it into your clipboard
    raw_dice_rolls = raw_data
    card_details = raw_dice_rolls.split("|")
    suits = deque([PlayingCard.card_suits[int(x.strip("[").strip().strip("]"))] for x in card_details[0].split(",")])
    regular_ranks = deque(
        [PlayingCard.card_ranks[int(y.strip().strip("]").strip("["))] for y in card_details[1].split(",")])
    tarot_ranks = deque([TarotCard.tarot_ranks[int(z.strip().strip("]").strip("["))] for z in card_details[2].split(",")])

    assembledCards = deque([])

    while len(suits) > 0:
        if suits[0] == "Tarot":
            assembledCards.append(tarot_ranks.popleft() + "[" + suits.popleft() + "]")
        else:
            assembledCards.append(regular_ranks.popleft() + " of " + suits.popleft())

    for x, value in enumerate(range(int(len(assembledCards) / 3))):
        print("Lot "
              + str(value + 1)
              + ": "
              + assembledCards.popleft() + ", "
              + assembledCards.popleft() + ", "
              + assembledCards.popleft())


def preprocess(raw_data):
    print("1: Sort by Rank | 2: Sort by Suit | 3: Sort by Color | 4: Sort by Tradition |  ! after num to output wiki "
          "format")
    raw_input = input()
    try:
        which_sort = raw_input[0]
    except IndexError:
        which_sort = 1
    except ValueError:
        which_sort = 1

    try:
        output_format = raw_input[1]
    except ValueError:
        output_format = None
    except IndexError:
        output_format = None

    process_hand(raw_data, which_sort, output_format)


def process_hand(raw_data, sort_style, output_format):
    GetPlayers = create_player_list(raw_data)

    for z in GetPlayers:
        CurrentPlayer = clean_inventory(z)

        def sort_by():
            CurrentHand = [b.strip("{").strip("}").strip() for b in CurrentPlayer[3].split(" ") if b]
            HandDetails = []
            TarotSleeve = []

            for B in CurrentHand:
                card_type = B.find("Card")
                #Creates a card (playing / tarot split) object and calls interpret method
                if card_type > -1:
                    HandDetails.append(PlayingCard())
                    HandDetails[-1].rank_num = B[5]
                    HandDetails[-1].suit_num = B[7:]
                    HandDetails[-1].interpret()
                else:
                    TarotSleeve.append(TarotCard())
                    TarotSleeve[-1].ranknum = B[6:]
                    TarotSleeve[-1].interpret()

            # Uses pythons sort function to sort peoples hands
            if sort_style == 1:
                HandDetails.sort(key=lambda z: z.suit_num)
                HandDetails.sort(key=lambda z: z.rank_num)
            elif sort_style == 2:
                HandDetails.sort(key=lambda z: z.rank_num)
                HandDetails.sort(key=lambda z: z.suit_num)
            elif sort_style == 3:
                HandDetails.sort(key=lambda z: z.rank_num)
                HandDetails.sort(key=lambda z: z.color)
            elif sort_style == 4:
                HandDetails.sort(key=lambda z: z.rank_num)
                HandDetails.sort(key=lambda z: z.tradition)
            else:
                HandDetails.sort(key=lambda z: z.suit_num)
                HandDetails.sort(key=lambda z: z.rank_num)
            hand_print = ""
            
            #Controls if the output is human readable or wiki format
            if output_format is None:
                hand_print = CurrentPlayer[0] + ": "
            elif output_format == "!":
                hand_print = "|-\n| " + CurrentPlayer[0] + " || " + CurrentPlayer[1] + " || " + CurrentPlayer[
                    2] + " || "

            for y in HandDetails:
                #This part changes how it prints cards, adds color and tradition if those are the sort
                if output_format is None:
                    hand_print += y.rank + " " + y.suit
                    if sort_style == 3:
                        hand_print += " [" + y.color + "]"
                    elif sort_style == 4:
                        hand_print += " [" + str(y.tradition) + "]"
                    hand_print += ", "
                    
                #
                elif output_format == "!":
                    hand_print += "{{Card|"
                    try:
                        rank_text = PlayingCard.invrank_alpha[y.rank_num]
                    except KeyError:
                        rank_text = str(y.rank_num)
                    hand_print += rank_text + "|"
                    try:
                        suit_text = PlayingCard.invsuit_alpha[y.suit_num]
                    except KeyError:
                        suit_text = "Error, sorry :("
                    hand_print += suit_text + "}} "
                    
            #Adds any tarot cards at the end
            if len(TarotSleeve) > 0:
                if output_format is None:
                    hand_print += "Tarot Cards: "
                for a in TarotSleeve:
                    if output_format is None:
                        hand_print += "[" + a.rank + "]"
                    elif output_format == "!":
                        hand_print += "{{Tarot|"
                        TarotText = a.ranknum
                        hand_print += TarotText + "}} "

            print(hand_print)

        try:
            if CurrentPlayer[3] != "-":
                #doesn't call a sort if the player has no inventory
                sort_by()
        except IndexError:
            print("Make sure you copy the wiki table")
            return
    print("")


if __name__ == '__main__':
    #This is the main menu, directs to one of the subfunctions based on input
    #Accepts ! as an argument after the number to allow pulling from the wiki directly
    while True:
        print("1: Tax | 2: Interp Raw dicerolls | 3: Hand | 4: Test || Add ! after to pull directly from wiki (slow)")
        which_program = str(input())

        try:
            which_program[0]
        except IndexError:
            which_program = "0"

        if which_program[0] == "1":
            if len(which_program) > 1:
                if which_program[1] == "!":
                    process_taxes(grab_table())
            else:
                process_taxes(clipboard())
            input()

        elif which_program[0] == "2":
            process_dice_roles(clipboard())
            input()

        elif which_program[0] == "3":
            if len(which_program) > 1:
                if which_program[1] == "!":
                    preprocess(grab_table())
            else:
                preprocess(clipboard())
        elif which_program[0] == "4":
            test_function()
            input()
        else:
            print("That's not an option")
