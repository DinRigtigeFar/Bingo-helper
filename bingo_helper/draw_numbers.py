from random import randint

"""
Small script to simulate the drawing of bingo numbers
"""

drawn_numbers = []

while len(drawn_numbers) != 90:
    i = randint(1,91)
    if i not in drawn_numbers:
        drawn_numbers.append(i)

print(drawn_numbers)
