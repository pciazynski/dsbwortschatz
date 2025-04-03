from urllib.request import urlopen
import sys
import os
import shutil
import sqlite3
import time
from config import *
import re
import string
n=sys.argv[1]

deudict = {}

with open("data/langDetect"+str(n)+"/deu.txt", "r", encoding="utf8") as inf:
    for line in inf:
        deudict[line.split("\t")[0].strip()]=1

if not os.path.exists("data"):
    os.mkdir("data")

def reset():
    print("Reset")
    if os.path.exists("data/langseparation"):
        shutil.rmtree("data/langseparation")
    os.mkdir("data/langseparation")
    if os.path.exists("data/langseparationperyear"):
        shutil.rmtree("data/langseparationperyear")
    os.mkdir("data/langseparationperyear")

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
        
    
def langseparation(urn):
    global ctsurl
    global copyrighttoken
    requestctsurl(urn)
    res = ""
    data = urlopen(ctsurl+"plain/structuretext.php?urn="+urn+"&deletexml"+"&copyrighttoken="+copyrighttoken) 
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

def collect():
    global count
    reset()
    print("Collect...")
    doclist = inventory("dsb").split("\n")
    if count == -1:
        count = len(doclist)
            
    for line in doclist:
        urn = line.split("\t")[0]
        urnarr = urn.split(".")
        year = line.split("\t")[2]

        if (len(year)>1 and count!=0):
            count-=1
            rs = langseparation(urn)
            print(str(count)+" "+urn+" "+str(len(rs.strip())))
            if len(rs.strip())>0:
                with open ("data/langseparation/"+urn.replace(":","_#_")+".txt", "w",encoding="utf8") as outf,open ("data/langseparationperyear/"+year+".txt", "a",encoding="utf8") as outyf:
                    outf.write(rs)
                    outyf.write(rs)

    with open (foldername+"/_all.txt", "w", encoding="utf8") as outf:
        for yearfile in sorted(os.listdir(foldername+"peryear")):
            print("process "+foldername+":"+yearfile)
            with open (foldername+"peryear/"+yearfile, "r", encoding="utf8") as inf:
                for line in inf:
                    outf.write(line)

if len(sys.argv)==3:
    if sys.argv[1] == "db":
        db()
    else:
        if sys.argv[1] == "collect":
            collect()
else:
    collect()
    db()
    
