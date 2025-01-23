import os
import shutil
import sqlite3
import sys
n=sys.argv[1]

deudict = {}
ff = {}
if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/langDetect"+n):
    shutil.rmtree("data/langDetect"+n)
os.mkdir("data/langDetect"+n)

def addff(tmp):
    if len(tmp)>0:
        ff[tmp] = 1
        ff[tmp.replace("s","ſ")] = 1
        ff[tmp.replace("s","ẜ")] = 1
        ff[tmp.replace("ẜ","s")] = 1
        ff[tmp.replace("ẜ","ſ")] = 1
        ff[tmp.replace("ſ","ẜ")] = 1
        ff[tmp.replace("ſ","s")] = 1
#d
        
with open("learn/falsefriends.txt", "r", encoding = "utf8") as inf:
    for line in inf:
        tmp = line.strip().lower()
        addff(tmp)
            
#with open("learn/ortsliste.txt", "r", encoding = "utf8") as inf:
#    for line in inf:
#        tmp = line.strip().lower().split("\t")[0]
#        addff(tmp)
#with open("learn/ortsliste_ergänzung.txt", "r", encoding = "utf8") as inf:
#    for line in inf:
#        tmp = line.strip().lower().split("\t")[0]
#        addff(tmp)
#with open("learn/namen_pre.txt", "r", encoding = "utf8") as inf:
#    for line in inf:
#        tmp = line.strip().lower().split("\t")[0]
#        addff(tmp)
#with open("learn/deutschevornamen.txt", "r", encoding = "utf8") as inf:
#    for line in inf:
#        tmp = line.strip().lower().split("\t")[0]
#        addff(tmp)
#with open("learn/weiterenamen.txt", "r", encoding = "utf8") as inf:
#    for line in inf:
#        tmp = line.strip().lower().split("\t")[0]
#        addff(tmp)
           

with open("learn/deu_mixed-typical_2011_1M-words.txt", "r", encoding = "utf8") as inf:
    for line in inf:
        tmp = line.strip().lower()
        if not tmp in ff:
            deudict[tmp] = 1
            tmp = tmp.replace("ſ","s").replace("ẜ","s")
            deudict[tmp] = 1
            
with open("learn/ids_a-h.txt", "r", encoding = "utf8") as inf:
    for line in inf:
        tmp = (line+" ").split(" ")[0].strip().lower()
        if not tmp in ff:
            deudict[tmp] = 1
            tmp = tmp.replace("ſ","s").replace("ẜ","s")
            deudict[tmp] = 1

with open("learn/found_deu.txt", "r", encoding = "utf8") as inf:
    for line in inf:
        tmp = line.strip().lower()
        deudict[tmp] = 1
        tmp = tmp.replace("ſ","s").replace("ẜ","s")
        deudict[tmp] = 1

with open("learn/stopwords_deu.txt", "r", encoding = "utf8") as inf:
    for line in inf:
            tmp = line.strip().lower()
            if not tmp in ff:
                deudict[tmp] = 1
                tmp = tmp.replace("ſ","s").replace("ẜ","s")
                deudict[tmp] = 1
        

with open("data/ngram"+n+"/_all.txt", "r", encoding = "utf8") as inf,open("data/langDetect"+n+"/ngram"+n+"_deu.txt", "w", encoding = "utf8") as deuoutf, open("data/langDetect"+n+"/ngram"+n+"_mix.txt", "w", encoding = "utf8") as mixoutf, open("data/langDetect"+n+"/ngram"+n+"_dsb.txt", "w", encoding = "utf8") as dsboutf, open("data/langDetect"+n+"/ngram"+n+"_langDetect.txt", "w", encoding = "utf8") as langDetect:
    for line in inf:
        #line = line.replace("ſ","s").replace("ẜ","s")
        line=line.lower()
        tmp = line.split("\t")[0].strip()
        tmparr = tmp.split("_")
        occ_deu = 0
        numberfound=0
        for token in tmparr:
            token = token.replace("ſ","s").replace("ẜ","s")
            if token.isdigit():
                numberfound+=1
            else:
                if token in deudict or "ä" in token or "ö" in token or "ü" in token or "½" in token or "¼" in token or "¾" in token:
                    occ_deu += 1
        if (numberfound + occ_deu) == int(n):
            occ_deu = int(n)

        if occ_deu==int(n):
            deuoutf.write(line)
        else:
            if occ_deu==0:
                dsboutf.write(line)
            else:
                mixoutf.write(line.strip()+"\t"+str(occ_deu)+"\n")
        langDetect.write(tmp+"\t"+str(occ_deu)+"\n")

deudict = {}
dsbdict = {}
mixdict = {}
mix1dict = {}
mix2dict = {}

with open("data/langDetect"+n+"/ngram"+n+"_mix.txt", "r", encoding = "utf8") as inf:
    for line in inf:
        tmparr = line.split("\t")[0].split("_")
        for tmp in tmparr:
            mixdict[tmp] = 1
            if line.split("\t")[2].strip() == "1":
                mix1dict[tmp] = 1
            if line.split("\t")[2].strip() == "2":
                mix2dict[tmp] = 1


with open("data/langDetect"+n+"/ngram"+n+"_deu.txt", "r", encoding = "utf8") as inf:
    for line in inf:
        tmparr = line.split("\t")[0].split("_")
        for tmp in tmparr:
            deudict[tmp] = 1

with open("data/langDetect"+n+"/ngram"+n+"_dsb.txt", "r", encoding = "utf8") as inf:
    for line in inf:
        tmparr = line.split("\t")[0].split("_")
        for tmp in tmparr:
            dsbdict[tmp] = 1


with open("data/bagofwords/_all.txt", "r", encoding = "utf8") as inf, open("data/langDetect"+n+"/deu.txt", "w", encoding = "utf8") as deuoutf, open("data/langDetect"+n+"/deu_slim.txt", "w", encoding = "utf8") as deuoutfslim, open("data/langDetect"+n+"/dsb.txt", "w", encoding = "utf8") as dsboutf, open("data/langDetect"+n+"/dsb_slim.txt", "w", encoding = "utf8") as dsboutfslim,open("data/langDetect"+n+"/mix.txt", "w", encoding = "utf8") as mixoutf,open("data/langDetect"+n+"/mix1.txt", "w", encoding = "utf8") as mix1outf,open("data/langDetect"+n+"/mix2.txt", "w", encoding = "utf8") as mix2outf:
    for line in inf:
        #line = line.replace("ſ","s").replace("ẜ","s")
        line = line.lower()
        tmp = line.split("\t")[0].strip()
        if tmp in deudict and not tmp in dsbdict and not tmp in mixdict:
            deuoutf.write(line)
            deuoutfslim.write(line.split("\t")[0]+"\n")
        if tmp in dsbdict and not tmp in deudict and not tmp in mixdict:
            dsboutf.write(line)
            dsboutfslim.write(line.split("\t")[0]+"\n")
        if tmp in mixdict:
            mixoutf.write(line)
        if tmp in mix1dict and not tmp in mix2dict:
            mix1outf.write(line)
        if tmp in mix2dict:
            mix2outf.write(line)

def initTables():
    if os.path.exists("data/langDetect"+n+".db"):
        os.remove("data/langDetect"+n+".db")
    con = sqlite3.connect("data/langDetect"+n+".db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE langDetectdeungram(ngram VARCHAR (50),frequency INTEGER);")
    cursor.execute("CREATE INDEX langDetectdeungramindex ON langDetectdeungram(ngram);")
    cursor.execute("CREATE TABLE langDetectdeutoken(token VARCHAR (50),frequency INTEGER);")
    cursor.execute("CREATE INDEX langDetectdeutokenindex ON langDetectdeutoken(token);")
    
    cursor.execute("CREATE TABLE langDetectdsbngram(ngram VARCHAR (50),frequency INTEGER);")
    cursor.execute("CREATE INDEX langDetectdsbngramindex ON langDetectdsbngram(ngram);")
    cursor.execute("CREATE TABLE langDetectdsbtoken(token VARCHAR (50),frequency INTEGER);")
    cursor.execute("CREATE INDEX langDetectdsbtokenindex ON langDetectdsbtoken(token);")

    cursor.execute("CREATE TABLE langDetectmixngram(ngram VARCHAR (50),frequency INTEGER, deu INTEGER);")
    cursor.execute("CREATE INDEX langDetectmixngramngramindex ON langDetectmixngram(ngram);")
    cursor.execute("CREATE INDEX langDetectmixdeuindex ON langDetectmixngram(deu);")
    
    con.commit()
    con.close()

initTables()
con = sqlite3.connect("data/langDetect"+n+".db")
cursor = con.cursor()

def insertNgramIntoTable(name):
    print("sql nGram "+name)

    with open ("data/langDetect"+n+"/ngram"+n+"_"+name+".txt", "r", encoding="utf8") as inf:
        inserts = []
        
        for line in inf.readlines():
            if len(line.strip())>0:
                linearr = line.split("\t")
                if name == "deu":
                    inserts.append(("_"+linearr[0]+"_",linearr[1]))
                    query = "INSERT INTO langDetectdeungram(ngram,frequency) VALUES(?,?)"
                elif name == "dsb":
                    inserts.append(("_"+linearr[0]+"_",linearr[1]))
                    query = "INSERT INTO langDetectdsbngram(ngram,frequency) VALUES(?,?)"
                else:
                    inserts.append(("_"+linearr[0]+"_",linearr[1],linearr[2]))
                    query = "INSERT INTO langDetectmixngram(ngram,frequency,deu) VALUES(?,?,?)"
        cursor.executemany(query,inserts)
        con.commit()

def insertTokenIntoTable(name):
    print("sql Token "+name)
    if name == "deu":
        deuval=3
    elif name == "dsb":
        deuval=0
    with open ("data/langDetect"+n+"/"+name+".txt", "r", encoding="utf8") as inf:
        inserts = []
                    
        for line in inf.readlines():
            if len(line.strip())>0:
                linearr = line.split("\t")
                if name == "deu":
                    inserts.append((linearr[0],linearr[1]))
                    query="INSERT INTO langDetectdeutoken(token,frequency) VALUES(?,?)"
                elif name == "dsb":
                    inserts.append((linearr[0],linearr[1]))
                    query="INSERT INTO langDetectdsbtoken(token,frequency) VALUES(?,?)"
        cursor.executemany(query,inserts)
        con.commit()

insertNgramIntoTable("deu")
insertNgramIntoTable("dsb")
insertNgramIntoTable("mix")

insertTokenIntoTable("deu")
insertTokenIntoTable("dsb")

