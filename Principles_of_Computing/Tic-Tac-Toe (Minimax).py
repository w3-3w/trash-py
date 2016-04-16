"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    desired_move = (-1, -1)
    winner = board.check_win()
    if winner:
        #print board
        #print (SCORES[winner], desired_move), SCORES[player]
        return (SCORES[winner], desired_move)
    else:
        emptys = board.get_empty_squares()
        maximum = (-900, (-1, -1))
        for place in emptys:
            new_board = board.clone()
            new_board.move(place[0], place[1], player)
            now = mm_move(new_board, provided.switch_player(player))
            if (SCORES[player] * now[0] > maximum[0]):
                maximum = (SCORES[player] * now[0], place)
        #print board
        #print (maximum[0] * SCORES[player], maximum[1]), SCORES[player]
        return (maximum[0] * SCORES[player], maximum[1])

#b1 = provided.TTTBoard(3)
#b1.move(0, 0, provided.PLAYERO)
#b1.move(0, 1, provided.PLAYERX)
#b1.move(1, 0, provided.PLAYERO)
#b1.move(1, 1, provided.PLAYERX)
#b1.move(2, 1, provided.PLAYERO)
#b1.move(2, 2, provided.PLAYERX)
#mm_move(b1, provided.PLAYERX)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
