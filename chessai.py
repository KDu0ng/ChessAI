import copy

class ChessAI:    
    def make_move(self, state, white=True):
        if white:
            eval, move, succ = self.max_value(state, 4, float('-inf'), float('inf')) 
        else:
            eval, move, succ = self.min_value(state, 4, float('-inf'), float('inf')) 

        if move is None:
            if eval == float('-inf'):
                move = 'black win'
            elif eval == float('inf'):
                move = 'white win'
            else:
                raise ValueError('No move found')
        
        return eval, move, succ

    def max_value(self, state, depth, alpha, beta):  # White's turn
        if depth == 0:
            return self.evaluate(state), None, None

        succs = self.get_succs(state, True)
        best_move = None
        best_succ = None
        max_eval = float('-inf')

        if not succs: 
            if self.is_in_check(state, True):  # White in check: checkmate
                return float('-inf'), None, None
            else:  # Stalemate
                return 0, '$', None

        for s, m in succs:
            eval, _, _ = self.min_value(s, depth - 1, alpha, beta)

            if eval > max_eval:
                max_eval = eval
                best_move = m
                best_succ = s

            alpha = max(alpha, max_eval) 
            if beta <= alpha:
                break

        return max_eval, best_move, best_succ


    def min_value(self, state, depth, alpha, beta):  # Black's turn
        if depth == 0:
            return self.evaluate(state), None, None

        succs = self.get_succs(state, False)
        best_move = None
        best_succ = None
        min_eval = float('inf')

        if not succs: 
            if self.is_in_check(state, False):  # Black in check: checkmate
                return float('inf'), None, None
            else:  # Stalemate
                return 0, '$', None

        for s, m in succs:
            eval, _, _ = self.max_value(s, depth - 1, alpha, beta)

            if eval < min_eval:
                min_eval = eval
                best_move = m
                best_succ = s

            beta = min(beta, min_eval) 
            if beta <= alpha:
                break

        return min_eval, best_move, best_succ
    
    def evaluate(self, board):
        piece_values = {
            'p': 1,
            'n': 3,
            'b': 3,
            'r': 5,
            'q': 9,
            'k': 0
        }

        score = 0
        for row in board:
            for piece in row:
                if piece == '':
                    continue
                value = piece_values.get(piece[0], 0)
                if piece[1] == 'w':
                    score += value
                elif piece[1] == 'b':
                    score -= value

        return score
    
    def get_succs(self, board, white):
        succs = []
        player_color = 'w' if white else 'b'

        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece and piece[1] == player_color:
                    piece_type = piece[0]
                    if piece_type == 'p':
                        succs.extend(self.generate_pawn_moves(board, i, j, white))
                    elif piece_type == 'r':
                        succs.extend(self.generate_rook_moves(board, i, j, white))
                    elif piece_type == 'n':
                        succs.extend(self.generate_knight_moves(board, i, j, white))
                    elif piece_type == 'b':
                        succs.extend(self.generate_bishop_moves(board, i, j, white))
                    elif piece_type == 'q':
                        succs.extend(self.generate_queen_moves(board, i, j, white))
                    elif piece_type == 'k':
                        succs.extend(self.generate_king_moves(board, i, j, white))

        succs = self.filter_checks(succs, white)
        return succs


    def generate_pawn_moves(self, board, row, col, white):
        moves = []
        direction = -1 if white else 1
        start_row = 6 if white else 1
        enemy_color = 'b' if white else 'w'

        # One step forward
        if 0 <= row + direction < 8 and board[row + direction][col] == '':
            new_board = copy.deepcopy(board)
            new_board[row + direction][col] = board[row][col]
            new_board[row][col] = ''
            moves.append((new_board, self.to_notation('p', False, row + direction, col, row, col)))

            # Two steps forward from starting row
            if row == start_row and board[row + 2 * direction][col] == '':
                new_board = copy.deepcopy(board)
                new_board[row + 2 * direction][col] = board[row][col]
                new_board[row][col] = ''
                moves.append((new_board, self.to_notation('p', False, row + 2 * direction, col, row, col)))

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
                    moves.append((new_board, self.to_notation('p', True, new_row, new_col, row, col)))

        return moves

    def generate_rook_moves(self, board, row, col, white):
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
                    moves.append((new_board, self.to_notation('R', False, r, c, row, col)))
                elif target[1] == enemy_color:
                    new_board = copy.deepcopy(board)
                    new_board[r][c] = board[row][col]
                    new_board[row][col] = ''
                    moves.append((new_board, self.to_notation('R', True, r, c, row, col)))
                    break  # Can't move beyond capture
                else:  # Friendly piece blocks movement
                    break
                r += dr
                c += dc

        return moves


    def generate_knight_moves(self, board, row, col, white):
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
                    moves.append((new_board, self.to_notation('N', target != '' and target[1] == enemy_color, r, c, row, col)))

        return moves

    def generate_bishop_moves(self, board, row, col, white):
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
                    moves.append((new_board, self.to_notation('B', False, r, c, row, col)))
                elif target[1] == enemy_color:
                    new_board = copy.deepcopy(board)
                    new_board[r][c] = board[row][col]
                    new_board[row][col] = ''
                    moves.append((new_board, self.to_notation('B', True, r, c, row, col)))
                    break
                else:  # Blocked by friendly piece
                    break
                r += dr
                c += dc

        return moves

    def generate_queen_moves(self, board, row, col, white):
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
                    moves.append((new_board, self.to_notation('Q', False, r, c, row, col)))
                elif target[1] == enemy_color:
                    new_board = copy.deepcopy(board)
                    new_board[r][c] = board[row][col]
                    new_board[row][col] = ''
                    moves.append((new_board, self.to_notation('Q', True, r, c, row, col)))
                    break
                else:  # Friendly piece
                    break
                r += dr
                c += dc

        return moves

    def generate_king_moves(self, board, row, col, white):
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
                    moves.append((new_board, self.to_notation('K', target != '' and target[1] == enemy_color, r, c, row, col)))

        return moves

    def to_notation(self, piece, capture, row, col=0, src_row=0, src_col=0):
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

    def filter_checks(self, succs, white):
        legal_moves = []

        for board, move in succs:
            # If own king is in check, discard move
            if self.is_in_check(board, white):
                continue

            # If opponent's king is now in check, add '+' to notation
            if self.is_in_check(board, not white):
                move += '+'

            legal_moves.append((board, move))

        return legal_moves

    def is_in_check(self, board, white):
        # Find the king position
        king_symbol = 'kw' if white else 'kb'
        king_pos = None
        for i in range(8):
            for j in range(8):
                if board[i][j] == king_symbol:
                    king_pos = (i, j)
                    break
            if king_pos:
                break
        if not king_pos:
            return False  # invalid board — king not found

        xk, yk = king_pos

        directions = {
            'rook': [(-1, 0), (1, 0), (0, -1), (0, 1)],
            'bishop': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            'knight': [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
        }

        # Pieces of the opposing color are enemies
        enemy = lambda p: p.endswith('b') if white else p.endswith('w')

        # Knight checks
        for dx, dy in directions['knight']:
            nx, ny = xk + dx, yk + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board[nx][ny]
                if piece == ('n' + ('b' if white else 'w')):
                    return True

        # Rook / Queen checks
        for dx, dy in directions['rook']:
            for dist in range(1, 8):
                nx, ny = xk + dx * dist, yk + dy * dist
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                piece = board[nx][ny]
                if piece == "":
                    continue
                if enemy(piece) and piece[0] in ('r', 'q'):
                    return True
                break

        # Bishop / Queen checks
        for dx, dy in directions['bishop']:
            for dist in range(1, 8):
                nx, ny = xk + dx * dist, yk + dy * dist
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                piece = board[nx][ny]
                if piece == "":
                    continue
                if enemy(piece) and piece[0] in ('b', 'q'):
                    return True
                break

        # Pawn checks
        pawn_dir = -1 if white else 1
        for dx in [-1, 1]:
            px, py = xk + pawn_dir, yk + dx
            if 0 <= px < 8 and 0 <= py < 8:
                if board[px][py] == ('p' + ('b' if white else 'w')):
                    return True

        return False