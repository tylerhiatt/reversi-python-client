import numpy as np
import random as rand
import reversi

class ReversiBot:
    def __init__(self, move_num):
        self.move_num = move_num

    def get_state_after_move(self, state, move, bot_made_move):
        opponent_num = 1 if self.move_num == 2 else 2
        new_board = np.array(state.board, copy=True)
        new_board[move[0], move[1]] = self.move_num if bot_made_move else opponent_num

        return reversi.ReversiGameState(new_board, 2 - bot_made_move)

    def make_move(self, state):
        '''
        This is the only function that needs to be implemented for the lab!
        The bot should take a game state and return a move. There are lots of
        things that make this easy. A game state has two attributes: board
        and turn. Turn is 1 if it's player one's turn. Turn is 2 if it's player
        2's turn. You can know the turn of your bot by using its self.move_num
        attribute. The board attribute is an 8x8 numpy array with zeros where
        there are no pieces, 1's where player 1's pieces are, and 2's where
        player 2's pieces are. To get a list of all valid moves for the state,
        simply do state.get_valid_moves(), which returns a list of tuples
        representing valid moves. To see what the state of the game would be
        after taking a particular move in the current state, use the
        self.get_state_after_move() method. Pass in the current state, the move
        tuple you want to consider, and a boolean telling whether or not the bot
        made the move.
        '''
        valid_moves = state.get_valid_moves()

        move = rand.choice(valid_moves) # Moves randomly...for now
        return move
