# -*- coding: utf-8 -*-
import numpy as np
import time
from scipy.signal import convolve2d
import instances


def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You may assume there will always be a solution.
    """

    temp_board = board
    for i in range(len(temp_board)):
        for j in range(len(temp_board[0])):
            if temp_board[i, j] == 1:
                temp_board[i, j] = 0
            else:
                temp_board[i, j] = 1
    extended_board = np.pad(temp_board, ((2, 2), (2, 2)), 'constant', constant_values=(1, 1))
    global solveALL
    solveALL = False

    for idx in range(len(pents), 0, -1):
        tile_rec(pents, extended_board, idx)
        if solveALL:
            break

    new_b = extended_board[2:-2, 2:-2]
    print(new_b)
    return new_b


def aera_expand(b, i, j, c):
    if b[i, j] != 0:
        return c

    c += 1
    # visited
    b[i, j] = -1
    c = aera_expand(b, i + 1, j, c)
    c = aera_expand(b, i, j + 1, c)
    c = aera_expand(b, i - 1, j, c)
    c = aera_expand(b, i, j - 1, c)
    return c


def valid_place(b):
    """
    check if the the board rest places is the multiple of 5
    Return False when the empty aera is not allowed
    """
    for i in range(2, b.shape[0] - 2):
        for j in range(2, b.shape[1] - 2):
            c = aera_expand(b, i, j, c=0)
            if c % 5 != 0:
                b[np.where(b == -1)] = 0
                return False
    b[np.where(b == -1)] = 0
    return True


def tile_rec(pet, board, c):

    global solveALL
    if solveALL:
        print("SOLVE ALL")
        print()
        return

    # the core part inside, left the surrounding 2 levels
    bv = board[2:-2, 2:-2]
    flag = 1
    for i in range(len(bv)):
        for j in range(len(bv[0])):
            if bv[i, j] == 0:
                flag = 0
                break
        if flag == 0:
            break
    solveALL = flag

    if solveALL:
        print("SOLVE ALL")
        print()
        print(board[2:-2, 2:-2])
        return

    piece = pet[len(pet) - c]
    piece_idx = len(pet) + 1 - c

    # determine the mirror kind first
    for i in range(piece[1]):
        # then is the rotation
        for j in range(piece[2]):
            # fix the convolution in the whole board,
            # while the kernel should be reversed
            C = convolve2d(bv, piece[0][::-1, ::-1], 'same', fillvalue=1)
            empty_points = np.where(C == 0)

            if empty_points[0].size == 0:
                # recover the rotation
                piece[0] = np.rot90(piece[0])
                continue  # for next

            hw_i = (piece[0].shape[0] - 1) // 2
            hw_j = (piece[0].shape[1] - 1) // 2
            flag = piece[0].astype(bool)

            for k in range(empty_points[0].size):
                ioff, joff = empty_points[0][k] + 2, empty_points[1][k] + 2

                # now place it on the board
                board[ioff - hw_i:ioff + hw_i + 1, joff - hw_j:joff + hw_j + 1][flag] = piece_idx

                if valid_place(board):
                    for pos_c in range(len(pet), 0, -1):
                        if solveALL:
                            return
                        tile_rec(pet, board, pos_c)

                # now it means that it is not valid
                board[ioff - hw_i:ioff + hw_i + 1, joff - hw_j:joff + hw_j + 1][flag] = 0

            # end of cycle one, then should consider the rotation
            piece[0] = np.rot90(piece[0])
        # end of cycle two, then should consider the flip
        piece[0] = np.flip(piece[0], axis=1)
    return

test_board = instances.board_6x10
pent = instances.pentominos

solve(test_board, pent)