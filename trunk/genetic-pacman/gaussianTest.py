'''
Created on Oct 24, 2012

@author: BONET
'''
from math import exp

# Gaussian Value: (x0,y0,A,s)

def createGaussianMatrix():
    
    height = 10;
    width = 10;
    grid = [[0 for x in range(10)] for x in range(10)]
    
    gaussianParam = [[10.0, 1.0, 3.0, 3.0],
             [-10.0, 1.0, 6.0, 6.0]];
             
            
    grid = [[sum([(gaussian2(row, col, gauss)) for gauss in gaussianParam]) for col in range(width)] for row in range(height)];
            
    return grid

def sq(x):
    return x * x


def gaussian2(x, y, g):
    return gaussian(x, y, g[0], g[1], g[2], g[3])

def gaussian(x, y, A, sigma, x0, y0):
    return A * exp(-(sq(x - x0) + sq(y - y0)) / (2.0 * sq(sigma)))
    
    
    



if __name__ == '__main__':
    
    grid = createGaussianMatrix()
    
    print "[",
    for i in range(10):
        print "[",
        for x in range(10):
            print(grid[i][x])," ",
        
        print "];"
    print "]"
    #pass
