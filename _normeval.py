import os
import shutil

normbag = {}
normambiquebag = {}
normgroupbag = {}
normuniquebag = {}

if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/normmapping"):
    shutil.rmtree("data/normmapping")
os.mkdir("data/normmapping")
    
with open ("data/lemmamapping/_all.txt", "r", encoding="utf8") as inf:
    for line in inf:
        linearr = line.split("\t")
        norm = linearr[2]
        norm = norm[1:-1]
        if len(norm) > 0:
            normarr = norm.split("|")
            if(len(normarr)>1):
                if norm in normgroupbag:
                    normgroupbag[norm] = normgroupbag[norm]+1
                else:
                    normgroupbag[norm] = 1
                for key in normarr:
                    if key in normambiquebag:
                        normambiquebag[key] = normambiquebag[key]+1
                    else:
                        normambiquebag[key] = 1
                    
            for key in normarr:
                if key in normbag:
                    normbag[key] = normbag[key]+1
                else:
                    normbag[key] = 1

normuniquenessbag = {}
normunique = {}

for norm in normbag:
    insg = normbag[norm]
    if norm in normambiquebag:
        ambique = normambiquebag[norm]
    else:
        normambiquebag[norm] = 0
        ambique = 0
    unique = insg - ambique
    normunique[norm] = unique
    normuniquenessbag[norm] = unique / insg
with open("data/normmapping/_normuniqueness.txt", "w", encoding="utf8") as outf:
    for norm,value in sorted(normuniquenessbag.items(), key = lambda x:x[1], reverse=True):
        outf.write(norm+"\t"+str(normuniquenessbag[norm]) + "\t" + str(normunique[norm]) +"\t" + str(normambiquebag[norm]) + "\n")
        
