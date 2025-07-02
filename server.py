from flask import Flask, render_template, jsonify
import chess

app = Flask(__name__)
chessboard = chess.ChessBoard()

@app.route('/')
def show_board():
    return render_template('index.html', board=chessboard.board)

@app.route('/update_board', methods=['POST'])
def update_board():
    chessboard.make_move() 
    return jsonify(board=chessboard.board) 

if __name__ == '__main__':
    app.run(debug=True)