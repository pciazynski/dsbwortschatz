from urllib.request import urlopen
import sys
import os
import shutil
import sqlite3
import sys
from config import *

n=sys.argv[1]
bagofwords = {}

with open("data/bagofwords/_all.txt", "r", encoding = "utf8") as bwin:
    for line in bwin:
        linearr = line.split("\t")
        bagofwords[linearr[0]] = int(linearr[1])


if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/ngram"+n):
    shutil.rmtree("data/ngram"+n)
os.mkdir("data/ngram"+n)
if os.path.exists("data/ngram"+n+"peryear"):
    shutil.rmtree("data/ngram"+n+"peryear")
os.mkdir("data/ngram"+n+"peryear")


def inventory(endpoint):
    global ctsurl
    requestctsurl(endpoint)
    res = ""
    print(ctsurl+"plain/editions.php")
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

def tokencheck(line):
    linearr = line.split("\t")[0].split("_")
    for token in linearr:
        if not token.strip() in bagofwords:
            return False
    return True
    
    
def ngram(urn,ngramsize):
    global ctsurl
    requestctsurl(urn)
    res = ""
    data = urlopen(ctsurl+"tm/ngrams.php?urn="+urn+"&sort&&lowercase&n="+str(ngramsize))
    for line in data:
        line = line.decode('utf-8')    
        if tokencheck(line):
            res+=line
        else:
            with open("_error.txt", "a", encoding="utf8") as errout:
                errout.write(urn+" ngram "+ngramsize+" unknown tokens in "+line + "\n")
            #print(line)
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
                outf.write(token+"\t"+str(value)+"\n")
            
            
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
            outf.write(token+"\t"+str(value)+"\n")



for line in inventory("dsb").split("\n"):
    urn = line.split("\t")[0]
    urnarr = urn.split(".")
    year = line.split("\t")[2]

    if (len(year)>1 and count!=0):
        count-=1
        print(str(count)+" "+urn)
        with open ("data/ngram"+n+"/"+urn.replace(":","_#_")+".txt", "w",encoding="utf8") as outf,open ("data/ngram"+n+"peryear/"+year+".txt", "a",encoding="utf8") as outyf:
            rs = ngram(urn,n)
            outf.write(rs)
            outyf.write(rs)

process("data/ngram"+n)


def initTables(n):
    if os.path.exists("data/ngram"+n+".db"):
        os.remove("data/ngram"+n+".db")
    con = sqlite3.connect("data/ngram"+n+".db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE ngramdatecount(ngram VARCHAR (50),date DATE,frequency INTEGER);")
    cursor.execute("CREATE INDEX ngramdateindex ON ngramdatecount(ngram);")
    cursor.execute("CREATE INDEX dateindex ON ngramdatecount(date);")
    cursor.execute("CREATE TABLE ngramcount(ngram VARCHAR (50),frequency INTEGER);")
    cursor.execute("CREATE INDEX ngramindex ON ngramcount(ngram);")
    con.commit()
    con.close()


initTables(n)
con = sqlite3.connect("data/ngram"+n+".db")
cursor = con.cursor()

#for file in sorted(os.listdir("data")):
#    if(file.startswith("ngram")  and not ".db" in file and file.endswith("peryear")):
for year in sorted(os.listdir("data/ngram"+n+"peryear")):
    print("sql ngram"+n+"peryear:"+year)
    with open ("data/ngram"+n+"peryear/"+year, "r", encoding="utf8") as inf:
        for line in inf.readlines():
            if len(line.strip())>0:
                linearr = line.split("\t")
                vals = '"_'+linearr[0]+'_",'+year.replace(".txt","")+','+linearr[1].strip()
                query="INSERT INTO ngramdatecount(ngram,date,frequency) VALUES("+vals+")"
                cursor.execute(query)
            
con.commit()

#for file in sorted(os.listdir("data")):
#    if(file.startswith("ngram") and not ".db" in file and not file.endswith("peryear")):
with open ("data/ngram"+n+"/_all.txt", "r", encoding="utf8") as inf:
    for line in inf.readlines():
        if len(line.strip())>0:
            linearr = line.split("\t")
            vals = '"_'+linearr[0]+'_",'+linearr[1].strip()
            query="INSERT INTO ngramcount(ngram,frequency) VALUES("+vals+")"
            cursor.execute(query)
con.commit()

con.close()

