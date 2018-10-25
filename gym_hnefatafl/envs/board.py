import numpy as np
from enum import IntEnum


class TileState(IntEnum):
    empty = 0   # neutral
    white = 1   # hostile to black
    black = 2   # hostile to white and king
    king = 3    # unarmed, hostile to no one
    throne = 4  # the empty throne is hostile to any piece
    corner = 5  # target tile for the king, hostile to any piece
    border = 6  # not a reachable tile, but hostile to king


class TileBattleState(IntEnum):
    hostile = -1
    neutral = 0
    allied = 1


# Describes whether a tile is traversable.
# Note that the empty throne is traversable by any piece but can not be occupied by a soldier
# Corners and the empty throne can only be occupied by the king
class TileMoveState(IntEnum):
    traversable = 0    # empty, throne
    blocking = 1  # white, black, border, corner


class HnefataflBoard:

    def __init__(self):
        # empty
        self.board = np.zeros((13, 13))
        self.white_board = np.zeros((13, 13))
        self.black_board = np.zeros((13, 13))
        self.king_board = np.zeros((13, 13))
        self.move_board = np.zeros((13, 13))
        # black (four battalions)
        self.board[1, 4:9] = TileState.black
        self.board[2, 6] = TileState.black
        self.board[11, 4:9] = TileState.black
        self.board[10, 6] = TileState.black
        self.board[4:9, 1] = TileState.black
        self.board[6, 2] = TileState.black
        self.board[4:9, 11] = TileState.black
        self.board[6, 10] = TileState.black
        # white (fortress)
        self.board[5:8, 5:8] = TileState.white
        self.board[4, 6] = TileState.white
        self.board[6, 8] = TileState.white
        self.board[6, 4] = TileState.white
        self.board[8, 6] = TileState.white
        # king
        self.board[6, 6] = TileState.king
        # border
        self.board[0, :] = TileState.border
        self.board[12, :] = TileState.border
        self.board[:, 0] = TileState.border
        self.board[:, 12] = TileState.border
        # corner
        self.board[1, 1] = TileState.corner
        self.board[1, 11] = TileState.corner
        self.board[11, 11] = TileState.corner
        self.board[11, 1] = TileState.corner

        self.update_board()

    def update_board(self):

        # battle state for white soldiers (corners, empty throne and black soldiers are hostile)
        # white soldiers are allied and the king is neutral, since he is unarmed
        self.black_board = np.zeros((13, 13))
        hostile_mask = (self.board == TileState.black) | (self.board == TileState.corner) | (self.board == TileState.throne)
        np.place(self.white_board, self.board == TileState.white, TileBattleState.allied)
        np.place(self.white_board, hostile_mask, TileBattleState.hostile)

        # battle state for black soldiers (corners, empty throne and white soldiers are hostile)
        # black soldiers are allied and the king is neutral, since he is unarmed
        self.black_board = np.zeros((13, 13))
        hostile_mask = (self.board == TileState.white) | (self.board == TileState.corner) | (self.board == TileState.throne)
        np.place(self.black_board, self.board == TileState.black, TileBattleState.allied)
        np.place(self.black_board, hostile_mask, TileBattleState.hostile)

        # battle state for king (borders, corners, empty throne and black soldiers are hostile)
        # anything else is neutral
        self.king_board = np.zeros((13, 13))
        hostile_mask = (self.board == TileState.border) | (self.board == TileState.corner) \
                       | (self.board == TileState.throne) | (self.board == TileState.black)
        np.place(self.king_board, hostile_mask, TileBattleState.hostile)

        # moveable state for any player (borders, corners, and soldiers are blocking)
        # anything else is traversable
        self.move_board = np.zeros((13, 13))
        blocking_mask = (self.board == TileState.border) | (self.board == TileState.corner) \
                       | (self.board == TileState.white) | (self.board == TileState.black)
        np.place(self.move_board, blocking_mask, TileMoveState.blocking)

    def __str__(self):
        return "Gameboard: \n" + str(self.board) + \
               "\nWhiteboard: \n" + str(self.white_board) + \
               "\nBlackboard: \n" + str(self.black_board) + \
               "\nKingboard: \n" + str(self.king_board) + \
               "\nMoveboard: \n" + str(self.move_board)

