'''
Created on Oct 20, 2012

@author: kraevam
'''
from pyevolve.G1DList import G1DList
from pyevolve.Initializators import G1DListInitializatorReal
from pyevolve.Mutators import G1DListMutatorRealGaussian
from pyevolve.Crossovers import G1DListCrossoverUniform
import PacmanConsts

RANGE_MIN = -1
RANGE_MAX = 1

class G1PacmanList(G1DList):
    '''
    One-Dimensional List that represents the chromosomes for the Pacman game
    '''

    def __init__(self):
        '''
        Constructor
        '''
        G1DList.__init__(self, PacmanConsts.NUMBER_OF_CHROMOSOMES)    
        self.setParams(rangemin=RANGE_MIN,rangemax=RANGE_MAX)
        self.initializator.set(G1DListInitializatorReal)
        self.mutator.set(G1DListMutatorRealGaussian)
        self.crossover.set(G1DListCrossoverUniform)
    
    '''
    Returns the value for a certain chromosome
    :param pacmanAlleleName: String from PacmanConsts that specifies the allele in which we are interested
    :rtype: a number, the value of the specified allele in this chromosome
    '''
    '''
    TODO: throw an exception instead of returning None in bad cases?
    '''
    def getAlleleValue(self, pacmanAlleleName):
        indexInList = PacmanConsts.CONSTANT_TO_CHROMOSOME_INDEX_MAPPING.get(pacmanAlleleName)
        if indexInList == None:
            # key not valid
            return None
        
        if indexInList >= self.genomeSize:
            # index out of bounds
            return None
        
        return self.genomeList[indexInList]
    
    '''
    Returns a dictionary in which keys are all the Pacman Alleles and the values are the corresponding values from this list
    '''
    def getValuesInDict(self):
        chromosomeAsDict = {}
        for alleleName in PacmanConsts.CONSTANT_TO_CHROMOSOME_INDEX_MAPPING.keys():
            chromosomeAsDict[alleleName] = self.getAlleleValue(alleleName)
        
        return chromosomeAsDict