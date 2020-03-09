
def make_cards(list_of_text):
    """
    A funciton to create bingo cards from text
    """

    with open(list_of_text, "r") as f:
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


class BingoCard:
    """
    A bingo card class
    """

    def __init__(self, card_list):
        self.row1 = card_list[0]
        self.row2 = card_list[1]
        self.row3 = card_list[2]

        # This is your bingo card
        self.card = {
            "row1": self.row1,
            "row2": self.row2,
            "row3": self.row3
        }

    def pop_number(self, number):
        """
        Remove a number from a row if it's there.
        Akin to putting a piece on top of a number in 'real' bingo.
        """
        # Iterate over key value pairs in card dict
        for row, value in self.card.items():
            if number in value:
                # Use list.index(element) to fetch the index of the number and pop it from the list
                you_had = f"You had {value.pop(value.index(number))}"
                if self.check_bingo():
                    rows = self.check_bingo()
                    return f"You have bingo on row(s) {rows}. Last number was {you_had}"
                return you_had
                # Use list.remove(element) instead
                # value.remove(number)

        return f"You didn't have {number}"

        if self.check_bingo():
            rows = self.check_bingo()
            print(f"You have bingo on row(s) {rows}")

    def lines(self, lines=1):
        """
        What line of bingo are we on: 1, 2 or 3.

        """
        self.lines = lines

        return self.lines

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


mine_plader = make_cards("cards.txt")
my_cards = [BingoCard(i) for i in mine_plader]


def pop_list(number, one_index=1, list_of_BingoCard_objects=my_cards):
    """
    Use to keep track of bingo cards when you have many.
    Ordered by the given list. Set one_index to 1 to get 1 index instead of 0.
    """
    for idx, card in enumerate(list_of_BingoCard_objects):
        print(f"{card.pop_number(number)} in card {idx+one_index}")

def next_line(number, list_of_BingoCard_objects=my_cards):
    """
    Put the number of the current line (a bingo round)
    """
    for i in list_of_BingoCard_objects:
        i.lines(number)


for i in my_cards:
    print(i.card)

pop_list(11)
pop_list(2)
pop_list(22)
pop_list(33)
next_line(2)
pop_list(44)
for i in my_cards:
    print(i.card)

pop_list(15)
pop_list(38)
pop_list(51)
pop_list(88)
pop_list(90)
