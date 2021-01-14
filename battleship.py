import numpy as np

def main():
    print("Hello! Welcome to Battleship. This game is designed for a user who is playing with ships of size 5, 4, 3 (2 ships), and 2. The grid is 10 x 10, numbered from 1 through 10 (1-indexed).")
    numQuestions = 0
    finished = False
    grid = np.array([[0 for _ in range(10)] for _ in range(10)]) # 0 = unchecked, 1 = miss, 2 = hit
    remainingShips = [5, 4, 3, 3, 2]

    while not finished:
        (x, y) = getMostProbablePosition(grid, remainingShips)
        isHit = input("Question " + str(numQuestions+1) + ": Is the coordinate <"+str(x+1)+", "+str(y+1)+"> a hit or a miss? Please enter \"hit\" or \"miss\": ")
        numQuestions += 1
        if isHit[0].lower() == 'h':
            (grid, shipLength, questionsAsked) = sinkShip(x, y, grid)
            remainingShips.remove(shipLength)
            numQuestions += questionsAsked
        else:
            grid[y, x] = 1

        finished = len(remainingShips)==0

    print("All your ships have been sunk! There were a total of "+str(numQuestions)+" asked.")

def getMostProbablePosition(grid, remainingShips):

    freq = np.array([[0 for _ in range(10)] for _ in range(10)])

    # calculates the total number of ways a ship could go through each point
    for shipLength in remainingShips:
        for i in range(10):
            for j in range(10):
                if grid[i, j] != 0:
                    continue
                for delta in range(shipLength):
                    # checking horizontal orientations of the current ship through the current point
                    if j+delta-shipLength+1 >= 0 and j+delta < 10:
                        valid = True
                        for temp in range(j+delta-shipLength+1, j+delta+1):
                            if grid[i, temp] != 0:
                                valid = False
                        if valid:
                            freq[i, j] += 1
                    # checking vertical orientations of the current ship through the current point
                    if i+delta-shipLength+1 >= 0 and i+delta < 10:
                        valid = True
                        for temp in range(i+delta-shipLength+1, i+delta+1):
                            if grid[temp, j] != 0:
                                valid = False
                        if valid:
                            freq[i, j] += 1

    x = 0
    y = 0
    for i in range(10):
        for j in range(10):
            # print("i: " + str(i) + ", j: " + str(j) + ", x: " + str(x) + ", y: " + str(y))
            # print("freq[i, j]: " + str(freq[i, j]) + ", freq[y, x]: " + str(freq[y, x]))
            if freq[i, j] > freq[y, x]:
                x = j
                y = i

    print("freq:")
    print(freq)
    print("(x, y): (" + str(x) + ", " + str(y) + ")")

    return (x, y)

# be wary of the edge case in which we hit (a) different ship(s) than the one first hit -- then we
# need to sink all of the ships that were hit -- could do this by maintaining a set of the
# positions that were hit and, once we sink a ship, we delete all of the positions from that set
# that are a part of the sunken ship, and if there are any positions left in that list, re-run
# sinkShip with those positions as an input
# that would probably also require moving the removal of ships from remainingShips to this function
def sinkShip(x, y, grid):
    #need to update grid
    #ask questions in loop -- if it is a hit and if it is a sink
    #keep independent track of hits versus misses

    shipLength = 4 #arbitrary//placeholder
    questionsAsked = 4
    return (grid, shipLength, questionsAsked)

main()
