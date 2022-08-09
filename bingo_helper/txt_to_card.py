"""
Parse raw bingo cards into actual ones used for bingo
"""
from typing import List, Union, Tuple
from os import path
import json

def make_cards(file_or_text: str)-> List[list]:
    """
    A function to create bingo cards.
    Format should be:\n
    no no no no no\n
    no no no no no\n
    no no no no no\n
    \n
    no...
    """
    # return path.isfile(file_or_text)
    if path.isfile(file_or_text):
        with open(file_or_text, "r") as f:
            parsed = [k.strip() for k in f.readlines()]
    else:
        parsed = [k.strip() for k in file_or_text.split("\n")]

    card = []
    cards = []
    for line in parsed:
        if len(line) == 0:
            card = []
            continue
        card_line = [int(i) for i in line.split(" ")]
        card.append(card_line)
        if len(card) == 3:
            cards.append(card)
            card = []

    return cards


class BingoCard:
    """
    A bingo card class.
    """

    def __init__(self, card_list: list, current_line: int = 1):
        """
        Take a list of raw cards and make a bingo card object.
        """
        self.row1 = card_list[0]
        self.row2 = card_list[1]
        self.row3 = card_list[2]

        # This is your bingo card
        self.card = {
            "row 1": self.row1,
            "row 2": self.row2,
            "row 3": self.row3
        }
        self.lines = current_line
    
    def __repr__(self):
        return json.dumps(self.card)

    def pop_number(self, number: int) -> Union[Tuple[str, Union[List[int], None]], None]:
        """
        Remove a number from a row if it's there.\n
        Akin to putting a piece on top of a number in 'real' bingo.\n
        Order: Check if number in card, check if missing one number for bingo, check if bingo (return bingo), else return number and row else return None (number not in card)
        """
        all_rows = ('row 1', 'row 2', 'row 3')
        # Iterate over key value pairs in card dict
        for row, value in self.card.items():
            if number in value:
                # Use list.index(element) to fetch the index of the number and pop it from the list
                called_number = value.pop(value.index(number))
                you_had = f"{called_number} was in {row}"
                # Check bingo (del row if bingo) always before close_to_bingo (uses amount of rows to check)
                cleared_row = self.check_bingo()
                missing_one = self.close_to_bingo()
                if cleared_row != False:
                    bingo_rows = [i for i in all_rows if i not in self.card.keys()]
                    if self.lines in (1, 2):
                        return f"You have bingo on: {', '.join(i for i in bingo_rows)}", missing_one
                    else:
                        return f"You have bingo on all of", missing_one

                # TODO: Maybe change "you_had" into the values so they are easier to modify for presentation. missing_one is a dict of row and missing number for bingo
                return you_had, missing_one

        return None

    def check_bingo(self) -> bool:
        """
        Do I have bingo on the current line?
        Delete key if bingo
        row_number is bool
        """
        # If rows left in card + lines (how many rows for bingo) == 4 (3+1; 2+2; 1+3)
        if len(self.card.keys()) + self.lines == 4:
            row_number = self.aux_remove_row()
            return row_number
        else:
            self.aux_remove_row()
            return False

    def close_to_bingo(self) -> Union[List[int], None]:
        """
        Check whether you're missing one number for bingo.
        """
        missing_nums = []
        # If rows left in card + lines (how many rows for bingo (1, 2 or 3)) == 4 (3+1; 2+2; 1+3)
        if len(self.card.keys()) + self.lines == 4:
            for value in self.card.values():
                if len(value) == 1:
                    # Append the only number in the row and do so for all rows in card
                    missing_nums.append(value[0])

        return missing_nums if missing_nums else None

    def aux_remove_row(self) -> Union[bool, int]:
        """
        Aux function to remove row from card (used in check bingo)\n
        Delete key if we have bingo
        """
        row_number = False
        for row, value in self.card.items():
            # Remove the row if no values in it and return the row number
            if len(value) == 0:
                row_number = True
                self.card.pop(row)
                # Useless to continue since a number can only appear once in a card
                break
        # Return False or int
        return row_number


class BingoCardDict(BingoCard):
    """
    A bingo card class to create a bingo card from a dict rather than from raw list.\n
    Otherwise the same as the regular BingoCard class.
    """

    def __init__(self, card_dict: dict, current_line: int = 1):
        """
        Takes a dict and current row and creates a bingo card
        """
        # This is your bingo card
        self.card = card_dict
        self.lines = current_line


def pop_list(number: int, list_of_BingoCard_objects: list, one_index: int = 1) -> Tuple[List[str], List[str]]:
    """
    Use to keep track of bingo cards when you have many.
    Ordered by the given list. Set one_index to 0 to get 0 index instead of 1.
    """
    # Try to pop values and return only the cards with popped values
    pop_values = [card.pop_number(number) for card in list_of_BingoCard_objects]
    removed_numbers = [f"{i[0]} {'' if i[0].endswith('all of') else 'in'} card {idx+one_index}" for idx, i in enumerate(pop_values) if i != None]
    
    missing = [f"Missing {', '.join(str(k) for k in i[1])} in card {idx+one_index} for bingo" for idx,
               i in enumerate(pop_values) if i != None and i[1] != None]

    return removed_numbers, missing
