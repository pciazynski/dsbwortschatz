from urllib.request import urlopen
import sys
import os
import shutil
import sqlite3
from config import *

from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

print("Init")

ctsurl = ""

if not os.path.exists("data"):
    os.mkdir("data")
if os.path.exists("data/topicmodel"):
    shutil.rmtree("data/topicmodel")
os.mkdir("data/topicmodel")

print("Stopwords...")

stopwords = {}
stopwordcount = 150
if len(sys.argv) > 1:
    stopwordcount = sys.argv[1]
    
stopwordstr = ""
if os.path.exists("data/bagofwords/_all.txt"):
    with open ("data/bagofwords/_all.txt", "r", encoding="utf8") as inf:
        for line in inf:
            stopwordcount-=1
            stopwordstr += "," + line.split("\t")[0]
            if stopwordcount<=0:
                break
    stopwordstr = stopwordstr[1:]
stopwords = stopwordstr.split(",")

print(str(len(stopwords)) + " Stopwords: "+str(stopwords))

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
        
def getPassage(urn):
    global ctsurl
    res = ""
    if len(ctsurl) > 0:
        data = urlopen(ctsurl+"plain/passage.php?deletexml&urn="+urn) 
        for line in data: 
            res+=line.decode('utf-8')

    return res 
    
count = -1

documents = []
urns = []
urnns = "dsb"

if not os.path.exists("data/passagecache.txt"):
    print("gathering document passages")
    for line in inventory(urnns).split("\n"):
        urn = line.split("\t")[0]
        urnarr = urn.split(".")

        if (count!=0):
            count-=1
            print(str(count)+"\t"+urn)
            documents.append(getPassage(urn))
            urns.append(urn)
    print("caching document passages")
            
    with open("data/passagecache.txt", "w", encoding="utf8") as outf:
        for i in range(len(urns)):
            outf.write(urns[i]+"\t"+documents[i]+"\n")

else:
    with open("data/passagecache.txt", "r", encoding="utf8") as inf:
        for line in inf:
            linearr = line.split("\t")
            urns.append(linearr[0])
            documents.append(linearr[1])

print("Topic Modelling")

vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words=stopwords)
bert_model = "distiluse-base-multilingual-cased-v1"
topic_model = BERTopic(embedding_model=bert_model,
                       vectorizer_model=vectorizer_model,
                       calculate_probabilities=True,
                       verbose=True,
                       nr_topics=min(30,len(documents)),
                       top_n_words=30,
                       min_topic_size=15,
                       n_gram_range=(1, 2))

topics, probs = topic_model.fit_transform(documents)

with open ("data/topicmodel/urn_topic.txt", "w",encoding="utf8") as out:
    for i in range(len(topics)):
        out.write(urns[i]+"\t"+str(topics[i])+"\n")
    
with open ("data/topicmodel/topic.txt", "w",encoding="utf8") as out:
    for i in range(len(topic_model.get_topics())-1):
        out.write(str(i) + "\t" + str(topic_model.get_topic(i))+"\n")
