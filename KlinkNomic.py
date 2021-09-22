import math
from collections import deque

if __name__ == '__main__':
    from tkinter import *

    CB = Tk()
    CB.withdraw()
    from playwright.sync_api import sync_playwright

import re

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

# inverted dictionary
invtarot_ranks = {v: k for k, v in tarot_ranks.items()}

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
# Creates inverted dictionary
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

# Creates inverted dictionary
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


class PlayingCard:
    def __init__(self):
        self.suit_num = 0
        self.rank_num = 0
        self.suit = ""
        self.rank = ""
        self.color = ""
        self.tradition = ""

    # Uses the suit num and rank num to populate the rest of the info for a card
    def interpret(self):
        try:
            self.suit = card_suits[int(self.suit_num)]
            self.suit_num = int(self.suit_num)
            self.color = card_colors[int(self.suit_num)]
            self.tradition = card_traditions[int(self.suit_num)]
        except ValueError:
            self.suit = card_suits[suit_alpha[self.suit_num]]
            self.suit_num = int(suit_alpha[self.suit_num])
            self.color = card_colors[self.suit_num]
            self.tradition = card_traditions[self.suit_num]

        try:
            self.rank = card_ranks[int(self.rank_num)]
            self.rank_num = int(self.rank_num)
        except ValueError:
            self.rank = card_ranks[rank_alpha[self.rank_num]]
            self.rank_num = int(rank_alpha[self.rank_num])


class TarotCard:

    def __init__(self):
        self.rank_num = ""
        self.rank = ""

    # uses raw rank to get rank name
    def interpret(self):
        self.rank = tarot_ranks[int(self.rank_num)]


class Player:
    list_of_players = []
    longest_name = 0

    def __init__(self):
        self.name = None
        self.raw_hand = None
        self.hand = []
        self.chips = 0
        self.trungs = 0
        self.misc_inv = ""

    def map_card_data(self):
        self.raw_hand = [b.strip("{").strip("}").strip() for b in self.raw_hand.split(" ") if b]
        for x in self.raw_hand:
            temp_data = x.split("|")

            if x.find("Card") > -1:
                self.hand.append(PlayingCard())
                self.hand[-1].rank_num = temp_data[1]
                self.hand[-1].suit_num = temp_data[2]
            elif x.find("Tarot") > -1:
                self.hand.append(TarotCard())
                self.hand[-1].rank_num = temp_data[1]

            self.hand[-1].interpret()


# Uses playwright to get the table info from the wiki
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


def process_raw_table_data(raw_data):
    raw_list = raw_data.splitlines()
    player_list = [x for x in raw_list if x != '|-'
                   and x != ''
                   and x != '== Players =='
                   and x != '{| class="wikitable sortable"'
                   and x != "|}"
                   and x != '! Player !! Chips !! Inventory !! Cards']
    return player_list


def clean_inventory(unprocessed_player_data):
    split = unprocessed_player_data.split("||")
    clean = [y.strip("|").strip() for y in split]
    return clean


def populate_players(raw_data):
    raw_inventories = raw_data.splitlines()

    list_of_inventories = [x for x in raw_inventories if x != '|-'
                           and x != ''
                           and x != '== Players =='
                           and x != '{| class="wikitable sortable"'
                           and x != "|}"
                           and x != '! Player !! Chips !! Inventory !! Cards']

    for x in list_of_inventories:
        current_player = Player()  # create player object and fill out what they own
        current_inventory = clean_inventory(x)
        current_player.name = current_inventory[0]

        if len(current_player.name) > Player.longest_name:
            Player.longest_name = len(current_player.name)

        if current_inventory[1].isdigit() is False:
            current_player.chips = 0
        else:
            current_player.chips = int(current_inventory[1])
        current_player.misc_inv = current_inventory[2]
        trung_match = re.search('(\d+) Trung', current_inventory[2])
        if trung_match is not None:
            current_player.trungs = int(trung_match.group(1))
        else:
            current_player.trungs = 0
        if current_inventory[3] == "-":
            current_player.raw_hand = ""
        else:
            current_player.raw_hand = current_inventory[3]  # currently raw data, need to process into card objects
            current_player.map_card_data()
        Player.list_of_players.append(current_player)


def process_taxes(raw_data):
    # make sure the wiki table is in your clipboard if you're not using the wiki
    if not Player.list_of_players:
        populate_players(raw_data)

    player_inventories = Player.list_of_players

    print("1: All Players | 2: Players with tax < 100")
    which_mode = input()
    try:
        int(which_mode)
    except ValueError:
        which_mode = 1

    tax_value = 0
    name_buffer = " "

    def buffer(value):
        buff = " " * (4 - len(str(value)))
        return " " + str(value) + buff + "| "

    for player in player_inventories:
        wealth_value2 = player.chips + (player.trungs * 20)

        if wealth_value2 >= 320:
            tax_value = math.floor(((player.trungs * 20) + player.chips - 300) / 20) * 5

            if tax_value > 100:
                tax_value = 100

        new_chip_value = player.chips + (100 - tax_value)

        if len(player.name) < Player.longest_name:
            name_buffer = " " * (1 + Player.longest_name - len(player.name))

        def print_inventory():
            print(player.name + name_buffer
                  + "| New Chips:" + buffer(new_chip_value)
                  + "Wealth:" + buffer(wealth_value2)
                  + "Chips:" + buffer(player.chips)
                  + "Trungs:" + buffer(player.trungs)
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
    suits = deque([card_suits[int(x.strip("[").strip().strip("]"))] for x in card_details[0].split(",")])
    regular_ranks = deque(
        [card_ranks[int(y.strip().strip("]").strip("["))] for y in card_details[1].split(",")])
    tarot_ranks_list = deque(
        [tarot_ranks[int(z.strip().strip("]").strip("["))] for z in card_details[2].split(",")])

    assembledCards = deque([])

    while len(suits) > 0:
        if suits[0] == "Tarot":
            assembledCards.append(tarot_ranks_list.popleft() + "[" + suits.popleft() + "]")
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
    if not Player.list_of_players:
        populate_players(raw_data)

    print("Sort by: 1: Rank | 2: Suit | 3: Color | 4: Tradition ||  Mods: ! for wiki "
          "format | @ to choose specific users")
    raw_input = input()
    format_for_wiki = False
    all_users = True
    which_sort = 0

    if len(raw_input) == 1:
        which_sort = raw_input
    elif len(raw_input) > 1:
        which_sort = raw_input[0]
        if str(raw_input).find("@") > -1:
            all_users = False

        if str(raw_input).find("!") > -1:
            format_for_wiki = True
    else:
        print("Defaulting to Rank sort")
        which_sort = 1

    try:
        int(which_sort)
    except ValueError:
        print("ValueError: Defaulting to Rank sort")
        which_sort = 1

    process_hand(which_sort, format_for_wiki, all_users)


def process_hand(sort_style, wiki_formatted, all_users):
    GetPlayers = Player.list_of_players

    if all_users is False:
        longest_name = 0
        name_buffer = " "
        number_buffer = " "
        formatted_string = ""
        selected_players = []

        for x in Player.list_of_players:
            if len(x.name) > longest_name:
                longest_name = len(x.name)

        count = 1

        for x in GetPlayers:
            if count > 9:
                number_buffer = ""
            if len(x.name) < longest_name:
                name_buffer = " " * (1 + longest_name - len(x.name))
            formatted_string += str(count) + ". " + number_buffer + x.name + name_buffer + " | "
            if count % 5 == 0:
                formatted_string += "\n"
            count += 1

        print(formatted_string)
        print("Input inv numbers, comma separated || Mods: ! to add/remove cards if providing a single inventory (WIP)")
        input_holder = input()

        # Once I add the logic to add,remove cards it'll go here
        if input_holder.find("!") > -1:
            input_holder = input_holder.replace("!", "")

        specific_players = input_holder.split(",")
        for y in specific_players:
            selected_players.append(GetPlayers[int(y)-1])
        GetPlayers = selected_players

    for player_holder in GetPlayers:

        def sort_by():
            CurrentHand = player_holder.hand
            HandDetails = []
            TarotSleeve = []

            for card in CurrentHand:

                # Sorts cards out into playing/tarot
                if type(card).__name__ == "PlayingCard":
                    HandDetails.append(card)
                else:
                    TarotSleeve.append(card)

            # Uses pythons sort function to sort peoples hands
            if sort_style == 1:
                HandDetails.sort(key=lambda a: a.suit_num)
                HandDetails.sort(key=lambda b: b.rank_num)
            elif sort_style == 2:
                HandDetails.sort(key=lambda c: c.rank_num)
                HandDetails.sort(key=lambda d: d.suit_num)
            elif sort_style == 3:
                HandDetails.sort(key=lambda e: e.rank_num)
                HandDetails.sort(key=lambda f: f.color)
            elif sort_style == 4:
                HandDetails.sort(key=lambda g: g.rank_num)
                HandDetails.sort(key=lambda h: h.tradition)
            else:
                HandDetails.sort(key=lambda i: i.suit_num)
                HandDetails.sort(key=lambda j: j.rank_num)
            hand_print = ""

            # Controls if the output is human readable or wiki format
            if wiki_formatted is False:
                hand_print = player_holder.name + ": "
            elif wiki_formatted is True:
                hand_string = ""
                for card_text in player_holder.raw_hand:
                    hand_string += " {{" + card_text + "}}"

                if hand_string == "":
                    hand_string = "-"

                hand_print = "|-\n| " + player_holder.name + " || " \
                             + str(player_holder.chips) + " || " \
                             + str(player_holder.misc_inv) + " || "  \
                             + hand_string + " || "

            for c in HandDetails:
                if wiki_formatted is False:
                    hand_print += c.rank + " " + c.suit
                    if sort_style == 3:
                        hand_print += " [" + c.color + "]"
                    elif sort_style == 4:
                        hand_print += " [" + str(c.tradition) + "]"
                    hand_print += ", "
                elif wiki_formatted is True:
                    hand_print += "{{Card|"
                    try:
                        rank_text = invrank_alpha[c.rank_num]
                    except KeyError:
                        rank_text = str(c.rank_num)
                    hand_print += rank_text + "|"
                    try:
                        suit_text = invsuit_alpha[c.suit_num]
                    except KeyError:
                        suit_text = "Error, sorry :("
                    hand_print += suit_text + "}} "

            # Adds any tarot cards at the end
            if len(TarotSleeve) > 0:
                if wiki_formatted is False:
                    hand_print += "Tarot Cards: "
                for a in TarotSleeve:
                    if wiki_formatted is False:
                        hand_print += "[" + a.rank + "]"
                    elif wiki_formatted is True:
                        hand_print += "{{Tarot|"
                        TarotText = a.rank_num
                        hand_print += TarotText + "}} "

            print(hand_print)

        try:
            if player_holder.hand != "-":
                # doesn't call a sort if the player has no inventory
                sort_by()
        except IndexError:
            print("Index error :( Make sure you copy the wiki table")
            return
    print("")


if __name__ == '__main__':
    # This is the main menu, directs to one of the subfunctions based on input
    # Accepts ! as an argument after the number to allow pulling from the wiki directly
    while True:
        print("1: Tax | 2: Interp Raw dice rolls | 3: Hand | 4: Test | 5: Quit || Mods: ! Pull table frm wiki (slow)")
        which_program = str(input())

        try:
            which_program[0]
        except IndexError:
            which_program = "0"

        # Send to process taxes
        if which_program[0] == "1":
            if len(which_program) > 1:
                if which_program[1] == "!":
                    process_taxes(grab_table())
            else:
                process_taxes(clipboard())
            input()
        # Sends to process dice rolls
        elif which_program[0] == "2":
            process_dice_roles(clipboard())
            input()
        # Sends to preprocess - > process the raw_hand, with options
        elif which_program[0] == "3":
            if len(which_program) > 1:
                if which_program[1] == "!":
                    preprocess(grab_table())
            else:
                preprocess(clipboard())
        # This sends it to the test function
        elif which_program[0] == "4":
            test_function()
            input()
        elif which_program[0] == "5":
            break
        else:
            print("That's not an option")
