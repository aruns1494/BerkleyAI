# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util, pacman, sys

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST

    return  [s, s, w, s, w, w, s, w]



def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    states = util.Stack()                                   # states holds the entire branch from the root to the leaf in a stack.
    visited = []                                            # visited list contains all visited states
    states.push([(problem.getStartState(), "Stop", 0)])

    while not states.isEmpty():
        direction = states.pop()                            # direction holds a list at all times as states has different elements as lists in it.
        s = direction[len(direction) - 1]
        if problem.isGoalState(s[0]):
            return [x[1] for x in direction][1:]            # return the entire sequence of action on reaching the goal state
        if s[0] not in visited:
            visited.append(s[0])
            for successor in problem.getSuccessors(s[0]):   # For every node that has not been visited already, the path from the root to that node and the each of the node's
                if successor[0] not in visited:             # successors is appended and the entire list is pushed into the stack. The last element in the stack being either the
                    successorPath = direction[:]            # goal state or the node that needs to be expanded.
                    successorPath.append(successor)
                    states.push(successorPath)
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    states = util.PriorityQueueWithFunction(len)            # This code works the same way as the DFS in handling the nodes. Here the states are a Queue instead of a stack. Hence the
    visited = []                                            # tree is seached according to each level and not depth wise.
    states.push([(problem.getStartState(), "Stop", 0)])

    while not states.isEmpty():
        direction = states.pop()
        s = direction[len(direction) - 1]
        if problem.isGoalState(s[0]):
            return [x[1] for x in direction][1:]
        if s[0] not in visited:
            visited.append(s[0])
            for successor in problem.getSuccessors(s[0]):
                if successor[0] not in visited:
                    successorPath = direction[:]
                    successorPath.append(successor)
                    states.push(successorPath)
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    states = util.PriorityQueue()                           # In the UCS, the goal is reached at the lowest cost possible.
    states.push((problem.getStartState(), [], 0), 0)        # Here each state holds a tuple in which the first element holds the state, direction and cost. the second element holds
    state, directions, allcost = states.pop()               # total cost. The visited again keeps track of all the nodes that have previously been visited.
    visited = [(state, 0)]
    while (not problem.isGoalState(state)):
        successors = problem.getSuccessors(state)
        for nextState, action, cost in successors:
            flag = False
            totalCost = problem.getCostOfActions(directions + [action])     # totalCost is sum of cost of reaching the current node from Start State and the cost of the current action
            for i in range(len(visited)):
                state_tmp, cost_tmp = visited[i]
                if (nextState == state_tmp) and (totalCost >= cost_tmp):
                    flag = True
            if (not flag):
                states.push((nextState, directions + [action], totalCost), totalCost)
                visited.append((nextState, totalCost))
        state, directions, allcost = states.pop()
        # print "pop ",allcost

    return directions                                       # Direction holds the entire set of actions that denotes the path from the start state to the goal state.
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"                                # The A star search nehaves exactly like that of the UCS except that the totalCost is sum of actual cost till the node and
    states = util.PriorityQueue()                           # the heuristic of the next node.
    states.push((problem.getStartState(), [], 0), 0)
    state, directions, allcost = states.pop()
    visited = [(state, 0)]                                  # Visited keeps track of the previously explored nodes.
    while (not problem.isGoalState(state)):
        successors = problem.getSuccessors(state)
        for nextState, action, cost in successors:
            flag = False
            totalCost = problem.getCostOfActions(directions + [action])
            for i in range(len(visited)):
                state_tmp, cost_tmp = visited[i]
                if (nextState == state_tmp) and (totalCost >= cost_tmp):        # This is to ensure that even if the state has been reached, is it the optinal cost. Only if the state
                    flag = True                             # is already in visited AND if the cost of the already visited path is lower than the current path, the succersor is not
            if (not flag):                                  # stored. Else the successor is pushed into the queue
                states.push((nextState, directions + [action], totalCost), totalCost+heuristic(nextState,problem))
                visited.append((nextState, totalCost))
        state, directions, allcost = states.pop()
                                                            # The search goes on till it reaches the goal state and the fringe is clear of all other routes to goal
    return directions                                       # Directions returns the sequence of action that needs to be performed to reach the goal state
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
