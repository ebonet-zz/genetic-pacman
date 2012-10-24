'''
Created on Oct 24, 2012

@author: kraevam
'''
import Util
from pyevolve.G1DList import G1DList
from pyevolve.Crossovers import G1DListCrossoverUniform
from random import randint as rand_randint, uniform as rand_uniform

NUMBER_OF_GAUSSIANS_TYPES = 6
RANGE_SIGMA_MIN = 0
RANGE_SIGMA_MAX = 10

RANGE_MEAN_MIN = -50
RANGE_MEAN_MAX = 50

GAUSSIAN_FOOD = "foodGaussian"
GAUSSIAN_CAPSULES = "capsulesGaussian"
GAUSSIAN_ENEMIES = "enemiesGaussians"
GAUSSIAN_INVADERS = "invadersGaussians"
GAUSSIAN_GHOSTS = "ghostsGaussians"
GAUSSIAN_ALLIES = "alliesGaussians"

GAUSSIAN_TYPE_TO_LIST_POSITION = {GAUSSIAN_FOOD : 0, GAUSSIAN_CAPSULES : 1, GAUSSIAN_ENEMIES : 2, GAUSSIAN_INVADERS : 3, GAUSSIAN_GHOSTS : 4, GAUSSIAN_ALLIES : 5}

class PacmanGaussiansList(G1DList):
    '''
    One-Dimensional List that represents the chromosomes for the Pacman game
    '''

    def __init__(self, initialList = []):
        '''
        Constructor
        '''
        G1DList.__init__(self, 2*NUMBER_OF_GAUSSIANS_TYPES)    
        self.setParams(minMean=RANGE_MEAN_MIN, maxMean=RANGE_MEAN_MAX, minSigma=RANGE_SIGMA_MIN, maxSigma = RANGE_SIGMA_MAX)
        self.initializator.set(PacmanGaussianInitializator)
        self.mutator.set(PacmanGaussianMutator)
        self.crossover.set(G1DListCrossoverUniform)
        if initialList:
            self.genomeList = initialList
    
    def getGaussianAllele(self, gaussianName):
        '''
        :rype: a tuple (A, sigma) for the specified gaussian
        '''
        gaussianIndex = GAUSSIAN_TYPE_TO_LIST_POSITION.get(gaussianName)
        if gaussianIndex == None:
            return None # wrong gaussianName
        return (self.genomeList[gaussianIndex], self.genomeList[gaussianIndex + 1])

############################
## Gaussian Initializator ##
############################
def PacmanGaussianInitializator(genome, **args):
    listSize = genome.getListSize()
    if listSize % 2 != 0:
        return None # how do you throw an exception in python?
    
    minSigma = genome.getParam("minSigma")
    maxSigma = genome.getParam("maxSigma")
    minMean = genome.getParam("minMean")
    maxMean = genome.getParam("maxMean")
    result = []
    for i in range(0, listSize):
        if i%2 == 0:
            result.append(rand_uniform(minMean, maxMean))
        else:
            result.append(rand_uniform(minSigma, maxSigma))
    
    genome.genomeList = result        
    

############################
## Gaussian Mutator       ##
############################
def PacmanGaussianMutator(genome, **args):
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome)
   mutations = args["pmut"] * (listSize)

   if mutations < 1.0:
      mutations = 0
      for it in xrange(listSize):
         if Util.randomFlipCoin(args["pmut"]):
            if it%2 == 0:
                genome[it] = rand_uniform(genome.getParam("minMean"),
                                          genome.getParam("maxMean"))
            else:
                genome[it] = rand_uniform(genome.getParam("minSigma"),
                                          genome.getParam("maxSigma"))

            mutations += 1
   
   else: 
      for it in xrange(int(round(mutations))):
        which_gene = rand_randint(0, listSize-1)
        if which_gene%2 == 0:
            genome[which_gene] = rand_uniform(genome.getParam("minMean"),
                                      genome.getParam("maxMean"))
        else:
            genome[which_gene] = rand_uniform(genome.getParam("minSigma"),
                                      genome.getParam("maxSigma"))

   return int(mutations)