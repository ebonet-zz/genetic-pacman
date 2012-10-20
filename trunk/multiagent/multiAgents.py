# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

def myAwesomeEvaluationFunction(currentGameState, action):
    # Useful information you can extract from a GameState (pacman.py)
    
    oldPacmanPos = currentGameState.getPacmanPosition()
    oldNumFood = currentGameState.getNumFood()
    oldGhostPositions = currentGameState.getGhostPositions()
    oldRemainingCapsules = currentGameState.getCapsules()
    oldGhostStates = currentGameState.getGhostStates()
    oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
    
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPacmanPos = successorGameState.getPacmanPosition()
    newRemainingFood = successorGameState.getFood()
    newRemainingFoodPos = newRemainingFood.asList()
    newNumFood = successorGameState.getNumFood()
    newRemainingCapsules = successorGameState.getCapsules()
    
    newStateScore = 0
    
    #basics
    if successorGameState.isLose() or newPacmanPos == oldPacmanPos:
        return 0
    if successorGameState.isWin():
        return 99999999
    
    #higher is more likely to give priority
    penaltyForBeingInDanger = 1024.0;
    pointsForApproachingCapsulesWhenInDanger = 512
    pointsForEatingFood = 8
    dividingNumberForApproachingFoodDistance = 4.0;
    
    ghostNearbyRangeForNormalState = 2 #range
    
    avoidingGhostsPoints = 0
    approachingCapsulesPoints = 0
    approachingFoodPoints = 0
    eatingFoodPoints = 0
    
    # give points for approaching food
    newFoodDistances = [manhattanDistance(newRemainingFoodPos[index], newPacmanPos) for index in range(len(newRemainingFoodPos))]
    for i in range(len(newFoodDistances)):
        approachingFoodPoints = approachingFoodPoints + (dividingNumberForApproachingFoodDistance / newFoodDistances[i])
    
    # give points for eating food
    if newNumFood < oldNumFood:
        eatingFoodPoints = eatingFoodPoints + pointsForEatingFood 
        
    # give points for eating pellets
    if len(newRemainingCapsules) < len(oldRemainingCapsules):
        eatingFoodPoints = eatingFoodPoints + pointsForEatingFood + 1
        
    newGhostDistances = [manhattanDistance(oldGhostPositions[index], newPacmanPos) for index in range(len(oldGhostPositions))]
            
    anyScaredGhosts = False
    for i in range(len(oldScaredTimes)):
        if oldScaredTimes[i] > 1:
            anyScaredGhosts = True
            break
            
    if not anyScaredGhosts:
        # normal 
        ghostsNearbyIndices = [index for index in range(len(newGhostDistances)) if newGhostDistances[index] < ghostNearbyRangeForNormalState]
        if ghostsNearbyIndices:
            # There is a ghost nearby
            for i in range(len(ghostsNearbyIndices)): # for each ghost nearby
                newGhostDistance = newGhostDistances[i]
                # apply penalty for being close to a ghost
                avoidingGhostsPoints = avoidingGhostsPoints - (penaltyForBeingInDanger / (newGhostDistance + 0.1))
                    
            if oldRemainingCapsules and newPacmanPos in oldRemainingCapsules:
                # there are capsules
                # give points for approaching capsules when ghosts nearby
                approachingCapsulesPoints = approachingCapsulesPoints + pointsForApproachingCapsulesWhenInDanger

    newStateScore = newStateScore + avoidingGhostsPoints + approachingCapsulesPoints + eatingFoodPoints + approachingFoodPoints
    return newStateScore


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
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    return myAwesomeEvaluationFunction(currentGameState, action)

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

  def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  
  def Minimax(self, gameState, player, currentDepth):
    #Let Move be an object corresponding to a move, ScoredMove be an
    #object corresponding to a Move and its score.
    #Then:
    bestSoFar = (Directions.STOP, 0); # default
    
    # If the game is over, return a fake move and the score
    if gameState.isWin() or gameState.isLose() or currentDepth > self.depth:
        return (Directions.STOP, self.evaluationFunction(gameState));
    
    # We set scores initially out of range so as to ensure we will
    # get a move
    if player == 0:
        bestSoFar = (Directions.STOP, -9999999);
    else:
        bestSoFar = (Directions.STOP, 9999999);

    moves = gameState.getLegalActions(player)
    
    for m in range(len(moves)):
        move = moves[m]
        if move != Directions.STOP:
            nextGameState = gameState.generateSuccessor(player, move)
            nextPlayer = (player + 1) % gameState.getNumAgents()
            nextDepth = currentDepth
            if nextPlayer == 0:
                nextDepth = nextDepth + 1
                
            result = self.Minimax(nextGameState, nextPlayer, nextDepth)
                
            if player != 0 and result[1] < bestSoFar[1]:
                bestSoFar = (move, result[1]); # new best move
            elif player == 0 and result[1] > bestSoFar[1]:
                bestSoFar = (move, result[1]);
                    
    return bestSoFar;
      

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    
    minimax = self.Minimax(gameState, 0, 1)
    
    return minimax[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  
  def ABMinimax(self, gameState, player, currentDepth, alpha, beta):
    #Let Move be an object corresponding to a move, ScoredMove be an
    #object corresponding to a Move and its score.
    #Then:
    bestSoFar = (Directions.STOP, 0); # default
    
    # If the game is over, return a fake move and the score
    if gameState.isWin() or gameState.isLose() or currentDepth > self.depth:
        return (Directions.STOP, self.evaluationFunction(gameState));
    
    # We set scores initially out of range so as to ensure we will
    # get a move
    if player == 0:
        bestSoFar = (Directions.STOP, alpha);
    else:
        bestSoFar = (Directions.STOP, beta);

    moves = gameState.getLegalActions(player)
    
    for m in range(len(moves)):
        move = moves[m]
        if move != Directions.STOP:
            nextGameState = gameState.generateSuccessor(player, move)
            nextPlayer = (player + 1) % gameState.getNumAgents()
            nextDepth = currentDepth
            if nextPlayer == 0:
                nextDepth = nextDepth + 1
                
            result = self.ABMinimax(nextGameState, nextPlayer, nextDepth, alpha, beta)
                
            if player != 0 and result[1] < bestSoFar[1]:
                bestSoFar = (move, result[1]); # new best move
            elif player == 0 and result[1] > bestSoFar[1]:
                bestSoFar = (move, result[1]);
            
            if alpha >= beta:
                return bestSoFar;
                    
    return bestSoFar;

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    aplhaBeta = self.ABMinimax(gameState, 0, 1, -9999999, 9999999)
    
    return aplhaBeta[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  
  def Expectimax(self, gameState, player, currentDepth):
    #Let Move be an object corresponding to a move, ScoredMove be an
    #object corresponding to a Move and its score.
    #Then:
    bestSoFar = (Directions.STOP, 0); # default
    
    # If the game is over, return a fake move and the score
    if gameState.isWin() or gameState.isLose() or currentDepth > self.depth:
        return (Directions.STOP, self.evaluationFunction(gameState));
    
    # We set scores initially out of range so as to ensure we will
    # get a move
    if player == 0:
        bestSoFar = (Directions.STOP, -9999999);
    else:
        bestSoFar = (Directions.STOP, 9999999);

    moves = gameState.getLegalActions(player)
    if moves.count(Directions.STOP) > 0:
        moves.remove(Directions.STOP)
    
    results = []
    for m in range(len(moves)):
        move = moves[m]
        nextGameState = gameState.generateSuccessor(player, move)
        nextPlayer = (player + 1) % gameState.getNumAgents()
        nextDepth = currentDepth
        if nextPlayer == 0:
            nextDepth = nextDepth + 1
            
        result = self.Expectimax(nextGameState, nextPlayer, nextDepth)
        results.append(result[1])
            
        if player == 0 and result[1] > bestSoFar[1]:
            bestSoFar = (move, result[1]);
    
    if player != 0:
        return (move, sum(results) / len(moves)); # new best move
            
    return bestSoFar;

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    expectimax = self.Expectimax(gameState, 0, 1)
    
    return expectimax[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
    
      DESCRIPTION: <write something here so we know what you did>
    """
    
    # Useful information you can extract from a GameState (pacman.py)
    
    oldPacmanPos = currentGameState.getPacmanPosition()
    oldNumFood = currentGameState.getNumFood()
    oldGhostPositions = currentGameState.getGhostPositions()
    oldRemainingCapsules = currentGameState.getCapsules()
    oldGhostStates = currentGameState.getGhostStates()
    oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
    oldRemainingFood = currentGameState.getFood()
    oldRemainingFoodPos = oldRemainingFood.asList()
    
    newStateScore = 0
    
    #basics
    if currentGameState.isLose():
        return 0
    if currentGameState.isWin():
        return 99999999
    
    #higher is more likely to give priority
    penaltyForBeingInDanger = 1024.0;
    dividingNumberForApproachingFoodDistance = 4.0
    dividingNumberForApproachingPellets = 100.0
    
    ghostNearbyRangeForNormalState = 2 #range
    
    avoidingGhostsPoints = 0
    approachingCapsulesPoints = 0
    approachingFoodPoints = 0
    eatingFoodPoints = 0
    
    # give points for approaching food
    newFoodDistances = [manhattanDistance(oldRemainingFoodPos[index], oldPacmanPos) for index in range(len(oldRemainingFoodPos))]
    for i in range(len(newFoodDistances)):
        approachingFoodPoints = approachingFoodPoints + (dividingNumberForApproachingFoodDistance / newFoodDistances[i]) 
        
    #penalize for too much food
    approachingFoodPoints = approachingFoodPoints + (dividingNumberForApproachingFoodDistance / oldNumFood)     
    approachingFoodPoints = approachingFoodPoints + (dividingNumberForApproachingPellets / (len(oldRemainingCapsules) + 0.1))     
    
    newGhostDistances = [manhattanDistance(oldGhostPositions[index], oldPacmanPos) for index in range(len(oldGhostPositions))]
            
    anyScaredGhosts = False
    for i in range(len(oldScaredTimes)):
        if oldScaredTimes[i] > 1:
            anyScaredGhosts = True
            break
            
    if not anyScaredGhosts:
        # normal 
        ghostsNearbyIndices = [index for index in range(len(newGhostDistances)) if newGhostDistances[index] < ghostNearbyRangeForNormalState]
        if ghostsNearbyIndices:
            # There is a ghost nearby
            for i in range(len(ghostsNearbyIndices)): # for each ghost nearby
                newGhostDistance = newGhostDistances[i]
                # apply penalty for being close to a ghost
                avoidingGhostsPoints = avoidingGhostsPoints - (penaltyForBeingInDanger / (newGhostDistance + 0.1))
                    
    newStateScore = newStateScore + avoidingGhostsPoints + approachingCapsulesPoints + eatingFoodPoints + approachingFoodPoints
    return newStateScore + currentGameState.getScore()
  
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def ABMinimax(self, gameState, player, currentDepth, alpha, beta):
    #Let Move be an object corresponding to a move, ScoredMove be an
    #object corresponding to a Move and its score.
    #Then:
    bestSoFar = (Directions.STOP, 0); # default
    
    # If the game is over, return a fake move and the score
    if gameState.isWin() or gameState.isLose() or currentDepth > self.depth:
        return (Directions.STOP, betterEvaluationFunction(gameState));
    
    # We set scores initially out of range so as to ensure we will
    # get a move
    if player == 0:
        bestSoFar = (Directions.STOP, alpha);
    else:
        bestSoFar = (Directions.STOP, beta);

    moves = gameState.getLegalActions(player)
    
    for m in range(len(moves)):
        move = moves[m]
        if move != Directions.STOP:
            nextGameState = gameState.generateSuccessor(player, move)
            nextPlayer = (player + 1) % gameState.getNumAgents()
            nextDepth = currentDepth
            if nextPlayer == 0:
                nextDepth = nextDepth + 1
                
            result = self.ABMinimax(nextGameState, nextPlayer, nextDepth, alpha, beta)
                
            if player != 0 and result[1] < bestSoFar[1]:
                bestSoFar = (move, result[1]); # new best move
            elif player == 0 and result[1] > bestSoFar[1]:
                bestSoFar = (move, result[1]);
            
            if alpha >= beta:
                return bestSoFar;
                    
    return bestSoFar;

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    aplhaBeta = self.ABMinimax(gameState, 0, 1, -9999999, 9999999)
    
    return aplhaBeta[0]

