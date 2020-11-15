# Bingo helper

### A program to keep track of multiple bingo cards at a time in order to maximize changes of winning.
The interface is a webapp running on 127.0.0.1:5000. The interface is very simple and straightforward. It is localized in Danish and English.
 <br>

### Installation
```
git clone https://github.com/DinRigtigeFar/Bingo-helper.git
cd Bingo_reader
conda create --name bingo --file requirements.txt
python bingo_app.py
```
Then fire up your browser of choice and point it to [the webapp](127.0.0.1:5000)

### How it works: <br>
bingo_app.py is a fully functioning webbased bingo card GUI created in flask. <br>
It takes raw text in the format of a bingo card (see [cards.txt](https://github.com/DinRigtigeFar/Bingo_reader/blob/master/cards.txt) for the format), parses it and returns a bingo card object.
<br>
The page you're then redirected to is pretty self explanatory: Just press the called number!
<br>
The program will automatically check if you have it in your card(s) and display which row and card contained the called number. When you are one number away from having bingo, the program will tell you what number and which card it is in. Then you know exactly what to listen for. If you're lucky enough to get bingo then that will of course be displayed too.
<br>
When the first line is done simply press the "2" button below the bingo number grid to tell the program that you're now required to have two full lines in order to get bingo (the same goes for 3 lines).
<br>
Happy bingo games!
