from urllib.request import urlopen
import sys
import os
import shutil
import sqlite3
import time
from config import *
import re
import string

ctsurl = ""
deudict = {}

with open("data/langDetect3/deu.txt", "r", encoding="utf8") as inf:
    for line in inf:
        deudict[line.split("\t")[0].strip()]=1
        
if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/langseparation"):
    shutil.rmtree("data/langseparation")
os.mkdir("data/langseparation")
if os.path.exists("data/langseparationperyear"):
    shutil.rmtree("data/langseparationperyear")
os.mkdir("data/langseparation")

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
        data = urlopen("https://tiepilab.de/cts/nsresolver/"+ns) 
        for line in data: 
            ctsurl+=line.decode('utf-8')
        
    
def langseparation(urn):
    global ctsurl
    requestctsurl(urn)
    res = ""
    data = urlopen(ctsurl+"plain/structuretext.php?urn="+urn+"&deletexml") 
    print(ctsurl+"plain/structuretext.php?urn="+urn+"&deletexml")
    translator = re.compile('[%s]' % re.escape(string.punctuation))
    for line in data:
        line = line.decode('utf-8')
        translator.sub(' ', line)
        line = re.sub(' +',' ', line).strip()
        linearr = line.split("\t")
        if len(linearr)==3:
            urn = linearr[0]
            text = linearr[2].lower()
            translator.sub(' ', text)
            text = re.sub(' +',' ', text).strip()
            textarr = text.split(" ")
            occdeu = 0
            txtdict = {}
            founddeu = ""
            for token in textarr:
                if token in deudict and not token in txtdict:
                    occdeu += 1
                    txtdict[token] = 1
                    founddeu += token+" "

            if occdeu > 0:
                res+=line+"\t"+founddeu+"\n"
    return res




                
for line in inventory("dsb").split("\n"):
    urn = line.split("\t")[0]
    urnarr = urn.split(".")
    year = line.split("\t")[2]

    if (len(year)>1 and count!=0):
        count-=1
        print(str(count)+" "+urn)
        rs = langseparation(urn)
        if len(rs.strip())>0:
            with open ("data/langseparation/"+urn.replace(":","_#_")+".txt", "w",encoding="utf8") as outf,open ("data/langseparationperyear/"+year+".txt", "a",encoding="utf8") as outyf:
                outf.write(rs)
                outyf.write(rs)

def process(foldername):
    with open (foldername+"/_all.txt", "w", encoding="utf8") as outf:
        for yearfile in sorted(os.listdir(foldername+"peryear")):
            print("process "+foldername+":"+yearfile)
            with open (foldername+"peryear/"+yearfile, "r", encoding="utf8") as inf:
                for line in inf:
                    outf.write(line)

process("data/langseparation")
