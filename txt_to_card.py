
def make_cards_from_file(file_of_text):
    """
    A funciton to create bingo cards from text
    """

    with open(file_of_text, "r") as f:
        parsed = [k.strip() for k in f.readlines()]

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


def make_cards_from_list(list_of_text):
    """
    A funciton to create bingo cards from text
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
        self.row1 = card_list[0]
        self.row2 = card_list[1]
        self.row3 = card_list[2]

        # This is your bingo card
        self.card = {
            "row1": self.row1,
            "row2": self.row2,
            "row3": self.row3
        }
        self.lines = current_line

    def pop_number(self, number):
        """
        Remove a number from a row if it's there.
        Akin to putting a piece on top of a number in 'real' bingo.
        """
        # Iterate over key value pairs in card dict
        for row, value in self.card.items():
            if number in value:
                # Use list.index(element) to fetch the index of the number and pop it from the list
                you_had = f"You had {value.pop(value.index(number))} in {row}"

                if self.check_bingo() != False:
                    rows = self.check_bingo()
                    return f"You have bingo on row(s) {rows}. Last number was {you_had[8:]}"
                return you_had
                # Use list.remove(element) instead
                # value.remove(number)

        return None

        if self.check_bingo():
            rows = self.check_bingo()

    def check_bingo(self):
        """
        Do I have bingo on the current line?
        """
        cleared_rows = 0
        row_number = []

        for row, value in self.card.items():
            if len(value) == 0:
                cleared_rows += 1
                row_number.append(row)

        if cleared_rows == self.lines:
            return row_number
        else:
            return False


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
    removed_numbers = [f"{i} in card {idx+one_index}" for idx,
                       i in enumerate(pop_values) if i != None]
    return removed_numbers
