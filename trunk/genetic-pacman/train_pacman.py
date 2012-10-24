'''
Created on Oct 20, 2012

@author: BONET
'''

from pyevolve import GSimpleGA, PacmanGaussianGenome
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
    
    # Creates the genome
    genome = PacmanGaussianGenome
    
    # The evaluator function
    genome.evaluator.set(eval_func);

    # Genetic Algorithm Instance
    ga =  GSimpleGA.GSimpleGA(genome);
    
    # Set the Roulette Wheel selector method, the number of generations and
    # the termination criteria
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(n_generatios)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
    
    ga.evolve(freq_stats=100);  
  
if __name__ == "__main__":
    train()  