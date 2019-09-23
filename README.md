# Bingo reader

### A package to keep track of multiple bingo cards at a time in order to maximize changes of winning.
All you have to do is type a number in the terminal and if that number is in one of your cards the program will remove
 it from the internal cards. When you have bingo the program will display on what card and in what line of that card you have bingo.
 <br>

### Two programs: <br>
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
