#!/usr/bin/env python

import pytesseract
from PIL import Image
import argparse
import os
import re

ap = argparse.ArgumentParser()
# Adding an image to be read argument
ap.add_argument("-f", "--folder", required=True, help="path to input image to be OCR'd")
ap.add_argument("-v", "--verbose", type=bool, default=False, help="enable verbose mode to print every bingo card after it's been parsed")
args = vars(ap.parse_args())

# Create an empty list to store bingo cards in
card_list = []
check = 1

# Iterate through pictures do operations and delete them
for img in os.listdir(args["folder"]):
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    try:
        text = pytesseract.image_to_string(Image.open(args["folder"] + "/" + img), config='digits, -psm 1000')
    except OSError:
        continue
    # Make 1 list with items split by newline
    print(text)
    digText = re.split("\n", text)

    # Make 1 list with 3 items containing only digits
    digText2 = []
    for item in digText:
        digText2.append(''.join(re.findall(r'\d+', item)))

    # Creates a list from all digits in a string
    pre_card = [int(i) for i in text.split() if i.isdigit()]

    # Checks if the list contains 15 digits
    if len(pre_card) != 15:
        print(f"Expected len 15 got len {len(pre_card)}")

    # Create dictionary to hold this card
    card = {"line1": pre_card[0:5], "line2": pre_card[5:10], "line3": pre_card[10:]}

    # Verbose statement
    if args["verbose"] != False:
        print(f"This is your bingo card no. {check}: {card}")
        check += 1

    card_list.append(card)

while True:
    check_list = []
    try:
        current_number = int(input("Number called: "))
    except ValueError:
        print("Please input a number from 1-90")
        continue

    check_list.append(current_number)

    for card in card_list:
        for key in card:
            if current_number in card[key]:
                card[key].remove(current_number)
            if len(card[key]) == 0:
                print(f"Bingo on {key} in {card_list.index(card)+1}")



