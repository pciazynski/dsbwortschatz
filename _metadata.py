
import sys
import os
import shutil
import sqlite3
from config import *
from pythoncts import *


def reset():
    print("Reset")
    if not os.path.exists("data"):
        os.mkdir("data")
    if os.path.exists("data/metadata"):
        shutil.rmtree("data/metadata")
    os.mkdir("data/metadata")

def getdoclist(ctsns):
    tmplist = ""
    if os.path.exists("urnlist.txt"):
        with open("urnlist.txt","r",encoding="utf8") as inf:
            for line in inf:
                tmplist+=line
    else:
        tmplist = cts_inventory(ctsns)
    return tmplist.strip()
    
   
def collect():
    global count
    reset()
    print("Collect...")
    doclist = getdoclist(ctsns).split("\n")
    if count == -1:
        count = len(doclist)
    with open("data/metadata/_all.txt", "w",encoding="utf8") as outf:
        for line in doclist:
            urn = line.split("\t")[0]
            if (count!=0):
                outf.write(line+"\n")
                count-=1

def initTables():
    if os.path.exists("data/metadata.db"):
        os.remove("data/metadata.db")
    con = sqlite3.connect("data/metadata.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE docmeta(urn VARCHAR (50), title VARCHAR (50), author VARCHAR (50), restricted BOOLEAN, date INTEGER);")
    con.commit()
    con.close()

def index():
    con = sqlite3.connect("data/metadata.db")
    cursor = con.cursor()
    print("Indexing...")
    cursor.execute("CREATE INDEX docmetaurnindex ON docmeta(urn);")
    cursor.execute("CREATE INDEX docmetadateindex ON docmeta(date);")
    cursor.execute("CREATE INDEX docmetaauthorindex ON docmeta(author);")
    cursor.execute("CREATE INDEX docmetatitleindex ON docmeta(title);")
    cursor.execute("CREATE INDEX docmetarestrindex ON docmeta(restricted);")
    con.commit()
    con.close()

def db():
    print("DB...")
    initTables()
    con = sqlite3.connect("data/metadata.db")
    cursor = con.cursor()
    with open("data/metadata/_all.txt", "r",encoding="utf8") as inf:
        for line in inf:
            values = line.strip("\n").replace("\t\t","\tNULL\t").replace("\t",'","').replace('"NULL"','NULL')
            query = 'INSERT INTO docmeta(urn,title,date,author,restricted) VALUES("'+values+'")'
            cursor.execute(query)

    con.commit()
    con.close()
    index()

print("Metadata")
if len(sys.argv)==2:
    if sys.argv[1] == "db":
        print("DB")
        db()
    else:
        if sys.argv[1] == "collect":
            print("Collect")
            collect()
else:
    print("Collect & DB")
    collect()
    db()
    
