import numpy

def main():
   print("Hello! Welcome to Battleship. This game is designed for a user who is playing with ships of size 5, 4, 3 (2 ships), and 2. The grid is 10 x 10, numbered from 1 through 10 (1-indexed).")
   numQuestions = 0
   finished = False
   grid = np.array(10, 10)

   while not finished:
      (x, y) = getMostProbablePosition(grid)
      input("Is the coordinate ")

def getMostProbablePosition(grid):
   #horizontal (x) then vertical (y)
