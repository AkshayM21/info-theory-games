import numpy as np

coordDeltas = ((0, 1), (0, -1), (1, 0), (-1, 0))

def main():
    print("Hello! Welcome to Battleship. This game is designed for a user who is playing with ships of size 5, 4, 3 (2 ships), and 2. The grid is 10 x 10, numbered from 1 through 10 (1-indexed).")
    numQuestions = 0
    finished = False
    grid = np.array([[0 for _ in range(10)] for _ in range(10)]) # 0 = unchecked, 1 = miss, 2 = hit
    remainingShips = np.array([5, 4, 3, 3, 2])

    while not finished:
        (x, y) = getMostProbablePosition(grid, remainingShips)
        isHit = input("Question " + str(numQuestions+1) + ": Is the coordinate <"+str(x+1)+", "+str(y+1)+"> a hit or a miss? Please enter \"hit\" or \"miss\": ")
        numQuestions += 1
        if isHit[0].lower() == 'h':
            grid[y, x] = 2
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

    # print("freq:")
    # print(freq)
    # print("(x, y): (" + str(x) + ", " + str(y) + ")")

    return (x, y)

# be wary of the edge case in which we hit (a) different ship(s) than the one first hit -- then we
# need to sink all of the ships that were hit -- could do this by maintaining a set of the
# positions that were hit and, once we sink a ship, we delete all of the positions from that set
# that are a part of the sunken ship, and if there are any positions left in that list, re-run
# sinkShip with those positions as an input
# that would probably also require moving the removal of ships from remainingShips to this function
def sinkShip(shipCoords, grid):
    #need to update grid
    #ask questions in loop -- if it is a hit and if it is a sink
    #keep independent track of hits versus misses

    shipLength = 4 #arbitrary//placeholder
    questionsAsked = 4
    return (grid, shipLength, questionsAsked)

# returns the most probable position for the next part of the given ship
# shipCoords is a list (NON-NUMPY for the sort to work properly) of tuples of the (x, y) positions
# of the current shipCoords we have returns (x, y) of the most probable position
def sinkShipGetMostProbablePosition(shipCoords, grid):
    shipCoords.sort()

    freq = []
    if (len(shipCoords) == 1):
        freq = np.array([0 for _ in range(4)])
    else:
        freq = np.array([0 for _ in range(2)])

    if len(shipCoords) == 1:
        # check the freq of the spots all around (x, y)
        (x, y) = shipCoords[0]
        for shipLength in remainingShips:
            for ind in range(len(coordDeltas)):
                i = y + coordDeltas[ind][1]
                j = x + coordDeltas[ind][0]
                if i < 0 or i >= 10 or j < 0 or j >= 10 or grid[i, j] != 0:
                    continue
                for delta in range(shipLength):
                    # checking horizontal orientations of the current ship through the current point
                    if j+delta-shipLength+1 >= 0 and j+delta < 10:
                        valid = True
                        for temp in range(j+delta-shipLength+1, j+delta+1):
                            if (temp, i) not in shipCoords and grid[i, temp] != 0:
                                valid = False
                        if valid:
                            freq[ind] += 1
                    # checking vertical orientations of the current ship through the current point
                    if i+delta-shipLength+1 >= 0 and i+delta < 10:
                        valid = True
                        for temp in range(i+delta-shipLength+1, i+delta+1):
                            if (j, temp) not in shipCoords and grid[temp, j] != 0:
                                valid = False
                        if valid:
                            freq[ind] += 1
        maxInd = 0
        for ind in range(len(coordDeltas)):
            if freq[ind] > freq[maxInd]:
                maxInd = ind

        return (x+coordDeltas[maxInd][0], y+coordDeltas[maxInd][1])

    # the coords must be in a horizontal or vertical line
    else:
        checkCoords = []
        # if the coords are in a vertical line
        if shipCoords[0][0] == shipCoords[-1][0]:
            checkCoords = [(shipCoords[0][0], shipCoords[0][1]-1), (shipCoords[-1][0], shipCoords[-1][1]+1)]
        # if the coords are in a horizontal line
        else:
            assert shipCoords[0][1] == shipCoords[-1][1]
            checkCoords = [(shipCoords[0][0]-1, shipCoords[0][1]), (shipCoords[-1][0]+1, shipCoords[-1][1])]

        for ind in range(len(checkCoords)):
            i = checkCoords[ind][1]
            j = checkCoords[ind][0]
            for shipLength in remainingShips:
                if i < 0 or i >= 10 or j < 0 or j >= 10 or grid[i, j] != 0:
                    continue
                for delta in range(shipLength):
                    # checking horizontal orientations of the current ship through the current point
                    if j+delta-shipLength+1 >= 0 and j+delta < 10:
                        valid = True
                        for temp in range(j+delta-shipLength+1, j+delta+1):
                            if (temp, i) not in shipCoords and grid[i, temp] != 0:
                                valid = False
                        if valid:
                            freq[ind] += 1
                    # checking vertical orientations of the current ship through the current point
                    if i+delta-shipLength+1 >= 0 and i+delta < 10:
                        valid = True
                        for temp in range(i+delta-shipLength+1, i+delta+1):
                            if (j, temp) not in shipCoords and grid[temp, j] != 0:
                                valid = False
                        if valid:
                            freq[ind] += 1

        if (freq[0] == 0 and freq[1] == 0):
            for shipCoord in shipCoords:
                sinkShip(shipCoord, grid)

        if (freq[1] > freq[0]):
            return checkCoords[1]
        return checkCoords[0]

main()
