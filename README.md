# Bingo helper

### A program to keep track of multiple bingo cards at a time in order to maximize changes of winning.
All you have to do is type a number in the terminal and if that number is in one of your cards the program will remove
 it from the internal cards. When you have bingo the program will display on what card and in what line of that card you have bingo. It has been localized in Danish and English.
 <br>

### Installation
  git clone https://github.com/DinRigtigeFar/Bingo_reader.git
  cd Bingo_reader
  python3 -m venv bingo_helper
  pip install -r requirements.txt
  python bingo_app.py
Then fire up your browser of choice and point it to [localhost:5000](localhost:5000)

### How it works: <br>
bingo_app.py a fully function webbased bingo card GUI created in flask. <br>
It takes raw text in the format of a bingo card (see [cards.txt](https://github.com/DinRigtigeFar/Bingo_reader/blob/master/cards.txt) for the format), parses it and returns a bingo card object.
<br>
The page you're then redirected to is pretty self explanatory: Just press the called number!
<br>
The program will automatically check if you have it in your card(s) and display which row and card contained the called number. If you're lucky enough to get bingo then that will of course be displayed too.
<br>
When the first line is full simply press the "2" button below the bingo number grid to tell the program that you're now required to have two full lines in order to get bingo.
<br>
Happy bingo games, and may the odds be ever in your favor.
