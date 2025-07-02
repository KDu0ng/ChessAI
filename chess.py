import chessai

class ChessBoard:
    def __init__(self):
        self.board = [['rb', 'nb', 'bb', 'qb', 'kb', 'bb', 'nb', 'rb'],
                ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw'],
                ['rw', 'nw', 'bw', 'qw', 'kw', 'bw', 'nw', 'rw']]
        self.ai = chessai.ChessAI()
        self.whiteturn = True
            
    def print_board(self):
        for row in self.board:
            print(['  ' if cell == '' else cell for cell in row])

    def make_move(self):
        if self.whiteturn:
            eval, move, self.board = self.ai.make_move(self.board, True)
        else:
            eval, move, self.board = self.ai.make_move(self.board, False)
        self.whiteturn = not self.whiteturn

                    