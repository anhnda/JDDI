import numpy as np
import params
from utils import utils
import codecs

F_Names = ["./Data/demo202101_utf.csv_EN", "./Data/drug202101_utf.csv_EN", "./Data/hist202101_utf.csv_EN",
           "./Data/reac202101_utf.csv_EN"]


DS_T = 10
def loadMissTrans():

    d = dict()
    fin = open("%s/Translate/MissTranDssInp.txt" % params.OUTPUT_DIR)
    fin2 = open("%s/Translate/MissTranDssOut.txt" % params.OUTPUT_DIR)
    while True:
        line = fin.readline()
        if line == "":
            break
        d[line.strip()] = fin2.readline().strip().lower()
    fin.close()
    fin2.close()
    return d

def loadValidDis(t=0):
    lineIns = open("%s/Ds/DsStats.txt" % params.OUTPUT_DIR).readlines()
    d = dict()
    for line in lineIns:

            parts = line.strip().split("\t")
            ds = parts[0]
            k = int(parts[1])
            if k >= t:
                d[ds] = k
    return d

def exportCaseDisease():
    fName = F_Names[2]
    fin = codecs.open(fName, "r", 'utf-8')
    # Skip first line
    fin.readline()


    currentCaseNo = ""
    currentCaseSeCount = dict()
    dSeDuplicated = dict()
    cc = 0
    d = loadMissTrans()
    validDis = loadValidDis(DS_T)

    fout = open("%s/Ds/CaseDS.txt" % params.OUTPUT_DIR, "w")

    while True:
        line = fin.readline()
        if line == "":
            break
        cc += 1
        if cc % 100 == 0:
            print("\r%s" % cc, end="")
            pass
        line = line.lower()
        parts = line[:-1].split("\t")

        caseNo = parts[0]
        seName = parts[3]
        seName = utils.get_dict(d, seName, seName)
        if caseNo != currentCaseNo:
            if currentCaseNo != "":
                isValidCases = True
                for se in currentCaseSeCount.keys():
                    if se not in validDis:
                        isValidCases = False
                        break
                if isValidCases:
                    fout.write("%s\t%s\n"%(currentCaseNo, ",".join(list(currentCaseSeCount.keys()))))


            currentCaseNo = caseNo
            currentCaseSeCount = dict()
        utils.add_dict_counter(currentCaseSeCount, seName)

    fout.close()


def statsDiss():
    fName = F_Names[2]
    fin = codecs.open(fName, "r", 'utf-8')
    # Skip first line
    fin.readline()

    dSeCount = dict()

    currentCaseNo = ""
    currentCaseSeCount = dict()
    dSeDuplicated = dict()
    cc = 0
    d = loadMissTrans()
    while True:
        line = fin.readline()
        if line == "":
            break
        cc += 1
        if cc % 100 == 0:
            print("\r%s" % cc, end="")
            pass
        line = line.lower()
        parts = line[:-1].split("\t")

        caseNo = parts[0]
        seName = parts[3]
        seName = utils.get_dict(d, seName, seName)
        if caseNo != currentCaseNo:
            if currentCaseNo != "":
                for se, count in currentCaseSeCount.items():
                    utils.add_dict_counter(dSeCount, se)
            currentCaseNo = caseNo
            currentCaseSeCount = dict()
        utils.add_dict_counter(currentCaseSeCount, seName)
    utils.save_obj(dSeCount, "%s/Ds/DsCount" % params.OUTPUT_DIR)
    fout = open("%s/Ds/DsStats.txt" % params.OUTPUT_DIR, "w")
    kvs = utils.sort_dict(dSeCount)
    for kv in kvs:
        k, v = kv
        fout.write("%s\t%s\n" % (k, v))
    fout.close()

def exportMissTrans():
    lineIns = open("%s/Ds/DsStats.txt" % params.OUTPUT_DIR).readlines()
    fout = open("%s/Translate/MissTranDssInp.txt" % params.OUTPUT_DIR, "w")
    for line in lineIns:
        if not line[0].isascii():
            parts = line.strip().split("\t")
            fout.write("%s\n" % parts[0])
    fout.close()
def processSeStats():
    dSeCout = utils.load_obj("%s/Ds/DsCount" % params.OUTPUT_DIR)

    kvs = utils.sort_dict(dSeCout)
    counts = []
    fout = open("%s/Ds/DsFreq.txt" % params.OUTPUT_DIR, "w")

    for kv in kvs:
        k, v = kv
        fout.write("%8s\t%s\n" % (v, k))
        counts.append(v)
    fout.close()

    from plotLib import plotHistS, plotCul
    for xlim in [10, 100, 500, 10000, -1]:
        plotHistS(counts, 100, "DsFreq_%s" % xlim, xlim=xlim)

    plotCul(kvs[::-1], 50, 2, "DsCutOff", xLabel="ThreshHold: Number of cases >=", yLabel="Number of Dss")


if __name__ == "__main__":
    # statsDiss()
    exportCaseDisease()
    # exportMissTrans()
    # processSeStats()
    pass
