from datetime import datetime
import os
import shutil
import sys

if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists("data/editdistance"):
    os.mkdir("data/editdistance")

tab = "\t"
nl = "\n"
sumtoklen = 0
oldtypos = {}
if os.path.exists("data/editdistance/typos.txt"):
    with open ("data/editdistance/typos.txt","r",encoding="utf8") as bwin:
        for line in bwin:
            linearr = line.split(tab)
            oldtypos[linearr[1].split(":")[0]] = 1


bw = dict()
with open ("data/bagofwords/_all.txt","r",encoding="utf8") as bwin:
    for line in bwin:
        linearr = line.split(tab)
        bw[linearr[0]] = int(linearr[1])
        sumtoklen += len(linearr[0].strip())

#Source https://www.python-kurs.eu/levenshtein_distanz.php
def iterative_levenshtein(s, t):
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    for i in range(1, rows):
        dist[i][0] = i
    for i in range(1, cols):
        dist[0][i] = i
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution
    return dist[row][col]

counter = -1
if len(sys.argv) >1:
    counter = int(sys.argv[1].split(" ")[0])

maxls = 1

start = datetime.now()
avgtoklen = int(sumtoklen / len(bw))
res = {}
typofrequency = 1

print("Start " +start.strftime("%m/%d/%Y, %H:%M:%S")+" avgtoklen: "+str(avgtoklen))
for token1,tokencount in sorted(bw.items(),key = lambda x:x[1], reverse=True):
    if counter != 0:
        if len(token1)>=avgtoklen and not token1 in oldtypos and not token1 in res and int(bw[token1])>typofrequency:
            for token2 in bw:
                if int(bw[token2]) == 1:
                    if token1 != token2 and not abs(len(token1)-len(token2)) > maxls :
                        ls = iterative_levenshtein(token1, token2)
                        if(ls<=maxls and ls < len(token1) and ls < len(token2)):
                            res[token2] = token1
                            if counter>0:
                                counter -= 1
                            print(token1+tab+token2+tab+str(ls)+tab+str(bw[token2])+tab+str(counter))
end = datetime.now()
with open ("data/editdistance/typos.txt", "a", encoding="utf8") as outf:
    for typo,token in sorted(res.items(),key = lambda x:x[1], reverse=False):
        outf.write(typo+tab+token+":"+str(bw[res[typo]])+nl)

print(str(end-start))

