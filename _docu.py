import sys
import os
import shutil
import sqlite3
import datetime
import time
from config import *
import hashlib

if not os.path.exists("doc"):
    os.mkdir("doc")

curtime = str(datetime.datetime.now()).replace("-","_").replace(":","_").replace(".","_")
with open("doc/data_consistency-"+curtime+".txt", "w",encoding="utf8") as out:
    out.write("File\tBytes\tMD5 Hash\tLast Modified\n")

db_php = {}
params_php = {}

for file in os.listdir("php"):
    with open("php/"+file, "r", encoding="utf8") as inf:
        for line in inf:
            if "isset(" in line:
                param = line.split("$_GET['")[1].split("'")[0]
                if file in params_php:
                    params_php[file] = params_php[file]+","+param
                else:
                    params_php[file] = param
            if "new PDO" in line:
                db = line.split("sqlite:../data/")[1].split(")")[0][:-1]
                if not "'.$n.'" in db:
                    if not db in db_php:
                        db_php[db] = file
                    else:
                        if not file in db_php[db]:
                            db_php[db] = db_php[db] + ","+file
                else:
                    db2 = db.replace( "'.$n.'", "2")
                    if not db2 in db_php:
                        db_php[db2] = file
                    else:
                        if not file in db_php[db2]:
                            db_php[db2] = db_php[db2] + ","+file
                    db2 = db.replace( "'.$n.'", "3")
                    if not db2 in db_php:
                        db_php[db2] = file
                    else:
                        if not file in db_php[db2]:
                            db_php[db2] = db_php[db2] + ","+file
                    db2 = db.replace( "'.$n.'", "5")
                    if not db2 in db_php:
                        db_php[db2] = file
                    else:
                        if not file in db_php[db2]:
                            db_php[db2] = db_php[db2] + ","+file

with open("doc/php_params.txt", "w", encoding="utf8") as outf:
    for php in params_php:
        outf.write(php+"\t"+params_php[php])
def db(fn):
    global db_php
    print("DB "+fn)
    if fn in db_php:
        scripts = db_php[fn]
    else:
        scripts = "NONE oder Optionaler Parameter im Datenbanknamen"
    
    con = sqlite3.connect("data/"+fn)
    cur = con.cursor()
    res = "\n"+"#"*len(fn)+"\n"+fn+"\n"+"#"*len(fn)+"\n"

    res += "\n\tScripts: "+scripts+"\n"

    res += "\n\tTables\n"
    cur.execute('SELECT * FROM sqlite_master WHERE type="table"')
    rows = cur.fetchall()
    for row in rows:
        res += "\t\t"+row[1] + "\t" + row[4]+"\n"
        cur.execute('SELECT COUNT(*) FROM '+row[1])
        rows2 = cur.fetchall()
        for row2 in rows2:
            res+="\t\t\t"+str(row2[0])+" Entries\n"

    res += "\n\tIndices\n"
    cur.execute('SELECT * FROM sqlite_master WHERE type="index"')
    rows = cur.fetchall()
    for row in rows:
        res += "\t\t"+row[1]+"\t"+row[4]+"\n"
    with open("doc/database_files-"+curtime+".txt", "a",encoding="utf8") as out:
        out.write(res)

def file2md5(filename):
    return hashlib.md5(open(filename,'rb').read()).hexdigest()

def lastmodified(filename):
    return str(time.ctime(os.path.getmtime(filename)))
    
    
with open("doc/data_consistency-"+curtime+".txt", "a",encoding="utf8") as out:
        for file in os.listdir("data"):
            if os.path.isdir("data/"+file):
                for file2 in os.listdir("data/"+file):
                    out.write(file+"/"+file2+"\t"+str(os.path.getsize("data/"+file+"/"+file2))+"\t"+file2md5("data/"+file+"/"+file2)+"\t"+lastmodified("data/"+file+"/"+file2)+"\n")
            else:
                out.write(file+"\t"+str(os.path.getsize("data/"+file))+"\t"+file2md5("data/"+file)+"\t"+lastmodified("data/"+file)+"\n")

for file in os.listdir("data"):
    if file.endswith(".db"):
        db(file)

