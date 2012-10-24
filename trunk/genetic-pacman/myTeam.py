# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions, Grid, Actions
import game
from sys import maxint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='MyAgent', second='MyAgent'):
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
class gameGrid:
    def __init__(self, grid):
        self.grid = grid.copy()
        self.height = grid.height
        self.width = grid.width
        
    def setPoints(self, coordinateTuple, points):
        if self.grid[int(coordinateTuple[0])][int(coordinateTuple[1])] != True:
            self.grid[int(coordinateTuple[0])][int(coordinateTuple[1])] = points
        
    def getPoints(self, coordinateTuple):
        if self.grid[int(coordinateTuple[0])][int(coordinateTuple[1])] != True:
            return self.grid[int(coordinateTuple[0])][int(coordinateTuple[1])]
        return -maxint    
    
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

    return random.choice(actions)

##################################
#           My Team              #
##################################

class MyAgent(CaptureAgent):
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

    ''' 
    Your initialization code goes here, if you need any.
    '''
    self.grid = gameGrid(gameState.getWalls())

  def chooseAction(self, gameState):
      
    actions = gameState.getLegalActions(self.index)
    
    previousPos = gameState.getAgentState(self.index).getPosition()

    self.updateGrid(gameState)
    
    possibleCells = [self.getActionCoordinates(action, previousPos) for action in actions]
    
    actionPoints = [self.grid.getPoints(cell) for cell in possibleCells]
    
    if not actionPoints:
        return Directions.STOP
    
    maxValue = max(actionPoints)
    bestActions = [a for a, v in zip(actions, actionPoints) if v == maxValue]

    return random.choice(bestActions)
    
  def updateGrid(self, gameState):
      for y in range(self.grid.height):
          for x in range(self.grid.width):
              self.grid.setPoints((x, y), x + y)
      
  def getActionCoordinates(self, action, previousCoordinates):
      dx, dy = Actions.directionToVector(action)
      return (previousCoordinates[0] + dx, previousCoordinates[1] + dy)
        
    
def getStateScore(captureAgent, selfgameState, importances):
    
    finalScore = 0;

    if captureAgent.isPacman():
        finalScore += importances[0] * getScoreForDistanceToClosesGhost();
        finalScore += importances[1] * getScoreForFoodProximity();
        finalScore += importances[2] * getScoreForNotLeavingIsolatedFood();
        finalScore += importances[3] * getScoreForProximityToCapsule();
        finalScore += importances[4] * getScoreForProximityToAlliedPacman();
        finalScore += importances[5] * getScoreForChangeToDefense();
        finalScore += importances[6] * getScoreForSearchRegion();
        
    else:
        finalScore += importances[7] * getScoreForDefenseAreaSize();
        finalScore += importances[8] * getScoreForPatrolling();
        finalScore += importances[9] * getScoreForWalkOverFood();
        finalScore += importances[10] * getScoreForChasing();
        finalScore += importances[11] * getScoreForProtectingPaths();
        finalScore += importances[12] * getScoreForProtectingCapsules();
        finalScore += importances[13] * getScoreForProximityToAlliedGhost();
        
    return finalScore;

def getScoreForDistanceToClosesGhost():
    return 0;

def getScoreForFoodProximity():
    return 0;
    
def getScoreForNotLeavingIsolatedFood():
    return 0;

def getScoreForProximityToCapsule():
    return 0;

def getScoreForProximityToAlliedPacman():
    return 0;

def getScoreForChangeToDefense():
    return 0;

def getScoreForSearchRegion():
    return 0;

def getScoreForDefenseAreaSize():
    return 0;

def getScoreForPatrolling():
    return 0;

def getScoreForWalkOverFood():
    return 0;

def getScoreForChasing():
    return 0;

def getScoreForProtectingPaths():
    return 0;

def getScoreForProximityToAlliedGhost():
    return 0;

def getScoreForProtectingCapsules():
    return 0;
    
    
