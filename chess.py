import copy

def get_starting_board(white=True):
    return [['rb', 'nb', 'bb', 'qb', 'kb', 'bb', 'nb', 'rb'],
            ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw'],
            ['rw', 'nw', 'bw', 'qw', 'kw', 'bw', 'nw', 'rw']]
        
def get_succs(board, white=True):
    succs = []
    player_color = 'w' if white else 'b'

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece and piece[1] == player_color:
                piece_type = piece[0]
                if piece_type == 'p':
                    succs.extend(generate_pawn_moves(board, i, j, white))
                elif piece_type == 'r':
                    succs.extend(generate_rook_moves(board, i, j, white))
                elif piece_type == 'n':
                    succs.extend(generate_knight_moves(board, i, j, white))
                elif piece_type == 'b':
                    succs.extend(generate_bishop_moves(board, i, j, white))
                elif piece_type == 'q':
                    succs.extend(generate_queen_moves(board, i, j, white))
                elif piece_type == 'k':
                    succs.extend(generate_king_moves(board, i, j, white))

    return succs


def generate_pawn_moves(board, row, col, white):
    moves = []
    direction = -1 if white else 1
    start_row = 6 if white else 1
    enemy_color = 'b' if white else 'w'

    # One step forward
    if 0 <= row + direction < 8 and board[row + direction][col] == '':
        new_board = copy.deepcopy(board)
        new_board[row + direction][col] = board[row][col]
        new_board[row][col] = ''
        moves.append([new_board, to_notation('p', False, row + direction, col, row, col)])

        # Two steps forward from starting row
        if row == start_row and board[row + 2 * direction][col] == '':
            new_board = copy.deepcopy(board)
            new_board[row + 2 * direction][col] = board[row][col]
            new_board[row][col] = ''
            moves.append([new_board, to_notation('p', False, row + 2 * direction, col, row, col)])

    # Captures
    for dc in [-1, 1]:  # Diagonal left and right
        new_col = col + dc
        new_row = row + direction
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target and target[1] == enemy_color:
                new_board = copy.deepcopy(board)
                new_board[new_row][new_col] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('p', True, new_row, new_col, row, col)])

    return moves

def generate_rook_moves(board, row, col, white):
    moves = []
    player_color = 'w' if white else 'b'
    enemy_color = 'b' if white else 'w'
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == '':
                new_board = copy.deepcopy(board)
                new_board[r][c] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('R', False, r, c, row, col)])
            elif target[1] == enemy_color:
                new_board = copy.deepcopy(board)
                new_board[r][c] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('R', True, r, c, row, col)])
                break  # Can't move beyond capture
            else:  # Friendly piece blocks movement
                break
            r += dr
            c += dc

    return moves


def generate_knight_moves(board, row, col, white):
    moves = []
    player_color = 'w' if white else 'b'
    enemy_color = 'b' if white else 'w'

    # 8 possible L-shaped moves
    knight_jumps = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2),  (1, 2),
        (2, -1),  (2, 1)
    ]

    for dr, dc in knight_jumps:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == '' or target[1] == enemy_color:
                new_board = copy.deepcopy(board)
                new_board[r][c] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('N', target != '' and target[1] == enemy_color, r, c, row, col)])

    return moves

def generate_bishop_moves(board, row, col, white):
    moves = []
    player_color = 'w' if white else 'b'
    enemy_color = 'b' if white else 'w'

    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == '':
                new_board = copy.deepcopy(board)
                new_board[r][c] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('B', False, r, c, row, col)])
            elif target[1] == enemy_color:
                new_board = copy.deepcopy(board)
                new_board[r][c] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('B', True, r, c, row, col)])
                break
            else:  # Blocked by friendly piece
                break
            r += dr
            c += dc

    return moves

def generate_queen_moves(board, row, col, white):
    moves = []
    player_color = 'w' if white else 'b'
    enemy_color = 'b' if white else 'w'

    # Combine rook + bishop directions
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),    
        (-1, -1), (-1, 1), (1, -1), (1, 1)     
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == '':
                new_board = copy.deepcopy(board)
                new_board[r][c] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('Q', False, r, c, row, col)])
            elif target[1] == enemy_color:
                new_board = copy.deepcopy(board)
                new_board[r][c] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('Q', True, r, c, row, col)])
                break
            else:  # Friendly piece
                break
            r += dr
            c += dc

    return moves

def generate_king_moves(board, row, col, white):
    moves = []
    player_color = 'w' if white else 'b'
    enemy_color = 'b' if white else 'w'

    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # up-left, up, up-right
        (0, -1),           (0, 1),   # left,       right
        (1, -1),  (1, 0),  (1, 1)    # down-left, down, down-right
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == '' or target[1] == enemy_color:
                new_board = copy.deepcopy(board)
                new_board[r][c] = board[row][col]
                new_board[row][col] = ''
                moves.append([new_board, to_notation('K', target != '' and target[1] == enemy_color, r, c, row, col)])

    return moves

def to_notation(piece, capture, row, col=0, src_row=0, src_col=0):
    piece_map = {
        'p': '', 
        'n': 'N',
        'r': 'R',
        'b': 'B',
        'q': 'Q',
        'k': 'K'
    }

    dest_file = chr(ord('a') + col)     # col → file
    dest_rank = str(8 - row)            # row → rank
    
    src_file = chr(ord('a') + src_col)
    src_rank = str(8 - src_row)

    if piece.lower() == 'p' and capture: 
        notation = f"{src_file}x{dest_file}{dest_rank}"
    else:
        symbol = piece_map.get(piece.lower(), '')
        notation = symbol
        if capture:
            notation += 'x'
        notation += f"{dest_file}{dest_rank}"

    return notation

if __name__ == '__main__':
    board = [['rb', 'nb', 'bb', 'qb', 'kb', 'bb', 'nb', 'rb'],
            ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw'],
            ['rw', 'nw', 'bw', 'qw', 'kw', 'bw', 'nw', 'rw']]
    result = get_succs(board, True)
    for b, m in result:
        for r in b:
            print(r)
        print(m)
        print()