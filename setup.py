from urllib.request import urlopen
from urllib.parse import urlencode
import os
import sys
import subprocess

ns = sys.argv[1]

print(ns)

with open("config_def.py", "r", encoding="utf8") as confdef:
    with open("config.py", "w", encoding="utf8") as conf:
        for line in confdef:
            if line.startswith("ctsns"):
                line = 'ctsns="'+ns+'"\n'
            conf.write(line)
            
confstr = ""
ctsurl = ""

with open("lib/config_def.js", "r", encoding="utf8") as confdef:
    for line in confdef:
        if line.startswith("var ctsurl"):
            data = urlopen("https://urncts.eu/namespaceresolver/"+ns) 
            for reline in data:
                ctsurl+=reline.decode('utf-8')
            line = 'var ctsurl = "'+ctsurl+'cts/"'
        if line.startswith("document.title"):
            line = 'document.title = "CTM '+ ns +'"'
        if line.startswith("var minDate"):
            data = urlopen(ctsurl+"plain/daterange.php")
            for reline in data:
                if len(reline)>3:
                    line = "var minDate = " + reline.decode('utf-8').split("\t")[0]
        if line.startswith("var maxDate"):
            data = urlopen(ctsurl+"plain/daterange.php")
            for reline in data:
                if len(reline)>3:
                    line = "var maxDate = " + reline.decode('utf-8').split("\t")[1]
        confstr+=line.strip() + "\n"
with open("lib/config.js", "w", encoding="utf8") as conf:
    conf.write(confstr)

subprocess.run(["python3","_bagofwords.py"])
subprocess.run(["python3","_ngram.py","2"])
subprocess.run(["python3","_ngram.py","3"])
subprocess.run(["python3","_ngram.py","5"])
subprocess.run(["python3","_collocation.py"])
subprocess.run(["python3","_spoznajrec.py","3"])
subprocess.run(["python3","_zelenjerec.py"])
#subprocess.run(["python3","_typorecognition.py"]) 
subprocess.run(["python3","_stats.py"]) 


