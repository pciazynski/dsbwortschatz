import os

bw = {}
bl = {}

with open ("data/lemmamapping/_all.txt", "r", encoding="utf8") as bwin:
    for line in bwin:
        linearr = line.split("\t")
        bl[linearr[0]] = 1

unlem = 0
lem = 0
with open ("data/bagofwords/_all.txt", "r", encoding="utf8") as bwin, open ("data/lemmamapping/_yay.txt", "w", encoding="utf8") as outlem,open ("data/lemmamapping/_nay.txt", "w", encoding="utf8") as outunlem:
    for line in bwin:
        linearr = line.split("\t")
        if linearr[0] in bl:
            outlem.write(line)
            lem += 1
        else:
            unlem += 1
            outunlem.write(line)
with open ("data/lemmamapping/_stats.txt", "w", encoding="utf8") as out:
    out.write("Lemmatisiert / Alle: "+str(lem)+" / "+str(lem+unlem)+"\n")

lemmabag = {}
lemmaambiquebag = {}
lemmagroupbag = {}
lemmauniquebag = {}

with open ("data/lemmamapping/_all.txt", "r", encoding="utf8") as inf:
    for line in inf:
        linearr = line.split("\t")
        lemma = linearr[1]
        lemma = lemma[1:-1]
        if len(lemma) > 0:
            lemmaarr = lemma.split("|")
            if(len(lemmaarr)>1):
                if lemma in lemmagroupbag:
                    lemmagroupbag[lemma] = lemmagroupbag[lemma]+1
                else:
                    lemmagroupbag[lemma] = 1
                for key in lemmaarr:
                    if key in lemmaambiquebag:
                        lemmaambiquebag[key] = lemmaambiquebag[key]+1
                    else:
                        lemmaambiquebag[key] = 1
                    
            for key in lemmaarr:
                if key in lemmabag:
                    lemmabag[key] = lemmabag[key]+1
                else:
                    lemmabag[key] = 1

lemmauniquenessbag = {}
lemmaunique = {}

for lemma in lemmabag:
    insg = lemmabag[lemma]
    if lemma in lemmaambiquebag:
        ambique = lemmaambiquebag[lemma]
    else:
        lemmaambiquebag[lemma] = 0
        ambique = 0
    unique = insg - ambique
    lemmaunique[lemma] = unique
    lemmauniquenessbag[lemma] = unique / insg
with open("data/lemmamapping/_lemmauniqueness.txt", "w", encoding="utf8") as outf:
    for lemma,value in sorted(lemmauniquenessbag.items(), key = lambda x:x[1], reverse=True):
        outf.write(lemma+"\t"+str(lemmauniquenessbag[lemma]) + "\t" + str(lemmaunique[lemma]) +"\t" + str(lemmaambiquebag[lemma]) + "\n")
        


        

