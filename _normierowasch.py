import os
import shutil
import sys
import sqlite3
from config import *

normbag = {}
normambiquebag = {}
normgroupbag = {}
normuniquebag = {}

if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/normmapping"):
    shutil.rmtree("data/normmapping")
os.mkdir("data/normmapping")

def collect():
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
            


def index():
    con = sqlite3.connect("data/normmapping.db")
    cursor = con.cursor()
    print("Indexing...")
    cursor.execute("CREATE INDEX normtokenlemmaindex ON normtokenfrequency(norm);")
    cursor.execute("CREATE INDEX normtokentokenindex ON normtokenfrequency(token);")
    con.commit()
    con.close()
    
def initTables():
    if os.path.exists("data/normmapping.db"):
        os.remove("data/normmapping.db")
    con = sqlite3.connect("data/normmapping.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE normtokenfrequency(norm VARCHAR (50),token VARCHAR ("+str(tokenlength)+"),frequency INTEGER);")
    con.commit()
    con.close()
    
def db():
    initTables()
    con = sqlite3.connect("data/normmapping.db")
    cursor = con.cursor()

    normtokenbag = {}
    yearfiles = sorted(os.listdir("data/lemmamappingperyear"))
    for year in yearfiles:
        print("sql normmappingperyear:"+year)
        with open ("data/lemmamappingperyear/"+year, "r", encoding="utf8") as inf:
            for line in inf.readlines():
                if len(line.strip())>0:
                    linearr = line.split("\t")
                    toknorm = linearr[0]+"\t"+linearr[2]

                    if toknorm in normtokenbag:
                        normtokenbag[toknorm] = normtokenbag[toknorm]+int(linearr[5])
                    else:
                        normtokenbag[toknorm] = int(linearr[5])
    for normtoken in normtokenbag:
        vals = '"'+normtoken.replace("\t",'","')+'",'+str(normtokenbag[normtoken])
        query = "INSERT INTO normtokenfrequency(token,norm,frequency) VALUES("+vals+")"
        cursor.execute(query)
    con.commit()
    con.close()
    index()

if len(sys.argv)==2:
    if sys.argv[1] == "db":
        db()
    else:
        if sys.argv[1] == "collect":
            collect()
else:
    collect()
    db()
    