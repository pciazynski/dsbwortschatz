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
    data = urlopen(thisurl+requesturl)
    for line in data: 
        res+=line.decode('utf-8')
    return res

def inventory(ns):
    checkConfig(ns)
    return requestFromCts("plain/editions.php").strip()
    
def docurns(ns):
    checkConfig(ns)
    return requestFromCts("plain/editionsslim.php").strip()

    
def urnsperlang(urn, params=""):
    checkConfig(urn)
    return requestFromCts("plain/urnsperlang.php?urn="+urn+params).strip()


def structuretext(urn):
    checkConfig(urn)
    return requestFromCts("plain/structuretext.php?urn="+urn).strip()


def bagofwords(urn, params="&sort&lowercase"):
    checkConfig(urn)
    return requestFromCts("tm/bagofwords.php?urn="+urn+params).strip()

def textpassage(urn, params="&deletexml"):
    checkConfig(urn)
    return requestFromCts("plain/passage.php?urn="+urn+params).strip()
