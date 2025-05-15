from urllib.request import urlopen

ctsurl=""
oldns = ""
manualurl = ""

def setmanualurl(newurl):
    global manualurl
    manualurl = newurl
    
def setCtsSource(url):
    global ctsurl
    ctsurl = url
    
def requestCtsUrl(ns):
    global ctsurl
    data = urlopen("https://urncts.eu/namespaceresolver/"+ns) 
    for line in data:
        ctsurl+=line.decode('utf-8')
   
def checkConfig(reference):
    global ctsurl
    global manualurl
    global oldns
    if reference.startswith("urn:"):
        reference = reference.split(":")[2]
    if(oldns != reference):
        ctsurl = ""
        oldns = reference
    if(len(ctsurl) == 0 and len(manualurl)==0):
        requestCtsUrl(reference)

def requestFromCts (requesturl):
    global ctsurl
    global manualurl
    if len(manualurl)>0:
        thisurl = manualurl
    else:
        thisurl = ctsurl
    
    res = ""
#    print(thisurl+requesturl)
#    exit()
    data = urlopen(thisurl+requesturl)
    for line in data: 
        res+=line.decode('utf-8')
    return res.strip("\n")

def daterange(ns):
    checkConfig(ns)
    return requestFromCts("plain/daterange.php")

def doccount(ns):
    checkConfig(ns)
    return requestFromCts("plain/doccount.php")

def urncount(ns):
    checkConfig(ns)
    return requestFromCts("plain/urncount.php")

def dates(ns):
    checkConfig(ns)
    return requestFromCts("plain/dates.php")

def doclanguages(ns):
    checkConfig(ns)
    return requestFromCts("plain/doclanguages.php")

def authors(ns):
    checkConfig(ns)
    return requestFromCts("plain/authors.php")

def anyworkurn(ns):
    checkConfig(ns)
    return requestFromCts("plain/anyworkurn.php")

def anyurn(ns):
    checkConfig(ns)
    return requestFromCts("plain/anyurn.php")
    
def inventory(ns):
    checkConfig(ns)
    return requestFromCts("plain/editions.php")
    
def docurns(ns):
    checkConfig(ns)
    return requestFromCts("plain/editionsslim.php")

    
def urnsperlang(urn, params=""):
    checkConfig(urn)
    if len(params)>0 and not params.startswith("&"):
        params = "&"+params
    return requestFromCts("plain/urnsperlang.php?urn="+urn+params)

def label(urn):
    checkConfig(urn)
    return requestFromCts("plain/label.php?urn="+urn)

def prevnexturn(urn):
    checkConfig(urn)
    return requestFromCts("plain/prevnexturn.php?urn="+urn)

def firsturn(urn):
    checkConfig(urn)
    return requestFromCts("plain/firsturn.php?urn="+urn)

def validreff(urn):
    checkConfig(urn)
    return requestFromCts("plain/validreff.php?urn="+urn)


def structuretext(urn, params=""):
    checkConfig(urn)
    if len(params)>0 and not params.startswith("&"):
        params = "&"+params
    return requestFromCts("plain/structuretext.php?urn="+urn+params)

def structurebagofwords(urn, params="&sort&lowercase"):
    checkConfig(urn)
    if len(params)>0 and not params.startswith("&"):
        params = "&"+params
    return requestFromCts("tm/structurebagofwords.php?urn="+urn+params)

def bagofwords(urn, params="&sort&lowercase"):
    checkConfig(urn)
    if len(params)>0 and not params.startswith("&"):
        params = "&"+params
    return requestFromCts("tm/bagofwords.php?urn="+urn+params)

def ngram(urn,params="&sort&lowercase&n=3"):
    checkConfig(urn)
    if len(params)>0 and not params.startswith("&"):
        params = "&"+params
    return requestFromCts("tm/ngrams.php?urn="+urn+params)
    
def textpassage(urn, params="&deletexml"):
    checkConfig(urn)
    if len(params)>0 and not params.startswith("&"):
        params = "&"+params
    return requestFromCts("plain/passage.php?urn="+urn+params)

def textpassage_xml(urn, params="&deletexml"):
    checkConfig(urn)
    if len(params)>0 and not params.startswith("&"):
        params = "&"+params
    return requestFromCts("cts/?request=GetPassage&urn="+urn+params)

def textsearch(urn, params=""):
    if not "snippet=" in params:
        return ""
    checkConfig(urn)
    if not params.startswith("&"):
        params = "&"+params
    return requestFromCts("plain/textsearch.php?urn="+urn+params)
    
def exactsearch(urn, params=""):
    if not "snippet=" in params:
        return ""
    checkConfig(urn)
    if not params.startswith("&"):
        params = "&"+params
    return requestFromCts("plain/exactsearch.php?urn="+urn+params)
