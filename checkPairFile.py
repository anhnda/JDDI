import params
def checkdrug():
    linesv4 = open("Data/DrugBank/DrugBankNamesV4.txt").readlines()
    linesv5 = open("Data/DrugBank/DrugBankNamesV5.txt").readlines()

    pv4 = set()
    for line in linesv4:
        parts = line.strip().split("||")
        pv4.add(parts[0])


    pv5 = set()
    for line in linesv5:
        parts = line.strip().split("||")
        pv5.add(parts[0])
        for v in parts[1].split("|"):
            pv5.add(v)
    vs = []
    for v in pv4:
        if v not in pv5:
            vs.append(v)
    fout = open("%s/MissingV5.txt" % params.OUTPUT_DIR, "w")
    fout.write("\n".join(vs))
    fout.close()


def checkTypos():
    fino = open("misc/typosMatching/MatchingDrugTypos_O.txt")
    lineso = fino.readlines()
    so = set()
    dReO = dict()
    for line in lineso:
        line = line.strip()
        dName = line.split("||")[0]
        so.add(dName)
        dReO[dName] = line



    finn = open("misc/typosMatching/FilterCandidateMatchingDrug2.txt")
    linesn = finn.readlines()
    dReN = dict()
    sn = set()
    for line in linesn:
        line = line.strip()
        dName = line.split("||")[0]
        sn.add(dName)
        dReN[dName] = line


    fout = open("misc/typosMatching/MissMatchTyposON.txt", "w")

    print(len(so), len(sn))
    for s in sn:
        if s not in so:
            fout.write("%s\n" % dReN[s])
    fout.close()


def checkPartial():
    fino = open("misc/finalMap/DrugMapH_O.txt")
    lineso = fino.readlines()
    so = set()
    dReO = dict()
    for line in lineso:
        line = line.strip()
        dName = line.split("||")[0]
        so.add(dName)
        dReO[dName] = line



    finn = open("misc/finalMap/DrugMap2.txt")
    linesn = finn.readlines()
    dReN = dict()
    sn = set()
    for line in linesn:
        line = line.strip()
        dName = line.split("||")[0]
        sn.add(dName)
        dReN[dName] = line


    fout = open("misc/finalMap/MissMatchHON.txt", "w")

    print(len(so), len(sn))
    for s in sn:
        if s not in so:
            fout.write("%s\n" % dReN[s])
    fout.close()
if __name__ == "__main__":
    # checkdrug()
    # checkTypos()
    checkPartial()