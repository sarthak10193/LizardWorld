import os
import time
import random
import math
import numpy as np

class LizardWorld:
    def __init__(self):
        self.filledPositions = []
        self.algo = ""
        self.n = 0
        self.lizardCount = 0
        self.inputMatrix = []
        self.treeLocations = None
        self.allPositions = dict()

    def getLizardCount(self):
        return self.lizardCount

    def getAlgo(self):
        return self.algo

    def getN(self):
        return self.n

    def readData(self, path):
        with open("input.txt", 'r') as f:
            a = f.readlines()
            self.algo = a[0]
            self.n = int(a[1])
            self.lizardCount = int(a[2])
            matrix =  [row.strip() for row in a[3:]]
            transformMatrix = []
            for r in matrix:
                transformMatrix.append(list(map(int, r)))

            self.inputMatrix = transformMatrix

        return self.algo, self.n, self.lizardCount, self.inputMatrix

    def printSolution(self):
        for row in range(self.n):
            for col in range(self.n):
                print(self.inputMatrix[row][col], end=",")
            print()

        print()

    def getTreeLocations(self, inputMatrix):

        treeLoc = []

        for row in range(self.n):
            for col in range(self.n):
                if inputMatrix[row][col] == 2:
                    treeLoc.append((row,col))

        return treeLoc

    def treeColProtection(self, row, col ,queenRow):

        for treerow, treecol in self.treeLocations:
             if treecol == col:
                 if  queenRow<treerow<row or row<treerow<queenRow:  # means a tree is present in btw
                     return True

        return  False

    # check if any tree in the same row can protect the lizard. if none of the trees offer protection return False
    def treeRowProtection(self, row, col, queenCol):
        for treerow, treecol in self.treeLocations:
            if treerow == row:
                if queenCol < treecol < col:
                    return True
        return False

    # check if any tree in the same right diagnal can protect the lizard. if none of the trees offer protection return False
    def treeRightDiagnalProtection(self, row, col, queenRow, queenCol):
        for treerow, treecol in self.treeLocations:
            if treerow + treecol == row + col:
                if (queenRow < treerow < row and col < treecol < queenCol) or (row < treerow < queenRow  and queenCol < treecol < col):
                    return True
        return False

    # check if any tree in the same left can protect the lizard. if none of the trees offer protection return False
    def treeLeftDiagnalProtection(self, row, col, queenRow, queenCol):
        for treerow, treecol in self.treeLocations:
            if treerow - treecol == row - col:
                if (queenRow < treerow < row and queenCol < treecol < col) or (row < treerow < queenRow  and queenCol < treecol < col):
                    return True

        return False

    '''
    ##########################################################################
    ############################## 1. DFS ####################################
    ##########################################################################
    '''

    def isPositionSafe(self, filledPositions, row, col):

        if self.inputMatrix[row][col] !=0:
            return False

        colSafe = True
        rowSafe = True
        leftD = True
        rightD = True

        for queen in self.filledPositions:
            if queen[1] == col:
                colSafe = False
                if self.treeColProtection(row,col, queen[0]):
                     colSafe = True

        for queen in self.filledPositions:
            if queen[0] == row:
                rowSafe = False
                if self.treeRowProtection(row,col, queen[1]):
                    rowSafe = True

        for queen in self.filledPositions:
            if queen[0] + queen[1] == row + col:
                rightD = False
                if self.treeRightDiagnalProtection(row, col,  queen[0], queen[1]):
                    rightD = True

        for queen in self.filledPositions:
            if queen[0] - queen[1] == row - col:
                leftD = False
                if self.treeLeftDiagnalProtection(row, col, queen[0], queen[1]):
                    leftD = True

        return colSafe and rowSafe and leftD and rightD


    def isPositionSafeNoTreeDFS(self,filledPositions, row, col):

        # note since we are never placing in the same row becauae we pass row+1 we just need to check for col, diagnoal1 and diagnal2
        # check if the column is ok , diagnal 1 is OK and diagnal 2 is OK
        for queen in self.filledPositions:
            if queen[0] + queen[1] == row + col or queen[0] - queen[1] == row - col or queen[1] == col or queen[0] == row:
                return False

        return True

    def solveLizardWorldUtilDFS(self, n, inputMatrix, rowStart, startTime):

        # if all lizards have been placed, return True
        if len(self.filledPositions) == self.lizardCount:
            # print("Filled Positions#:",len(self.filledPositions), "  ==>" , self.filledPositions)
            return True

        if (time.time() - startTime)/60 > 4.8:
            return False
        # search where to place the next lizard starting, given the last lizard was placed @ (rowinit, colinit)
        '''
        search 1:Next position could be in the same row if there is a tree in the row
        search 2: else simply search the next row
        '''

        for row in range(rowStart, n):
            for col in range(n):
                if self.isPositionSafe(self.filledPositions, row, col):
                    self.inputMatrix[row][col] = 1
                    self.filledPositions.append((row, col))

                    if self.solveLizardWorldUtilDFS(n, inputMatrix, row, startTime):
                        return True

                    self.inputMatrix[row][col] = 0
                    self.filledPositions.remove((row,col))

        return False

    def solveLizardWorldUtilNoTreeDFS(self, n, inputMatrix, row, startTime):
        # if all lizards have been placed, return True
        if len(self.filledPositions) == self.lizardCount:
            print("Filled Positions#:", len(self.filledPositions), "  ==>", self.filledPositions)
            return True

        if (time.time() - startTime)/60 >4.8:
            return False

        for col in range(n):
            if self.isPositionSafeNoTreeDFS(self.filledPositions, row, col):
                inputMatrix[row][col] = 1
                self.filledPositions.append((row, col))

                # now for row+1 try to find a col where we can place the next queen : For eg iter1 places @ (0,0). Next we pass row = 1 and check which col is safe for queen2. we find col = 2 place queen at (1,2)
                if self.solveLizardWorldUtilNoTreeDFS(n , inputMatrix, row + 1, startTime):
                    return True

                inputMatrix[row][col] = 0  # remove the previously places queen beacuase a False was propagated up the recursion Tree
                self.filledPositions.remove((row, col))

        return False


    '''
    ###########################################################################
    ################################ 2. BFS ###################################
    ###########################################################################
    '''
    def isPositionSafeBFS(self, currentFilled, row, col):

        if self.inputMatrix[row][col] !=0:
            return False

        colSafe = True
        rowSafe = True
        leftD = True
        rightD = True

        for queen in currentFilled:
            if queen[1] == col:
                colSafe = False
                if self.treeColProtection(row,col, queen[0]):
                     colSafe = True

        for queen in currentFilled:
            if queen[0] == row:
                rowSafe = False
                if self.treeRowProtection(row,col, queen[1]):
                    rowSafe = True

        for queen in currentFilled:
            if queen[0] + queen[1] == row + col:
                rightD = False
                if self.treeRightDiagnalProtection(row, col,  queen[0], queen[1]):
                    rightD = True

        for queen in currentFilled:
            if queen[0] - queen[1] == row - col:
                leftD = False
                if self.treeLeftDiagnalProtection(row, col, queen[0], queen[1]):
                    leftD = True

        return colSafe and rowSafe and leftD and rightD


    def isPositionSafeNoTreeBFS(self,currentFilledPositions, row, col):

        for queen in currentFilledPositions:
            if queen[0] + queen[1] == row + col or queen[0] - queen[1] == row - col or queen[1] == col or queen[0] == row:
                return False

        return True

    def solveLizardWorldUtilNoTreeBFS(self, n, inputMatrix, queue, startTime ):
        '''
        This function implements the BFS solution for the Lizard World Problem
        :param n: The dimension of nxn input matrix
        :param inputMatrix:  the start state for BFS is an empty matrix
        :param queue: queue for BFS solution, stores the current lizard positions
        :param startTime: startTime
        :return: bool
        '''

        for row in range(n):
            for col in range(n):
                if inputMatrix[row][col] == 0:
                    queue.append([(row, col)])

        while queue and  (time.time()-startTime)/60 < 4.8:

            queueFront = queue.pop(0)  # remove front element from the queue; gives the list of filled Lizard Positions
            lenofQueueFront = len(queueFront)

            if lenofQueueFront==self.lizardCount:
                self.filledPositions = queueFront
                # print("solution Found:", self.filledPositions)
                return True

            currentRowsFilled = {}

            for row, col in queueFront:
                currentRowsFilled[row] = 1

            row = 0
            while row < n and row not in currentRowsFilled:
                col = 0
                while col<n:
                    if self.isPositionSafeNoTreeBFS(queueFront, row, col):
                        if lenofQueueFront + 1 == self.lizardCount:
                            print("solution Found", queueFront + [(row, col)])
                            self.filledPositions = queueFront + [(row, col)]
                            return True
                        queue.append(queueFront + [(row,col)])
                    col+=1
                row+=1

        return False

    def solveLizardWorldUtilBFS(self, n, inputMatrix, queue, startTime) :

        for row in range(n):
            for col in range(n):
                if inputMatrix[row][col] == 0:
                    queue.append([(row, col)])

        while queue and  (time.time()-startTime)/60 < 4.8:
            queueFront = queue.pop(0)  # remove front element from the queue; gives the list of filled Lizard Positions
            if len(queueFront)==self.lizardCount:
                self.filledPositions = queueFront
                # print("solution Found:", self.filledPositions)
                return True

            for row in range(n):
                for col in range(n):
                    if self.isPositionSafeBFS(queueFront, row, col):
                        if len(queueFront + [(row, col)]) == self.lizardCount:
                            self.filledPositions = queueFront + [(row,col)]
                            return True
                        queue.append(queueFront + [(row, col)])
        return False

    '''
    ###########################################################################
    ################################# 3. SA  ##################################
    ###########################################################################
    '''

    def printSASolution(self, state):

        for row in range(self.n):
            for col in range(self.n):
                  key = str(row) + "," + str(col)
                  if key  in self.allPositions:
                      print(self.allPositions[key], end=",")
                  else:
                      print(2, end = ',')

            print()

        print()

    def getRandomStartState(self):
        for row in range(self.n):
            for col in range(self.n):
                if self.inputMatrix[row][col] == 0:   # could have been 0:free  or  2: tree present
                    self.allPositions[str(row)+","+ str(col)] = 0


        startState =  random.sample(self.allPositions.keys(), self.lizardCount)
        for key in startState:
            self.allPositions[key]  = 1  #  set to 1 i.e,  lizard present

        return startState

    def getCostTreePresent(self, currentState):
        # print(currentState)
        cost = 0
        for i in range(len(currentState)):
            for j in range(i + 1, len(currentState)):
                irow, icol = int(currentState[i].split(",")[0]), int(currentState[i].split(",")[1])
                jrow, jcol = int(currentState[j].split(",")[0]), int(currentState[j].split(",")[1])

                if (irow == jrow):
                    if not self.treeRowProtection(jrow, jcol, icol):
                        # print("oops:", (irow, icol), "and ", (jrow, jcol), "row collsion")
                        cost += 1

                if (icol == jcol):
                    if not self.treeColProtection(jrow, jcol, irow):
                        # print("oops:", (irow, icol), "and ", (jrow, jcol), "columnn collsion")
                        cost += 1

                if irow + icol == jrow + jcol:
                    if not self.treeRightDiagnalProtection(jrow, jcol, irow, icol):
                        # print("oops:", (irow, icol), "and ", (jrow, jcol), "right D collsion")
                        cost += 1

                if irow - icol == jrow - jcol:
                    if not self.treeLeftDiagnalProtection(jrow, jcol, irow, icol):
                        # print("oops:", (irow, icol), "and ", (jrow, jcol), "left D collsion")
                        cost += 1

        return cost

    def getCost(self, currentState):

        cost = 0
        for i in range(len(currentState)):
            for j in range(i + 1, len(currentState)):
                irow, icol = currentState[i].split(",")[0], currentState[i].split(",")[1]
                jrow, jcol = currentState[j].split(",")[0], currentState[j].split(",")[1]

                if (int(irow) == int(jrow)) or (int(icol) == int(jcol)) or (
                                int(irow) + int(icol) == int(jrow) + int(jcol)) or (
                                int(irow) - int(icol) == int(jrow) - int(jcol)):
                    # print("oops", currentState[i], currentState[j])
                    cost = cost + 1

        return cost

    def getNextState(self, currentState):  # randomly swap two values

        #print("all:", self.allPositions)
        availPositions = [key for key, value in self.allPositions.items() if value == 0]
        randomAvailPosition = random.sample(availPositions, 1)[0]    # this position is avail for you to set
        #print("avail positions:", availPositions, "randomAvail:", randomAvailPosition)


        currentFilledPositions = [key for key, value in self.allPositions.items() if value == 1]
        randomCurrentFilledPosition = random.sample(currentFilledPositions, 1)[0]
        #print("currentFilled:", currentFilledPositions, "randomCurrentFilled;", randomCurrentFilledPosition)

        self.allPositions[randomAvailPosition] = 1
        self.allPositions[randomCurrentFilledPosition] = 0


        #print("all:", self.allPositions)
        currentFilledPositions.remove(randomCurrentFilledPosition)
        currentFilledPositions.append(randomAvailPosition)
        #print(currentFilledPositions)

        return currentFilledPositions


    def solveLizardWorldUtilSA(self,n, inputMatrix, temp, startTime):

        def getbool(deltaE, temp):
            # print("woah", math.exp(-deltaE / temp) )
            if math.exp(-deltaE / temp) > random.uniform(0, 1):
                return True
            return False


        currentState = self.getRandomStartState()
        # self.printSASolution(currentState)

        currentCost = self.getCostTreePresent(currentState)
        iter = 1
        while (time.time() - startTime) / 60 < 4.9:
            temp = np.float128(temp * (1 / math.log(iter)))
            iter+=1
            nextState = self.getNextState(currentState)
            nextCost = self.getCost(nextState)
            deltaE = nextCost - currentCost
            if deltaE < 0 or getbool(deltaE=deltaE, temp=temp):
                currentState = nextState
                currentCost = nextCost
                if currentCost == 0:
                    self.printSASolution(currentState)
                    self.filledPositions = currentState
                    return currentState

        return None


    def solveLizardWorldUtilNoTreeSA(self,n, inputMatrix, temp, startTime):
        '''
        6*6 takes 1.2 min

        :param n:
        :param inputMatrix:
        :param temp:
        :param startTime:
        :return:
        '''

        currentState = self.getRandomStartState()
        currentCost = self.getCost(currentState)

        iter = 1
        while (time.time()- startTime)/60 < 4.9:
            iter+=1
            temp = np.float128(temp*(1/math.log(iter)))

            nextState = self.getNextState(currentState)
            nextCost = self.getCost(nextState)
            deltaE = nextCost - currentCost

            if deltaE<=0 or math.exp(-deltaE / temp) > random.uniform(0,1):
               currentState = nextState
               currentCost = nextCost
               if currentCost == 0:
                  # print("solution Found:", currentState, iter)
                  self.printSASolution(currentState)
                  self.filledPositions = currentState
                  return currentState
        # print(iter)
        return None

    '''
    ###########################################################################
    ################################# DRIVER  ##################################
    ###########################################################################
    '''

    def solveLizardWorldInit(self, algo, n, lizardCount, inputMatrix):
        print("Solving lizard world using:",  algo.strip(),"  dimension N:",  n, "  Lizard Count:", lizardCount, "\n")

        #self.printSolution()

        startTime = time.time()
        self.treeLocations = self.getTreeLocations(inputMatrix)

        ######################## 1. DFS #############################
        if algo.strip()=="DFS":
            if self.treeLocations:
                # print("Function : solveLizardWorldUtilDFS: Trees Present")
                self.solveLizardWorldUtilDFS(n, inputMatrix, 0, startTime)
            else:
                # print("Function : solveLizardWorldUtilNoTreeDFS : Trees Absent")
                self.solveLizardWorldUtilNoTreeDFS(n, inputMatrix, 0, startTime)

        ######################## 2. BFS #############################
        if algo.strip()=="BFS":
            if self.treeLocations:
                # print("Function: solveLizardWorldUtilBFS : Trees Present")
                self.solveLizardWorldUtilBFS(n, inputMatrix, [], startTime)
            else:
                # print("Function: solveLizardWorldUtilNoTreeBFS: Trees Absent")
                self.solveLizardWorldUtilNoTreeBFS(n , inputMatrix,[] , startTime)

        ######################## 3. SA #############################
        if algo.strip() == "SA":
            if self.treeLocations:
                # print("Function: solveLizardWorldUtilSA : Trees Present")
                self.solveLizardWorldUtilSA(n, inputMatrix, 300000, startTime)
            else:
                # print("Function: solveLizardWorldUtilNoTreeSA : Trees Absent")
                self.solveLizardWorldUtilNoTreeSA(n, inputMatrix, 1000, startTime)


        print("totalTime Taken:", (time.time()-startTime)/60 , "min", "or ",  (time.time()-startTime), "seconds")


    def writeOutput(self, status,algo, matrix=None):

        if algo.strip() == "DFS":
            with open("output.txt", 'w') as f:
                f.write(status)
                if matrix:
                    l = len(matrix)

                    for row in range(len(matrix)):
                        if row == l-1:
                            matrixrow = "".join(list(map(str, matrix[row])))
                        else:
                            matrixrow = "".join(list(map(str, matrix[row]))) + "\n"

                        f.write(matrixrow)

        if algo.strip() == "BFS":
            with open("output.txt", 'w') as f:
                f.write(status)
                if matrix:
                    # print(self.filledPositions)
                    filledDict = dict()
                    for row, col in self.filledPositions:
                        filledDict[str(row) + ","+ str(col)]  = 1
                    for row in range(self.n):
                        currentRow = ""
                        for col in range(self.n):
                            if str(row)+","+str(col) in filledDict:
                                currentRow+="1"
                            else:
                                currentRow+=str(self.inputMatrix[row][col])
                        f.write(currentRow+ "\n")

        if algo.strip() == "SA":
            with open("output.txt", 'w') as f:
                f.write(status)
                if matrix:
                    filledDict = dict()
                    for key in self.filledPositions:
                        filledDict[key] = 1
                    for row in range(self.n):
                        currentRow = ""
                        for col in range(self.n):
                            if str(row)+","+str(col) in filledDict:
                                currentRow+="1"
                            else:
                                currentRow+=str(self.inputMatrix[row][col])
                        f.write(currentRow+ "\n")


def main():
    liz = LizardWorld()
    algo, n, lizardCount, inputMatrix= liz.readData("input.txt")

    liz.solveLizardWorldInit(algo, n, lizardCount, inputMatrix)

    if len(liz.filledPositions) != lizardCount:
        liz.writeOutput("FAIL",algo,  None)
        print("FAIL")
    else:
        # liz.printSolution()
        liz.writeOutput("OK\n", algo, liz.inputMatrix)
        print("OK")


main()
