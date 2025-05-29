import chess
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    board = chess.get_starting_board()
    return render_template('index.html', board=board)

if __name__ == '__main__':
    app.run(debug=True)