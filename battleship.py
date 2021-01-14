import numpy as np
import sys

coordDeltas = ((0, 1), (0, -1), (1, 0), (-1, 0))

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
            grid[y, x] = 2
            shipCoords = [(x, y)]
            (grid, shipLength, questionsAsked) = sinkShip(shipCoords, grid, numQuestions, remainingShips)
            for length in shipLength:
                assert length in remainingShips
                remainingShips.remove(length)
            # print("shipLength: ")
            # print(shipLength)
            # print("remainingShips: ")
            # print(remainingShips)
            numQuestions += questionsAsked
        else:
            grid[y, x] = 1

        finished = len(remainingShips)==0

    print("All your ships have been sunk! There were a total of "+str(numQuestions)+" questions asked.")

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
def sinkShip(shipCoords, grid, numQuestions, remainingShips):
    #need to update grid
    #ask questions in loop -- if it is a hit and if it is a sink
    #keep independent track of hits versus misses

    questionsAsked = 0

    isSink = False

    while not isSink:
        (position, shipLengths) = sinkShipGetMostProbablePosition(shipCoords, grid, numQuestions, remainingShips)
        if(shipLengths==None):
            x = position[0]
            y = position[1]
            print("Question " + str(numQuestions + questionsAsked+ 1) + ": Is the coordinate <" + str(x + 1) + ", " + str(
                y + 1) + "> a hit or a miss? Please enter \"hit\" or \"miss\", and, if a ship has been sunk, please enter the length of the sunk ship separated by a space (e.g. \"hit 4\"): ")
            isHit = list(sys.stdin.readline()[:-1].split(" "))
            questionsAsked += 1
            if isHit[0][0].lower() == 'h':
                grid[y, x] = 2
                shipCoords.append(position)
                # print(sunkAnswer)
                if len(isHit) > 1:
                    # print("yay fully sunk")
                    #ship sunk
                    isSink = True
                    #check if more coordinates
                    assert isHit[1].isnumeric()
                    shipLength = int(isHit[1])
                    # print("this is ship length "+str(shipLength))
                    # print("shipcoord length "+str(len(shipCoords)))
                    #check vertical/horizontal
                    # if the coords are in a vertical line
                    if shipLength != len(shipCoords):
                        #start from current position, figure out if any of the other positions are current length away from this one, go in that direction
                        #up shipLength
                        if (x, y-(shipLength-1)) in shipCoords:
                            # print("it's up")
                            for i in range(shipLength):
                                shipCoords.remove((x, y-i))
                            # print("done")
                        #down shipLength
                        elif (x, y+(shipLength-1)) in shipCoords:
                            # print("it's down")
                            for i in range(shipLength):
                                shipCoords.remove((x, y+i))
                            # print("done")
                        #left shipLength
                        elif (x-(shipLength-1), y) in shipCoords:
                            # print("it's left")
                            for i in range(shipLength):
                                shipCoords.remove((x-i, y))
                            # print("done")
                        #right shiplength
                        else:
                            # print("it's right")
                            for i in range(shipLength):
                                shipCoords.remove((x+i, y))
                            # print("done")

                        (grid, addlShipLength, moreQuestions) = sinkShip(shipCoords, grid, numQuestions+questionsAsked, remainingShips)
                        return (grid, [shipLength]+addlShipLength, questionsAsked+moreQuestions)
                    else:
                        # print("returning...")
                        return (grid, [shipLength], questionsAsked)
            else:
                grid[y, x] = 1
        else:
            #all the questions have already been asked
            #position is actually questionsAsked
            # print("grid: ")
            # print(grid)
            # print("shipLengths: ")
            # print(shipLengths)
            return (grid, shipLengths, position)

    #ask questions using helper method
        #check output -- if its a tuple then go ahead, if its a number then hte sink ships have been finished and return w/o any printing out
    #if its a hit, mark with grid =2 and put in ship coords
    #perhaps ask follow up if its a sink?
    #if its not a hit, mark with grid = 1
    #if you sink a ship and there are more coordinates then run sink ship again
    #if its two verticals or two horizontals next to eahc other (not head to tail) then the helper method takes care of it
    #so return none means just return? since it already get returned

    return (grid, [None], questionsAsked)

# returns the most probable position for the next part of the given ship
# shipCoords is a list (NON-NUMPY for the sort to work properly) of tuples of the (x, y) positions
# of the current shipCoords we have returns (x, y) of the most probable position
def sinkShipGetMostProbablePosition(shipCoords, grid, numQuestions, remainingShips):
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

        return ((x+coordDeltas[maxInd][0], y+coordDeltas[maxInd][1]), None)

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
            additionalQuestions = 0
            shipLengths = []
            for shipCoord in shipCoords:
                (grid, shipLength, questionsAsked) = sinkShip([shipCoord], grid, numQuestions+additionalQuestions, remainingShips)
                additionalQuestions+= questionsAsked

                shipLengths = shipLengths + shipLength
                # print("helper shipLength: ")
                # print(shipLength)
                # print("helper shipLengths: ")
                # print(shipLengths)
            return (additionalQuestions, shipLengths)

        if (freq[1] > freq[0]):
            return (checkCoords[1], None)
        return (checkCoords[0], None)

main()
