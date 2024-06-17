"""
Tic Tac Toe Player
"""

import math,copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    count = 0
    
    for row in board:
        for cell in row:
            if cell!=EMPTY:
                count += 1
    if count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board2 = copy.deepcopy(board)
    
    (i,j) = action

    if i<0 or i>2 or j<0 or j>2:
        raise OutOfBoundsMove

    if board2[i][j] != EMPTY:
        raise TakenMove
    else:
        board2[i][j] = player(board2)

    return board2


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check rows
    for row in board:
        if row == [X,X,X]:
            return X
        if row == [O,O,O]:
            return O

    #check columns
    for i in range(3):
        if [board[0][i],board[1][i],board[2][i]] == [X,X,X]:
            return X
        if [board[0][i],board[1][i],board[2][i]] == [O,O,O]:
            return O
        
    #check diagonals
    if [board[0][0],board[1][1],board[2][2]] == [X,X,X]:
        return X
    if [board[0][0],board[1][1],board[2][2]] == [O,O,O]:
        return O
    if [board[0][2],board[1][1],board[2][0]] == [X,X,X]:
        return X
    if [board[0][2],board[1][1],board[2][0]] == [O,O,O]:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    W = winner(board)
    if W == X:
        return 1
    elif W == O:
        return -1
    else:
        return 0


def max_value(board):
    v = -2
    if terminal(board):
        return utility(board)

    for a in actions(board):
        
        v = max(v,min_value(result(board,a)))

    return v

def min_value(board):
    v = 2
    if terminal(board):
        return utility(board)

    for a in actions(board):
        v = min(v,max_value(result(board,a)))

    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    P = player(board)
    

    plus_moves = []
    neutral_moves = []
    minus_moves = []

    if P == X:
        for a in actions(board):
            a_val = min_value(result(board,a))
            if a_val == 1:
                plus_moves += [a]
            elif a_val == 0:
                neutral_moves += [a]
            else:
                minus_moves += [a]

    if P == O:
        for a in actions(board):
            a_val = max_value(result(board,a))
            if a_val == -1:
                plus_moves += [a]
            elif a_val == 0:
                neutral_moves += [a]
            else:
                minus_moves += [a]

    
    if plus_moves != []:
        return plus_moves[0]
    if neutral_moves != []:
        return neutral_moves[0]
    return minus_moves[0]


        
