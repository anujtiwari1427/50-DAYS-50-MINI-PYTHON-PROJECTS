import numpy as np
import random
from time import sleep
#  first creates an empty board
def my_create_board():
   return(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
# Check for empty places on board
def my_possibilities(board):
   l = []
   for i in range(len(board)):
      for j in range(len(board)):
         if board[i][j] == 0:
            l.append((i, j))
   return(l)
# Select a random place for the player
def my_random_place(board, my_player):
   selection = my_possibilities(board)
   current_loc = random.choice(selection)
   board[current_loc] = my_player
   return(board)
def my_row_win(board, my_player):
   for x in range(len(board)):
      win = True
      for y in range(len(board)):
         if board[x, y] != my_player:
            win = False
            continue
         if win == True:
            return(win)
      return(win)
def my_col_win(board, my_player):
   for x in range(len(board)):
      win = True
      for y in range(len(board)):
         if board[y][x] != my_player:
            win = False
            continue
      if win == True:
         return(win)
   return(win)
def my_diag_win(board, my_player):
   win = True
   for x in range(len(board)):
      if board[x, x] != my_player:
         win = False
   return(win)
def evaluate_game(board):
   my_winner = 0
   for my_player in [1, 2]:
      if (my_row_win(board, my_player) or
         my_col_win(board,my_player) or
         my_diag_win(board,my_player)):
         my_winner = my_player
   if np.all(board != 0) and my_winner == 0:
      my_winner = -1
   return my_winner
# Main function to start the game
def my_play_game():
   board, my_winner, counter = my_create_board(), 0, 1
   print(board)
   sleep(2)
   while my_winner == 0:
      for my_player in [1, 2]:
         board = my_random_place(board, my_player)
         print("Board after " + str(counter) + " move")
         print(board)
         sleep(2)
         counter += 1
         my_winner = evaluate_game(board)
         if my_winner != 0:
            break
   return(my_winner)
# Driver Code
print("Winner is: " + str(my_play_game()))