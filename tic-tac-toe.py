"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 10.0 # Score for squares played by the current player
SCORE_OTHER = 10.0   # Score for squares played by the other player

# Add your functions here.

def create_board_lists(board):
    """
    Takes a board and converts the rows, columns and diagonals into lists 
    where each element is EMPTY, PLAYERO or PLAYERX, returns a list of lists
    """
    
    board_lists = []
    
    for row in range(board.get_dim()):
        current_row = []
        for col in range(board.get_dim()):
            current_row.append(board.square(row, col))
        board_lists.append(current_row)
        
    for col in range(board.get_dim()):
        current_col = []
        for row in range(board.get_dim()):
            current_col.append(board.square(row, col))
        board_lists.append(current_col)
        
    diag1 = []
    for diag_square in range(board.get_dim()):
        diag1.append(board.square(diag_square, diag_square))
    board_lists.append(diag1)
    
    diag2 =[]
    for diag_square in range(board.get_dim()):
        diag2.append(board.square(diag_square, board.get_dim() - 1 - diag_square))
    board_lists.append(diag2)
    
    return board_lists
                     
def game_over(board):
    """
    checks whether game is over
    """
    
    draw = True
    
    for lst in create_board_lists(board):
        if lst[0] != provided.EMPTY:
            is_same = True
            for square in range(len(lst)):
                if lst[square] != lst[0]:
                    is_same = False
            if is_same:
                return True
            
    for lst in create_board_lists(board):
        for square in lst:
            if square == provided.EMPTY:
                draw = False 
                
    if draw:
        return True
         
    return False
    
def mc_trial(board, player):
    """
    Plays a game and modifies trial board accordingly
    """
    
    while not game_over(board):
        empty_squares = board.get_empty_squares()
        selected_square = random.choice(empty_squares)
        board.move(selected_square[0], selected_square[1], player)
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    """
    updates score grid after a completed game
    """
    
    if board.check_win() == player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] -= SCORE_OTHER
                           
    if board.check_win() == provided.switch_player(player):
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] -= SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += SCORE_OTHER      
    
def get_best_move(board, scores):
    """
    selects best move given a board and set of scores
    """
    
    highest_score = max([scores[square[0]][square[1]] for square in board.get_empty_squares()])
    
    possible_squares = [square for square in board.get_empty_squares() if scores[square[0]][square[1]] == highest_score]
    
    return random.choice(possible_squares)

def mc_move(board, player, trials):
    
    """
    makes a move
    """
    
    scores = [[0] * board.get_dim() for dummy_row in range(board.get_dim())] 
    
    for dummy_trial in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
