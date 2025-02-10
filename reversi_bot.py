import numpy as np
import random as rand
import reversi

class ReversiBot:
    def __init__(self, move_num):
        self.move_num = move_num # aka player
        self.opponent = 3 - move_num
        self.max_depth = 3

    def make_move(self, state):
        '''
        This is the only function that needs to be implemented for the lab!
        The bot should take a game state and return a move.

        The parameter "state" is of type ReversiGameState and has two useful
        member variables. The first is "board", which is an 8x8 numpy array
        of 0s, 1s, and 2s. If a spot has a 0 that means it is unoccupied. If
        there is a 1 that means the spot has one of player 1's stones. If
        there is a 2 on the spot that means that spot has one of player 2's
        stones. The other useful member variable is "turn", which is 1 if it's
        player 1's turn and 2 if it's player 2's turn.

        ReversiGameState objects have a nice method called get_valid_moves.
        When you invoke it on a ReversiGameState object a list of valid
        moves for that state is returned in the form of a list of tuples.

        Move should be a tuple (row, col) of the move you want the bot to make.
        '''
        valid_moves = state.get_valid_moves()
        # move = rand.choice(valid_moves) # Moves randomly
        if not valid_moves: return None

        best_move = None
        best_value = np.inf
        alpha = -np.inf
        beta = np.inf

        for move in valid_moves:
            # simulate move and get value
            new_state = self.simulate_move(state, move, self.move_num)
            move_value = self.minmax(new_state, self.max_depth, False, alpha, beta)

            # find best move
            if move_value > best_move:
                best_value = move_value
                best_move = move
            
            alpha = max(alpha, best_value)
        return best_move
    
    def minmax(self, state, depth, is_max_player, alpha, beta):
        valid_moves = state.get_valid_moves()

        if is_max_player:
            max_eval = -np.inf
            for move in valid_moves:
                new_state = self.simulate_move(state, move, self.move_num)
                eval_value = self.minmax(new_state, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break  # alpha-beta pruning
            return max_eval
        else:
            min_eval = np.inf
            for move in valid_moves:
                new_state = self.simulate_move(state, move, self.opponent)
                eval_value = self.minmax(new_state, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break  # alpha-beta pruning
            return min_eval
        
    def simulate_move(self, state, move, player):
        new_board = np.copy(state.board)
        new_board[move] = player  
        
        # flip opponent pieces in all directions
        for xdir in range(-1, 2):
            for ydir in range(-1, 2):
                if xdir == ydir == 0:
                    continue
                if state.capture_will_occur(move[0] + ydir, move[1] + xdir, xdir, ydir):
                    row, col = move
                    while True:
                        row += ydir
                        col += xdir
                        if state.board[row, col] == player:
                            break
                        new_board[row, col] = player

        return reversi.ReversiGameState(new_board, 3 - player)  # switch turns

    def evaluate(self, state):
        board = state.board
        score = 0

        # prioritize corners
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for x, y in corners:
            if board[x, y] == self.move_num:
                score += 50  # high weight for corners
            elif board[x, y] == self.opponent:
                score -= 50

        # prioritize edges
        edges = [(0, y) for y in range(8)] + [(7, y) for y in range(8)] + \
                [(x, 0) for x in range(8)] + [(x, 7) for x in range(8)]
        for x, y in edges:
            if board[x, y] == self.move_num:
                score += 10
            elif board[x, y] == self.opponent:
                score -= 10

        # Count mobility (number of moves available)
        my_moves = len(state.get_valid_moves())
        opponent_moves = len(self.simulate_move(state, (0, 0), self.opponent).get_valid_moves())
        score += (my_moves - opponent_moves) * 5

        # Count number of pieces
        my_pieces = np.count_nonzero(board == self.move_num)
        opponent_pieces = np.count_nonzero(board == self.opponent)
        score += (my_pieces - opponent_pieces)

        return score
