function loading(elementid){
	var ifrm = document.getElementById(elementid);
	ifrm = ifrm.contentWindow || ifrm.contentDocument.document || ifrm.contentDocument;
	ifrm.document.open();
	ifrm.document.write('Loading...');
	ifrm.document.close();
}

function diagrammlink(elementid){
	window.open(document.getElementById(elementid).src, '_blank');
}

function printlink(elementid){
	url = document.getElementById(elementid).src
	if(url.includes('&print=1')){url = url.replace('&print=1','')}else{url += '&print=1'}
	document.getElementById(elementid).src = url
}

function nolanguage(elementid){
	url = document.getElementById(elementid).src
	url=url.replace('&lang=DEU','').replace('&lang=DSB','')
	document.getElementById(elementid).src = url
}

function language(elementid){
	url = document.getElementById(elementid).src
	if(url.includes('&lang=DEU')){url = url.replace('&lang=DEU','')}else{url += '&lang=DEU'}
	document.getElementById(elementid).src = url
}

function hidewatermark(elementid){
	url = document.getElementById(elementid).src
	if(url.includes('&hidewatermark=1')){url = url.replace('&hidewatermark=1','')}else{url += '&hidewatermark=1'}
	document.getElementById(elementid).src = url
}


function datalink(elementid){
	thisdataurl = document.getElementById(elementid).src.split('data=')[1]
	if(thisdataurl.includes('.php')){
		window.open(phpurl+thisdataurl.replace('&','?'), '_blank');
	}else{
		window.open(dataurl+thisdataurl.split('&')[0]+'.txt', '_blank');
	}
}

function header(){
str='<div  class="header">'+
'<table>'
+'<tr style="text-align:center;">'
+'<td>'
+'Dokumente'
+'</td>'
+'<td>'
+'Worte'
+'</td>'
+'<td>'
+'Flektion'
+'</td>'
+'<td>'
+'Wortnähe'
+'</td>'
+'<td>'
+'nGram'
+'</td>'
+'<td>'
+'SpoznajRec'
+'</td>'
+'<td>'
+'Entitäten'
+'</td>'
+'<td>'
+'<a href="'+ctsurl+'?request=GetCapabilities">CTS Link</a>'
+'</td>'
+'</tr>'
+'<tr style="text-align:center;">'
+'<td>'
+'<a href="../docperword/">Wortreferenzen</a>'

+'</td>'
+'<td>'
+'<a href="../bwtoken/">Token</a> | '
+'<a href="../bwtime/">Zeitverlauf</a> | '
+'<a href="../tokenrec/">Token-Abdeckung | </a>'
+'<a href="../stats/">Statistiken</a>'
+'</td>'
+'<td>'
+'<a href="../bwlemma/">Lemma</a> | '
+'<a href="../lemmatree/">Lemmabaum</a>'
+'</td>'
+'<td>'
+'<a href="../collocation/">Kollokation</a> | <a href="../collocationperyear/">Pro Jahr</a> '
+'</td>'
+'<td>'
+'<a href="../ngram/?n=3">n=3</a> | <a href="../ngram/?n=5">n=5</a>'
+'</td>'
+'<td>'
+'<a href="../langdetect/?n=3">Rozeznaś</a> | <a href="../langrec/?n=3">Spóznaś</a>'
+'</td>'
+'<td>'
+'<a href="../ner_place/">Orte</a> | '
//+'<a style="color:white;"  href="../ner_person/">Personen</a>'
+'</td>'
+'<td>'
+'</td>'
+'</tr>'
+'</table>' 
+'</div>'
return str
}

function footer(){
str='<div class="header">'+
'<table>'
+'<tr>'
+'<td>'
+'<a href="../../">Projektseite</a>'
+'</td>'
+'<td>'
+'<a href="../../../">Hub Area</a>'
+'</td>'
+'</tr>'
+'</table>' 
+'</div>'
return str
}
