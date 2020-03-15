# Bingo reader

### A package to keep track of multiple bingo cards at a time in order to maximize changes of winning.
All you have to do is type a number in the terminal and if that number is in one of your cards the program will remove
 it from the internal cards. When you have bingo the program will display on what card and in what line of that card you have bingo.
 <br>

### Three programs: <br>
A program to prepare pictures of bingo cards for tesseract number extraction. <br>
Parameters to input:
<br>
	-h, --help            show this help message and exit <br>
  -f FOLDER, --folder FOLDER
                        path to input folder with images to be processed <br>
  -p PREPROCESS, --preprocess PREPROCESS
                        type of preprocessing to be done
                        
<br>

And a program to do the extraction and creation of bingo cards on your machine. <br>
Parameters to input:
<br>
  -h, --help            show this help message and exit <br>
  -f FOLDER, --folder FOLDER
                        path to input image to be OCR'd <br>
  -v VERBOSE, --verbose VERBOSE
                        enable verbose mode to print every bingo card after
                        it's been parsed

<br>
txt_to_card.py a program that parses a txt file containing raw bingo cards.
The format of that file should be: <br>
3 lines of 5 space delimited numbers followed by an empty line for as many lines as you want (see cards.txt). <br>
Use the make_cards function to turn the raw txt file into a list of lists containg the basic cards.
Then use list comprehension to turn all of these basic cards into a BingoCard object. <br>
You can view your cards by calling name_of_card.card <br>
Use the function pop_list to easily pop numbers from your cards if they contain them. <br>
Look at the terminal because it will tell you in which cards you had the number and if you're lucky it will automatically tell you if you have bingo. <br>
When the current line (when one line has been filled/poppep) is done use next_line(number) to set the empty lines required for bingo.