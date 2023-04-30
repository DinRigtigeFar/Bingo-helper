from os import environ

import txt_to_card
from flask import (Flask, make_response, redirect, render_template, request,
                   send_file, session, url_for)
from flask_babel import Babel, gettext

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")
babel = Babel(app)

# Make localization available
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['da', 'en'])
    # return 'da'


@app.route('/', methods=['POST', 'GET'])
def index():
    session.clear()
    session['drawn_numbers'] = []
    return render_template('index.html')


@app.route('/grid/', methods=['POST'])
def grid():
    """
    Parse the raw bingo cards and redirect to bingo number grid
    """
    if request.method == 'POST':
        raw_cards = request.form['raw_cards']
        if not raw_cards:
            return render_template('index.html', message='You should input some cards!')
        
        my_cards = txt_to_card.BigBingoHolder.make_cards(raw_cards)
        
        with open('og_cards.txt', 'w') as w:
            w.writelines(raw_cards)
        
        session['my_cards'] = my_cards.get_card()
        session['current_line'] = my_cards.lines
        
        return render_template('number_grid.html', message=session.get('my_cards'), sesh=session.get('current_line'), drawn_numbers=session.get('drawn_numbers'))
    
@app.route('/redo/<redo>', methods=['GET'])   
def redo(redo: bool = False):
    if request.method == "GET" and bool(redo) == True:
        my_cards = txt_to_card.BigBingoHolder.make_cards("og_cards.txt")
        
        session['my_cards'] = my_cards.get_card()
        session['current_line'] = my_cards.lines
        session['drawn_numbers'] = []
        
        return render_template('number_grid.html', message=session.get('my_cards'), sesh=session.get('current_line'), drawn_numbers=session.get('drawn_numbers'))

@app.route('/undo/<int:number>', methods=['GET'])   
def undo(number):
    if request.method == "GET":
        my_cards = txt_to_card.BigBingoHolder.make_cards("og_cards.txt", session.get("current_line"))
        drawn_numbers = session.get('drawn_numbers')
        drawn_numbers.pop(drawn_numbers.index(number))
        session["drawn_numbers"] = drawn_numbers
        my_cards.pop_many(drawn_numbers)
        session['my_cards'] = my_cards.get_card()
        
        return render_template('number_grid.html', message=[f"Undid drawing of number {number}"], sesh=session.get('current_line'), drawn_numbers=drawn_numbers)

@app.route('/grid/<int:number>', methods=['GET'])
def btn_click(number):
    """
    Do card.pop_number(number) on button click
    """
    if number not in session.get('drawn_numbers'):
        session['drawn_numbers'].insert(0, number)
    current_line = session.get('current_line')
    
    my_cards = txt_to_card.BigBingoHolder.make_from_dict(session.get('my_cards'), current_line)
    
    message, missing = my_cards.pop_list(number)
    
    session['my_cards'] = my_cards.get_card()
    return render_template('number_grid.html', message=message, missing=missing, sesh=current_line, drawn_numbers=session.get('drawn_numbers'), check_close=my_cards.close_to_bingo(combine=True))


@app.route('/newline/<int:number>', methods=['GET'])
def change_line(number):
    """
    Change the lines on button click
    """
    session['current_line'] = number
    line = gettext("Current line changed to")
    my_cards = txt_to_card.BigBingoHolder.make_from_dict(session.get('my_cards'), number)
    
    return render_template('number_grid.html', current_line=f"{line} {number}", sesh=number, drawn_numbers=session.get('drawn_numbers'), check_close=my_cards.close_to_bingo(combine=True))

if __name__ == '__main__':
    app.run()