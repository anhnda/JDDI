import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import params

def plotCul(kvs, nBins, stepSize, name, xLabel = None, yLabel=None):
    n = len(kvs)
    x = [stepSize * i for i in range(nBins)]
    y = np.zeros(nBins)
    jInd = 0
    for i in range(nBins):
        currentThreshold = x[i]
        for j in range(jInd, n):
            _, v = kvs[j]
            if v >= currentThreshold:
                jInd = j
                y[i] = n - j
                break

    fig, axs = plt.subplots()
    axs.plot(x, y)
    if xLabel is None:
        xLabel = "Threshold"
    plt.xlabel(xLabel)
    if yLabel is None:
        yLabel = "Number of instances"

    plt.ylabel(yLabel)

    plt.savefig("%s/%s.png" % (params.FIG_DIR, name))


def plotHistD(x, nBins, name, xlim=-1):
    fig, axs = plt.subplots()

    if xlim > 0:
        i = 0
        for i, xi in enumerate(x):
            if xi < xlim:
                break
        x = x[i:]
    axs.hist(x, bins=nBins)

    plt.xlabel("Freq Drug")
    plt.ylabel("Count")

    plt.savefig("%s/%s.png" % (params.FIG_DIR, name))


def plotHistS(x, nBins, name, xlim=-1):
    fig, axs = plt.subplots()

    if xlim > 0:
        i = 0
        for i, xi in enumerate(x):
            if xi < xlim:
                break
        x = x[i:]
    axs.hist(x, bins=nBins)

    plt.xlabel("Freq SE")
    plt.ylabel("Count")

    plt.savefig("%s/%s.png" % (params.FIG_DIR, name))


def plotHist(x, nBins, name, xlim=-1):
    fig, axs = plt.subplots()

    if xlim > 0:
        i = 0
        for i, xi in enumerate(x):
            if xi < xlim:
                break
        x = x[i:]
    axs.hist(x, bins=nBins)

    plt.xlabel("Num. Drug-drug pairs")
    plt.ylabel("Num. Side effects")

    plt.savefig("%s/%s.png" % (params.FIG_DIR, name))
