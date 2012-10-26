'''
Created on Oct 20, 2012

@author: BONET
'''

from pyevolve import GSimpleGA, PacmanGaussianGenome, Scaling
from capture import runGames
from capture import readCommand
from pyevolve import Selectors
from math import exp

POPULATION_SIZE = 30

def eval_func(chromosome):
    # arguments for the pacman game
    argv = ["-r", "myTeam", "-b", "baselineTeam", "-Q", "-n", "3"]
    options = readCommand(argv)  # Get game components based on input
    options["chromosome"] = chromosome.genomeList
    
    games = runGames(**options)    

    # scores = [game.state.data.score - len(game.state.getBlueFood().asList()) + 2 for game in games];
    # scores = [game.state.data.score + 100.0 * exp(-len(game.state.getBlueFood().asList()) + 2) for game in games];
    # scores = [50.0 * exp(-len(game.state.getBlueFood().asList()) + 2) for game in games];
    
#    foodEaten = [20 - len(game.state.getBlueFood().asList()) for game in games]
#    foodLost = [20 - len(game.state.getRedFood().asList()) for game in games]
#    pacmanKills = []
    scores = [game.state.data.score for game in games]
#    for i in range(len(games)):
#        killBalance = (games[i].state.data.score - (foodEaten[i] - foodLost[i])) / 10.0
#        pacmanKills.append(killBalance)
#        scores.append(foodEaten[i] - foodLost[i] + killBalance)
    
    avgScore = float(sum(scores)) / len(scores)
    
#    print "Chromosome: ",
#    print chromosome.genomeList,
#    print ""
#    print " got a score of: ",
#    print avgScore
    
    return avgScore
    # nWins = [s>0 for s in scores].count(True);

    # return nWins;
  
def train():
    import sys
    
    class Logger(object):
        def __init__(self, filename="Default.log"):
            self.terminal = sys.stdout
            self.filename = filename
            self.log = open(self.filename, "w")
            # self.log = open(self.filename, "a")
            self.log.close()
            
        def write(self, message):
            self.terminal.write(message)
            self.log = open(self.filename, "a")
            self.log.write(message)
            self.log.close()

    sys.stdout = Logger("evolution.txt")
    
    print "Evolution started"  # this is should be saved in yourlogfilename.txt

    n_generatios = 75
    
    # Creates the genome
    genome = PacmanGaussianGenome.PacmanGaussiansList()
    
    # The evaluator function
    genome.evaluator.set(eval_func);

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome);
    
    # Set the Roulette Wheel selector method, the number of generations and
    # the termination criteria
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(n_generatios)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
    ga.setPopulationSize(POPULATION_SIZE)
    ga.setMutationRate(0.06)
    
    ga.setMultiProcessing()
    
    ga.getPopulation().scaleMethod.set(Scaling.ExponentialScaling)
    print "Best individual: " + str(ga.evolve(freq_stats=1));  
  
if __name__ == "__main__":
    train()  
