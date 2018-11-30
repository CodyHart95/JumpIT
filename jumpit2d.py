#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Input file required.")
    exit()

'''
Extended bottom-up DP solution of the 2D Jump-It game.
   board - 2D list representing playing board
   costs - 2D list to store costs
'''

# Read the game board from a given file
with open(sys.argv[1], 'r') as boardfile:
    num_rows, num_cols = tuple(int(x) for x in boardfile.readline().split())
    board = []
    for line in boardfile:
        board.append([int(v) for v in line.split()])

# Initialize costs to zero
costs = [[0 for i in range(num_cols)] for j in range(num_rows)]


# -------------------------------------------------------------------
# 1. If you are at the exit cell, then you cannot move.
#
# |---|---|---|---|
# |---|---|---|---|
# |---|---|---|---|
# |---|---|---| X |
#
# -------------------------------------------------------------------

# Cost of the exit cell is equal to the board at the exit cell
board_at_exit = board[num_rows - 1][num_cols - 1]
costs[num_rows - 1][num_cols - 1] = board_at_exit

# -------------------------------------------------------------------
# 2. If you are 1 cell to the left of the exit cell, then your only
#    choice is to move right (into the exit cell).
#
# |---|---|---|---|
# |---|---|---|---|
# |---|---|---|---|
# |---|---| X |---|
#
# -------------------------------------------------------------------

# Cost is equal to the board at the the current cell + exit cell
board_left_of_exit = board[num_rows - 1][num_cols - 2]
costs[num_rows - 1][num_cols - 2] = board_left_of_exit + board_at_exit

# -------------------------------------------------------------------
# 3. If you are 1 cell above the exit cell, then your only choice is
#    to move down (into the exit cell).
#
# |---|---|---|---|
# |---|---|---|---|
# |---|---|---| X |
# |---|---|---|---|
#
# -------------------------------------------------------------------

# Cost is equal to the board at the the current cell + exit cell
board_above_exit = board[num_rows-2][num_cols-1] + board[num_rows-1][num_cols-1]
costs[num_rows - 2][num_cols - 1] = board_above_exit

# -------------------------------------------------------------------
# 4. If you are 1 cell above and 1 cell to the left of the exit cell
#    (the diagonal cell), then you have two choice:
#       (a) go down and then right, or
#       (b) go right and then down.
#
# |---|---|---|---|
# |---|---|---|---|
# |---|---| X |---|
# |---|---|---|---|
#
# -------------------------------------------------------------------

# Cost is equal to the exit cell + the minimum of the two choices
board_diagonal_exit = board[num_rows-2][num_cols-2]
down_cost = costs[num_rows - 1][num_cols - 2]
right_cost = costs[num_rows - 2][num_cols - 1]

costs[num_rows - 2][num_cols - 2] = board_diagonal_exit + min(
    down_cost, right_cost)

# -------------------------------------------------------------------
# 5. If you are in the last row (and not at the exit cell or the cell
#    to the left of the exit cell) then you need to consider two
#    choices:
#       (a) go right, or
#       (b) jump right.
#    You should fill in these values starting at the cell 2 to the
#    left of the exit cell, working your way to the first cell in the
#    last row.
#
# |---|---|---|---|
# |---|---|---|---|
# |---|---|---|---|
# | X | X |---|---|
#
# -------------------------------------------------------------------

# Fill in the rest of the last row using the recurrence formula
row = num_rows - 1
for col in range(num_cols - 3, -1, -1):

    # Cheaper to move to adjacent cell or to jump over adjacent cell?
    right_cost = costs[row][col + 1]
    jump_right_cost = costs[row][col + 2]

    costs[row][col] = board[row][col] + min(right_cost, jump_right_cost)

# -------------------------------------------------------------------
# 6. If you are in the last column (and not at the exit cell or the
#    cell above the exit cell) then you need to consider two choices:
#       (a) go down, or
#       (b) jump down.
#    You should fill these values in starting at the cell 2 above the
#    exit cell, working your way to the first cell in the last
#    column.
#
# |---|---|---| X |
# |---|---|---| X |
# |---|---|---|---|
# |---|---|---|---|
#
# -------------------------------------------------------------------

# Fill in the rest of last column using the recurrence formula
col = num_cols - 1
for row in range(num_rows - 3, -1, -1):

    # Cheaper to move to adjacent cell or to jump over adjacent cell?
    down_cost = costs[row+1][col]
    jump_down_cost = costs[row+2][col]

    costs[row][col] = board[row][col] + min(down_cost, jump_down_cost)

# -------------------------------------------------------------------
# 7. If you are in the second-to-last row (and not at the diagonal
#    cell or the last cell in the row), then you need to consider
#    three choices:
#       (a) go down,
#       (b) go right, or
#       (c) jump right.
#
# |---|---|---|---|
# |---|---|---|---|
# | X | X |---|---|
# |---|---|---|---|
#
# -------------------------------------------------------------------

row = num_rows - 2
for col in range(num_cols - 3, -1, -1):

    down_cost = costs[row+1][col]
    right_cost = costs[row][col+1]
    jump_right_cost = costs[row][col+2]

    costs[row][col] = board[row][col] + min(
        down_cost, right_cost, jump_right_cost)

# -------------------------------------------------------------------
# 8. If you are in the second-to-last column (and not at the diagonal
#    cell or the last cell in the column), then you need to consider
#    three choices:
#       (a) go right,
#       (b) go down, or
#       (c) jump down.
#
# |---|---| X |---|
# |---|---| X |---|
# |---|---|---|---|
# |---|---|---|---|
#
# -------------------------------------------------------------------

col = num_cols - 2
for row in range(num_rows - 3, -1, -1):
    down_cost = costs[row+1][col]
    right_cost = costs[row][col+1]
    jump_down_cost = costs[row+2][col]

    costs[row][col] = board[row][col] + min(
        down_cost, right_cost, jump_down_cost)
# -------------------------------------------------------------------
# 9. Finally, for all other cells you must consider four cases:
#       (a) go right,
#       (b) jump right,
#       (c) go down, or
#       (d) jump down.
#
# | X | X |---|---|
# | X | X |---|---|
# |---|---|---|---|
# |---|---|---|---|
#
# -------------------------------------------------------------------

for row in range(num_rows - 3, -1, -1):
    for col in range(num_cols - 3, -1, -1):
        down_cost = costs[row+1][col]
        right_cost = costs[row][col+1]
        jump_down_cost = costs[row+2][col]
        jump_right_cost = costs[row][col+2]

        costs[row][col] = board[row][col] + min(
            down_cost, right_cost, jump_down_cost,jump_right_cost)

# -------------------------------------------------------------------
# Print
# -------------------------------------------------------------------

print('\n'.join(' '.join(f'{val:2}' for val in row) for row in costs))