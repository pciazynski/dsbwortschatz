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
    if os.path.exists("data/authors"):
        shutil.rmtree("data/authors")
    os.mkdir("data/authors")

def collect():
    global count
    reset()
    print("Collect...")
    with open("data/metadata/_all.txt", "r",encoding="utf8") as inf, open("data/authors/_coauthors.txt", "w",encoding="utf8") as outf:
        for line in inf:
            linearr = line.split("\t")
            urn = linearr[0]
            year = linearr[2]
            authors = linearr[3].split(",")
            if len(authors)>2:
                for au in authors:
                    for coau in authors:
                        if au != coau:
                            outf.write(au.strip()+"\t"+urn+"\t"+coau.strip()+"\t"+year+"\n")

def initTables():
    if os.path.exists("data/authors.db"):
        os.remove("data/authors.db")
    con = sqlite3.connect("data/authors.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE coauthors(urn VARCHAR (50), author1 VARCHAR (50),author2 VARCHAR (50), year INTEGER);")
    con.commit()
    con.close()

def index():
    con = sqlite3.connect("data/authors.db")
    cursor = con.cursor()
    print("Indexing...")
    cursor.execute("CREATE INDEX author1index ON coauthors(author1);")
    cursor.execute("CREATE INDEX yearindex ON coauthors(year);")
    cursor.execute("CREATE INDEX author2index ON coauthors(author2);")
    cursor.execute("CREATE INDEX urnindex ON coauthors(urn);")
    con.commit()
    con.close()

def db():
    print("DB...")
    initTables()
    con = sqlite3.connect("data/authors.db")
    cursor = con.cursor()
    with open("data/authors/_coauthors.txt", "r",encoding="utf8") as inf:
        for line in inf:
            query = "INSERT INTO coauthors(author1,urn,author2,year) VALUES(?,?,?,?)"
            values = ['','','','']
            tmp = line.strip("\n").split("\t")
            counter = 0
            for key in tmp:
                values[counter] = key
                counter+=1
            cursor.execute(query,values)

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
    
