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
    # Initialize an empty list to store drawn numbers
    session['drawn_numbers'] = []
    return render_template('index.html')


@app.route('/grid/', methods=['GET', 'POST'])
def grid():
    """
    Parse the raw bingo cards and redirect to bingo number grid
    """

    if request.method == 'POST':
        # This is generated from the index.html form
        raw_cards = request.form['raw_cards']
        # Parse the raw string into bingo cards
        my_pre_cards = txt_to_card.make_cards_from_list(raw_cards)
        my_cards = [txt_to_card.BingoCard(i) for i in my_pre_cards]
        # Since we need the cards in the other views we create a session
        session['my_cards'] = [i.card for i in my_cards]
        # Also initialize a current_line session to be used for assembly later
        session['current_line'] = 1
    return render_template('number_grid.html', message=session.get('my_cards'))


@app.route('/grid/<int:number>', methods=['GET'])
def btn_click(number):
    """
    Do card.pop_number(number) on button click
    """
    # Have a list of already drawn numbers to keep track
    session['drawn_numbers'].insert(0, number)
    # Make the drawn numbers sorted insted? Uncomment this
    #session['drawn_numbers'].sort()
    current_line = session.get('current_line')
    # Since sessions store objects as json we have to 'assemble' the BingoCard objects again
    # We are using BingoCardDict since we create the object from a dict and not a list of lists
    my_cards = [txt_to_card.BingoCardDict(
        i, current_line) for i in session.get('my_cards')]
    # Store the popped numbers in a message. Only numbers removed from our cards are stored here. Also if missing one for bingo
    message, missing = txt_to_card.pop_list(number, my_cards)
    # Now we 'disassemble' the BingoCardDict object into a dict and override the session with the updated cards
    session['my_cards'] = [i.card for i in my_cards]

    return render_template('number_grid.html', message=message, missing=missing, sesh=current_line, drawn_numbers=session.get('drawn_numbers'))


@app.route('/newline/<int:number>', methods=['GET'])
def change_line(number):
    """
    Change the lines on button click
    """

    # We use the number from the click to set the current_line
    session['current_line'] = number

    line = gettext("Current line changed to")

    # Render the number_grid template, but the message is different.
    # This way when you click a number the btn_click view is called again.
    return render_template('number_grid.html', current_line=f"{line} {number}", sesh=number, drawn_numbers=session.get('drawn_numbers'))


if __name__ == '__main__':
    app.run()
