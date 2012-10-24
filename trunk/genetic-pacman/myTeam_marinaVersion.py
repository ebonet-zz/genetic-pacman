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
import sys
from util import nearestPoint
import math

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
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

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########
class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}

class DummyAgent(CaptureAgent):
    """
      A Dummy agent to serve as an example of the necessary agent structure.
      You should look at baselineTeam.py for more details about how to
      create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on). 
        
        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)
    
        IMPORTANT: This method may run for at most 15 seconds.
        """
    
        ''' 
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py. 
        '''
        CaptureAgent.registerInitialState(self, gameState)
        
        self.area = self.getFoodYouAreDefending(gameState).asList()  # To be calculated
        self.initialNumberOfFoodToProtect = len(self.getFoodYouAreDefending(gameState).asList())
        self.previousAction = None
        ''' 
        Your initialization code goes here, if you need any.
        '''


    def chooseAction(self, gameState):
        """
        Picks among actions randomly.
        """
        actions = gameState.getLegalActions(self.index)
    
        ''' 
        You should change this in your own agent.
        '''
        bestActions = []
        maxScore = -sys.maxint
        for action in actions:
            if action == Directions.STOP:
                continue
            nextState = gameState.generateSuccessor(self.index, action)
            score = self.evalFunction(nextState)
            if score > maxScore:
                maxScore = score
                bestActions = [action]
            elif score == maxScore:
                bestActions.append(action)
        if len(bestActions) > 1:
            result = bestActions[random.randint(0, len(bestActions)-1)]
            while result == self.previousAction:
                result = bestActions[random.randint(0, len(bestActions)-1)]
        else:
            result = bestActions[0]
            
        self.previousAction = result
        return result


    def evalFunction(self, gameState):
        rewardForWalkingOnFood = 10
        rewardForClosenessToEnemy = 50
        rewardForStayingInDefenseArea = 2
        penaltyForBeingInDanger = 200
        weightOfNumberOfInvaders = -50
        penaltyForStopping = -30
        rewardForDefending = 100
        
        sufficientNumberOfFood = True
        numberOfFoodLeftToProtect = self.getFoodYouAreDefending(gameState)
        if numberOfFoodLeftToProtect < self.initialNumberOfFoodToProtect / 2:
            sufficientNumberOfFood = False
    
        isGhost = 1
        myState = gameState.getAgentState(self.index)
        if myState.isPacman:
            isGhost = 0

        selfPosition = gameState.getAgentPosition(self.index)

        
        isStopped = 0
        previousState = self.getCurrentObservation()
        print previousState
        print gameState
        
        if previousState != None:
            previousPos = previousState.getAgentPosition(self.index)
            if selfPosition == previousPos:
                isStopped = 1
        
            
        if sufficientNumberOfFood:
            # TODO: make agent go for food instead of defending
            goForFood = 1
                
        closenessToFoodArea = self.distanceToArea(gameState)
        closenessCoeff = 1.0 / (closenessToFoodArea + 0.1)
        enemiesStates = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        invaders = [a for a in enemiesStates if a.isPacman and a.getPosition() != None]
        numberOfInvaders = len(invaders)

        
        enemies = self.getOpponents(gameState)
        levelOfDanger = 0
        enemiesForChasing = 0
        
        for enemy in enemies:
            enemyState = gameState.getAgentState(enemy)
            enemyScaredTime = enemyState.scaredTimer
            enemyPosition = gameState.getAgentPosition(enemy)

            if enemyPosition != None:
                # it is observable, so not too far away
                distanceToEnemy = self.getMazeDistance(selfPosition, enemyPosition)
                if enemyScaredTime > 0:
                    # run
                    if distanceToEnemy == 0:
                        return -sys.maxint / 2.0 # RUN
                    levelOfDanger = levelOfDanger - 1.0 / (distanceToEnemy + 0.1) # should be negative in order to be a penalty
                else:
                    if distanceToEnemy == 0:
                        return sys.maxint / 2.0 # EAT IT!
                    enemiesForChasing = enemiesForChasing + 1.0 / (distanceToEnemy + 0.1)
        
        walkingOnFood = 0
        x,y = selfPosition
        if self.getFoodYouAreDefending(gameState)[x][y]:
            walkingOnFood = 1
             
        result = closenessCoeff * rewardForStayingInDefenseArea + levelOfDanger * penaltyForBeingInDanger + numberOfInvaders * weightOfNumberOfInvaders
        result = result + enemiesForChasing * rewardForClosenessToEnemy + walkingOnFood * rewardForWalkingOnFood + isGhost * rewardForDefending #+ penaltyForStopping * isStopped
        return result
    
    def distanceToArea(self, gameState):
        '''
        :rtype: distance from closest food
        '''
        agentPosition = gameState.getAgentPosition(self.index)
        distances = [self.getMazeDistance(food, agentPosition) for food in self.area]
        return min(distances)
        
    
    