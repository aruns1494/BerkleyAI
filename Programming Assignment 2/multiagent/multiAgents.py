# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        moves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in moves]
        topScore = max(scores)
        bestIndices = [i for i in range(len(scores)) if scores[i] == topScore]
        chosen = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return moves[chosen]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)           # Gives the successor statae of PacMan.
        newPos = successorGameState.getPacmanPosition()                                 # Gives the position of PACMAN in x,y
        newFood = successorGameState.getFood()                                          # Food Positions
        newGhostStates = successorGameState.getGhostStates()                            # Position of Ghosts
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        heuristic = 0           # Final Heuristic value based on which action will be performed.

        for st in newScaredTimes:
            heuristic += st

        ghostDistances = []
        for gs in newGhostStates:
            ghostDistances += [manhattanDistance(gs.getPosition(), newPos)]             # Manhattan Distance of each ghost to the current position of PACMAN.


        foodList = newFood.asList()                                                     # Position of food or pellets as a list of co-ordinates

        wallList = currentGameState.getWalls().asList()
        emptyFoodNeighbors = 0
        foodDistances = []

        def foodNeighbors(foodPos):         # Function defines the neighbors of each food pallet.
            foodNeighbors = []
            foodNeighbors.append((foodPos[0] - 1, foodPos[1]))
            foodNeighbors.append((foodPos[0], foodPos[1] - 1))
            foodNeighbors.append((foodPos[0], foodPos[1] + 1))
            foodNeighbors.append((foodPos[0] + 1, foodPos[1]))
            return foodNeighbors

        for f in foodList:
            neighbors = foodNeighbors(f)
            for fn in neighbors:
                if fn not in wallList and fn not in foodList:       # Checks the number of valid neighbors that do not have food pallets in them.
                    emptyFoodNeighbors += 1                         # Less the number here, better it for the PACMAN to visit the node first.
            foodDistances += [manhattanDistance(newPos, f)]

        inverseFoodDist = 0
        if len(foodDistances) > 0:
            inverseFoodDist = 1.0 / (min(foodDistances))            # Least food distance is taken and is inversed.

        heuristic += (min(ghostDistances) * ((inverseFoodDist ** 4)))   # Heuristic is calculated depending on the nearest ghost position and inverseFood. Constants here are wights
        heuristic += successorGameState.getScore() - (float(emptyFoodNeighbors) * 3.5)  # that has been experimentally obtained.
        return heuristic

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        # The miniMax algorithm is implemented using maxPhase and minPhase functions. The maxPhase is called for PACMAN while the minPhase is called for the GHOSTS.

        def maxPhase(state, curDepth):
            curDepth = curDepth+1
            if(state.isWin() or state.isLose() or curDepth == self.depth):  # Check if PACMAN has eaten all the food or is dead
                return self.evaluationFunction(state)
            else:
                maximum = -999999.00;
                for actions in state.getLegalActions(0):                    # For all legal actions of PACMAN, compute the search tree and call Min Function as the Ghost has to play next
                    maximum = max(maximum, minPhase(state.generateSuccessor(0,actions),curDepth,1))
            return maximum

        def minPhase(state, curDepth, ghostRank):                           # ghostRank is used to determine the number of Ghosts. Multiple ghosts can be present and hence multiple
            if(state.isWin() or state.isLose()):                            # calls to min function is performed.
                return self.evaluationFunction(state)
            else:
                minimum = 999999.00
                for actions in state.getLegalActions(ghostRank):
                    if(ghostRank == (gameState.getNumAgents() - 1)):        # If this is the last ghost, then call max funtion for PACMAN. Else call MIN function again for then next ghost
                        minimum = min(minimum, maxPhase(state.generateSuccessor(ghostRank,actions),curDepth))
                    else:
                        minimum = min(minimum, minPhase(state.generateSuccessor(ghostRank,actions),curDepth,ghostRank+1))
                return minimum

        maximum = -999999.00                                                # MINIMAX startes execution here and calls minPhase for all possible pacman position.
        action = ''
        for possibleActions in gameState.getLegalActions(0):
            depth = 0
            tempMax = minPhase(gameState.generateSuccessor(0,possibleActions),depth,1)
            if(tempMax>maximum):
                maximum = tempMax
                action = possibleActions
        return action                                                       # Returnds the optimal action.
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    # The Alpha-Beta pruning is used to reduce the search tree to a minimum so as to enable faster search

    def maxPhase(self, gameState, depth, agentIndex, alpha, beta):

        maximum = -999999.00

        # if this is a leaf node with no more actions, return the evaluation function at this state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # otherwise, for evert action, find the successor, and run the minimize function on it. when a value
        # is returned, check to see if it's a new max value (or if it's bigger than the minimizer's best, then prune)
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)

            # run minimize (the minimize function will stack ghost responses)
            temp = self.minPhase(successor, depth, 1, alpha, beta)

            # prune
            if temp > beta:
                return temp

            if temp > maximum:
                maximum = temp
                maxAction = action
            alpha = max(alpha, maximum)             # Alpha is assigned with the new maximum value

        # if this is the first depth, then we're trying to return an ACTION to take. otherwise, we're returning a number. This
        if depth == 1:
            return maxAction
        else:
            return maximum

    def minPhase(self, gameState, depth, agentIndex, alpha, beta):
        minimum = 999999.00

        numAgents = gameState.getNumAgents()            # Gives the number of ghosts plus Pacman

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == numAgents - 1:             # If we are in the min Phase of last GHOST, then we should return value if we are at the depth. Else we have to call the max function
                if depth == self.depth:
                    temp = self.evaluationFunction(successor)
                else:
                    temp = self.maxPhase(successor, depth + 1, 0, alpha, beta)
            else:                                       # Else call min Phase again as there are still more ghosts to perform.
                temp = self.minPhase(successor, depth, agentIndex + 1, alpha, beta)

            if temp < alpha:            # Check if temp is less than alpha
                return temp
            if temp < minimum:          # Pruning step
                minimum = temp
                minAction = action
            beta = min(beta, minimum)   # Beta is assigned the new minumum value
        return minimum

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        maxAction = self.maxPhase(gameState, 1, 0, -999999.00, 999999.00)           # Starts by calling maxPhase function.
        return maxAction

        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        # Maxima Phase

        def maxPhase(state, depth):
            depth = depth + 1
            if state.isWin() or state.isLose() or depth == self.depth:          # Check if Pacman has won or lost or we have reached the depth
                return self.evaluationFunction(state)
            maximum = -999999.00
            for action in state.getLegalActions(0):
                maximum = max(maximum, expPhase(state.generateSuccessor(0, action), depth, 1))  # Call the EXP Phase for ghosts
            return maximum

        # Exp Phase

        def expPhase(state, depth, ghostRank):
            if state.isWin() or state.isLose():                                 # Check if PACMAN is alive
                return self.evaluationFunction(state)
            average = 0
            for action in state.getLegalActions(ghostRank):
                if ghostRank == gameState.getNumAgents() - 1:                   # Check to see if we are evaluating the last ghost as we have to call MAX for next PACMAN
                    average = average + (maxPhase(state.generateSuccessor(ghostRank, action), depth)) / len(state.getLegalActions(ghostRank))
                else:                                                           # ELSE We call exp phase again for the next Ghost
                    average = average + (expPhase(state.generateSuccessor(ghostRank, action), depth, ghostRank + 1)) / len(state.getLegalActions(ghostRank))
            return average

        # Body of expectimax starts here: #


        possibleActions = gameState.getLegalActions(0)      # All possible action of PACMAN from current state
        maximum = -999999.00
        maxAction = ''
        for action in possibleActions:
            depth = 0
            tempMax = expPhase(gameState.generateSuccessor(0, action), depth, 1)     # Call expPhase directly for the first ghost and hence starts the expectiMax function
            if tempMax > maximum or (tempMax == maximum and random.random() > .3):
                maximum = tempMax
                maxAction = action
        return maxAction                # Return action
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    heuristic = 0

    ghostDistances = []
    for gs in newGhostStates:
        ghostDistances += [manhattanDistance(gs.getPosition(), newPos)] # Get the manhattan distance between the current position and that of each Ghost and appemd to a list
    foodList = newFood.asList()         # Food co-ordinates as a list
    wallList = currentGameState.getWalls().asList() # Wall co-ordinates as a List
    emptyFoodNeighbors = 0
    foodDistances = []

    def foodNeighbors(foodPos):             # Function that identifies all the possible values of neighboring nodes in X,Y Format for a given position that has food
        foodNeighbors = []
        foodNeighbors.append((foodPos[0] - 1, foodPos[1]))
        foodNeighbors.append((foodPos[0], foodPos[1] - 1))
        foodNeighbors.append((foodPos[0], foodPos[1] + 1))
        foodNeighbors.append((foodPos[0] + 1, foodPos[1]))
        return foodNeighbors

    for f in foodList:                          # Loop for every food pallet, check then number of neighbors that have food in them as well
        neighbors = foodNeighbors(f)
        for fn in neighbors:
            if fn not in wallList and fn not in foodList:   # If it is a valid neighbor and no food is present, increment emptyFoodNeighbors by 1. This value should be low for the
                emptyFoodNeighbors += 1                     #  Pacman to visit it quicker as it can find a lot of food particles at the same time.
        foodDistances += [manhattanDistance(newPos, f)]
    inverseFoodDist = 0                     # Inverses the food distance by usinf the 1/foodDistances
    if len(foodDistances) > 0:
        inverseFoodDist = 1.0 / (min(foodDistances))
    heuristic += (min(ghostDistances) * ((inverseFoodDist ** 4)))       # Contants by experimentation only.
    heuristic += currentGameState.getScore() - (float(emptyFoodNeighbors) * 3)
    return heuristic        # Return Heuristic
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

