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

def fastCheckMissingDrug():
    fin = open("misc/Tmp/MissingW_1.txt")
    fout1 = open("misc/Tmp/MissingW_01.txt", "w")
    fout2 = open("misc/Tmp/MissingW_02.txt", "w")
    lines = fin.readlines()
    for line in lines:
        line = line.strip()
        if line[0].isnumeric() or line.__contains__("unk"):
            fout2.write("%s\n" %line)
        else:
            fout1.write("%s\n" %line)
    fin.close()
    fout1.close()
    fout2.close()

def compareONTypos():
    fin1 = open("misc/typosMatching/FilterCandidateMatchingDrug2.txt")
    fin2 = open("misc/typosMatching/MatchingDrugTypos.txt")

    fout1 = open("misc/typosMatching/C_MatchingDrugTypos.txt", "w")
    fout2 = open("misc/typosMatching/C_NoMatchingDrugTypos.txt", "w")


    lines1 = fin1.readlines()
    lines2 = fin2.readlines()

    # No matching:
    for line in lines2:
        if line.__contains__("##"):
            fout2.write("%s" % line)
        else:
            fout1.write("%s" % line)

    # Missing Matching Typos -> Filter

    d1 = dict()
    for line in lines1:
        parts = line.strip().split("||")
        d1[parts[0]] = line

    d2 = dict()
    for line in lines2:
        parts = line.strip().split("||")
        d2[parts[0]] = line

    for k, v in d1.items():
        if k not in d2:
            fout2.write("%s ## New no match\n" % v.strip())

    fout1.close()
    fout2.close()




def compareONPartialMatching():
    fin1 = open("misc/finalMap/DrugMap2.txt")
    fin2 = open("misc/finalMap/DrugMapH.txt")

    fout1 = open("misc/finalMap/C_DrugH.txt", "w")
    fout2 = open("misc/finalMap/C_NoDrugH.txt", "w")


    lines1 = fin1.readlines()
    lines2 = fin2.readlines()

    # No matching:
    for line in lines2:
        if line.__contains__("##"):
            fout2.write("%s" % line)
        else:
            fout1.write("%s" % line)

    # Missing Matching Typos -> Filter

    d1 = dict()
    for line in lines1:
        parts = line.strip().split("||")
        d1[parts[0]] = line

    d2 = dict()
    for line in lines2:
        parts = line.strip().split("||")
        d2[parts[0]] = line

    for k, v in d1.items():
        if k not in d2:
            fout2.write("%s\n" % v.strip())

    fout1.close()
    fout2.close()

def compareSalt():
    fin1 = open("misc/rawMatching/CandSaltFreq.txt")
    fin2 = open("misc/rawMatching/Salt.txt")

    fout1 = open("misc/rawMatching/C_Salt.txt", "w")
    fout2 = open("misc/rawMatching/C_NoSalt.txt", "w")


    lines1 = fin1.readlines()
    lines2 = fin2.readlines()
    salts = set()
    for line in lines2:
        if line.__contains__("#"):
            continue
        salts.add(line)
        fout1.write("%s" % line )

    for line in lines1:
        if line not in salts:
            fout2.write("%s" % line)
    fout1.close()
    fout2.close()

if __name__ == "__main__":
    # checkdrug()
    # checkTypos()
    # checkPartial()
    fastCheckMissingDrug()
    compareONTypos()
    compareONPartialMatching()
    compareSalt()