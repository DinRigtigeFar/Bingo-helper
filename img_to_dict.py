import argparse
import os
import re

import pytesseract
from PIL import Image

ap = argparse.ArgumentParser()
# Adding an image to be read argument
ap.add_argument("-f", "--folder", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-v", "--verbose", type=bool, default=False,
                help="enable verbose mode to print every bingo card after it's been parsed")
args = vars(ap.parse_args())

# Create an empty list to store bingo cards in
card_list = []
check = 1

# Iterate through pictures do operations and delete them
for img in os.listdir(args["folder"]):
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    try:
        text = pytesseract.image_to_string(Image.open(os.path.join(
            args["folder"], img)), config='digits, -psm 3, --oem 1')
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

    # Create a list of lists that will become a BingoCard object
    card = [pre_card[0:5], pre_card[5:10], pre_card[10:]]

    # Verbose statement
    if args["verbose"]:
        print(f"This is your bingo card no. {check}: {card}")
        check += 1

    card_list.append(card)
