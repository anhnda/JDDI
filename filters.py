import params
import codecs
from utils import utils

F_Names = ["./Data/demo202101_utf.csv_EN", "./Data/drug202101_utf.csv_EN", "./Data/hist202101_utf.csv_EN",
           "./Data/reac202101_utf.csv_EN"]

DRUG_T = 10
def loadDrugmap():
    fin = open("%s/finalMap/FinalMap.txt" % params.OUTPUT_DIR)
    lines = fin.readlines()
    lines = [line.strip() for line in lines]
    dMap = dict()
    for line in lines:
        parts = line.split("||")
        dMap[parts[0]] = parts[1]
    fin.close()


    dMapH = dict()
    fin = open("%s/finalMap/FinalMapH.txt" % params.OUTPUT_DIR)
    lines = fin.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        parts = line.split("||")
        dMapH[parts[0]] = parts[1].split("|")
    fin.close()

    fin = open("%s/FinalDrugFreq.txt" % params.OUTPUT_DIR)
    lines = fin.readlines()
    validDrugs = set()
    for line in lines:
        line = line.strip()
        parts = line.split("\t")
        v, k = int(parts[0]), parts[1]
        if v >= DRUG_T:
            validDrugs.add(k)
    return dMap, dMapH, validDrugs


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


def loadMissTrans():
    fin = open("%s/Translate/MissTrans" % params.OUTPUT_DIR)
    d  = dict()
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

def filterCases():
    dMap, dMapH, validDrugs = loadDrugmap()
    # print(splitDrugs("pentazocine"))
    # print("pentazocine" in dMap)
    # exit(-1)
    fName = F_Names[1]
    fin = codecs.open(fName, "r", 'utf-8')
    # Skip first line
    fin.readline()

    currentCaseNo = ""
    currentCaseDrugCount = dict()

    cc = 0
    nValidCase = 0
    nMiss2 = 0
    KM = 1

    fvout = open("%s/Tmp/Valid.txt" % (params.OUTPUT_DIR), "w")
    fvout2 = open("%s/Tmp/Valid_%s.txt" % (params.OUTPUT_DIR, KM), "w")

    fout = open("%s/Tmp/Missing_%s.txt" % (params.OUTPUT_DIR, KM), "w")
    fout2 = open("%s/Tmp/MissingW_%s.txt" % (params.OUTPUT_DIR, KM), "w")
    allMissing = set()
    dMiss = loadMissTrans()
    nCase = 0
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
        drugName1 = parts[4].strip()
        # if line.__contains__("プロカルバジン塩酸塩"):
        #     print("Contains")
        #     print(line)
        #     print(drugName1)
        #     print(splitDrugs(drugName1))
        #     if drugName1 == u"プロカルバジン塩酸塩":
        #         print("???")
        #     exit(-1)
        if len(drugName1) == 0:
            continue
        if caseNo != currentCaseNo:
            nCase += 1
            if currentCaseNo != "":
                isValid = True
                isValidSub = True
                nMatch = 0
                matchingSet = set()
                oDrugSet = set()
                dSet = set()
                dList = list()

                for drug, ct in currentCaseDrugCount.items():
                    isValidSub = True

                    drug = utils.get_dict(dMiss, drug, drug)

                    drugs = splitDrugs(drug)

                    for edrug in drugs:
                        edrug = utils.get_dict(dMiss, edrug, edrug)
                        d1 = utils.get_dict(dMap, edrug, -1)
                        d2 = utils.get_dict(dMapH, edrug, -1)
                        # print(type(validDrugs))
                        # print(type(d1), d1,  type(d2), d2)
                        # print(d1, d2)
                        if d1 == -1:
                            if d2 == -1:
                                isValidSub = False
                                if isValid:
                                    isValid = False
                            else:
                                for d2i in d2:
                                    if d2i not in validDrugs:
                                        isValidSub = False
                                        if isValid:
                                            isValid = False
                                        break
                                    dSet.add(d2i)
                                    dList.append(d2i)
                        elif d1 not in validDrugs:
                            isValidSub = False
                            if isValid:
                                isValid = False
                        else:
                            dSet.add(d1)
                            dList.append(d1)

                    if isValidSub:
                        nMatch += 1
                        matchingSet.add(drug)


                if isValid:

                    fvout.write("%s\t%s\n"% (currentCaseNo,",".join(list(dSet))))
                    nValidCase += 1
                if 1 <= len(currentCaseDrugCount) - nMatch <= KM:
                    nMiss2 += 1
                    # print(currentCaseDrugCount.keys(), "\n \t", matchingSet)
                    missingSet = set()
                    fvout2.write("%s\n" % currentCaseNo)
                    for d1 in currentCaseDrugCount.keys():
                        d1 = utils.get_dict(dMiss, d1, d1)
                        if d1 not in matchingSet:
                            missingSet.add(d1)
                            allMissing.add(d1)
                    fout.write("%s\n\t%s\n\t%s\n" % (
                    "|".join(list(currentCaseDrugCount.keys())), "|".join(list(matchingSet)),
                    "|".join(list(missingSet))))
            currentCaseNo = caseNo
            currentCaseDrugCount = dict()

        utils.add_dict_counter(currentCaseDrugCount, drugName1)
    print("\nNumber of case: ", nCase)
    print("\nTotal valid cases: ", nValidCase, nValidCase * 1.0 / nCase)
    print("\n Miss:", KM, " : ", nMiss2, (nValidCase + nMiss2) * 1.0 / nCase)

    fout.close()
    fout2.write("\n".join(list(allMissing)))
    fout2.close()
    fvout.close()
    fvout2.close()

if __name__ == "__main__":
    filterCases()
    pass
