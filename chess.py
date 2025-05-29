board = []

def get_starting_board(white=True):
    if white:
        board = [['rb', 'nb', 'bb', 'qb', 'kb', 'bb', 'nb', 'rb'],
                ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw'],
                ['rw', 'nw', 'bw', 'qw', 'kw', 'bw', 'nw', 'rw']]
    else:
        board = [['rw', 'nw', 'bw', 'kw', 'qw', 'bw', 'nw', 'rw'],
                ['pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
                ['rb', 'nb', 'bb', 'kb', 'qb', 'bb', 'nb', 'rb']]
    return board
        