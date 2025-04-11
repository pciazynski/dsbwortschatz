import os
import shutil
import re

if os.path.exists("data/charmix"):
    shutil.rmtree("data/charmix")
os.mkdir("data/charmix")

kyrilpattern = re.compile("^([a-z]+[а-яё]+)+$")
kyrilpattern2 = re.compile("^([а-яё]+[a-z]+)+$")
numberpattern = re.compile("^([a-z]+[0-9]+)+$")
numberpattern2 = re.compile("^([0-9]+[a-z]+)+$")

def checktoken(token):
    #html encoded emojis
    if(token.startswith("x1f")):
        return "clean"
    if(kyrilpattern.match(token)):
        return "cyrill"
    if(kyrilpattern2.match(token)):
        return "cyrill"
    if(numberpattern.match(token)):
        return "number"
    if(numberpattern2.match(token)):
        return "number"
    return "clean"
    

mixbag = {}

for file in os.listdir("data/bagofwords/"):
    if(file.startswith("urn_#_")):
        with open ("data/bagofwords/"+file, "r", encoding="utf8") as f, open ("data/charmix/_all.txt", "a", encoding="utf8") as outf, open ("data/charmix/_cyr.txt", "a", encoding="utf8") as outfcyr, open ("data/charmix/_num.txt", "a", encoding="utf8") as outfnum:
            for line in f:
                linearr = line.strip().split("\t")
                token = linearr[0]
                evalres = checktoken(token)
                if evalres == "cyrill":
                    outfcyr.write(token+"\t" +linearr[1]+"\t"+file.replace(".txt","").replace("_#_",":")+"\n")
                    outf.write(token+"\t" +linearr[1]+"\t"+file.replace(".txt","").replace("_#_",":")+"\n")
                    mixbag[token] = 1
                if evalres == "number":
                    outfnum.write(token+"\t" +linearr[1]+"\t"+file.replace(".txt","").replace("_#_",":")+"\n")
                    outf.write(token+"\t" +linearr[1]+"\t"+file.replace(".txt","").replace("_#_",":")+"\n")
                    mixbag[token] = 1


        
        
