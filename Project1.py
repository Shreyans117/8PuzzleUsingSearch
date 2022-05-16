from math import sqrt
import copy
import bisect 
import time


puzzleSize = 8                              #Puzzle size   
goalState = [1, 2, 3, 4, 5, 6, 7, 8, 0]     #Goal state
gridSize = int(sqrt(puzzleSize + 1))        #Size of puzzle grid/matrix
testCases = [[1, 2, 3, 4, 5, 6, 7, 8, 0], [1, 2, 3, 4, 5, 6, 0, 7, 8], [1, 2, 3, 5, 0, 6, 4,7, 8], [1, 3, 6, 5, 0, 2, 4, 7, 8],\
 [1, 3, 6, 5, 0, 7, 4, 8, 2], [1, 6, 7, 5, 0, 3, 4, 8, 2], [7, 1, 2, 4, 8, 5, 6, 3, 0], [0, 7, 2, 4, 6, 1, 3, 5, 8]]  #Test cases


def noHeuristic(state):                     #Default heuristic function for Uniform cost search
    return 0

def misplacedTiles(state):                  #Misplaced tiles heuristic function for A* search
    count = 0
    for i in range(puzzleSize+1):
        if (goalState[i] != state[i]):
            count += 1
    return count

def manhattanDistance(state):               #Manhattan distance heuristic function for A* search
    distance = 0
    for i in range(puzzleSize+1):
        if state[i] == 0:
            continue
        if state[i] == goalState[i]:
            continue
        goalRow = (state[i]-1)//gridSize
        goalCol = (state[i]-1) % gridSize
        stateRow = i // gridSize
        stateCol = i % gridSize
        distance += abs(goalRow - stateRow) + abs(goalCol - stateCol)
    return distance

def goalTest(state):                        #Terminal test
    return state == goalState

def expand(parentState):
    position = parentState.index(0)
    row = position // gridSize                 #As grid row index is same as the integer floor value of array index divided by grid size
    col = position % gridSize                  #As grid col index is same as the remainder of array index divided by grid size
    nextFrontier = []
    if row > 0:                             #Checks for boundary conditions for the next set of possible moves (max 4) that can be expanded
        newState = copy.deepcopy(parentState)
        exchange(newState, position, position-gridSize)
        nextFrontier.append(newState)
    if row < gridSize -1:
        newState = copy.deepcopy(parentState)
        exchange(newState, position, position+gridSize)
        nextFrontier.append(newState)
    if col > 0:
        newState = copy.deepcopy(parentState)
        exchange(newState, position, position-1)
        nextFrontier.append(newState)
    if col <  gridSize -1:
        newState = copy.deepcopy(parentState)
        exchange(newState, position,position+1)
        nextFrontier.append(newState)
    return nextFrontier

#Generate a unique string encoding representing each state whose hash value can be compared in the Set used to track repeated states.
def generateHash(state):
    string = ""
    for i in range(puzzleSize+1):
        string += chr(ord('@') + state[i])
    return string

def checkState(state):
    # Check if entries are valid.
    if sorted(state) == sorted(goalState):
        # Check if number of inversions is even.
        count = 0
        for i in range(0,puzzleSize + 1):
            for j in range(i+1, puzzleSize + 1):
                if state[i]>state[j] and state[i]!=0 and state[j]!=0:
                    count += 1
        if count%2==0:
            return True
        else:
            print("Input state is not solvable! \n")
            return False
    else:
        print("Input state is invalid! \n")
        return False


class Move:                                             #Class created to keep track of each node's attributes
    def __init__(self, state, depth, heuristic):
        self.state = state
        self.depth = depth
        self.heuristic = heuristic
        self.totalCost = heuristic+depth

    def __lt__(self, other):                            #Overridden system method for comparison of objects with totalCost as the default and depth and heuristic as tie-breakers in that order respectively.
        if(self.totalCost < other.totalCost):
            return True
        elif (self.totalCost == other.totalCost):
            if(self.depth < other.depth):
                return True
            else:
                return self.heuristic < other.heuristic 
        else:
            return False

def exchange(element, i, j):                            #For swapping array elements.
    temp = element[i]
    element[i] = element[j]
    element[j] = temp

def generalSearch(heuristicFunction, inputState):       #General search method based Dr. Keogh's slides from CS205 at UC Riverside
    repeated = set()                                    #Set to track repeated states
    inputNode = Move(inputState, 0, heuristicFunction(inputState))
    queue = []
    queue.append(inputNode)
    while(len(queue)>0):
        node=queue.pop(0)                               #Pop the front of the queue
        repeated.add(generateHash(node.state))          #Generate unique hashable string to be stored in set to track repeated states.
        if goalTest(node.state):
            return (len(repeated), node.depth)
        nextFrontier = expand(node.state)               #Expand the node
        for state in nextFrontier:
            if (generateHash(state) in repeated):       #Checks if state is a repeated state
                continue
            bisect.insort(queue,Move(state, node.depth + 1,  heuristicFunction(state))) #Insert new entries in sorted order in the queue
    return (len(repeated), -1)

def printPuzzle(initialState):                          #Prints the input puzzle
    for i in range(puzzleSize+1):
        print(initialState[i], end=' ')
        if (i % gridSize == gridSize - 1):
            print("\n")

def solvePuzzle(initialState):
    print("The input state is: ")
    printPuzzle(initialState)

    start = time.perf_counter()
    result = generalSearch(noHeuristic, initialState)
    stop = time.perf_counter()
    if(result[1]==-1):
        print("Uniform cost search failed!\n")
        exit()
    print(f"Uniform cost search took {stop-start:0.3f}s of time and explored {result[0]} nodes with depth {result[1]}")
    
    start = time.perf_counter()
    result = generalSearch(misplacedTiles, initialState)
    stop = time.perf_counter()
    if(result[1]==-1):
        print("A* search with misplaced tile heuristic failed!\n")
        exit()
    print(f"A* search with misplaced tile heuristic took {stop-start:0.3f}s of time and explored {result[0]} nodes with depth {result[1]}")
    
    start = time.perf_counter()
    result = generalSearch(manhattanDistance, initialState)
    stop = time.perf_counter()
    if(result[1]==-1):
        print("A* search with manhattan distance heuristic failed!\n")
        exit()
    print(f"A* search with manhattan distance heuristic took {stop-start:0.3f}s of time and explored {result[0]} nodes with depth {result[1]}")

def menu():
    print("Please input 1 to execute your own test case or 2 to execute a pre-selected set of test cases. \n")
    userInput=int(input())
    if(userInput==1):
        initialState = []
        print("Please input the initial state, one number at a time, with a 0 representing the empty tile. \n")
        for i in range(puzzleSize+1):
            temp = int(input())
            initialState.append(temp)
        if not checkState(initialState):
            exit()
        solvePuzzle(initialState)
    elif(userInput==2):
        for i in testCases:
            if not checkState(i):
                exit()
            solvePuzzle(i)
menu()
