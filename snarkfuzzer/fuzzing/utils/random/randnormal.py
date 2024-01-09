import scipy.stats
import numpy as np
import random

import fuzzing.utils.random.drawgraph as graph

SIZE = 10000

def truncnorm(mean, sd, low, upp):
    return scipy.stats.truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale = sd)

def randomNormal(low, upp, mean, draw = False):
    std = mean / 2.5

    X = truncnorm(mean = mean, sd = std, low = low, upp = upp)

    data = X.rvs(SIZE)

    if (draw):
        graph.drawGraph(data)

    return round(random.choice(list(data)))

def randomInvNormal(low, upp, draw = False):
    mean = (low + upp) / 2
    std = mean / 2.5

    X1 = truncnorm(mean = low, sd = std, low = low, upp = upp)
    X2 = truncnorm(mean = upp, sd = std, low = low, upp = upp)

    x1 = X1.rvs(SIZE)
    x2 = X2.rvs(SIZE)
    data = np.concatenate((x1, x2), axis = 0)

    if (draw):
        graph.drawGraph(data)

    return round(random.choice(list(data)))
