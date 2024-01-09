import scipy.stats
import numpy as np
import random

import fuzzing.utils.random.drawgraph as graph

SIZE = 100000

# Compute row-col difference samples
def triang(low, upp, half = False):
    c = 1

    # mean, var, skew, kurt = scipy.stats.triang.stats(c, moments = 'mvsk')
    # x = np.linspace(scipy.stats.triang.ppf(0.01, c), scipy.stats.triang.ppf(0.99, c), 100)
    # rv = scipy.stats.triang(c)
    # vals = scipy.stats.triang.ppf([0.001, 0.5, 0.999], c)
    #np.allclose([0.001, 0.5, 0.999], scipy.stats.triang.cdf(vals, c))

    r = scipy.stats.triang.rvs(c, size = SIZE // (half * 2 + 1))

    diff = upp - low
    r = r * diff

    return r

# Pick row-col difference
def randomTriangular(low1, upp1, low2, upp2, draw = False):
    X1 = triang(low = low1, upp = upp2)
    X2 = triang(low = low2, upp = upp1, half = True)

    data = np.concatenate((X1, X2), axis = 0)

    if (draw):
        graph.drawGraph(data)

    return round(random.choice(list(data)))

# Pick row-col pair
def randomSize(low1, upp1, low2, upp2):
    while (True):
        while (True):
            diff = randomTriangular(low1, upp1, low2, upp2)

            avail = []
            if (low1 <= upp2 - diff):
                avail.append(0)
            if (low2 <= upp1 - diff):
                avail.append(1)
            
            if (len(avail) != 0):
                break

        select = random.choice(avail)
        if (select == 0):
            x = random.randint(low1, upp2 - diff)
        else:
            x = random.randint(low2, upp1 - diff)

        y = x + diff

        if (x <= upp1 and x >= low1 and y <= upp2 and y >= low2):
            return (x, y)