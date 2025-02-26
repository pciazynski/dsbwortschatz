from urllib.request import urlopen
import sys
import os
import shutil
import portermarekdiacrit as porter
import sqlite3
from config import *

entitytypes = {}

tag = ""

if len(sys.argv) > 1:
    tag = sys.argv[2]
    for learnfile in sorted(os.listdir("learn")):
        if learnfile.startswith(sys.argv[1]) and learnfile.endswith(".txt"):
            with open ("learn/"+learnfile, "r", encoding = "utf8") as infile:
                for line in infile:
                    if len(line.strip()) > 0:
                        linearr = line.split("\t")
                        if len(linearr[1].strip()) == 0:
                            linearr[1] = "NULL"
                        linearr[0] = porter.myporter(linearr[0])

                        if not linearr[0] in entitytypes or len(entitytypes[linearr[0]])<len(linearr[1].strip()):
                            entitytypes[linearr[0]] = linearr[1].strip()
else:
    for learnfile in sorted(os.listdir("learn")):
        if learnfile.endswith(".txt"):
            with open ("learn/"+learnfile, "r", encoding = "utf8") as infile:
                for line in infile:
                    if len(line.strip()) > 0:
                        linearr = line.split("\t")
                        if len(linearr[1].strip()) == 0:
                            linearr[1] = "NULL"
                        linearr[0] = porter.myporter(linearr[0])

                        if not linearr[0] in entitytypes or len(entitytypes[linearr[0]])<len(linearr[1].strip()):
                            entitytypes[linearr[0]] = linearr[1].strip()

dbname = "data/entities"+tag+".db"

if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/entities"+tag):
    shutil.rmtree("data/entities"+tag)
os.mkdir("data/entities"+tag)
if os.path.exists("data/entities"+tag+"peryear"):
    shutil.rmtree("data/entities"+tag+"peryear")
os.mkdir("data/entities"+tag+"peryear")

def initTables(dbname):
    if os.path.exists(dbname):
        os.remove(dbname)
    con = sqlite3.connect(dbname)
    cursor = con.cursor()
    cursor.execute("CREATE TABLE stemmingmapping(stemming VARCHAR (50),mapping VARCHAR (50));")
    cursor.execute("CREATE TABLE tokendatecount(token VARCHAR (50),tag VARCHAR (50), date DATE,frequency INTEGER);")
    cursor.execute("CREATE TABLE tokenurndatecount(token VARCHAR (50),tag VARCHAR (50), urn VARCHAR (50), date DATE, frequency INTEGER);")
    cursor.execute("CREATE INDEX tokenindex ON tokendatecount(token);")
    cursor.execute("CREATE INDEX tokendateindex ON tokendatecount(date);")
    cursor.execute("CREATE INDEX tokentagindex ON tokendatecount(tag);")
    cursor.execute("CREATE INDEX tokenurntokenindex ON tokenurndatecount(token);")
    cursor.execute("CREATE INDEX tokenurndateindex ON tokenurndatecount(date);")
    cursor.execute("CREATE INDEX tokenurnindex ON tokenurndatecount(urn);")
    cursor.execute("CREATE INDEX tokenurntagindex ON tokenurndatecount(tag);")
    cursor.execute("CREATE INDEX stemmingindex ON stemmingmapping(stemming);")
    cursor.execute("CREATE INDEX stemmingmappingindex ON stemmingmapping(mapping);")
    con.commit()
    con.close()
mapping = {}

def inventory(endpoint):
    global ctsurl
    requestctsurl(endpoint)
    res = ""
    data = urlopen(ctsurl+"plain/editions.php") 
    for line in data: 
        res+=line.decode('utf-8')
    return res.strip()

def requestctsurl(ns):
    global ctsurl
    if len(ctsurl) == 0:
        if not ns.startswith("urn:cts"):
            ns = "urn:cts:"+ns
        ns = ns.split(":")[2]
        data = urlopen("https://urncts.eu/namespaceresolver/"+ns) 
        for line in data: 
            ctsurl+=line.decode('utf-8')
        

def entities(urn):
    entitiesfreq = {}
    global ctsurl
    print(ctsurl+"tm/entities.php?urn="+urn+"&sort")
    requestctsurl(urn)
    data = urlopen(ctsurl+"tm/entities.php?urn="+urn+"&sort")
    for line in data: 
        enttype = ""
        line = line.strip()
        linearr = line.decode('utf-8').split("\t")
        token = porter.myporter(linearr[0])
        if not token in mapping:
            mapping[token] = linearr[0]+","
        if not ","+linearr[0]+"," in ","+mapping[token]:
            mapping[token] = mapping[token] + linearr[0]+","
        if token in entitytypes or len(sys.argv) == 1:
            if token in entitiesfreq:
                entitiesfreq[token] = entitiesfreq[token] + int(linearr[1])
            else:
                entitiesfreq[token] = int(linearr[1])
    res = ""
    for token in entitiesfreq:
        if token in entitytypes:
            enttype = entitytypes[token]
        else:
            enttype=""
        res+=token+"\t"+str(entitiesfreq[token])+"\t"+enttype+"\n"
    return res

def process(foldername):
    for yearfile in sorted(os.listdir(foldername+"peryear")):
        print("process "+foldername+":"+yearfile)
        wb = dict()
        with open (foldername+"peryear/"+yearfile, "r", encoding="utf8") as inf:
            for line in inf:
                linearr=line.split("\t")
                token = linearr[0]
                if token in wb:
                    wb[token] = wb[token] + int(linearr[1])
                else:
                    wb[token] = int(linearr[1])
        with open (foldername+"peryear/"+yearfile, "w", encoding="utf8") as outf:
            for token,value in sorted(wb.items(), key = lambda x:x[1], reverse=True):
                enttype = ""
                if token in entitytypes:
                    enttype = entitytypes[token]
                outf.write(token+"\t"+str(value)+"\t"+enttype+"\n")

    wb = dict()
    for yearfile in sorted(os.listdir(foldername+"peryear")):
        with open (foldername+"peryear/"+yearfile, "r", encoding="utf8") as inf:
            for line in inf:
                linearr=line.split("\t")
                token = linearr[0]
                if token in wb:
                    wb[token] = wb[token] + int(linearr[1])
                else:
                    wb[token] = int(linearr[1])
    with open (foldername+"/_all.txt", "w", encoding="utf8") as outf:
        for token,value in sorted(wb.items(), key = lambda x:x[1], reverse=True):
            enttype = ""
            if token in entitytypes:
                enttype = entitytypes[token]
            outf.write(token+"\t"+str(value)+"\t"+enttype+"\n")


for line in inventory("dsb").split("\n"):
    urn = line.split("\t")[0]
    urnarr = urn.split(".")
    year = line.split("\t")[2]
    if (len(year)>1 and count!=0):
        print(str(count)+" "+urn)
        count-=1
        with open ("data/entities"+tag+"/"+urn.replace(":","_#_")+".txt", "w",encoding="utf8") as outf,open ("data/entities"+tag+"peryear/"+year+".txt", "a",encoding="utf8") as outyf:
            rs = entities(urn)
            print("requested")
            outf.write(rs)
            outyf.write(rs)

with open ("data/stemmingmapping"+tag+".txt", "w", encoding="utf8") as pout:
    for key in mapping:
        pout.write(key+"\t"+mapping[key][:-1]+"\n")

#process erzeugt _all.txt und komprimiert die Jahres-.txt
process("data/entities"+tag)

initTables(dbname)
con = sqlite3.connect(dbname)
cursor = con.cursor()

with open ("data/stemmingmapping"+tag+".txt", "r", encoding="utf8") as inf:
    for line in inf.readlines():
        if len(line.strip())>0:
            linearr = line.split("\t")
            mappingarr = linearr[1].split(",")
            for m in mappingarr:
                vals = '"'+linearr[0]+'",'+'"'+m+'"'
                query="INSERT INTO stemmingmapping(stemming,mapping) VALUES("+vals+")"
                cursor.execute(query)
con.commit()

for year in sorted(os.listdir("data/entities"+tag+"peryear")):
    print("sql entities"+tag+"peryear:"+year)
    with open ("data/entities"+tag+"peryear/"+year, "r", encoding="utf8") as inf:
        for line in inf.readlines():
            if len(line.strip())>0:
                linearr = line.split("\t")
                vals = '"'+linearr[0]+'",'+'"'+linearr[2]+'",'+year.replace(".txt","")+','+linearr[1]
                query="INSERT INTO tokendatecount(token,tag,date,frequency) VALUES("+vals+")"
                cursor.execute(query)
    con.commit()


for urn in sorted(os.listdir("data/entities"+tag)):
    if not urn.startswith("_all"):
        yeararr = urn.split(".")
        year = "NULL"
        for yearcandi in yeararr:
            if len(yearcandi)==4 and yearcandi.isdigit():
                year = yearcandi
        with open ("data/entities"+tag+"/"+urn, "r", encoding="utf8") as inf:
            urn = urn.replace("&",":").replace(".txt","")
            print("sql entities"+tag+":"+urn+" "+year)
            for line in inf.readlines():
                if len(line.strip())>0:
                    linearr = line.split("\t")
                    vals = '"'+linearr[0]+'",'+'"'+linearr[2]+'","'+urn+'",'+year+','+linearr[1]
                    query="INSERT INTO tokenurndatecount(token,tag,urn,date,frequency) VALUES("+vals+")"
                    cursor.execute(query)
    con.commit()
