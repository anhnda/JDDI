import pandas as pd
import csv
import codecs
import io

F_Names = ["./Data/demo202101_utf.csv", "./Data/drug202101_utf.csv", "./Data/hist202101_utf.csv",
           "./Data/reac202101_utf.csv"]
# F_SKIPS = [{0, 1}, {0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {0, 1, 2}, {0, 1, 2, 5}]
F_SKIPS = [{0, 1}, {0, 1, 2, 7, 8, 9, 10, 11, 16}, {0, 1, 2}, {0, 1, 2, 5}]
N_F = 470



def readNLines(f, nLine):
    lines = []
    cc = 0
    while True:
        line = f.readline()
        if line == "":
            break
        cc += 1
        lines.append(line)
        if cc == nLine:
            break

    return lines


def export(fName, skipIds=set()):
    print("Extracting... %s" % fName)

    f = codecs.open(fName, "r", "utf-8")
    names = set()
    cc = 0
    while True:
        lines = readNLines(f, 10000)
        if len(lines) == 0:
            break
        for line in lines:
            if line == "\n":
                break
            cc += 1

            if cc > 0:
                if not line[0].isalpha():
                    continue

            if cc % 100 == 0:
                print("\r%s" % cc, end="")

            ios = io.StringIO(line.strip())
            vv = list(csv.reader(ios))

            if len(vv) == 0:
                continue
            vv = vv[0]

            for i in range(len(vv)):
                if i in skipIds:
                    continue
                name = vv[i]
                names.add(name)
    f.close()
    print("\nFound: %s phrases" % len(names))
    return names


def getPhrases():
    names = set()
    for i in range(len(F_Names)):
        ni = export(F_Names[i], F_SKIPS[i])
        for n in ni:
            names.add(n)

    print("\nTotal: %s phrases" % len(names))
    fNameOut = "./Data/AllPhrasesFull.txt"
    fOut = codecs.open(fNameOut, "w", "utf-8")
    for n in names:
        fOut.write("%s\n" % n)
    fOut.close()


# def getPhrasesMiss():
#     names = set()
#     for i in range(len(F_Names)):
#         ni = export(F_Names[i], F_SKIPS[i])
#         for n in ni:
#             names.add(n)
#
#     print("\nTotal: %s phrases" % len(names))
#     fNameOut = "./Data/AllPhrasesMiss.txt"
#
#     fOld = codecs.open("./Data/AllPhrases1.txt", "r", "utf-8")
#     oldPhrases = set()
#     while True:
#         line = fOld.readline()
#         if line == "":
#             break
#         oldPhrases.add(line.strip())
#     fOld.close()
#
#     fOut = codecs.open(
#
#     fNameOut, "w", "utf-8")
#     for n in names:
#         if n not in oldPhrases:
#             fOut.write("%s\n" % n)
#     fOut.close()


def segs():
    fin = codecs.open("./Data/AllPhrasesFull.txt", "r", "utf-8")

    dirout = "./Data/Segs/"
    allPhrases = []
    nChars = 0
    i = N_F
    MAX = 4900
    while True:
        line = fin.readline()
        if line == "":
            if nChars > 0:
                fout = codecs.open("%sF_%s" % (dirout, i), "w", 'utf-8')
                for p in allPhrases:
                    fout.write("%s\n" % p)
                fout.close()
            break
        line = line.strip()
        if line == "":
            continue
        nChars += len(line) + 1
        if nChars < MAX:
            allPhrases.append(line)
        else:
            fout = codecs.open("%sF_%s" % (dirout, i), "w", 'utf-8')
            for p in allPhrases:
                fout.write("%s\n" % p)
            fout.close()
            i += 1
            nChars = 0
            allPhrases = []


# def segsMiss():
#     fin = codecs.open("./Data/AllPhrasesMiss.txt", "r", "utf-8")
#     dirout = "./Data/Segs/"
#     allPhrases = []
#     nChars = 0
#     i = N_F
#     MAX = 4900
#     while True:
#         line = fin.readline()
#         if line == "":
#             if nChars > 0:
#                 fout = codecs.open("%sF_%s" % (dirout, i), "w", 'utf-8')
#                 for p in allPhrases:
#                     fout.write("%s\n" % p)
#                 fout.close()
#             break
#         line = line.strip()
#         if line == "":
#             continue
#         nChars += len(line) + 1
#         if nChars < MAX:
#             allPhrases.append(line)
#         else:
#             fout = codecs.open("%sF_%s" % (dirout, i), "w", 'utf-8')
#             for p in allPhrases:
#                 fout.write("%s\n" % p)
#             fout.close()
#             i += 1
#             nChars = 0
#             allPhrases = []


def loadDict():
    dirJP = "./Data/Segs/"
    dirEN = "./Data/Trans/"
    d = dict()

    for i in range(N_F):
        fin1 = codecs.open("%sF_%s" % (dirJP, i), "r", 'utf-8')
        fin2 = codecs.open("%sF_%s" % (dirEN, i), "r", 'utf-8')
        while True:
            line1 = fin1.readline()
            if line1 == "":
                break
            lineJP = line1.strip()
            lineEN = fin2.readline().strip()

            d[lineJP] = lineEN

        fin1.close()
        fin2.close()

    return d


def getDictK(d, k):
    v = k
    try:
        v = d[k]
    except:
        pass
    return v


def tranFiles(fName, skips, d):
    f = codecs.open(fName, "r", "utf-8")
    fout = codecs.open("%s_EN" % fName, 'w', 'utf-8')
    cc = 0
    nSize = 0
    while True:
        lines = readNLines(f, 10000)
        if len(lines) == 0:
            print("\n Total lines: ", cc)

            break
        for line in lines:
            if line == "":
                print(fName, cc)
                break
            cc += 1
            if cc > 0:
                if not line[0].isalpha():
                    continue
            if cc % 100 == 0:
                print("\r%s" % cc, end="")
            ios = io.StringIO(line.strip())
            vv = list(csv.reader(ios))

            if len(vv) == 0:
                continue
            vv = vv[0]
            if nSize == 0:
                nSize = len(vv)
            outs = []
            for i, v in enumerate(vv):
                if i not in skips:
                    v = getDictK(d, v)
                v = v.replace("\t", " ").strip()
                v = v.replace("\"", "")
                outs.append(v)
            if len(outs) < nSize:
                for i in range(len(outs), nSize):
                    outs.append("")

            liner = "\t".join(outs)
            fout.write("%s\n" % liner)

            # if cc == 3086388:
            #

            #     print(line)
            #     print(vv)
            #     print(outs)
            #     print(len(outs))
            #     print(liner)
            #     exit(-1)

    print("\n")
    fout.close()


def transAll():
    d = loadDict()

    for i in range(0, len(F_Names)):
        print("Translate: ...", F_Names[i])
        tranFiles(F_Names[i], F_SKIPS[i], d)

def checkW():
    d = loadDict()
    w = "revo"
    for k, v in d.items():
        if v.lower().__contains__(w):
            print (k, v)

if __name__ == "__main__":
    # transAll()
    checkW()
    pass
