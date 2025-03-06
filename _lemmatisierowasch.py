from urllib.request import urlopen
import sys
import os
import shutil
import sqlite3
from config import *

lemmabag = {}
bagofwords = {}

with open("data/bagofwords/_all.txt", "r", encoding = "utf8") as bwin:
    for line in bwin:
        linearr = line.split("\t")
        bagofwords[linearr[0]] = int(linearr[1])

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
        

def tokencheck(token):
    if not token in bagofwords:
        return False
    return True
    
def lemmamapping(urn):
    global ctsurl
    global copyrighttoken
    requestctsurl(urn)
    res = ""
    data = urlopen(ctsurl+"plain/passage.php?urn="+urn+"&copyrighttoken="+copyrighttoken) 
    print("requested")
    for line in data: 
        res+=line.decode('utf-8')
    
    wordelements = res.split("<w")
    res = ""
    for we in wordelements:
        if("</w" in we):
            wetype = ""
            subtype=""
            lemma=""
            norm=""
            token = we.split('>')[1].split('</')[0].replace('"',' ').replace("'"," ").replace(".","").strip().lower()
            if tokencheck(token):
                if 'lemma="' in we:
                    lemma = "|"+we.split('lemma="')[1].split('"')[0].replace('"',' ').replace("'"," ").strip()+"|"
                    if len(lemma) == 2:
                        lemma=""
                    else:
                        lemmaarr=lemma.split("|")
                        for lemmatoken in lemmaarr:
                            if lemmatoken in lemmabag:
                                lemmabag[lemmatoken] = lemmabag[lemmatoken]+1
                            else:
                                lemmabag[lemmatoken] = 1
                if 'norm="' in we:
                    norm = "|"+we.split('norm="')[1].split('"')[0].replace('"','')+"|"
                    if len(norm) == 2:
                        norm=""
                if "subtype" in we:
                    subtype = we.split('subtype="')[1].split('"')[0]
                if "type" in we:
                    wetype = we.split('type="')[1].split('"')[0]
                if len(lemma.strip())>0:
                    res +=token +"\t"+lemma+"\t"+norm+"\t"+wetype+"\t"+subtype +"\n"
            else:
                with open("_error.txt", "a", encoding="utf8") as errout:
                    errout.write(urn+" lemmatisierowasch unknown token "+token + "\n")
                    
    return res

    

def process(foldername):
    for yearfile in sorted(os.listdir(foldername+"peryear")):
        print("process "+foldername+":"+yearfile)
        wb = dict()
        with open (foldername+"peryear/"+yearfile, "r", encoding="utf8") as inf:
            for line in inf:
                token = line.replace("\n","")
                if token in wb:
                    wb[token] = wb[token] + 1
                else:
                    wb[token] = 1
        with open (foldername+"peryear/"+yearfile, "w", encoding="utf8") as outf:
            for token,value in sorted(wb.items(), key = lambda x:x[1], reverse=True):
                outf.write(token+"\t"+str(value)+"\n")
            
            
    wb = dict()
    for yearfile in sorted(os.listdir(foldername+"peryear")):
        with open (foldername+"peryear/"+yearfile, "r", encoding="utf8") as inf:
            for line in inf:
                linearr=line.split("\t")
                token_lemma = linearr[0]+"\t"+linearr[1]+"\t"+linearr[2]+"\t"+linearr[3]+"\t"+linearr[4]
                if token_lemma in wb:
                    wb[token_lemma] = wb[token_lemma] + int(linearr[5])
                else:
                    wb[token_lemma] = int(linearr[5])
    with open (foldername+"/_all.txt", "w", encoding="utf8") as outf:
        for token_lemma,value in sorted(wb.items(), key = lambda x:x[1], reverse=True):
            outf.write(token_lemma+"\t"+str(value)+"\n")

def collect():
    global count
    if not os.path.exists("data"):
        os.mkdir("data")
    if os.path.exists("data/lemmamapping"):
        shutil.rmtree("data/lemmamapping")
    os.mkdir("data/lemmamapping")
    if os.path.exists("data/lemmamappingperyear"):
        shutil.rmtree("data/lemmamappingperyear")
    os.mkdir("data/lemmamappingperyear")
    for line in inventory("dsb").split("\n"):
        urn = line.split("\t")[0]
        urnarr = urn.split(".")
        year = line.split("\t")[2]

        if (len(year)>1 and count!=0):
            count-=1
            print(str(count)+" "+urn)
            with open ("data/lemmamapping/"+urn.replace(":","_")+".txt", "w",encoding="utf8") as outf,open ("data/lemmamappingperyear/"+year+".txt", "a",encoding="utf8") as outyf:
                rs = lemmamapping(urn)
                outf.write(rs)
                outyf.write(rs)

    process("data/lemmamapping")
    with open ("data/lemmamapping/_lemmabag.txt", "w",encoding="utf8") as outf:
        for token,value in sorted(lemmabag.items(), key = lambda x:x[1], reverse=True):
            if len(token.strip())>0:
                outf.write(token+"\t"+str(value)+"\n")


def index():
    con = sqlite3.connect("data/lemmamapping.db")
    cursor = con.cursor()
    print("Indexing...")
    cursor.execute("CREATE INDEX tokenindextype ON tokenlemmanormtypesubtypefrequency(token);")
    cursor.execute("CREATE INDEX lemmaindextype ON tokenlemmanormtypesubtypefrequency(lemma);")
    cursor.execute("CREATE INDEX normindextype ON tokenlemmanormtypesubtypefrequency(norm);")
    cursor.execute("CREATE INDEX typeindextype ON tokenlemmanormtypesubtypefrequency(type);")
    cursor.execute("CREATE INDEX subtypeindextype ON tokenlemmanormtypesubtypefrequency(subtype);")
    cursor.execute("CREATE INDEX tokenindex ON tokenlemmanormtypesubtypedatefrequency(token);")
    cursor.execute("CREATE INDEX lemmaindex ON tokenlemmanormtypesubtypedatefrequency(lemma);")
    cursor.execute("CREATE INDEX normindex ON tokenlemmanormtypesubtypedatefrequency(norm);")
    cursor.execute("CREATE INDEX typeindex ON tokenlemmanormtypesubtypedatefrequency(type);")
    cursor.execute("CREATE INDEX subtypeindex ON tokenlemmanormtypesubtypedatefrequency(subtype);")
    cursor.execute("CREATE INDEX dateindex ON tokenlemmanormtypesubtypedatefrequency(date);")
    cursor.execute("CREATE INDEX lemmafrequencyindex ON lemmafrequency(lemma);")
    cursor.execute("CREATE INDEX lemmatokenlemmaindex ON lemmatokenfrequency(lemma);")
    cursor.execute("CREATE INDEX lemmatokentokenindex ON lemmatokenfrequency(token);")

def initTables():
    if os.path.exists("data/lemmamapping.db"):
        os.remove("data/lemmamapping.db")
    con = sqlite3.connect("data/lemmamapping.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE tokenlemmanormtypesubtypedatefrequency(token VARCHAR ("+str(tokenlength)+"),lemma VARCHAR (50),norm VARCHAR (50),type VARCHAR (10),subtype VARCHAR (10),date DATE,frequency INTEGER);")
    cursor.execute("CREATE TABLE tokenlemmanormtypesubtypefrequency(token VARCHAR ("+str(tokenlength)+"),lemma VARCHAR (50),norm VARCHAR (50),type VARCHAR (10),subtype VARCHAR (10),frequency INTEGER);")
    cursor.execute("CREATE TABLE lemmafrequency(lemma VARCHAR (50),frequency INTEGER);")
    cursor.execute("CREATE TABLE lemmatokenfrequency(lemma VARCHAR (50),token VARCHAR ("+str(tokenlength)+"),frequency INTEGER);")
    con.commit()
    con.close()
    
def db():
    initTables()
    con = sqlite3.connect("data/lemmamapping.db")
    cursor = con.cursor()

    lemmatokenbag = {}
    lemmatokennormtypesubtypebag = {}

    yearfiles = sorted(os.listdir("data/lemmamappingperyear"))
    for year in yearfiles:
        print("sql lemmamappingperyear:"+year)
        with open ("data/lemmamappingperyear/"+year, "r", encoding="utf8") as inf:
            for line in inf.readlines():
                if len(line.strip())>0:
                    linearr = line.split("\t")
                    toklem = linearr[0]+"\t"+linearr[1]
                    toklemnormtypesubtype = linearr[0]+"\t"+linearr[1]+"\t"+linearr[2]+"\t"+linearr[3]+"\t"+linearr[4]

                    if toklemnormtypesubtype in lemmatokennormtypesubtypebag:
                        lemmatokennormtypesubtypebag[toklemnormtypesubtype] = lemmatokennormtypesubtypebag[toklemnormtypesubtype]+int(linearr[5])
                    else:
                        lemmatokennormtypesubtypebag[toklemnormtypesubtype] = int(linearr[5])
                        

                    if toklem in lemmatokenbag:
                        lemmatokenbag[toklem] = lemmatokenbag[toklem]+int(linearr[5])
                    else:
                        lemmatokenbag[toklem] = int(linearr[5])

                    vals = '"'+linearr[0]+'","'+linearr[1]+'","'+linearr[2]+'","'+linearr[3]+'","'+linearr[4]+'",'+year.replace(".txt","")+','+linearr[5].strip()
                    query="INSERT INTO tokenlemmanormtypesubtypedatefrequency(token,lemma,norm,type,subtype,date,frequency) VALUES("+vals+")"
                    cursor.execute(query)
        con.commit()
    with open ("data/lemmamapping/_lemmabag.txt", "r", encoding="utf8") as inf:
        for line in inf.readlines():
            if len(line.strip())>0:
                linearr = line.split("\t")
                vals = '"'+linearr[0]+'",'+linearr[1].strip()
                query="INSERT INTO lemmafrequency(lemma,frequency) VALUES("+vals+")"
                cursor.execute(query)
        con.commit()
    for lemmatoken in lemmatokenbag:
        vals = '"'+lemmatoken.replace("\t",'","')+'",'+str(lemmatokenbag[lemmatoken])
        query = "INSERT INTO lemmatokenfrequency(token,lemma,frequency) VALUES("+vals+")"
        cursor.execute(query)
    con.commit()
    for toklemtypesubtypenorm in lemmatokennormtypesubtypebag:
        vals = '"'+toklemtypesubtypenorm.replace("\t",'","')+'",'+str(lemmatokennormtypesubtypebag[toklemtypesubtypenorm])
        query = "INSERT INTO tokenlemmanormtypesubtypefrequency(token,lemma,norm,type,subtype,frequency) VALUES("+vals+")"
        cursor.execute(query)
    con.commit()

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
    
