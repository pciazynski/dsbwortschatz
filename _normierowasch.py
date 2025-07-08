from urllib.request import urlopen
import sys
import os
import shutil
import sqlite3
from config import *
from pythoncts import *

normbag = {}
bagofwords = {}

with open("data/bagofwords/_all.txt", "r", encoding = "utf8") as bwin:
    for line in bwin:
        linearr = line.split("\t")
        bagofwords[linearr[0]] = int(linearr[1])

def tokencheck(token):
    if not token in bagofwords:
        return False
    return True


    
def normmapping(urn):
    global ctsurl
    global copyrighttoken
    res = textpassage(urn,"&copyrighttoken="+copyrighttoken)

    
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
                    #if len(lemma) == 2:
                    #    lemma=""
                    #else:
                        #lemmaarr=lemma.split("|")
                        #for lemmatoken in lemmaarr:
                if 'norm="' in we:
                    norm = "|"+we.split('norm="')[1].split('"')[0].replace('"','')+"|"
                    #if len(norm) == 2:
                    #    norm=""
                    if norm in normbag:
                        normbag[norm] = normbag[norm]+1
                    else:
                        normbag[norm] = 1
                if "subtype" in we:
                    subtype = we.split('subtype="')[1].split('"')[0]
                if "type" in we:
                    wetype = we.split('type="')[1].split('"')[0]
                if len(norm.strip())>0:
                    res +=token +"\t"+lemma+"\t"+norm+"\t"+wetype+"\t"+subtype +"\n"
            else:
                with open("_error.txt", "a", encoding="utf8") as errout:
                    errout.write(urn+" normierowasch unknown token "+token + "\n")
                    
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
                token_norm = linearr[0]+"\t"+linearr[1]+"\t"+linearr[2]+"\t"+linearr[3]+"\t"+linearr[4]
                if token_norm in wb:
                    wb[token_norm] = wb[token_norm] + int(linearr[5])
                else:
                    wb[token_norm] = int(linearr[5])
    with open (foldername+"/_all.txt", "w", encoding="utf8") as outf:
        for token_norm,value in sorted(wb.items(), key = lambda x:x[1], reverse=True):
            outf.write(token_norm+"\t"+str(value)+"\n")

def reset():
    if not os.path.exists("data"):
        os.mkdir("data")
    if os.path.exists("data/normmapping"):
        shutil.rmtree("data/normmapping")
    os.mkdir("data/normmapping")
    if os.path.exists("data/normmappingperyear"):
        shutil.rmtree("data/normmappingperyear")
    os.mkdir("data/normmappingperyear")
    
def getdoclist(ctsns):
    tmplist = ""
    if os.path.exists("urnlist.txt"):
        with open("urnlist.txt","r",encoding="utf8") as inf:
            for line in inf:
                tmplist+=line
    else:
        tmplist = inventory(ctsns)
    return tmplist.strip()

def collect():
    global count
    reset()
    print("Collect...")
    doclist = getdoclist(ctsns).split("\n")
    if count == -1:
        count = len(doclist)
    for line in doclist:
        urn = line.split("\t")[0]
        urnarr = urn.split(".")
        year = line.split("\t")[2]

        if (len(year)>1 and count!=0):
            print(str(count)+" "+urn)
            count-=1
            with open ("data/normmapping/"+urn.replace(":","_")+".txt", "w",encoding="utf8") as outf,open ("data/normmappingperyear/"+year+".txt", "a",encoding="utf8") as outyf:
                rs = normmapping(urn)
                outf.write(rs)
                outyf.write(rs)

    process("data/normmapping")
    with open ("data/normmapping/_normbag.txt", "w",encoding="utf8") as outf:
        for token,value in sorted(normbag.items(), key = lambda x:x[1], reverse=True):
            if len(token.strip())>0:
                outf.write(token+"\t"+str(value)+"\n")


def index():
    con = sqlite3.connect("data/normmapping.db")
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
    cursor.execute("CREATE INDEX normfrequencyindex ON normfrequency(norm);")
    cursor.execute("CREATE INDEX normtokenlemmaindex ON normtokenfrequency(norm);")
    cursor.execute("CREATE INDEX normtokentokenindex ON normtokenfrequency(token);")
    con.commit()
    con.close()
    
def initTables():
    if os.path.exists("data/normmapping.db"):
        os.remove("data/normmapping.db")
    con = sqlite3.connect("data/normmapping.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE tokenlemmanormtypesubtypedatefrequency(token VARCHAR ("+str(tokenlength)+"),lemma VARCHAR (50),norm VARCHAR (50),type VARCHAR (10),subtype VARCHAR (10),date DATE,frequency INTEGER);")
    cursor.execute("CREATE TABLE tokenlemmanormtypesubtypefrequency(token VARCHAR ("+str(tokenlength)+"),lemma VARCHAR (50),norm VARCHAR (50),type VARCHAR (10),subtype VARCHAR (10),frequency INTEGER);")
    cursor.execute("CREATE TABLE normfrequency(norm VARCHAR (50),frequency INTEGER);")
    cursor.execute("CREATE TABLE normtokenfrequency(norm VARCHAR (50),token VARCHAR ("+str(tokenlength)+"),frequency INTEGER);")
    con.commit()
    con.close()
    
def db():
    initTables()
    con = sqlite3.connect("data/normmapping.db")
    cursor = con.cursor()

    normtokenbag = {}
    lemmatokennormtypesubtypebag = {}

    yearfiles = sorted(os.listdir("data/normmappingperyear"))
    for year in yearfiles:
        print("sql normmappingperyear:"+year)
        with open ("data/normmappingperyear/"+year, "r", encoding="utf8") as inf:
            for line in inf.readlines():
                if len(line.strip())>0:
                    linearr = line.split("\t")
                    toknorm = linearr[0]+"\t"+linearr[2]
                    toklemnormtypesubtype = linearr[0]+"\t"+linearr[1]+"\t"+linearr[2]+"\t"+linearr[3]+"\t"+linearr[4]

                    if toklemnormtypesubtype in lemmatokennormtypesubtypebag:
                        lemmatokennormtypesubtypebag[toklemnormtypesubtype] = lemmatokennormtypesubtypebag[toklemnormtypesubtype]+int(linearr[5])
                    else:
                        lemmatokennormtypesubtypebag[toklemnormtypesubtype] = int(linearr[5])
                        

                    if toknorm in normtokenbag:
                        normtokenbag[toknorm] = normtokenbag[toknorm]+int(linearr[5])
                    else:
                        normtokenbag[toknorm] = int(linearr[5])

                    vals = '"'+linearr[0]+'","'+linearr[1]+'","'+linearr[2]+'","'+linearr[3]+'","'+linearr[4]+'",'+year.replace(".txt","")+','+linearr[5].strip()
                    query="INSERT INTO tokenlemmanormtypesubtypedatefrequency(token,lemma,norm,type,subtype,date,frequency) VALUES("+vals+")"
                    cursor.execute(query)
        con.commit()
    with open ("data/normmapping/_normbag.txt", "r", encoding="utf8") as inf:
        for line in inf.readlines():
            if len(line.strip())>0:
                linearr = line.split("\t")
                vals = '"'+linearr[0]+'",'+linearr[1].strip()
                query="INSERT INTO normfrequency(norm,frequency) VALUES("+vals+")"
                cursor.execute(query)
        con.commit()
    for normtoken in normtokenbag:
        vals = '"'+normtoken.replace("\t",'","')+'",'+str(normtokenbag[normtoken])
        query = "INSERT INTO normtokenfrequency(token,norm,frequency) VALUES("+vals+")"
        cursor.execute(query)
    con.commit()
    for toklemtypesubtypenorm in lemmatokennormtypesubtypebag:
        vals = '"'+toklemtypesubtypenorm.replace("\t",'","')+'",'+str(lemmatokennormtypesubtypebag[toklemtypesubtypenorm])
        query = "INSERT INTO tokenlemmanormtypesubtypefrequency(token,lemma,norm,type,subtype,frequency) VALUES("+vals+")"
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
    
