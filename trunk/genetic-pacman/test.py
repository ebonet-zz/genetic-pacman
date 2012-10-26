from capture import runGames, readCommand
def eval_func():
    # arguments for the pacman game
    argv = ["-r", "myTeam", "-b", "baselineTeam", "-Q", "-n", "10"]
    options = readCommand(argv)  # Get game components based on input
    games = runGames(**options)    

    scores = [game.state.data.score for game in games];
    
    average = sum(scores) / 10.0;
    maxi = max(scores)
    mini = min(scores)
    return [average, maxi, mini]

if __name__ == "__main__":
    print "Avg/Max/Min: ",
    print eval_func() 
