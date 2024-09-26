from urllib.request import urlopen
import sys
import os
import sqlite3


ctsurl = ""


if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists("data/bagofwords"):
    os.mkdir("data/bagofwords")
if not os.path.exists("data/bagofwordsperyear"):
    os.mkdir("data/bagofwordsperyear")
if not os.path.exists("data/entities"):
    os.mkdir("data/entities")
if not os.path.exists("data/entitiesperyear"):
    os.mkdir("data/entitiesperyear")
if not os.path.exists("data/ngram3"):
    os.mkdir("data/ngram3")
if not os.path.exists("data/ngram3peryear"):
    os.mkdir("data/ngram3peryear")
    

def initTables():
    con = sqlite3.connect("data/ctstm.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE entitydatecount(token VARCHAR (50),date DATE,frequency INTEGER);")
    cursor.execute("CREATE INDEX entityindex ON entitydatecount(token);")
    cursor.execute("CREATE INDEX entitydateindex ON entitydatecount(date);")
    cursor.execute("CREATE TABLE tokendatecount(token VARCHAR (50),date DATE,frequency INTEGER);")
    cursor.execute("CREATE INDEX tokenindex ON tokendatecount(token);")
    cursor.execute("CREATE INDEX dateindex ON tokendatecount(date);")
    for file in os.listdir("data"):
        if(file.startswith("ngram") and not "peryear" in file):
            cursor.execute("CREATE TABLE "+file+"datecount(ngram VARCHAR (50),date DATE,frequency INTEGER);")
            cursor.execute("CREATE INDEX "+file+"ngramondateindex ON "+file+"datecount(ngram);")
            cursor.execute("CREATE INDEX "+file+"dateindex ON "+file+"datecount(date);")
            cursor.execute("CREATE TABLE "+file+"count(ngram VARCHAR (50),frequency INTEGER);")
            cursor.execute("CREATE INDEX "+file+"index ON "+file+"count(ngram);")
    con.commit()
    con.close()

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
        
def myporter(token):
    oldtoken = ""
    token = token.replace("ó","o").replace("ó","o").replace("Ẃ","W").replace("ẃ","w").replace("ń","n").replace("ṅ","n")
    token = token.replace("Ž","Z").replace("Ź","Z").replace("Ż","Z").replace("ž","z").replace("ź","z").replace("ž","z").replace("ż","z")
    token = token.replace("ć","c").replace("Č","C").replace("č","c").replace("ź","z")
    token = token.replace("ŕ","r").replace("ṙ","r").replace("ř","r")
    token = token.replace("Š","S").replace("š","s").replace("š","s")
    token = token.replace("ě","e").replace("ė","e").replace("é","e")
    token = token.replace("ė","e").replace("ḣ","h").replace("ẜ","ſ")
    token = token.replace("ẇ","w").replace("ṕ","p")
    
    token = token.replace("Ḿ","M").replace("Ǹ","N").replace("ḿ","m").replace("ṅ","n").replace("ḃ","b").replace("ȯ","o").replace("Ṅ","N")
    while len(oldtoken) != len(token):
        oldtoken = token
        if(token.endswith("skoho")  or token.endswith("owego")) or token.endswith("owicz"):
            token = token[0:-5]
        else:
            if(token.endswith("kego")  or token.endswith("keje") or token.endswith("owem") or token.endswith("owiz") or token.endswith("oweg") or token.endswith("owan") or token.endswith("owas")  or token.endswith("ſcho")  or token.endswith("arow") or token.endswith("owej") or token.endswith("kimi")  or token.endswith("kemu") or token.endswith("arje") or token.endswith("kich")):
                token = token[0:-4]
            else:
                if(token.endswith("keg") or token.endswith("jec") or token.endswith("kec") or token.endswith("cho") or token.endswith("ach") or token.endswith("oho") or token.endswith("ych") or token.endswith("owſ") or token.endswith("owk") or token.endswith("ojſ") or token.endswith("sko") or token.endswith("ſko") or token.endswith("cho") or token.endswith("ojz") or token.endswith("owy") or token.endswith("kej") or token.endswith("owe") or token.endswith("kew") or token.endswith("kem") or token.endswith("are") or token.endswith("two") or token.endswith("kim") or token.endswith("kem") or token.endswith("usu")):
                    token = token[0:-3]
                else:
                    if(token.endswith("ke") or token.endswith("ij") or token.endswith("ce") or token.endswith("ło") or token.endswith("ym") or token.endswith("sc") or token.endswith("ow") or token.endswith("jo") or token.endswith("sk") or token.endswith("ar") or token.endswith("ce") or token.endswith("oj") or token.endswith("my")  or token.endswith("om")  or token.endswith("am")  or token.endswith("ej") or token.endswith("je") or token.endswith("ki") or token.endswith("ka") or token.endswith("uw")):
                        token = token[0:-2]
                    else: 
                        if(token.endswith("a") or token.endswith("nj") or token.endswith("bſ") or token.endswith("tſ") or token.endswith("kſ") or token.endswith("wſ") or token.endswith("mſ") or token.endswith("dſ") or token.endswith("gſ") or token.endswith("rſ") or token.endswith("zſ") or token.endswith("lſ") or token.endswith("nſ") or token.endswith("vſ") or token.endswith("u") or token.endswith("ſk") or token.endswith("ſn") or token.endswith("e") or token.endswith("y") or token.endswith("i")):
                            token = token[0:-1]
        if(len(token)<3):
            token = oldtoken
    return token

def entities(urn):
    global ctsurl
    requestctsurl(urn)
    res = ""
    data = urlopen(ctsurl+"tm/entities.php?urn="+urn+"&sort") 
    for line in data: 
        linearr = line.decode('utf-8').split("\t")
        token = myporter(linearr[0])
        res+=token+"\t"+linearr[1]
    return res

    
def bagofwords(urn):
    global ctsurl
    requestctsurl(urn)
    res = ""
    data = urlopen(ctsurl+"tm/bagofwords.php?urn="+urn+"&sort&lowercase") 
    for line in data: 
        res+=line.decode('utf-8')
    return res

def ngram(urn,ngramsize):
    global ctsurl
    requestctsurl(urn)
    res = ""
    data = urlopen(ctsurl+"tm/ngrams.php?urn="+urn+"&sort&n="+str(ngramsize))
    for line in data: 
        res+=line.decode('utf-8').replace(" ","-")
    return res
    

def process(foldername):
    for yearfile in os.listdir(foldername+"peryear"):
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
    for yearfile in os.listdir(foldername+"peryear"):
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

count = -1

for line in inventory("dsb").split("\n"):
    urn = line.split("\t")[0]
    urnarr = urn.split(".")
    year = line.split("\t")[2]

    if (len(year)>1 and count!=0):
        count-=1
        print(str(count)+" "+urn)
        with open ("data/entities/"+urn.replace(":","_")+".txt", "w",encoding="utf8") as outf,open ("data/entitiesperyear/"+year+".txt", "a",encoding="utf8") as outyf:
            rs = entities(urn)
            outf.write(rs)
            outyf.write(rs)
        with open ("data/bagofwords/"+urn.replace(":","_")+".txt", "w",encoding="utf8") as outf,open ("data/bagofwordsperyear/"+year+".txt", "a",encoding="utf8") as outyf:
            rs = bagofwords(urn)
            outf.write(rs)
            outyf.write(rs)
        with open ("data/ngram3/"+urn.replace(":","_")+".txt", "w",encoding="utf8") as outf,open ("data/ngram3peryear/"+year+".txt", "a",encoding="utf8") as outyf:
            rs = ngram(urn,3)
            outf.write(rs)
            outyf.write(rs)

process("data/bagofwords")
process("data/ngram3")
process("data/entities")

if not os.path.exists("data/ctstm.db"):
    initTables()
con = sqlite3.connect("data/ctstm.db")
cursor = con.cursor()

yearfiles = os.listdir("data/bagofwordsperyear")
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

yearfiles = os.listdir("data/entitiesperyear")
for year in yearfiles:
    print("sql entitiesperyear:"+year)
    with open ("data/entitiesperyear/"+year, "r", encoding="utf8") as inf:
        for line in inf.readlines():
            if len(line.strip())>0:
                linearr = line.split("\t")
                vals = '"'+linearr[0]+'",'+year.replace(".txt","")+','+linearr[1]
                query="INSERT INTO entitydatecount(token,date,frequency) VALUES("+vals+")"
                cursor.execute(query)
    con.commit()

for file in os.listdir("data"):
    if(file.startswith("ngram") and file.endswith("peryear")):
        yearfiles = os.listdir("data/"+file)
        for year in yearfiles:
            print("sql "+file+":"+year)
            with open ("data/"+file+"/"+year, "r", encoding="utf8") as inf:
                for line in inf.readlines():
                    if len(line.strip())>0:
                        linearr = line.split("\t")
                        vals = '"-'+linearr[0]+'-",'+year.replace(".txt","")+','+linearr[1]
                        query="INSERT INTO "+file.replace("peryear","")+"datecount(ngram,date,frequency) VALUES("+vals+")"
                        cursor.execute(query)
            
    con.commit()

for file in os.listdir("data"):
    if(file.startswith("ngram") and not file.endswith("peryear")):
        with open ("data/"+file+"/_all.txt", "r", encoding="utf8") as inf:
            for line in inf.readlines():
                if len(line.strip())>0:
                    linearr = line.split("\t")
                    vals = '"-'+linearr[0]+'-",'+linearr[1]
                    query="INSERT INTO "+file.replace("peryear","")+"count(ngram,frequency) VALUES("+vals+")"
                    cursor.execute(query)

con.commit()

con.close()
