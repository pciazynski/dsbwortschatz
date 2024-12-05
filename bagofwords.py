from urllib.request import urlopen
import sys
import os
import shutil
import sqlite3
from config import *

if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/bagofwords"):
    shutil.rmtree("data/bagofwords")
os.mkdir("data/bagofwords")
if os.path.exists("data/bagofwordsperyear"):
    shutil.rmtree("data/bagofwordsperyear")
os.mkdir("data/bagofwordsperyear")

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
    
def bagofwords(urn):
    global ctsurl
    requestctsurl(urn)
    res = ""
    data = urlopen(ctsurl+"tm/bagofwords.php?urn="+urn+"&sort&lowercase")
    print("requested")
    for line in data: 
        res+=line.decode('utf-8')
    return res.strip()

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
    
    wb_max = dict()
    wb_min = dict()
    for yearfile in sorted(os.listdir(foldername+"peryear")):
        with open (foldername+"peryear/"+yearfile, "r", encoding="utf8") as inf:
            for line in inf:
                year = int(yearfile.replace(".txt",""))
                token = line.split("\t")[0]
                if token in wb_max:
                    if year > wb_max[token]:
                        wb_max[token] = year
                else:
                    wb_max[token] = year
                if token in wb_min: 
                    if year < wb_min[token]:
                        wb_min[token] = year
                else:
                    wb_min[token] = year                    
    with open (foldername+"/_minmaxyearzipf.txt", "w", encoding="utf8") as outf:
        for token,value in sorted(wb.items(),key = lambda x:x[1], reverse=True):
            outf.write(token+"\t"+str(wb_min[token])+"\t"+str(wb_max[token])+"\t"+str(value)+"\n")
    daterange = {}
    for token,value in sorted(wb_min.items(),key = lambda x:x[1], reverse=False):
        drange = str(wb_min[token])+"\t"+str(wb_max[token])
        if not drange in daterange:
            daterange[drange] = token
        else:
            daterange[drange] = daterange[drange]+","+token
    with open (foldername+"/_minmaxyearmin.txt", "w", encoding="utf8") as outf:
        for key in daterange:
            outf.write(key+"\t"+daterange[key]+"\n")
            
    daterange = {}
    for token,value in sorted(wb_max.items(),key = lambda x:x[1], reverse=False):
        drange = str(wb_min[token])+"\t"+str(wb_max[token])
        if not drange in daterange:
            daterange[drange] = token
        else:
            daterange[drange] = daterange[drange]+","+token
    with open (foldername+"/_minmaxyearmax.txt", "w", encoding="utf8") as outf:
        for key in daterange:
            outf.write(key+"\t"+daterange[key]+"\n")

def sanitycheck(rs):
    for line in rs.split("\n"):
        linearr = line.split("\t")
        if len(linearr)!= 2:
            print("+"+line)
            return False
    return True
    
for line in inventory("dsb").split("\n"):
    urn = line.split("\t")[0]
    urnarr = urn.split(".")
    year = line.split("\t")[2]

    if (len(year)>1 and count!=0):
        count-=1
        print(str(count)+" "+urn)
        with open ("data/bagofwords/"+urn.replace(":","_#_")+".txt", "w",encoding="utf8") as outf,open ("data/bagofwordsperyear/"+year+".txt", "a",encoding="utf8") as outyf:
            rs = bagofwords(urn)
            if sanitycheck(rs):
                outf.write(rs)
                outyf.write(rs+"\n")
            else:
                with open ("_error.txt", "a", encoding="utf8") as errout:
                    errout.write(urn+"->bagofwords incomplete\n")

process("data/bagofwords")

def initTables():
    if os.path.exists("data/bagofwords.db"):
        os.remove("data/bagofwords.db")
    con = sqlite3.connect("data/bagofwords.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE tokendatecount(token VARCHAR (50),date DATE,frequency INTEGER);")
    cursor.execute("CREATE TABLE urnwordbag(urn VARCHAR (50),date DATE,wordbag text);")
    cursor.execute("CREATE INDEX tokenindex ON tokendatecount(token);")
    cursor.execute("CREATE INDEX tokenurnindex ON urnwordbag(urn);")
    cursor.execute("CREATE INDEX urnindex ON urnwordbag(wordbag);")
    cursor.execute("CREATE INDEX urndateindex ON urnwordbag(date);")
    cursor.execute("CREATE INDEX dateindex ON tokendatecount(date);")
    con.commit()
    con.close()
    
initTables()
con = sqlite3.connect("data/bagofwords.db")
cursor = con.cursor()

yearfiles = sorted(os.listdir("data/bagofwordsperyear"))
for year in yearfiles:
    print("sql bagofwordsperyear:"+year)
    with open ("data/bagofwordsperyear/"+year, "r", encoding="utf8") as inf:
        for line in inf.readlines():
            if len(line.strip())>0:
                linearr = line.split("\t")
                vals = '"'+linearr[0]+'",'+year.replace(".txt","")+','+linearr[1]
                query="INSERT INTO tokendatecount(token,date,frequency) VALUES("+vals+")"
                cursor.execute(query)
    con.commit()
    
files = sorted(os.listdir("data/bagofwords"))
for file in files:
    if file.startswith("urn_#_"):
        print("sql bagofwordsperurn:"+file)
        with open ("data/bagofwords/"+file, "r", encoding="utf8") as inf:
            wordbag = "|"
            for line in inf.readlines():
                if len(line.strip())>0:
                    wordbag += line.split("\t")[0]+"|"
            urn = file.replace(".txt","").replace("_#_",":")
            year = urn.split(":")[3].split(".")[2]
            vals = '"'+urn+'","'+year+'","'+wordbag+'"'
            query="INSERT INTO urnwordbag(urn,date,wordbag) VALUES("+vals+")"
            cursor.execute(query)
    con.commit()
