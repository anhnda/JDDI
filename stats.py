import numpy as np
import params
from utils import utils
import codecs

F_Names = ["./Data/demo202101_utf.csv_EN", "./Data/drug202101_utf.csv_EN", "./Data/hist202101_utf.csv_EN",
           "./Data/reac202101_utf.csv_EN"]


def splitDrugs(drugString):
    if drugString.__contains__("/"):
        drugs = drugString.split("/")
        drugs = [drug.strip() for drug in drugs]
    elif drugString.__contains__(","):
        drugs = drugString.split(",")
        drugs = [drug.strip() for drug in drugs]
    else:
        drugs = [drugString.strip()]
    drugx = []
    for drug in drugs:
        if drug == "":
            continue
        drugx.append(drug)

    return drugx


def statsDrug():
    fName = F_Names[1]
    fin = codecs.open(fName, "r", 'utf-8')
    # Skip first line
    fin.readline()

    dDrugCount = dict()
    dDrugCount2 = dict()
    dDrug2Reasons = dict()

    currentCaseNo = ""
    currentCaseDrugCount = dict()
    currentCaseDrug2Use = dict()
    dDrugDuplicated = dict()
    cc = 0
    while True:
        line = fin.readline()
        if line == "":
            break
        cc += 1
        if cc % 100 == 0:
            print("\r%s" % cc, end="")
            pass
        line = line.lower()
        if line.__contains__("Insulin"):
            print("Error Upper")
            exit(-1)
        parts = line[:-1].split("\t")

        caseNo = parts[0]
        drugName1 = parts[4]
        drugs = splitDrugs(drugName1)
        if len(drugName1) == 0:
            continue
        reasonOfUse = parts[12]
        if caseNo != currentCaseNo:
            if currentCaseNo != "":
                for drug, ct in currentCaseDrugCount.items():
                    utils.add_dict_counter(dDrugCount, drug)
                    drugs = splitDrugs(drug)
                    for edrug in drugs:
                        utils.add_dict_counter(dDrugCount2, edrug)
                    # reasonsx = utils.get_insert_key_dict(dDrug2Reasons, drug, set())
                    currentCaseReason = currentCaseDrug2Use[drug]
                    # for r in currentCaseReason:
                    #     reasonsx.add(r)

                    # if ct > 1:
                    #     reasonDup = utils.get_insert_key_dict(dDrugDuplicated, drug, [])
                    #     reasonDup.append(reasonsx)

            currentCaseNo = caseNo
            currentCaseDrugCount = dict()

        utils.add_dict_counter(currentCaseDrugCount, drugName1)
        reasons = utils.get_insert_key_dict(currentCaseDrug2Use, drugName1, [])
        reasons.append(reasonOfUse)

    utils.save_obj((dDrugCount, dDrugCount2, dDrug2Reasons, dDrugDuplicated), "%s/Tmp/DrugStats_1" % params.OUTPUT_DIR)


def loadMissTrans():
    fin = open("%s/Translate/MissTrans" % params.OUTPUT_DIR)
    d = dict()
    while True:
        line = fin.readline()
        if line == "":
            break
        parts = line.strip().split("||")
        d[parts[0]] = parts[1].lower()
    fin.close()

    fin = open("%s/Translate/MissTranIn.txt" % params.OUTPUT_DIR)
    fin2 = open("%s/Translate/MissTranOut.txt" % params.OUTPUT_DIR)
    while True:
        line = fin.readline()
        if line == "":
            break
        d[line.strip()] = fin2.readline().strip().lower()
    fin.close()
    fin2.close()
    return d


def processDrugStats():
    dDrugCount, dDrugCount2, dDrug2Reasons, dDrugDuplicated = utils.load_obj("%s/Tmp/DrugStats_1" % params.OUTPUT_DIR)
    missTrans = loadMissTrans()
    kvs = utils.sort_dict(dDrugCount)
    kvs2 = utils.sort_dict(dDrugCount2)

    counts = []
    fout = open("%s/Tmp/DrugFreq.txt" % params.OUTPUT_DIR, "w")
    fout2 = open("%s/Tmp/DrugFreq2.txt" % params.OUTPUT_DIR, "w")

    # foutr = open("%s/DrugFreq_Reason.txt" % params.OUTPUT_DIR, "w")

    for kv in kvs:
        k, v = kv
        # reasons = dDrug2Reasons[k]
        # reasonsS = ",".join(reasons)

        k = utils.get_dict(missTrans, k, k)
        fout.write("%8s\t%s\n" % (v, k.lower().strip()))

        # foutr.write("%8s\t%s\t%s\n" % (v, k, reasonsS))
        counts.append(v)
    fout.close()

    for kv in kvs2:
        k, v = kv
        k = utils.get_dict(missTrans, k, k)
        fout2.write("%8s\t%s\n" % (v, k.lower().strip()))

    fout2.close()

    # foutr.close()

    # fout2 = open("%s/DrugReasonDup.txt" % params.OUTPUT_DIR, "w")
    # for drug, rss in dDrugDuplicated.items():
    #
    #     fout2.write("%s\t" % drug)
    #     for rs in rss[:-1]:
    #         fout2.write("%s|" % ",".join(rs))
    #     fout2.write("%s\n" % ",".join(rss[-1]))
    #
    # fout2.close()

    from plotLib import plotHistD, plotCul
    for xlim in [10, 100, 500, 10000, -1]:
        plotHistD(counts, 100, "DrugFreq_%s" % xlim, xlim=xlim)

    plotCul(kvs[::-1], 50, 2, "DrugCutOff", xLabel="ThreshHold: Freq >=", yLabel="Number of Drugs")


def exportMissTransIn():
    fin = open("%s/Tmp/DrugFreq.txt" % params.OUTPUT_DIR)
    fout = open("%s/Translate/MissTranIn.txt" % params.OUTPUT_DIR, "w")
    while True:
        line = fin.readline()
        if line == "":
            break
        if not line.isascii():
            fout.write("%s\n" % line.strip().split("\t")[-1])
    fin.close()
    fout.close()


def exportMissTransIn2():
    fin = open("%s/Tmp/MissingW_1.txt" % params.OUTPUT_DIR)
    fout = open("%s/Translate/MissTranIn2.txt" % params.OUTPUT_DIR, "w")
    while True:
        line = fin.readline()
        if line == "":
            break
        if not line.isascii():
            fout.write("%s" % line)
    fin.close()
    fout.close()



def statsDemo():
    fName = F_Names[0]
    fin = codecs.open(fName, "r", 'utf-8')
    fin.readline()

    def isValid(v):
        return len(v) > 1 and v.lower() != "unknown"

    nC = 0
    nGA = 0
    nAll = 0
    while True:
        line = fin.readline()
        if line == "":
            break
        nC += 1

        parts = line[:-1].split("\t")

        gender = parts[2]
        age = parts[3]
        weight = parts[4]
        height = parts[5]

        if isValid(gender) and isValid(age):
            nGA += 1
            if isValid(weight) and isValid(height):
                nAll += 1

    fout = open("%s/DemoStats.txt" % params.OUTPUT_DIR, "w")
    fout.write(
        "Total: %s\n Gender+Sex: %s %s \n Gender+Sex+W+H: %s %s\n" % (nC, nGA, nGA * 1.0 / nC, nAll, nAll * 1.0 / nC))
    fout.close()


def statsDemo2():
    # Valid Cases:
    fin = open("%s/Tmp/Valid.txt" % params.OUTPUT_DIR)
    lines = fin.readlines()
    validCases = set([line.strip().split("\t")[0] for line in lines])

    fName = F_Names[0]
    fin = codecs.open(fName, "r", 'utf-8')
    fin.readline()

    def isValid(v):
        return len(v) > 1 and v.lower() != "unknown"

    nC = 0
    nGA = 0
    nAll = 0
    nV = 0
    while True:
        line = fin.readline()
        if line == "":
            break
        nC += 1

        parts = line[:-1].split("\t")
        caseId = parts[0].lower()
        if caseId in validCases:
            nV += 1
        gender = parts[2]
        age = parts[3]
        weight = parts[4]
        height = parts[5]

        if isValid(gender) and isValid(age):
            nGA += 1
            if isValid(weight) and isValid(height):
                nAll += 1

    fout = open("%s/DemoStats.txt" % params.OUTPUT_DIR, "w")
    fout.write(
        "Total: %s\n Gender+Sex: %s %s \n Gender+Sex+W+H: %s %s\n" % (nC, nGA, nGA * 1.0 / nC, nAll, nAll * 1.0 / nC))
    fout.write("Valid+Demo: %s %s\n" % (nV, nV * 1.0 / len(validCases)))
    fout.close()


def statsDemo3():
    def isValid(v):
        return len(v) > 1 and v.lower() != "unknown"

    fName = F_Names[0]
    fin = codecs.open(fName, "r", 'utf-8')
    fin.readline()

    fout = open("%s/CaseDemo.txt" % params.OUTPUT_DIR, "w")

    nC = 0
    nGA = 0
    nAll = 0
    nV = 0
    while True:
        line = fin.readline()
        if line == "":
            break
        nC += 1
        line = line.lower()
        parts = line[:-1].split("\t")
        caseId = parts[0].lower()

        gender = parts[2]
        age = parts[3]
        weight = parts[4]
        height = parts[5]

        if isValid(gender) and isValid(age):
            fout.write("%s\t%s,%s\n"%(caseId, gender, age))


    fout.close()

if __name__ == "__main__":
    # statsDrug()
    # processDrugStats()
    # exportMissTransIn()
    # exportMissTransIn2()

    # statsSEs()
    # processSeStats()

    statsDemo3()
    pass
