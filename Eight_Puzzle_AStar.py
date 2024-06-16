from copy import deepcopy
import time

# Node class defines each state of the puzzle.
class Node:
    def __init__(self, current_state, previous_state, g, h, dir):
        self.current_state = current_state
        self.previous_state = previous_state
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

# Puzzle class defines the initial state, the goal state and the solution algorithm functions.
class Puzzle:
    
    size = 3 # 3x3

    def __init__(self, *args):
        self.developedNodes = 0
        self.createdNodes = 0

        # If no arguments were passed to the constructor, take the initial state and goal state values from user input.
        if len(args) == 0:
            validInput = False
            while not validInput:
                self.initial = []
                check = []
                try:
                    print("\nEnter values for Initial State:")
                    print("- 3 in each row seperated by comma, e.g. 1,2,3")
                    print("- Duplicate values are not allowed, and the value 0 is required.")
                    for _ in range(self.size):
                        self.initial.append(input().split(","))
                    for row in range(self.size):
                        # Check that the row size is valid
                        if len(self.initial[row]) != self.size:
                            raise ValueError
                        for col in range(self.size):
                            # Parse to int
                            self.initial[row][col] = int(self.initial[row][col])
                            # Check for duplicate values
                            if self.initial[row][col] in check:
                                raise ValueError
                            check.append(self.initial[row][col]) 
                    # Check that 0 was input
                    if 0 not in check:
                        raise ValueError
                    validInput = True
                except(ValueError):
                    print("Invalid input for Initial State, please try again.")

            validInput = False
            while not validInput:
                self.goal = []
                check = []
                try:
                    print("\nEnter values for Goal State:")
                    print("- 3 in each row seperated by comma, e.g. 1,2,3")
                    print("- Duplicate values are not allowed, and the value 0 is required.")
                    print("- All values must be present in the initial state.")
                    for _ in range(self.size):
                        self.goal.append(input().split(","))
                    for row in range(self.size):
                        # Check that the row size is valid
                        if len(self.goal[row]) != self.size:
                            raise ValueError
                        for col in range(self.size):
                            # Parse to int
                            self.goal[row][col] = int(self.goal[row][col])
                            # Check that the goal state values are present in the initial state
                            if (self.goal[row][col] not in self.initial[0] 
                            and self.goal[row][col] not in self.initial[1]
                            and self.goal[row][col] not in self.initial[2]):
                                raise ValueError
                            # Check for duplicate values
                            if self.goal[row][col] in check:
                                raise ValueError
                            check.append(self.goal[row][col]) 
                    # Check that 0 was input
                    if 0 not in check:
                        raise ValueError
                    validInput = True
                except(ValueError):
                    print("Invalid input for Goal State, please try again.")

        # If 2 arguments were passed to the constructor, take the initial state and goal state values from the passed arguments.
        elif len(args) == 2:
            self.initial = args[0]
            check = []
            # Check that the input type is valid
            if type(self.initial) != list:
                raise TypeError("Invalid input type for Initial State (Must be a list not {}).".format(type(self.initial).__name__))
            # Check that the column size is valid
            if len(self.initial) != self.size:
                raise ValueError("Invalid input size for Initial State (Must be {} not {}).".format(self.size, len(self.initial)))
            for row in range(self.size):
                # Check that the row size is valid
                if type(self.initial[row]) != list or len(self.initial[row]) != self.size:
                    raise ValueError("Invalid input for Initial State.")
                for col in range(self.size):
                    # Check that the type of the elements is int
                    if type(self.initial[row][col]) != int:
                        raise ValueError("Invalid input for Initial State.")
                    # Check for duplicate values
                    if self.initial[row][col] in check:
                        raise ValueError("Invalid input for Initial State.")
                    check.append(self.initial[row][col]) 
            # Check that 0 was input
            if 0 not in check:
                raise ValueError("Invalid input for Initial State.")

            self.goal = args[1]
            check = []
            # Check that the input type is valid
            if type(self.goal) != list:
                raise TypeError("Invalid input type for Goal State (Must be a list not {}).".format(type(self.goal).__name__))
            # Check that the column size is valid
            if len(self.goal) != self.size:
                raise ValueError("Invalid input size for Goal State (Must be {} not {}).".format(self.size, len(self.goal)))
            for row in range(self.size):
                # Check that the row size is valid
                if type(self.goal[row]) != list or len(self.goal[row]) != self.size:
                    raise ValueError("Invalid input for Goal State.")
                for col in range(self.size):
                    # Check that the type of the elements is int
                    if type(self.goal[row][col]) != int:
                        raise ValueError("Invalid input for Goal State.")
                    # Check that the goal state values are present in the initial state
                    if (self.goal[row][col] not in self.initial[0] 
                    and self.goal[row][col] not in self.initial[1]
                    and self.goal[row][col] not in self.initial[2]):
                        raise ValueError("Invalid input for Goal State.")
                    # Check for duplicate values
                    if self.goal[row][col] in check:
                        raise ValueError("Invalid input for Goal State.")
                    check.append(self.goal[row][col]) 
            # Check that 0 was input
            if 0 not in check:
                raise ValueError("Invalid input for Goal State.")

        # If any number of arguments other than 0 or 2 were passed to the constructor, raise a TypeError.
        else:
            raise TypeError("Puzzle() only takes 0 or 2 arguments ({} given).".format(len(args)))

    # Gets the y, x position of an element in a state.
    def getPos(self, current_state, element):
        for row in range(self.size):
            if element in current_state[row]:
                return (row, current_state[row].index(element))

    # Calculates sum of Manhattan distance from a state to the goal.
    def manhattan(self, current_state):
        h = 0
        for row in range(self.size):
            for col in range(self.size):
                if current_state[row][col] == 0:
                    continue
                pos = self.getPos(self.goal, current_state[row][col])
                h += abs(row - pos[0]) + abs(col - pos[1])
        return h

    # Generates node children.
    def genChildren(self, node):
        childern = []
        emptyPos = self.getPos(node.current_state, 0)
        directions = {"UP": [-1, 0], "DOWN": [1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}

        for dir in directions.keys():
            newPos = (emptyPos[0] + directions[dir][0], emptyPos[1] + directions[dir][1])
            if 0 <= newPos[0] < self.size and 0 <= newPos[1] < self.size:
                newState = deepcopy(node.current_state)
                newState[emptyPos[0]][emptyPos[1]] = node.current_state[newPos[0]][newPos[1]]
                newState[newPos[0]][newPos[1]] = 0
                childern.append(Node(newState, node.current_state, node.g + 1, self.manhattan(newState), dir))
                self.createdNodes += 1

        self.developedNodes += 1
        return childern

    # Gets the node with the least f cost and if there are nodes that 
    # have the same least f cost, it gets the one with the least h cost.
    def getBestNode(self, open):
        nodes = list(open.values())
        bestNode = nodes[0]
        bestF = bestNode.f()
        for node in nodes:
            f = node.f()
            if f < bestF:
                bestNode = node
                bestF = f
            elif f == bestF:
                if node.h < bestNode.h:
                    bestNode = node
        return bestNode

    # Generates the shortest path from the initial state to the goal state.
    def genSolutionPath(self, closed):
        node = closed[str(self.goal)]
        path = []

        while node.dir != "INITIAL":
            path.append({
                'dir': node.dir,
                'state': node.current_state,
                'g': node.g,
                'h': node.h,
                'f': node.f()
            })
            node = closed[str(node.previous_state)]
        path.append({
            'dir': "INITIAL",
            'state': node.current_state,
            'g': node.g,
            'h': node.h,
            'f': node.f()
        })
        path.reverse()

        return path

    # A* algorithm to solve the puzzle.
    def a_star(self):
        open = {str(self.initial): Node(self.initial, self.initial, 0, self.manhattan(self.initial), "INITIAL")}
        closed = {}

        while open != {}:
            bestNode = self.getBestNode(open)
            del open[str(bestNode.current_state)]
            closed[str(bestNode.current_state)] = bestNode

            if bestNode.current_state == self.goal:
                return self.genSolutionPath(closed)

            children = self.genChildren(bestNode)
            for node in children:
                if str(node.current_state) not in open.keys() and str(node.current_state) not in closed.keys(): 
                    open[str(node.current_state)] = node
                elif str(node.current_state) in open.keys() and open[str(node.current_state)].g > node.g:
                    open[str(node.current_state)] = node
                elif str(node.current_state) in closed.keys() and closed[str(node.current_state)].g > node.g:
                    closed[str(node.current_state)] = node
        
        # open == {}
        return False

    # Returns a string representation of the puzzle state.
    def printState(self, state):
        s = ""
        s += "—————————————\n"
        for row in range(self.size):
            for col in range(self.size):
                s += "| " + str(state[row][col]) + " "
            s += "|\n—————————————\n"
        return s

    # Solves the puzzle using the a_star function and returns the result.
    def solve(self):
        t1 = time.process_time()
        path = self.a_star()
        t2 = time.process_time()
        result = ""
        if path:
            result += "\nShortest Solution Path:\n(" + str(len(path) - 1) + " Steps)\n"
            for node in path:
                result += "\ng(n) = {} , h(n) = {} , f(n) = {}\n".format(node['g'], node['h'], node['f'])
                result +="\n{:^13}\n".format("—[ " + node['dir'] + " ]—")
                result += self.printState(node['state'])
            result += "\nGOAL REACHED!\n"
            result += "\nSolution steps: " + str(len(path) - 1)
        else:
            result += "\nThe Puzzle Is Unsolvable!\n"
        result += "\nDeveloped nodes: " + str(self.developedNodes)
        result += "\nCreated nodes: " + str(self.createdNodes)
        result += "\nSearch time: " + str(round(t2 - t1, 6)) + " second(s)\n\n"
        return result


if __name__ == '__main__':

    # Take input from user.
    p = Puzzle()
    sol = p.solve()
    print(sol)

    # Take input directly.
    #p = Puzzle([[1,0,4],[2,5,3],[6,8,7]], [[1,2,3],[4,5,6],[7,8,0]])
    #sol = p.solve()
    #print(sol)

#=======================================================================
#
# ---------------------- Solvable Examples ----------------------
#
# All combinations of these initial and goal states are solvable.
#
# Initial states:
#
# 6,2,8
# 4,7,1
# 0,3,5
#----------
# 3,2,1
# 4,6,5
# 0,7,8
#----------
# 1,0,4
# 2,5,3
# 6,8,7
#----------
# 8,0,3
# 4,5,2
# 6,7,1
#
# Goal states:
#
# 1,2,3
# 4,5,6
# 7,8,0
#----------
# 0,8,7
# 6,5,4
# 3,2,1
#----------
# 4,1,3
# 2,6,8
# 7,0,5
#----------
# 6,1,7
# 4,5,8
# 3,2,0
#
# ---------------------- Unsolvable Example ----------------------
#
# Output:
#
# Enter values for Initial State:
# - 3 in each row seperated by comma, e.g. 1,2,3
# - Duplicate values are not allowed, and the value 0 is required.
# 5,4,3
# 7,8,1
# 2,0,6
#
# Enter values for Goal State:
# - 3 in each row seperated by comma, e.g. 1,2,3
# - Duplicate values are not allowed, and the value 0 is required.
# - All values must be present in the initial state.
# 1,2,3
# 4,5,6
# 7,8,0
#
# The Puzzle Is Unsolvable!
#
# Developed nodes: 181440
# Created nodes: 483840
# Search time: 291.390625 second(s)