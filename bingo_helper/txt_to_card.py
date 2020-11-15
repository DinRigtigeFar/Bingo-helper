"""
A test vesion of txt_to_card.py with added features and some optimizations, but maybe not entirely bug free. Use at own risk.
"""


def make_cards_from_file(file_of_text):
    """
    A funciton to create bingo cards from a text file.
    Format should be (in the file):
    no no no no no
    no no no no no
    no no no no no

    no...
    """

    with open(file_of_text, "r") as f:
        parsed = [k.strip() for k in f.readlines()]

    card = []
    cards = []
    for line in parsed:
        if len(line) == 0:
            card = []
            # continue means start over
            continue
        card_line = [int(i) for i in line.split(" ")]
        card.append(card_line)
        if len(card) == 3:
            cards.append(card)

    return cards


def make_cards_from_list(list_of_text):
    """
    A funciton to create bingo cards from plain text.
    Format same as 'make_cards_from_file'
    """
    parsed = [k.strip() for k in list_of_text.split("\n")]
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

    return cards


class BingoCard:
    """
    A bingo card class.
    """

    def __init__(self, card_list, current_line=1):
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

    def pop_number(self, number):
        """
        Remove a number from a row if it's there.
        Akin to putting a piece on top of a number in 'real' bingo.
        Order: Check if number in card, check if missing one number for bingo, check if bingo (return bingo), else return number and row else return None (number not in card)
        """
        # Iterate over key value pairs in card dict
        for row, value in self.card.items():
            if number in value:
                # Use list.index(element) to fetch the index of the number and pop it from the list
                called_number = value.pop(value.index(number))
                you_had = f"You had {called_number} in {row}"
                # Check bingo (del row if bingo) always before close_to_bingo (uses amount of rows to check)
                bingo_rows = self.check_bingo()
                i_has_bingo = self.close_to_bingo()
                if bingo_rows != False:
                    if self.lines == 1:
                        return f"!!!!!!!!!!!!!!You have bingo on one row!!!! Last number was {called_number} in row {bingo_rows[0][4]}", i_has_bingo
                    elif self.lines == 2:
                        return f"!!!!!!!!!!!!!!You have bingo on two rows!!!! Last number was {called_number} in row {bingo_rows[0][4]}", i_has_bingo
                    else:
                        return f"!!!!!!!!!!!!!!You have the whole card full!!!! Last number was {called_number} in row {bingo_rows[0][4]}", i_has_bingo

                # TODO: Maybe change "you_had" into the values so they are easier to modify for presentation. i_has_bingo is a dict of row and missing number for bingo
                return you_had, i_has_bingo

        return None

    def check_bingo(self):
        """
        Do I have bingo on the current line?
        Delete key if bingo (makes it easier to check for close to bingo)
        row_number will never be anything else than 0 or 1 since any number can only appear on the same card once!
        """
        # All rows stil present = no bingo yet = self.lines == 1
        if len(self.card.items()) == 3 and self.lines == 1:
            cleared_rows, row_number = self.aux_remove_row()
        # One row has been removed due to it being full
        elif len(self.card.items()) == 2 and self.lines == 2:
            cleared_rows, row_number = self.aux_remove_row()
        elif len(self.card.items()) == 1 and self.lines == 3:
            cleared_rows, row_number = self.aux_remove_row()
        else:
            cleared_rows, row_number = self.aux_remove_row()
            cleared_rows = 0

        return row_number if cleared_rows == 1 else False

    def close_to_bingo(self):
        """
        Function to check whether you're missing one number for bingo.
        """

        missing_nums = []
        rows_left = len(self.card.items())
        # One from one row
        if rows_left == 3 and self.lines == 1:
            for row, value in self.card.items():
                if len(value) == 1:
                    # Append the only number in the row and do so for all rows in card
                    missing_nums.append(value[0])
        # One from two rows
        elif rows_left == 2 and self.lines == 2:
            for row, value in self.card.items():
                if len(value) == 1:
                    # Append the only number in the row and do so for all rows in card
                    missing_nums.append(value[0])
        # One from whole card
        elif rows_left == 1 and self.lines == 3:
            for row, value in self.card.items():
                if len(value) == 1:
                    # Append the only number in the row
                    missing_nums.append(value[0])

        return missing_nums if len(missing_nums) != 0 else None

    def aux_remove_row(self):
        """
        Aux function to remove row from card (used in check bingo)
        Delete key if bingo (makes it easier to check for close_to_bingo)
        """
        cleared_rows = 0
        row_number = []
        for row, value in self.card.items():
            # If no values == bingo
            if len(value) == 0:
                cleared_rows += 1
                row_number.append(row)
                # Remove 0 val line from dict
                self.card.pop(row)
                break
        # Only return the variables if they aren't 0 and empty
        return cleared_rows, row_number if cleared_rows and row_number else False


class BingoCardDict(BingoCard):
    """
    A bingo card class to create a bingo card from a dict rather than from raw list.
    Otherwise the same as the regular BingoCard class.
    """

    def __init__(self, card_dict, current_line=1):
        # This is your bingo card
        self.card = card_dict
        self.lines = current_line


def pop_list(number, list_of_BingoCard_objects, one_index=1):
    """
    Use to keep track of bingo cards when you have many.
    Ordered by the given list. Set one_index to 0 to get 0 index instead of 1.
    """
    # List comp to do the operations
    # It's annoying to be told that a number isn't in your card so we check if it's None before returning the f-string
    pop_values = [card.pop_number(number)
                  for card in list_of_BingoCard_objects]
    removed_numbers = [f"{i[0]} in card {idx+one_index}" for idx,
                       i in enumerate(pop_values) if i != None]
    # TODO: Unpack the i[1] list inside string
    missing = [f"Missing {i[1]} in card {idx+one_index} for bingo" for idx,
               i in enumerate(pop_values) if i != None and i[1] != None]

    return removed_numbers, missing
