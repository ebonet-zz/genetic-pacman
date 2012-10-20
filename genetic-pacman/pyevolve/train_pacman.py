'''
Created on Oct 20, 2012

@author: BONET
'''

from pyevolve import Crossovers, Initializators
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Mutators
from capture import runGames
from capture import readCommand
from pyevolve import Selectors

def eval_func(chromosome):
    # arguments for the pacman game
    argv = ["-r", "myTeam","-b","baselineTeam","-q","-n","5"]
    options = readCommand(argv)  # Get game components based on input
    
    games = runGames(**options)    

    scores = [game.state.data.score for game in games];
    
    nWins = [s>0 for s in scores].count(True);

    return nWins;
  
  
def train():
    
    n_generatios = 500;
    n_genes = 14;
    rage_max = 1;
    rage_min = -1;
    
    
    # Creates the genome
    genome = G1DList.G1DList(n_genes)
    
    # Sets the range max and min of the 1D List
    genome.setParams(rangemin=rage_min,rangemax=rage_max)
    
    # The evaluator function
    genome.evaluator.set(eval_func);
    
    # The mutator
    genome.mutator.set(Mutators.G1DListMutatorRealGaussian);
    
    
    # Genetic Algorithm Instance
    ga =  GSimpleGA.GSimpleGA(genome);
    
    # Set the Roulette Wheel selector method, the number of generations and
    # the termination criteria
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(n_generatios)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
    
    ga.evolve(freq_stats=100);  
  
  