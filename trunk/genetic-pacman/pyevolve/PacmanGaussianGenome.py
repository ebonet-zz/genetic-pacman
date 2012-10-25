'''
Created on Oct 24, 2012

@author: kraevam
'''
import Util
from pyevolve.G1DList import G1DList
from random import randint as rand_randint, uniform as rand_uniform, gauss as rand_gauss
from pyevolve import Consts, Crossovers

NUMBER_OF_CROSSOVERS = 5

NUMBER_OF_GAUSSIANS_TYPES = 11
CHROMOSOME_LENGTH = 23

RANGE_SIGMA_MIN = 0.01
RANGE_SIGMA_MAX = 3

RANGE_MEAN_MIN = -300
RANGE_MEAN_MAX = 300

RANGE_WALL_PENALTY_MIN = 0
RANGE_WALL_PENALTY_MAX = 1

GAUSSIAN_FOOD = "foodGaussian"
GAUSSIAN_CAPSULES = "capsulesGaussian"
GAUSSIAN_ENEMIES = "enemiesGaussians"
GAUSSIAN_INVADERS = "invadersGaussians"
GAUSSIAN_GHOSTS = "ghostsGaussians"
GAUSSIAN_ALLIES = "alliesGaussians"

DEFENDED_FOOD = "foodToDefend"
DEFENDED_CAPSULES = "capsulesToDefend"

GAUSSIAN_TYPE_TO_LIST_POSITION = {GAUSSIAN_FOOD : [0, 1], GAUSSIAN_CAPSULES : [2, 3], GAUSSIAN_ENEMIES : [4, 5], GAUSSIAN_INVADERS : [6, 7], GAUSSIAN_GHOSTS : [8, 9], GAUSSIAN_ALLIES : [10, 11]}

class PacmanGaussiansList(G1DList):
    '''
    One-Dimensional List that represents the chromosomes for the Pacman game
    '''

    def __init__(self, initialList=[]):
        '''
        Constructor
        '''
        G1DList.__init__(self, CHROMOSOME_LENGTH)    
        self.setParams(minMean=RANGE_MEAN_MIN, maxMean=RANGE_MEAN_MAX, minSigma=RANGE_SIGMA_MIN, maxSigma=RANGE_SIGMA_MAX,
                       minWallPenalty=RANGE_WALL_PENALTY_MIN, maxWallPenalty=RANGE_WALL_PENALTY_MAX)
        self.initializator.set(PacmanGaussianInitializator)
        self.mutator.set(PacmanGaussianMutator)
        self.crossover.set(Crossovers.G1DListCrossoverUniform)
        if initialList:
            self.genomeList = initialList
    
    def getGaussianAllele(self, gaussianName):
        '''
        :rype: a tuple (A, sigma) for the specified gaussian
        '''
        gaussianIndex = GAUSSIAN_TYPE_TO_LIST_POSITION.get(gaussianName)
        if gaussianIndex == None:
            return None  # wrong gaussianName
        return (self.genomeList[gaussianIndex], self.genomeList[gaussianIndex + 1])

############################
# # Gaussian Initializator ##
############################
def PacmanGaussianInitializator(genome, **args):
    listSize = genome.getListSize()
    
    minSigma = genome.getParam("minSigma")
    maxSigma = genome.getParam("maxSigma")
    minMean = genome.getParam("minMean")
    maxMean = genome.getParam("maxMean")
    minWallPenalty = genome.getParam("minWallPenalty")
    maxWallPenalty = genome.getParam("maxWallPenalty")
    
    result = []
    for i in range(0, listSize - 1):
        if i % 2 == 0:
            result.append(rand_uniform(minMean, maxMean))
        else:
            result.append(rand_uniform(minSigma, maxSigma))
    result.append(rand_uniform(minWallPenalty, maxWallPenalty))
    genome.genomeList = result        
    

############################
# # Gaussian Mutator       ##
############################
def PacmanGaussianMutator(genome, **args):
    if args["pmut"] <= 0.0: return 0
    listSize = len(genome)
    mutations = args["pmut"] * (listSize)

    mu = genome.getParam("gauss_mu")
    sigma = genome.getParam("gauss_sigma")

    if mu is None:
        mu = Consts.CDefG1DListMutRealMU
   
    if sigma is None:
        sigma = Consts.CDefG1DListMutRealSIGMA

    if mutations < 1.0:
        mutations = 0
        for it in xrange(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                if it % 2 != 0:
                    final_value = genome[it] + rand_uniform(-0.1, 0.1)
                    final_value = max(final_value, genome.getParam("minSigma"))
                    final_value = min(final_value, genome.getParam("maxSigma"))
                
                    genome[it] = final_value
                elif it < listSize - 1:
                    final_value = genome[it] + rand_uniform(-10, 10)
                    final_value = max(final_value, genome.getParam("minMean"))
                    final_value = min(final_value, genome.getParam("maxMean"))
                
                    genome[it] = final_value
                else:
                    final_value = genome[it] + rand_uniform(-0.03, 0.03)
                    final_value = max(final_value, genome.getParam("minWallPenalty"))
                    final_value = min(final_value, genome.getParam("maxWallPenalty"))
                
                    genome[it] = final_value

                mutations += 1
   
    else: 
        for it in xrange(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            if which_gene % 2 != 0:
                final_value = genome[which_gene ] + rand_uniform(-0.1, 0.1)
                final_value = max(final_value, genome.getParam("minSigma"))
                final_value = min(final_value, genome.getParam("maxSigma"))
            
                genome[which_gene] = final_value
            elif which_gene < listSize - 1:
                final_value = genome[which_gene] + rand_uniform(-10, 10)
                final_value = max(final_value, genome.getParam("minMean"))
                final_value = min(final_value, genome.getParam("maxMean"))
            
                genome[which_gene] = final_value
            else:
                final_value = genome[which_gene] + rand_uniform(-0.03, 0.03)
                final_value = max(final_value, genome.getParam("minWallPenalty"))
                final_value = min(final_value, genome.getParam("maxWallPenalty"))
            
                genome[which_gene] = final_value

    return int(mutations)
def PacmanCrossover(genome, **args):
    """ The G1DList Uniform Crossover """
    gMom = args["mom"]
    gDad = args["dad"]

    sister = gMom.clone()
    brother = gDad.clone()
    sister.resetStats()
    brother.resetStats()

    switchedIndices = []
    for i in range(NUMBER_OF_CROSSOVERS):
        randomIndex = rand_randint(0, len(gMom) - 1)
        while randomIndex in switchedIndices:
            randomIndex = rand_randint(0, len(gMom) - 1)
        switchedIndices.append(randomIndex)
       
        temp = sister[randomIndex]
        sister[randomIndex] = brother[randomIndex]
        brother[randomIndex] = temp
            
    return (sister, brother)
