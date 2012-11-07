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
# from test.pickletester import MyStr

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='GeneticAgent', second='GeneticAgent2'):
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


class GeneticAgent(CaptureAgent):
  
  def __init__(self, index):
    print("Agent 1")
    # weightList = [0.004982152049084192, 0.08286448689091214, 0.09861639174094662, 0.045172303531868595, 0.004569002511278474, 0.21967119376033742, 0.31360050423585645, 0.007197877622700905, 0.0039965615285935795, 0.014530753330826242, 0.010880580183025821, 0.01661487974004077, 0.0008655625469600981, 0.005083041191514647, 0.00474438265180724, 0.08577710307918396, 0.026591797977987896, 0.01732568655346677, 0.01740478829637864, 0.005370947070373622, 0.002084185084571211, 0.012055818422284672]
    weightList = [0.0009297522592335832, 0.0003143461402194751, 0.04350540750799075, 0.05911730446834428, 0.2900446908924417, 0.07882342187834714, 0.0005007831176437158, 0.002573928515440776, 0.000142874854018344, 0.041815279885317476, 0.00918878103786739, 0.032692363818152395, 0.02665355877195833, 0.005027584855513291, 0.0009335045800774498, 0.00014965495281564348, 0.004561300446332249, 0.09113851994787965, 0.00020250612169947995, 0.10022991703559667, 0.11194284242921972, 0.0989120407695277, 8.191734655416286e-05, 0.0005177183678087127]
    """
    Lists several variables you can query:
    self.index = index for this agent
    self.red = true if you're on the red team, false otherwise
    self.agentsOnTeam = a list of agent objects that make up your team
    self.distancer = distance calculator (contest code provides this)
    self.observationHistory = list of GameState objects that correspond
        to the sequential order of states that have occurred so far this game
    self.timeForComputing = an amount of time to give each turn for computing maze distances
        (part of the provided distance calculator)
    """
    # Agent index for querying state
    self.index = index

    # Whether or not you're on the red team
    self.red = None

    # Agent objects controlling you and your teammates
    self.agentsOnTeam = None

    # Maze distance calculator
    self.distancer = None

    # A history of observations
    self.observationHistory = []

    # Time to spend each turn on computing maze distances
    self.timeForComputing = .1  # timeForComputing

    # Access to the graphics
    self.display = None
    self.FoodHuntingWeight = weightList[0]
    self.ScoreWeight = weightList[1]
    self.PacmanHunterWeight = weightList[2]
    self.PreventingWeight = weightList[3]
    self.EatingGhost = weightList[4]
    self.RunningGhost = weightList[5]
    self.CapsuleWeight = weightList[6]
    self.CountDownWeight = weightList[7]
    self.BorderWeight = weightList[8]
    self.PathesWeight = weightList[9]
    self.SeperationWeight = weightList[10]
    self.RandomWeight = weightList[11]
      
      
      
  def chooseAction(self, gameState):
      
      
      actions = gameState.getLegalActions(self.index)
      actions.remove(Directions.STOP)
      if actions:
          max = actions[0] 
          maxVal = self.evaluateAction(actions[0], gameState)
          for a in actions: 
              currentVal = self.evaluateAction(a, gameState)
              # print("max value is: ", maxVal)
              # print("current value is: ")
              if  currentVal > maxVal: 
                  maxVal = currentVal
                  max = a
          return max
      return 

  def evaluateAction(self, action, gameState):
      successor = gameState.generateSuccessor(self.index, action)
      # score calculations
      score = successor.getScore()
      sum = 0;
      # print("score :", score)
      if self.red: 
          sum = score * self.ScoreWeight * 10
      else:
          sum = -score * self.ScoreWeight * 10
      # food calculations
      newFood = self.getFood(gameState)
      spots = []
      foodDistances = []
      count = 0
      for f in newFood:
        c = 0
        for ff in f: 
            if newFood[count][c]:
                spots.append((count, c))
            c = c + 1
        count = count + 1
      for s in spots: 
          foodDistances.append(self.getMazeDistance(successor.getAgentState(self.index).getPosition(), s))
      # print("min food distance is: ", min(foodDistances))
      sum = sum - (min(foodDistances)) * self.FoodHuntingWeight
      # capsule calculations
      count = 0 
      newCapsules = self.getCapsules(gameState) 
      capsuleDistances = []
      sucPos = successor.getAgentPosition(self.index)
      for s in newCapsules: 
          capsuleDistances.append(self.getMazeDistance(sucPos, s))
      if capsuleDistances:
          sum = sum - (min(capsuleDistances)) * self.CapsuleWeight
      # food defending calculations
      en = self.getOpponents(gameState)
      tspots = []
      tfood = self.getFood(successor)
      count = 0
      for f in tfood:
        c = 0
        for ff in f: 
            if tfood[count][c]:
                tspots.append((count, c))
            c = c + 1
        count = count + 1
      enFoodCount = len(tspots)
      # print("enFoodCount is: ", enFoodCount)
      sum = sum - (enFoodCount * self.CountDownWeight)
      enemyClosest = []
      for x in en:
        tempSpots = []
        for z in tspots:
          tempSpots.append((self.getMazeDistance(z, gameState.getAgentPosition(x)), z))
        enemyClosest.append(self.getMazeDistance(min(tempSpots)[1], successor.getAgentPosition(self.index)))
      enemyDistToDot = min(enemyClosest)
      # print("EnemyDistToDot ", enemyDistToDot)
      sum = sum - enemyDistToDot * self.PreventingWeight
      # seperation calculations
      team = self.getTeam(gameState)
      teamDistance = self.getMazeDistance(successor.getAgentPosition(team[0]), successor.getAgentPosition(team[1]))
      # print("TeamDistance is: ", teamDistance)
      sum = sum + teamDistance * self.SeperationWeight
      # pathes calculation
      numMoves = len(successor.getLegalActions(self.index))
#      if successor.getAgentPosition(self.index) in self.getFood(gameState).asList():
#          numMoves = 5
      sum = sum + numMoves * self.PathesWeight
      # fleeing and attacking ghosts
      attack = successor.getWalls().width + successor.getWalls().height
      flee = 5
      opponents = self.getOpponents(gameState)
      myState = successor.getAgentState(self.index)
      for opponent in opponents:
          opponentState = gameState.getAgentState(opponent)
          if (not opponentState.isPacman) and opponentState.scaredTimer != 0:
              attack = min(attack, self.getMazeDistance(successor.getAgentPosition(self.index), gameState.getAgentPosition(opponent)))
          if ((not myState.isPacman) and myState.scaredTimer != 0) or (myState.isPacman and (not opponentState.isPacman) and opponentState.scaredTimer == 0):
              flee = min(flee, self.getMazeDistance(successor.getAgentPosition(self.index), gameState.getAgentPosition(opponent)))
      
      # print("attack is: ", attack, " flee is: ", flee)
      sum = sum - (attack * self.EatingGhost) + (flee * self.RunningGhost)
      # border calculations  
      borderDist = 9999999999999999999
      walls = successor.getWalls()
      colorshift = 0
      if self.red:
          colorshift = -1
      for i in range(0, walls.height):
          if not walls[walls.width / 2][i]:
              borderDist = min(borderDist, self.getMazeDistance(successor.getAgentPosition(self.index), (walls.width / 2 + colorshift, i)))
      sum = sum - borderDist * self.BorderWeight

      
      attack = successor.getWalls().width + successor.getWalls().height
      opponents = self.getOpponents(gameState)
      myState = successor.getAgentState(self.index)
      for opponent in opponents:
          opponentState = gameState.getAgentState(opponent)
          if opponentState.isPacman and (myState.isPacman or myState.scaredTimer == 0):
              attack = min(attack, self.getMazeDistance(successor.getAgentPosition(self.index), gameState.getAgentPosition(opponent)))
      sum -= attack * self.PacmanHunterWeight

      sum += random.random() * 10 * self.RandomWeight
      op1d = self.getMazeDistance(successor.getAgentPosition(self.index), successor.getAgentPosition(opponents[0]))
      op2d = self.getMazeDistance(successor.getAgentPosition(self.index), successor.getAgentPosition(opponents[1])) 
#      if  op1d > op2d :
#          if successor.getAgentState(opponents[1]).isPacman:
#              #print("op1d is: ", op1d)
#              if successor.getAgentState(self.index).isPacman:
#                  sum = sum  - (op1d * self.PacmanHunterWeight)
#      else: 
#          if successor.getAgentState(opponents[0]).isPacman: 
#              if successor.getAgentState(self.index).isPacman:
#                  sum = sum - (op2d * self.PacmanHunterWeight)
              # print("op2d is: ", op2d)
#      print("sum is: ", sum)
      return sum
          
        
class GeneticAgent2(GeneticAgent):
  def __init__(self, index):
    print("Agent2")
    # weightList = [0.004982152049084192, 0.08286448689091214, 0.09861639174094662, 0.045172303531868595, 0.004569002511278474, 0.21967119376033742, 0.31360050423585645, 0.007197877622700905, 0.0039965615285935795, 0.014530753330826242, 0.010880580183025821, 0.01661487974004077, 0.0008655625469600981, 0.005083041191514647, 0.00474438265180724, 0.08577710307918396, 0.026591797977987896, 0.01732568655346677, 0.01740478829637864, 0.005370947070373622, 0.002084185084571211, 0.012055818422284672]
    weightList = [0.02665355877195833, 0.005027584855513291, 0.0009335045800774498, 0.00014965495281564348, 0.004561300446332249, 0.09113851994787965, 0.00020250612169947995, 0.10022991703559667, 0.11194284242921972, 0.0989120407695277, 8.191734655416286e-05, 0.0005177183678087127]
    """
    Lists several variables you can query:
    self.index = index for this agent
    self.red = true if you're on the red team, false otherwise
    self.agentsOnTeam = a list of agent objects that make up your team
    self.distancer = distance calculator (contest code provides this)
    self.observationHistory = list of GameState objects that correspond
        to the sequential order of states that have occurred so far this game
    self.timeForComputing = an amount of time to give each turn for computing maze distances
        (part of the provided distance calculator)
    """
    # Agent index for querying state
    self.index = index

    # Whether or not you're on the red team
    self.red = None

    # Agent objects controlling you and your teammates
    self.agentsOnTeam = None

    # Maze distance calculator
    self.distancer = None

    # A history of observations
    self.observationHistory = []

    # Time to spend each turn on computing maze distances
    self.timeForComputing = .1  # timeForComputing

    # Access to the graphics
    self.display = None
    self.FoodHuntingWeight = weightList[0]
    self.ScoreWeight = weightList[1]
    self.PacmanHunterWeight = weightList[2]
    self.PreventingWeight = weightList[3]
    self.EatingGhost = weightList[4]
    self.RunningGhost = weightList[5]
    self.CapsuleWeight = weightList[6]
    self.CountDownWeight = weightList[7]
    self.BorderWeight = weightList[8]
    self.PathesWeight = weightList[9]
    self.SeperationWeight = weightList[10]
    self.RandomWeight = weightList[11]
















class AlphaBetaAgent(CaptureAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  def __init__(self, index):
    # Agent index for querying state
    self.index = index

    # Whether or not you're on the red team
    self.red = None

    # Agent objects controlling you and your teammates
    self.agentsOnTeam = None

    # Maze distance calculator
    self.distancer = None

    # A history of observations
    self.observationHistory = []

    # Time to spend each turn on computing maze distances
#    self.timeForComputing = timeForComputing

    # Access to the graphics
    self.display = None

  def chooseAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    
    x = self.process(gameState, self.index, 2, (1, 0, Directions.STOP), (-1, 0, Directions.STOP))
    return x[1]

  def process(self, state, agentIndex, ply, minimum, maximum):
    if ply == 0 and agentIndex == self.index:
        return (self.evaluationFunction(state, agentIndex), Directions.STOP)
    if agentIndex == state.getNumAgents():
        return self.process(state, 0, ply - 1, minimum, maximum)
    if agentIndex % 2 == 0:
        current = (-1, 0, Directions.STOP)
    else:
        current = (1, 0, Directions.STOP)
    for action in state.getLegalActions(agentIndex):
        if agentIndex % 2 == 0:
            current = max(current, (0, self.process(state.generateSuccessor(agentIndex, action), agentIndex + 1, ply, minimum, max(current, maximum))[0], action))
            if current > minimum:
                break
        else:
            current = min(current, (0, self.process(state.generateSuccessor(agentIndex, action), agentIndex + 1, ply, min(current, minimum), maximum)[0], action))
            if current < maximum:
                break
    if current[0] != 0:
        return (self.evaluationFunction(state, agentIndex), Directions.STOP)
    return (current[1], current[2])

  def evaluationFunction(self, currentGameState, agentIndex):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getAgentPosition(agentIndex)
    Food = self.getFood(currentGameState)
    opponents = self.getOpponents(currentGameState)
    
#    if newPos[0]>=8 and newPos[0]<=11 and newPos[0] == 5:
#        return 0
    
    for opponent in opponents:
        ghostPos = currentGameState.getAgentPosition(opponent)
        if (self.getMazeDistance(Pos, ghostPos) <= 1) and currentGameState.getAgentState(opponent).scaredTimer == 0:
            return -99999999
    minFoodDist = (1, 0)
    for food in Food.asList():
        minFoodDist = min(minFoodDist, (0, self.getMazeDistance(food, Pos)))
    return currentGameState.getScore() * 100 - minFoodDist[1] - 200 * len(currentGameState.getCapsules())



















        
        
geneLength = 22
probs = [0.1544200202, 0.1576537777, 0.1512525920, 0.1363637389, 0.1155293991, 0.09197790668, 0.06881319473, 0.04837899685, 0.03196234444, 0.01984342642, 0.01157685408, 0.006346873535, 0.003269821209, 0.001583005700, 0.0007201693720, 0.0003078788466]
def mutate():
    t = random.random()
    for i in range(0, 16):
        t -= probs[i]
        if t < 0:
            return i / 16. + random.random() / 16
    return 1

def crossover(gene1, gene2):
    child1 = [];
    child2 = [];
    for i in range(0, len(gene1)):
        if random.random() < 1. / len(gene1):
            child1.append(mutate())
            child2.append(mutate())
        elif random.random() < 0.5:
            child1.append(gene1[i])
            child2.append(gene2[i])
        else:
            child1.append(gene2[i])
            child2.append(gene1[i])
    s1 = sum(child1)
    s2 = sum(child2)
    if s1 == 0:
        child1 = [1] * len(gene1)
        s1 = len(gene1)
    if s2 == 0:
        child2 = [1] * len(gene2)
        s2 = len(gene2)
    for i in range(0, len(gene1)):
        child1[i] /= s1
        child2[i] /= s2
    return child1, child2

def randGene():
    gene = [];
    for i in range(0, geneLength):
        gene.append(mutate())
    s = sum(gene)
    if s == 0:
        gene = [1] * geneLength
        s = geneLength
    for i in range(0, geneLength):
        gene[i] /= s
        gene[i] /= s
    return gene

population = 16
genes = []
for i in range(0, population):
    genes.append((0, randGene(), `i`))

def compete(gene1, gene2):
    # return evalGame(gene1,gene2)
    return 0

def Genetic_Algorithm(genes):
    population = len(genes)
    random.shuffle(genes)
    for competition in range(0, population / 2):
        winner = compete(genes[competition][1], genes[population - competition - 1][1])
        if winner:
            tempgene = genes[competition]
            genes[competition] = genes[population - competition - 1]
            genes[population - competition - 1] = tempgene
        if genes[population - competition - 1][0]:
            for i in range(population / 2 - 1, -1, -1):
                if i != competition and not genes[i][0]:
                    genes[i] = (0, genes[population - competition - 1][1], genes[population - competition - 1][2])
                    break
    genes = genes[0:population / 2]
    for competition in range(0, population / 4):
        winner = compete(genes[competition][1], genes[population / 2 - competition - 1][1])
        if winner:
            tempgene = genes[competition]
            genes[competition] = genes[population / 2 - competition - 1]
            genes[population / 2 - competition - 1] = tempgene
        if genes[population / 2 - competition - 1][0]:
            for i in range(population / 4 - 1, -1, -1):
                if i != competition and not genes[i][0]:
                    genes[i] = (0, genes[population / 2 - competition - 1][1], genes[population / 2 - competition - 1][2])
                    break
    genes = genes[0:population / 4]
    for competition in range(0, population / 8):
        winner = compete(genes[competition][1], genes[population / 4 - competition - 1][1])
        if winner:
            tempgene = genes[competition]
            genes[competition] = genes[population / 4 - competition - 1]
            genes[population / 4 - competition - 1] = tempgene
        genes[competition] = (1, genes[competition][1], genes[competition][2])
        genes[population / 4 - competition - 1] = (0, genes[population / 4 - competition - 1][1], genes[population / 4 - competition - 1][2])
    tomake = population / 4 * 3
    while tomake > 0:
        for i in range(0, population / 4 - 1):
            for j in range(i + 1, population / 4):
                if tomake <= 0:
                    break
                children = crossover(genes[i][1], genes[j][1])
                genes.append((0, children[0], "(" + genes[i][2] + " " + genes[j][2] + ")"))
                genes.append((0, children[1], "(" + genes[j][2] + " " + genes[i][2] + ")"))
                tomake -= 2
            if tomake <= 0:
                break
    return genes

# for i in range(0,population):
#    print(genes[i][2])
# genes = Genetic_Algorithm(genes)
# print("")
# for i in range(0,population):
#    print(genes[i][2])
# genes = Genetic_Algorithm(genes)
# print("")
# for i in range(0,population):
#    print(genes[i][2])
