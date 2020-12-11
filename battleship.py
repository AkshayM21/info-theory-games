import numpy as np

def main():
   print("Hello! Welcome to Battleship. This game is designed for a user who is playing with ships of size 5, 4, 3 (2 ships), and 2. The grid is 10 x 10, numbered from 1 through 10 (1-indexed).")
   numQuestions = 0
   finished = False
   grid = np.array(10, 10)
   remainingShips = [5, 4, 3, 3, 2]

   while not finished:
      (x, y) = getMostProbablePosition(grid, remainingShips)
      isHit = input("Is the coordinate <"+str(x)+", "+str(y)+"> a hit? Please answer 'True' or 'False' only.")=='True'
      numQuestions += 1
      if isHit:
         (grid, shipLength, questionsAsked) = sinkShip(x, y, grid)
         remainingShips.remove(shipLength)
         numQuestions += questionsAsked
      
      finished = len(remainingShips)==0
   
   print("All your ships have been sunk! There were a total of "+str(numQuestions)+" asked.")

def getMostProbablePosition(grid, remainingShips):
   #horizontal (x) then vertical (y)
   x = 0
   y = 0
   return (x, y)

def sinkShip(x, y, grid):
   #need to update grid
   #ask questions in loop -- if it is a hit and if it is a sink
   #keep independent track of hits versus misses

   shipLength = 4 #arbitrary//placeholder
   questionsAsked = 4
   return (grid, shipLength, questionsAsked)
