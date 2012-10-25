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
from math import exp

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='DoubleAgent', second='DoubleAgent'):
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
    
class AttackAgent(CaptureAgent):
    """
    You should look at baselineTeam.py for more details about how to
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
      
        actions = gameState.getLegalActions(self.index)
        # actions = [a for a in actions if a != Directions.STOP]
    
        previousPos = gameState.getAgentState(self.index).getPosition()

        foodGrid = self.getFood(gameState)
        foodList = foodGrid.asList()
        capsules = self.getCapsules(gameState)
      
        allies = [gameState.getAgentState(i) for i in self.getTeam(gameState)]
        hunters = [a for a in allies if a.isPacman and a.getPosition() != None]
        # defenders = [a for a in allies if not a.isPacman and a.getPosition() != None]
        
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        # invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      
        evalFunc = self.generateEvalFunc(self.generateOffensiveGaussians(foodList, foodGrid, capsules, hunters, ghosts))
    
        possibleCells = [self.getActionCoordinates(action, previousPos) for action in actions]
        actionPoints = [evalFunc(cell) for cell in possibleCells]
        
        if not actionPoints:
            return Directions.STOP
    
        maxValue = max(actionPoints)

#        for i in range(len(possibleCells)):
#            self.debugDraw(possibleCells[i], [actionPoints[i] / 60, 0, 0] if actionPoints[i] > 0 else [0, -actionPoints[i] / 250, 0], False) 
        
        bestActions = [a for a, v in zip(actions, actionPoints) if v == maxValue]

        return random.choice(bestActions)
    
    def getActionCoordinates(self, action, previousCoordinates):
        dx, dy = Actions.directionToVector(action)
        return (previousCoordinates[0] + dx, previousCoordinates[1] + dy)

    def generateOffensiveGaussians(self, foodList, foodGrid, capsules, hunters, ghosts):
        # def cellEvaluation(coordinates):
        #    return coordinates[0] + coordinates[1]
      
        self.chromoawesome = [20.0, 1.0, -150.0, 0.8, 200.0, 0.5, -5, 0.5, 22.0, 0.8, 100.0, 0.3]
        gaussians = []
      
        for food in foodList:
            gaussians.append(self.gaussian(self.chromoawesome[0], self.chromoawesome[1], food[0], food[1]))
            
            isLonely = True
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    isCellInGrid = (food[0] + i < foodGrid.width) and (food[0] + i >= 0) and (food[1] + j < foodGrid.height) and (food[1] + j) >= 0
                    if (i != 0 or j != 0) and isCellInGrid and foodGrid[food[0] + i][food[1] + j]:
                        isLonely = False
                        break
            
            if isLonely:
                gaussians.append(self.gaussian(self.chromoawesome[10], self.chromoawesome[11], food[0], food[1]))                            
            
        for capsule in capsules:
            gaussians.append(self.gaussian(self.chromoawesome[8], self.chromoawesome[9], capsule[0], capsule[1]))
      
        for ghost in ghosts:
            if ghost.scaredTimer == 0:
                gaussians.append(self.gaussian(self.chromoawesome[2], self.chromoawesome[3], ghost.getPosition()[0], ghost.getPosition()[1]))
            else:
                gaussians.append(self.gaussian(self.chromoawesome[4], self.chromoawesome[5], ghost.getPosition()[0], ghost.getPosition()[1]))
                
        for hunter in hunters:
            gaussians.append(self.gaussian(self.chromoawesome[6], self.chromoawesome[7], hunter.getPosition()[0], hunter.getPosition()[1]))
              
        return gaussians

    def generateEvalFunc(self, gaussians):
        def evalC(coordinate):
            return sumGaussians(coordinate[0], coordinate[1], gaussians)
        return evalC;
      
    def gaussian(self, A, sigma, x0, y0):
        def gaussianFunc(x, y):
            distance = self.getMazeDistance((x, y), (x0, y0))
            return A * exp(-(distance) / (2.0 * sq(sigma)))
        return gaussianFunc
    
    def setChromosome(self, chromosome):
        self.chromoawesome = chromosome
        
class DoubleAgent(CaptureAgent):

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
        
        actions = gameState.getLegalActions(self.index)
        # actions = [a for a in actions if a != Directions.STOP]
    
        previousPos = gameState.getAgentState(self.index).getPosition()

        foodGrid = self.getFood(gameState)
        foodList = foodGrid.asList()
        capsules = self.getCapsules(gameState)
        
        defenseFoodGrid = self.getFoodYouAreDefending(gameState)
        defenseFoodList = defenseFoodGrid.asList()
        defenseCapsules = self.getCapsulesYouAreDefending(gameState)
      
        allies = [gameState.getAgentState(i) for i in self.getTeam(gameState) if i != self.index]
        hunters = [a for a in allies if a.isPacman and a.getPosition() != None]
        defenders = [a for a in allies if not a.isPacman and a.getPosition() != None]
        
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      
        isPacman = gameState.getAgentState(self.index).isPacman
        amScared = gameState.getAgentState(self.index).scaredTimer != 0
        
        defendMode = False
        if not isPacman:
            if not defenders:
                defendMode = True
        
        if not defendMode:
            evalFunc = self.generateEvalFunc(self.generateOffensiveGaussians(foodList, foodGrid, capsules, hunters, ghosts))
        else:
            evalFunc = self.generateEvalFunc(self.generateDefenseGaussians(amScared, defenseFoodList, defenseCapsules, defenders, invaders))
            
        possibleCells = [self.getActionCoordinates(action, previousPos) for action in actions]
        actionPoints = [evalFunc(cell) for cell in possibleCells]
        
        if not actionPoints:
            return Directions.STOP
    
        maxValue = max(actionPoints)

#        for i in range(len(possibleCells)):
#            self.debugDraw(possibleCells[i], [actionPoints[i] / 60, 0, 0] if actionPoints[i] > 0 else [0, -actionPoints[i] / 250, 0], False) 
        
        bestActions = [a for a, v in zip(actions, actionPoints) if v == maxValue]

        return random.choice(bestActions)

    def generateOffensiveGaussians(self, foodList, foodGrid, capsules, hunters, ghosts):
        # def cellEvaluation(coordinates):
        #    return coordinates[0] + coordinates[1]
      
        chromoawesome = [20.0, 1.0, -150.0, 0.8, 200.0, 0.5, -5, 0.5, 22.0, 0.8, 100.0, 0.3]
        gaussians = []
      
        for food in foodList:
            gaussians.append(self.gaussian(chromoawesome[0], chromoawesome[1], food[0], food[1]))
            
            isLonely = True
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    isCellInGrid = (food[0] + i < foodGrid.width) and (food[0] + i >= 0) and (food[1] + j < foodGrid.height) and (food[1] + j) >= 0
                    if (i != 0 or j != 0) and isCellInGrid and foodGrid[food[0] + i][food[1] + j]:
                        isLonely = False
                        break
            
            if isLonely:
                gaussians.append(self.gaussian(chromoawesome[10], chromoawesome[11], food[0], food[1]))                            
            
        for capsule in capsules:
            gaussians.append(self.gaussian(chromoawesome[8], chromoawesome[9], capsule[0], capsule[1]))
      
        for ghost in ghosts:
            if ghost.scaredTimer == 0:
                gaussians.append(self.gaussian(chromoawesome[2], chromoawesome[3], ghost.getPosition()[0], ghost.getPosition()[1]))
            else:
                gaussians.append(self.gaussian(chromoawesome[4], chromoawesome[5], ghost.getPosition()[0], ghost.getPosition()[1]))
                
        for hunter in hunters:
            gaussians.append(self.gaussian(chromoawesome[6], chromoawesome[7], hunter.getPosition()[0], hunter.getPosition()[1]))
              
        return gaussians

    def generateDefenseGaussians(self, amScared, defenseFoodList, defenseCapsules, defenders, invaders):
        # def cellEvaluation(coordinates):
        #    return coordinates[0] + coordinates[1]
      
        chromoawesome = [20.0, 1.0, -150.0, 0.8, 200.0, 0.5, -5, 0.5, 22.0, 0.8, 100.0, 0.3,
                         10.0, 1.0, -150.0, 0.8, 300.0, 0.8, -5, 0.5, 22.0, 0.8, 100.0, 0.3]
        gaussians = []
      
        for food in defenseFoodList:
            gaussians.append(self.gaussian(chromoawesome[12], chromoawesome[13], food[0], food[1]))         
            
        for capsule in defenseCapsules:
            gaussians.append(self.gaussian(chromoawesome[20], chromoawesome[21], capsule[0], capsule[1]))
      
        for invader in invaders:
            if amScared:
                gaussians.append(self.gaussian(chromoawesome[14], chromoawesome[15], invader.getPosition()[0], invader.getPosition()[1]))
            else:
                gaussians.append(self.gaussian(chromoawesome[16], chromoawesome[17], invader.getPosition()[0], invader.getPosition()[1]))
                
        for defender in defenders:
            gaussians.append(self.gaussian(chromoawesome[18], chromoawesome[19], defender.getPosition()[0], defender.getPosition()[1]))
              
        return gaussians
    
    def getActionCoordinates(self, action, previousCoordinates):
        dx, dy = Actions.directionToVector(action)
        return (previousCoordinates[0] + dx, previousCoordinates[1] + dy)
    
    def generateEvalFunc(self, gaussians):
        def evalC(coordinate):
            return sumGaussians(coordinate[0], coordinate[1], gaussians)
        return evalC;
      
    def gaussian(self, A, sigma, x0, y0):
        def gaussianFunc(x, y):
            distance = self.getMazeDistance((x, y), (x0, y0))
            return A * exp(-(distance) / (2.0 * sq(sigma)))
        return gaussianFunc
    
    def setChromosome(self, chromosome):
        self.chromoawesome = chromosome

def sq(x):
    return x * x

def gaussianValueAt(x, y, g):
    return g(x, y)

def sumGaussians(x, y, gaussians):
    return sum([gaussianValueAt(x, y, gauss) for gauss in gaussians])    
