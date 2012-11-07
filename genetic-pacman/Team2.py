# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from search import findPathToClosestDot

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed, testGenome = ""):#, genome1, genome2):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  return [IntelligentAgent(firstIndex, 0), IntelligentAgent(secondIndex, 1)]

  # The following line is an example only; feel free to change it.
  

##########
# Agents #
##########

def helper(state, agentNum, depth, evalf):
    successors = []
    evalSuccessors = []
    if (state.isOver()):
        return (evalf(state, agentNum), Directions.STOP)
    
    if(depth == 0):
        return (evalf(state, agentNum), Directions.STOP)
    else:
        actions = state.getLegalActions(agentNum)

#        print ("Actions of agent #", agentNum, ":", actions)
        if(Directions.STOP in actions and len(actions) > 1):
            actions.remove(Directions.STOP)
        for action in actions:
            successors = successors + [(state.generateSuccessor(agentNum, action), action)]
            #sucessors = [ (resutlant_state, causing_action), ... ]
        #print ("Successors:", successors)
        for successor in successors:
            if(agentNum + 1 == state.getNumAgents()):
                evalSuccessors = evalSuccessors + [(helper(successor[0],            0, depth - 1, evalf)[0],successor[1])]
            else:
                evalSuccessors = evalSuccessors + [(helper(successor[0], agentNum + 1,     depth, evalf)[0],successor[1])]
        #evalSuccessors = [(value_of_new_state, action_to_get_to_this_new_state), ... ]
        if (agentNum == 0):
            extremeState = evalSuccessors[0]
            for evalS in evalSuccessors:
                if(extremeState[0] < evalS[0]):
                    extremeState = evalS
            #print(tuple(extremeState), " ; ", agentNum, " ; ", depth)
            return tuple(extremeState)
        else:
            val = 0
            for evalS in evalSuccessors:
                val += evalS[0]
            #print(tuple(extremeState), " ; ", agentNum, " ; ", depth)
            return (val/len(evalSuccessors),Directions.STOP)

def evalFn(currentGameState, agentNum):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    
    DESCRIPTION: 
    We decided on some values that would make a move more or less attractive. The base of our evaluation
    function is the game score. We penalized the gameState if
    -it was far from the closest food
    -there was a lot of food left
    -there are close ghosts
    -there are many power pellets left
    Then we adjusted the weight of each of these penalties until Pacman reigned supreme.
    -
    """
    
    print 'evaluation'
    red = currentGameState.isOnRedTeam(agentNum)
    pos = currentGameState.getAgentPosition(agentNum)
    newScore = currentGameState.getScore()
    
    if(red):
        currentFood = currentGameState.getBlueFood()
        ghostStates = currentGameState.getBlueTeamIndices()
        caps = currentGameState.getBlueCapsules()
    else:
        currentFood = currentGameState.getRedFood()
        ghostStates = currentGameState.getRedTeamIndices()
        newScore = -newScore
        caps = currentGameState.getRedCapsules()
        
    ghostStates = [currentGameState.getAgentState(x) for x in ghostStates]
    ghostStates = [x for x in ghostStates if not x.isPacman]
    
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    closestFood = len(findPathToClosestDot(currentGameState, agentNum, currentFood))
    ghostScore = 0
    goodGhost = 0
    distToClosestCap = 9999
    for i in range(len(ghostStates)):
        
        if (scaredTimes[i] < 3):
            ghostScore += max(0, 10 * (5 - manhattanDistance(pos, ghostStates[i].getPosition())))

    return newScore - closestFood - (len(currentFood.asList()) * 5) - (ghostScore * 5) - (50* len(caps))

def reEvaluateFood(actions, gameState, agentNum):
    if len(actions) == 0:
        return True
    if actions[0] not in gameState.getLegalActions(agentNum):
        return True
    return False

class IntelligentAgent(CaptureAgent):

  def __init__(self, index, genome):
    CaptureAgent.__init__(self,index,1)
    self.genome = genome

  def registerInitialState(self, gameState):
    CaptureAgent.registerInitialState(self,gameState)
    self.actions = []

  def chooseAction(self, gameState):
    """actions = gameState.getLegalActions(self.index)

    bestAction = Directions.STOP
    bestEvaluation = self.genome.getGenomeValue(gameState, self.index, False)

    foodCount = gameState.getRedFood().count() + gameState.getBlueFood().count()

    for a in actions:
      newState = gameState.generateSuccessor(self.index, a)
      newFood = newState.getRedFood().count() + newState.getBlueFood().count()

      newEvaluation = self.genome.getGenomeValue(newState, self.index, newFood < foodCount)

      if newEvaluation > bestEvaluation:
        bestEvaluation = newEvaluation
        bestAction = a

    return bestAction"""
    
    if(gameState.isOnRedTeam(self.index)):
        ourFood = gameState.getRedFood().asList()
        currentFood = gameState.getBlueFood().asList()
        currentFood += gameState.getBlueCapsules()
        ally = gameState.getAgentState([x for x in gameState.getRedTeamIndices() if x is not self.index][0])
        enemies = gameState.getBlueTeamIndices()
    else:
        ourFood = gameState.getBlueFood().asList()
        currentFood = gameState.getRedFood().asList()
        currentFood += gameState.getRedCapsules()
        ally = gameState.getAgentState([x for x in gameState.getBlueTeamIndices() if x is not self.index][0])
        enemies = gameState.getRedTeamIndices()
        
    myAgent = gameState.getAgentState(self.index)
    enemies = [gameState.getAgentState(x) for x in enemies]
    validActions = gameState.getLegalActions(self.index)
    
    enemyPacmen = [x for x in enemies if x.isPacman]
    enemyGhost = [x for x in enemies if (not x.isPacman) and x.scaredTimer==0]
    enemyScaredGhost = [x for x in enemies if (not x.isPacman) and x.scaredTimer>5]
    
    edibles = [x.getPosition() for x in enemyPacmen] + [x.getPosition() for x in enemyScaredGhost]
    
    if(len(edibles) > 0):
        pathClosestEatableEnemy = findPathToClosestDot(gameState, self.index, edibles)
    else:
        pathClosestEatableEnemy = range(100)
    
    if(len(enemyGhost) > 0):
        pathToClosestDeath = findPathToClosestDot(gameState, self.index, [x.getPosition() for x in enemyGhost])
    else:
        pathToClosestDeath = range(100)
    
    foodCount = len(currentFood)/2

    currentFood = sorted(currentFood, key = lambda x: x[1])


    if(myAgent.getPosition()[1] < ally.getPosition()[1]):
        currentFood = currentFood[0:foodCount]
    else:
        currentFood = currentFood[foodCount:]
    
    if(reEvaluateFood(self.actions, gameState, self.index)):
        self.actions = findPathToClosestDot(gameState, self.index, currentFood)

    if self.actions is None:
        self.actions = [Directions.STOP]

    if len(self.actions) is 0:
        self.actions = [Directions.STOP]

    if(pathClosestEatableEnemy != None):
        if(len(pathClosestEatableEnemy) < len(self.actions)):
            self.actions = pathClosestEatableEnemy
    
    if pathToClosestDeath is not None: 
        if len(pathToClosestDeath) < 3:
            validActions.remove(self.actions[0])
            if len(validActions) > 1 and Directions.STOP in validActions:
                validActions.remove(Directions.STOP)
         
            distance = 0
            
            for action in validActions:
                state = gameState.generateSuccessor(self.index, action)
                ourPos = state.getAgentState(self.index).getPosition()
                newDeath = len(findPathToClosestDot(gameState, self.index, [x.getPosition() for x in enemyGhost]))
                if newDeath > distance:
                    distance = newDeath
                    self.actions = [action]
   

    currentAction = self.actions[0]
    self.actions = self.actions[1:]
    return currentAction

