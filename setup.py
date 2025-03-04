from urllib.request import urlopen
from urllib.parse import urlencode
import os
import sys
import subprocess

ns = sys.argv[1]

print(ns)

subprocess.run(["python3","_bagofwords.py"])
subprocess.run(["python3","_lemmatisierowasch.py"])
subprocess.run(["python3","_ngram.py","2"])
subprocess.run(["python3","_ngram.py","3"])
subprocess.run(["python3","_ngram.py","5"])
subprocess.run(["python3","_collocation.py"])
subprocess.run(["python3","_spoznajrec.py","3"])
subprocess.run(["python3","_zelenjerec.py"])
#subprocess.run(["python3","_typorecognition.py"]) 
subprocess.run(["python3","_stats.py"]) 


