"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    Takes a current board and the next player to move
    modifies board input
    """
    player_flag = True
    player_dict = {True: player, False: provided.PLAYERX if (player == provided.PLAYERO) else provided.PLAYERO}
    emptys = board.get_empty_squares()
    while (emptys):
        selected = emptys.pop(random.randrange(len(board.get_empty_squares())))
        board.move(selected[0], selected[1], player_dict[player_flag])
        if (board.check_win()):
            break
        player_flag = not player_flag
    
#    if (not board.check_win()):
#        selected = random.choice(board.get_empty_squares())
#        board.move(selected[0], selected[1], player)
#        mc_trial(board, provided.PLAYERX if (player == provided.PLAYERO) else provided.PLAYERO)
    
def mc_update_scores(scores, board, player):
    """
    Modifies scores board according to the result
    of a simulation
    """
    result = board.check_win()
    if (result):
        if (result != provided.DRAW):
            for row in range(board.get_dim()):
                for col in range(board.get_dim()):
                    scores[row][col] += (MCMATCH if (board.square(row, col) == player) else 0 if (board.square(row, col) == provided.EMPTY) else - MCOTHER) * (1 if (player == result) else -1)

def get_best_move(board, scores):
    """
    Returns the best move as (row, column)
    tuple which has the highest score
    """
    emptys = board.get_empty_squares()
    best = emptys[0]
    ite = 1
    while (ite < len(emptys)):
        if (scores[emptys[ite][0]][emptys[ite][1]] > scores[best[0]][best[1]]):
            best = emptys[ite]
        ite += 1
    return best

def new_scores(dim):
    """
    Generates a new scores board
    """
    scores = []
    row = 0
    while (row < dim):
        temp = []
        col = 0
        while (col < dim):
            temp.append(0)
            col += 1
        scores.append(temp)
        row += 1
    return scores
    
def mc_move(board, player, trials):
    """
    Compute the best move and commit the move
    """
    now = 1
    scores = new_scores(board.get_dim())
    while (now <= trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
        now += 1
    return get_best_move(board, scores)
    
    
# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
