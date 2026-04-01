from urllib.request import urlopen
from urllib.parse import urlencode
import os
import sys
import subprocess

ns = sys.argv[1]

if (len(sys.argv)==3):
    count = sys.argv[2]
else:
    count = -1
print(str(count)+" documents from " +ns)
if os.path.exists("_error.txt"):
    os.remove("_error.txt")
    
with open("config_def.py", "r", encoding="utf8") as confdef:
    with open("config.py", "w", encoding="utf8") as conf:
        for line in confdef:
            if line.startswith("ctsns"):
                line = 'ctsns="'+ns+'"\n'
            if line.startswith("count"):
                line = 'count='+str(count)+'\n'
            conf.write(line)
            
confstr = ""

print(ns)

subprocess.run(["python3","_bagofwords.py"])
subprocess.run(["python3","_singleusewords.py"])
subprocess.run(["python3","_metadata.py"])
subprocess.run(["python3","_authors.py"])
subprocess.run(["python3","_characters.py"])
subprocess.run(["python3","_lemmatisierowasch.py"])
subprocess.run(["python3","_lemmaeval.py"])
subprocess.run(["python3","_normierowasch.py"])
subprocess.run(["python3","_normeval.py"])
subprocess.run(["python3","_ngram.py","2"])
subprocess.run(["python3","_ngram.py","3"])
subprocess.run(["python3","_ngram.py","5"])
subprocess.run(["python3","_collocation.py"])
subprocess.run(["python3","_spoznajrec.py","3"])
subprocess.run(["python3","_psedcytas.py","3"])
#subprocess.run(["python3","_zelenjerec.py","3"])
subprocess.run(["python3","_typorecognition.py"]) 
subprocess.run(["python3","_stats.py"]) 
subprocess.run(["python3","_docu.py"]) 


