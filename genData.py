from utils import utils
import params


def loadCaseMap(path):
    fin = open(path)
    dCase2Map = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split("\t")
        dCase2Map[parts[0]] = parts[1]
    fin.close()
    return dCase2Map


def export():
    fout = open("%s/FinalJADER.txt" % params.OUTPUT_DIR, "w")
    pathCaseDrug = "%s/Tmp/Valid.txt" % params.OUTPUT_DIR
    pathCaseDemo = "%s/CaseDemo.txt" % params.OUTPUT_DIR
    pathCaseDs = "%s/Ds/CaseDS.txt" % params.OUTPUT_DIR
    pathCaseSes = "%s/SEs/CaseSE.txt" % params.OUTPUT_DIR

    dCase2Drug = loadCaseMap(pathCaseDrug)
    dCase2Demo = loadCaseMap(pathCaseDemo)
    dCase2Ds = loadCaseMap(pathCaseDs)
    dCaseSes = loadCaseMap(pathCaseSes)

    caseMaps = [dCase2Demo, dCase2Ds, dCaseSes]
    cc = 0
    for k, v in dCase2Drug.items():
        vs = [utils.get_dict(d, k, -1) for d in caseMaps]
        isValid = True
        for vi in vs:
            if vi == -1:
                isValid = False
        if isValid:
            fout.write("%s\t%s\t%s\n" % (k, v, "\t".join(vs)))
            cc += 1
    print(cc)
    fout.close()


def statsDrugDis():
    fin =open("%s/FinalJADER.txt" % params.OUTPUT_DIR)

    fout = open("%s/ManySEs.txt" % params.OUTPUT_DIR, "w")
    dDrugCount = dict()
    SeCount = dict()
    nBloodI = 0

    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split("\t")
        nD = len(parts[1].split(","))
        nC = len(parts[-1].split(","))
        if line.__contains__("increased blood"):
            nBloodI += 1
        if nC > 10:
            print(line)

            fout.write("%s" % line)
        # if nD > 20:
        #    print(line)
        utils.add_dict_counter(dDrugCount, nD)
        utils.add_dict_counter(SeCount, nC)
    # counts = list(dDrugCount.keys())
    # from plotLib import plotHistD, plotCul
    # #for xlim in [10, 100, 500, 10000, -1]:
    # plotHistD(counts, 10, "SDrugComb_%s" % -1, xlim=-1)

    kvs = utils.sort_dict(SeCount)
    ks, vs = [], []
    for kv in kvs:
        k, v = kv
        print(k,v)
        ks.append(k)
        vs.append(v)

    from matplotlib import pyplot as plt
    plt.scatter(ks,vs)
    print("NBI: ", nBloodI)
    plt.show()
    fout.close()
    fin.close()
if __name__ == "__main__":
    # export()
    statsDrugDis()
    pass