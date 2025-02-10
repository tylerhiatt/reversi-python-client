import time
import numpy as np
import reversi
from reversi_bot import ReversiBot, MonteCarloReversiBot 

def test_algorithms(num_games=5):
    minimax_wins, monte_wins = 0, 0
    minimax_depths, monte_depths = [], []
    minimax_times, monte_times = [], []
    minimax_scores, monte_scores = [], []

    for i in range(num_games):
        print(f"\n[DEBUG] Running Game {i+1}/{num_games}")
        
        # Reset game state
        state = create_initial_game_state()

        # Choose who goes first
        if i % 2 == 0:
            bot1, bot2 = ReversiBot(1), MonteCarloReversiBot(2)
        else:
            bot1, bot2 = MonteCarloReversiBot(1), ReversiBot(2)

        start_time = time.time()
        while True:
            if state.turn == bot1.move_num:
                move_start = time.time()
                move = bot1.make_move(state)
                move_end = time.time()
                minimax_times.append(move_end - move_start)
            else:
                move_start = time.time()
                move = bot2.make_move(state)
                move_end = time.time()
                monte_times.append(move_end - move_start)

            if move is None:
                break  # Game over

            state = reversi.ReversiGameState(np.copy(state.board), 3 - state.turn)  

        end_time = time.time()

        # Determine winner
        winner = state.determine_winner()
        if winner == bot1.move_num:
            minimax_wins += 1
        else:
            monte_wins += 1

        # Store metrics
        minimax_depths.append(bot1.max_depth)
        monte_depths.append(bot2.max_depth)
        minimax_scores.append(state.get_final_score(bot1.move_num))
        monte_scores.append(state.get_final_score(bot2.move_num))

    # Print Results
    print("\n==== Final Results ====")
    print(f"Minimax Wins: {minimax_wins}/{num_games} ({(minimax_wins/num_games)*100:.2f}%)")
    print(f"Monte Carlo Wins: {monte_wins}/{num_games} ({(monte_wins/num_games)*100:.2f}%)")
    print(f"Average Minimax Search Depth: {sum(minimax_depths)/len(minimax_depths):.2f}")
    print(f"Average Monte Carlo Simulations: {sum(monte_depths)/len(monte_depths):.2f}")
    print(f"Avg Decision Time - Minimax: {sum(minimax_times)/len(minimax_times):.2f}s")
    print(f"Avg Decision Time - Monte Carlo: {sum(monte_times)/len(monte_times):.2f}s")
    print(f"Avg Score Difference - Minimax: {sum(minimax_scores)/len(minimax_scores):.2f}")
    print(f"Avg Score Difference - Monte Carlo: {sum(monte_scores)/len(monte_scores):.2f}")



def initial_board():
    board = np.zeros((8, 8), dtype=int)  # 8x8 board filled with 0s
    board[3, 3], board[4, 4] = 2, 2  # White pieces
    board[3, 4], board[4, 3] = 1, 1  # Black pieces
    return board

def create_initial_game_state():
    return reversi.ReversiGameState(initial_board(), turn=1)


if __name__ == '__main__':
    test_algorithms()