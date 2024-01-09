import numpy as np
import matplotlib.pyplot as plt

def drawGraph(data):
    y, binEdges = np.histogram(data, bins = 50)
    bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])

    # plt.hist(x12, bins = 200, density = True)
    plt.plot(bincenters, y, '-')
    plt.show()