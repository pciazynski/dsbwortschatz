import os
import shutil

word_lemma = {}
lemma_wordbag = {}
items = {}
lemmaitems = {}

counter = 0

def reset():
    if not os.path.exists("data"):
        os.mkdir("data")
    if os.path.exists("data/mjenjoweda"):
        shutil.rmtree("data/mjenjoweda")
    os.mkdir("data/mjenjoweda")
reset()

with open ("learn/ortsliste.txt","r",encoding="utf8") as oin:
    for line in oin:
        linearr = line.split("\t")
        tmp = linearr[0].lower()
        items[tmp] = line
            
with open ("data/lemmamapping/_all.txt", "r", encoding="utf8") as bwin:
    for line in bwin:
        linearr = line.split("\t")
        if linearr[0] in items:
            lemma_wordbag[linearr[1]] = {}
            lemmaitems[linearr[1]] = items[linearr[0]]
            
with open ("data/lemmamapping/_all.txt", "r", encoding="utf8") as bwin:
    for line in bwin:
        linearr = line.split("\t")
        if linearr[1] in lemma_wordbag:
            if not (linearr[0]) in lemma_wordbag[linearr[1]]:
                tmp = lemma_wordbag[linearr[1]]
                tmp[linearr[0]] = 1
                lemma_wordbag[linearr[1]] = tmp

with open("data/mjenjoweda/ortsliste.txt", "w", encoding="utf8") as out,open("data/mjenjoweda/ortsinfo.txt", "w", encoding="utf8") as out2:
    for lemma in sorted(lemma_wordbag):
        tmp = "|"
        for word in lemma_wordbag[lemma]:
            tmp+=word+"|"
        out.write(lemma+"\t"+tmp+"\n")
        out2.write(lemmaitems[lemma])
    
