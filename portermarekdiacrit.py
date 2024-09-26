import sys
import re

def myporter(token):
    oldtoken = ""
    '''
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
                        if(token.endswith("a") or token.endswith("nj") or token.endswith("bſ") or token.endswith("tſ") or token.endswith("kſ") or token.endswith("wſ") or token.endswith("mſ") or token.endswith("hſ") or token.endswith("dſ") or token.endswith("gſ") or token.endswith("rſ") or token.endswith("zſ") or token.endswith("lſ") or token.endswith("nſ") or token.endswith("vſ") or token.endswith("u") or token.endswith("ſk") or token.endswith("ſn") or token.endswith("e") or token.endswith("y") or token.endswith("i")):
                            token = token[0:-1]
        if(len(token)<3):
            token = oldtoken
    return token
'''
    
    exceptions = {
        # fem.subst.
        "sotša"        : "^sotš(a(mi?|ch)?|y|e|u|o(wu?|ma))$",    # 1a
        "kmótša"    : "^kmótš(a(mi?|ch)?|y|e|u|o(wu?|ma))$",    # 1a
        "łdza"        : "^łdz(a(mi?|ch)?|y|e|u|o(wu?|ma))$",    # 1a
        "śpa"        : ["śpa","śpy","jśpy","śpě","jśpě","śpu","jśpu","śpowu","jśpowu","śpoma","jśpoma","śpow","jśpow","śpam","jśpam","śpami","jśpami","śpach","jśpach",],    # 10
        "gła"        : ["gła","gły","glě","głu","głowu","głoma","głow","głam","głami","głach"],    # 11
        "škla"        : ["škla","šklě","škli","šklu","šklowu","škloma","šklow","šklam","šklami","šklach"],    # 12
        "škrja"        : ["škrja","škrě","škri","škrju","škrjowu","škrjoma","škrjow","škrjam","škrjami","škrjach"],    # 13
        "maś"        : ["maś","maśerje","maśeri","maśerju","maśerjowu","maśerjoma","maśerjow","maśerjam","maśerjami","maśerjach"],    # 14
        "wjas"        : "^wjas$|^js(y|u|o(wu?|ma)|a(mi?|ch))$", # 15
        "kšej"        : "^kš(ej|w(ě|i|ju))$",    # 16
        # mask.subst.
        "źeń"        : "^źeń$|^dn(j(a(mi?|ch)?|u|o(ma?|wu?)|)|y)$",    # 23
        # neutr.subst.
        "cło"        : "^c(ł(o(ju|ma?|wu?)?|a(mi?|ch)?)|lě)$",    # 25
        "spło"        : "^sp(ł(o(ju|ma?|wu?)?|a(mi?|ch)?)|lě)$",    # 25
        "zgło"        : "^zg(ł(o(ju|ma?|wu?)?|a(mi?|ch)?)|lě)$",    # 25
        "wucho"        : "^wu(ch(o(ju|m|w)?|a(mi?|ch)?|u)|š(y(m(a|i))?|o(wu?)|a(m|ch)))$",    # 31
        "woko"        : "^w(ok(o(ju|m|w)?|a(mi?|ch)?|u)|óc(y(m(a|i))?|o(wu?)|a(m|ch)))$",    # 32
        "śele"        : "^śele(ś(a|eju|im?|u|o(wu|ma))|t(a(mi?|ch)?|ow))?$",    # 37, dort noch andere gelistet
        "góle"        : "^źiś(e|i(mi)?|a(m|ch))$|^góle(ś(a|eju|im|u|o(wu|ma)))?$",    # 38 (oder źiśe als stem?)
        "płomje"    : "^płomje(n(j(a(mi?|ch)?|eju|u|o(wu?|ma))|im?))?$",    # 39, dort noch andere gelistet
        "mě"        : "^m(ě|jen(j(a(mi?|ch)?|eju|u|o(wu?|ma))|im?))$",    # 40
        # pl.tant.
        "žni"        : "^žn(i|j(ow|a(mi?|ch)))$",    # 46
        "slě"        : "^sl(ě|ow|a(mi?|ch))$",    # 46
        # pron.
        "naš"        : "^naš(a|e(j(e|u)?)?|u|o(go|mu?)?|y(m(a|i)?|ch))?$",    # 50
        "waš"        : "^waš(a|e(j(e|u)?)?|u|o(go|mu?)?|y(m(a|i)?|ch))?$",    # 50
        "ten"        : "^t(a|e(j(e|u)?)?|u|o(go|mu?)?|y(m(a|i)?|ch)|en)$",    # 50
        "žeden"        : "^žed(n(a|e(j(e|u)?)?|u|o(go|mu?)?|y(m(a|i)?|ch))|en)$",    # 50
        "sam"        : "^sam(a|e(j(e|u)?)?|u|o(go|mu?)?|y(m(a|i)?|ch))?$",    # 50
        "mój"        : "^mój(a|e(j(e|u)?)?|u|o(go|mu?)?|i(m(a|i)?|ch))?$",    # 51
        "twój"        : "^twój(a|e(j(e|u)?)?|u|o(go|mu?)?|i(m(a|i)?|ch))?$",    # (51)
        "swój"        : "^swój(a|e(j(e|u)?)?|u|o(go|mu?)?|i(m(a|i)?|ch))?$",    # (51)
        "wšen"        : "^wš(a|e(j(e|u)?|n)?|u|o(go|mu?)?|y(mi?|ch))$|^wob(eju?|yma)$",    # 52
        "wšyken"    : "^wšyk(n(a|e(j(e|u)?)?|u|o(go|mu?)?|y(mi?|ch))|en)$|^wob(eju?|yma)$",    # 52
        "jaden"        : "^jad(n(a|e(j(e|u)?)?|u|o(go|mu?)?|y(m(a|i)?|ch))|en)$",    # 53
        "dwa"        : "^dw(ě(ma)?|eju|a)$",    # 54
        "tśi"        : "^tś(i(ch|mi?)?|o(ch|mi?)?)$",    # 55, dort noch andere gelistet
        "styri"        : "^styr(i(ch|mi?)?|jo(ch|mi?)?)$",    # 55
        "chto"        : "^chto$|^k(o(go|mu)|im)$",    # 56
        "něchten"    : "^něcht(en)?$|^něk(o(go|mu)|im)$",    # 56
        "nichten"    : "^nicht(en)?$|^nik(o(go|mu)|im)$",    # 56
        "co"        : "^c(o(go|mu?)?|ym)$",    # 57
        "něco"        : "^něc(o(go|mu?)?|ym)$",    # 57
        "nic"        : "^nic(o(go|mu?)|ym)?$",    # 57
        "ja"        : ["ja","mě","mnjo","mnu"], # 58
        "mej"        : ["mej","naju","nama"], # 58
        "my"        : ["my","nas","nam","nami"], # 58
        "ty"        : ["ty","śi","tebje","tobu"],    # 59
        "wej"        : ["wej","waju","wama"],    # 59
        "wy"        : ["wy","was","wam","wami"], # 59
        "wón"        : "^wón(a|o|ej|i)?$|^n?j(o(go|mu)?|e(n|j(e|u)?)?|u)$|^njom$|^(j|n)i(ma?|ch)$|^nimi$",    # 60
        "sebje"        : ["sebje","sobu"],    # 61
        # verb.
        "la"        : "^l(a(ś|t|ł(a|o|ej)?|li)|ej(u|o(m(ej|y)?|š|tej|śo)?|tej|śo|a(ch|šo))?)$",    # 67 (oder laś als stem? was ist mit adjektivischen Partizipien (lecujy, laty)?)
        "pisa"        : "^pisa(ś|ch|šo|ł(a|o|ej)?|li|m(ej|y)?|š|tej|śo|j(tej|śo)?)?$|^piš(u|o(m(ej|y)?|š|tej|śo)?|tej|śo)?$",    # 70 (oder andere stemform? partizipien?)
        "płak"        : "^płac(u|o(m(ej|y)?|š|tej|śo)?|tej|śo)?$",    # 70a
        "wěz"        : "^wěž(u|o(m(ej|y)?|š|tej|śo)?|tej|śo)?$",    # 70a
        "rigot"        : "^rigoc(u|o(m(ej|y)?|š|tej|śo)?|tej|śo)?$",    # 70a
        "kubł"        : "^kubl(u|o(m(ej|y)?|š|tej|śo)?|i(tej|śo)?)$",    # 70a
        "gib"        : "^gib(j(u|o(m(ej|y)?|š|tej|śo)?)|tej|śo)?$",    # 70a
        "łam"        : "^łam(j(u|o(m(ej|y)?|š|tej|śo)?)|tej|śo)?$",    # 70a
        "syp"        : "^syp(j(u|o(m(ej|y)?|š|tej|śo)?)|tej|śo)?$",    # 70a
        "wór"        : "^wórj(u|o(m(ej|y)?|š|tej|śo)?)|wóŕ(tej|śo)?$",    # 70a
        "pjac"        : "^pjak(u|ł(a|o|ej)?|li)$",    # 72
        "kład"        : "^kła(sć|ź(o(m(ej|y)?|š|tej|śo)?|tej|śo|e(ch|šo))?|d(u|ł(a|o|ej)?|li))$",    # 72a
        "kwit"        : "^kwi(sć|ś(o(m(ej|y)?|š|tej|śo)?|tej|śo|e(ch|šo))?|t(u|ł(a|o|ej)?|li))$",    # 72a
        "rost"        : "^ro(sć|sć(o(m(ej|y)?|š|tej|śo)?|e(ch|šo))|stu|s(ł(a|o|ej)?|li|tej|śo))$",    # 72a
        "móg"        : "^mó(c|ž(o(m(ej|y)?|š|tej|śo)?|a(ch|šo))|g(u|a?ł(a|o|ej)?|li))$",    # 72a
        "pomog"        : "^pomo(c|ž(o(m(ej|y)?|š|tej|śo)?|e(ch|šo))?|g(u|ł(a|o|ej)?|li))$",    # 72a
        "wjed"        : "^wja(sć|d(u|ł(a|o|ej)?|li))$|^wje(du|ź(o(m(ej|y)?|š|tej|śo)?|tej|śo)?)$",    # 73
        "mjet"        : "^mja(sć|t(u|ł(a|o|ej)?|li))$|^mje(tu|ś(o(m(ej|y)?|š|tej|śo)?|tej|śo)?)$",    # 73
        # 74a-h
        # 89a-c
        "kśě"        : "^c(u|o(m(ej|y)?|š|tej|śo)?)$|^kśě(ś|ł(a|o|ej)?|li|ch|šo)?$",    # 90
        "njekśě"    : "^njoc(o(m(ej|y)|š|tej|śo)?)$|^njok$|^njekśě(ś|ł(a|o|ej)?|li|ch|šo)?$",    # 90
        "ma"        : "^m(a(m(ej|y)?|š|tej|śo|ju)?|ě(ś|ł(a|o|ej)?|li|ja(ch|šo)|j(tej|śo)?))$|^změj(u|o(m(ej|y)?|š|tej|śo)?)$",    # 91
        # 92a-c
        "jěd"        : "^jě(ś|du|ź(o(m(ej|y)?|š|tej|śo)?|tej|ćo|e(ch|šo))?|ł(a|o|ej)?|li)$",    # 93
        "by"        : "^b(y(ś|ł(a|o|ej)?|li)|u(du|źo(m(ej|y)?|š|tej|śo)|ch(mej|my|u)?|štej|šćo|ź(tej|śo)?)?|ě(ch|šo))$|^s(om|y|(m|t)ej|my|ćo|u)$|^jo$",    # 94
        # 95–100 (Komparation von Adjektiven)
        # 101–106 (Komparation von Adverbien und Prädikativa)        
                
        # Konflikte:
            # mě -> mě und ja
            # wón/a/o/ej/i nicht nach Genus und Numerus unterschieden (im Gegensatz zu Personalpronomina)
            # co -> kśě und co
            
            # Binnenflexion: kótaryž, což, něcožkuli...
            # Negation, Superlativ, Präfixe allgemein
            # Diachrone Varianz
    }

    for stem,forms in exceptions.items():
        if (isinstance(forms,str)):
            if (re.search(forms,token,re.IGNORECASE)):
                return stem
        else:
            for form in forms:
                if (token == form):
                    return stem
    
    while len(oldtoken) != len(token):
        oldtoken = token

        match = False
        
        ends = [
            "dnjomej","dnjotej",    # verb.
        ]
        for end in ends:
            if (token.endswith(end)):
                token = token[0:-7]
                match = True
                break
        if (not(match)):    
            ends = [
                "ujomej","ujotej","owałej","njomej","njotej",    # verb.
                "dnjomy","dnjośo","dnitej","ijomej","ijotej",    # verb.
                "yjomej","yjotej",    # verb.
            ]
            for end in ends:
                if (token.endswith(end)):
                    token = token[0:-6]
                    match = True
                    break
            if (not(match)):
                ends = [
                    "ujomy","ujośo","ujtej","owała","owało","owali","owach","owašo","jomej","jotej","njomy","njośo","djnom","dnjoš",    # verb.
                    "djnom","dnjoš","dniśo","dnjon","ijomy","ijośo",    # verb.
                    "yjomy","yjośo",    # verb.
                ]
                for end in ends:
                    if (token.endswith(end)):
                        token = token[0:-5]
                        match = True
                        break
                if (not(match)):
                    ends = [
                        "jowu","joma","jami","jach",    # fem.subst.
                        "joju",    # mask.subst.
                        "jeju",    # neutr.subst.
                        "jeje","jego","jemu",    # adj.
                        "owaś","ujom","ujoš","ujśo","ował","ujuc","owan","jomy","jośo","itej","ułej","jech","ješo","njom","njoš","ńtej",    # verb.
                        "dnjo","jtej","jach","jašo","omej","otej","ałej","imej","itej","ijom","ijoš",    # verb.
                        "ymej","ytej","yjom","yjoš","yłej",    # verb.
                        "ełej",    # verb.
                    ]
                    for end in ends:
                        if (token.endswith(end)):
                            token = token[0:-4]
                            match = True
                            break
                    if (not(match)):
                        ends = [
                            "owu","oma","ami","ach","jow","jam",    # fem.subst.
                            "oju","jom",    # mask.subst.
                            "eju",    # neutr.subst.
                            "eje","ego","emu","yma","ych","ymi","ima","ich","imi","jej","jem","ogo","omu",    # adj.
                            "uju","ujo","jom","još","iśo","uła","uło","uli","jec","jon","ńśo","łej",    # verb.
                            "dnu","dni","jśo","juc","omy","ośo","tej","ała","ało","ali","ach","ašo",    # verb.
                            "ech","ešo","mej","tej","imy","iśo","iła","iło","ili","iju","ijo","ich",    # verb.
                            "ymy","yśo","yju","yjo","yła","yło","yli","ych",    # verb.
                            "eła","eło","eli",    # verb.
                        ]
                        for end in ends:
                            if (token.endswith(end)):
                                token = token[0:-3]
                                match = True
                                break
                        if (not(match)):
                            ends = [
                                "je","ow","am","ja","ej","ju",    # fem.subst.
                                "om",    # mask.subst.
                                "jo","im",    # neutr.subst.
                                "ym","em",    # adj.
                                "uj","uś","jo","uł","uc","nu","ła","ło","li","ch",    # verb.
                                "ju","šo","om","oš","śo","ał","ćo","ec","my","je","im","iš","ił","on",    # verb.
                                "yś","ym","yš","ył",    # verb.
                                "eł",    # verb.
                            ]
                            for end in ends:
                                if (token.endswith(end)):
                                    token = token[0:-2]
                                    match = True
                                    break
                            if (not(match)):
                                ends = [
                                    "a","y","u","e","i","ě",    # fem.subst.
                                    "o",    # neutr.subst.
                                    "u","i","ś","ń","ł","t",    # verb.
                                    "j","o","ć","n","m","š",    # verb.
                                    "y","e",    # verb.
                                ]
                                for end in ends:
                                    if (token.endswith(end)):
                                        token = token[0:-1]
                                        #match = True
                                        break
        if(len(token)<3):
            token = oldtoken
    token = token.replace("ó","o").replace("ó","o").replace("Ẃ","W").replace("ẃ","w").replace("ń","n").replace("ṅ","n")
    token = token.replace("Ž","Z").replace("Ź","Z").replace("Ż","Z").replace("ž","z").replace("ź","z").replace("ž","z").replace("ż","z")
    token = token.replace("ć","c").replace("Č","C").replace("č","c").replace("ź","z")
    token = token.replace("ŕ","r").replace("ṙ","r").replace("ř","r")
    token = token.replace("Š","S").replace("š","s").replace("š","s")
    token = token.replace("ě","e").replace("ė","e").replace("é","e")
    token = token.replace("ė","e").replace("ḣ","h").replace("ẜ","ſ")
    token = token.replace("ẇ","w").replace("ṕ","p")

    token = token.replace("Ḿ","M").replace("Ǹ","N").replace("ḿ","m").replace("ṅ","n").replace("ḃ","b").replace("ȯ","o").replace("Ṅ","N")
        
    return token
        
        
        
        

if len(sys.argv) > 1:
    print(myporter(sys.argv[1]))
else:
    print(myporter("Abeſſiniſka"))