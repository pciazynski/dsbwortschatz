from datetime import datetime
import os
import shutil
import sys

if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/editdistance"):
    shutil.rmtree("data/editdistance")
os.mkdir("data/editdistance")

tab = "\t"
nl = "\n"
sumtoklen = 0

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

counter = 2000
if len(sys.argv) >2:
    maxls = sys.argv[1]
else:
    maxls = 1

start = datetime.now()
avgtoklen = int(sumtoklen / len(bw))
print("Start " +start.strftime("%m/%d/%Y, %H:%M:%S")+" avgtoklen: "+str(avgtoklen))
with open ("data/editdistance/levenshtein.txt", "w", encoding="utf8") as outf:
    for token1 in bw:
        if counter > 0:
            if len(token1)>=avgtoklen:
                for token2 in bw:
                    if counter > 0:
                        if token1 != token2 and not len(token1)-len(token2) > maxls :
                            ls = iterative_levenshtein(token1, token2)
                            if(ls<=maxls and ls < len(token1) and ls < len(token2)):
                                outf.write(token1+tab+token2+tab+str(ls)+nl)
                                counter -= 1
                                print(token1+tab+token2+tab+str(ls)+tab+str(counter))
end = datetime.now()

print(str(end-start))

