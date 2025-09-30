function loading(elementid){
	var ifrm = document.getElementById(elementid);
	ifrm = ifrm.contentWindow || ifrm.contentDocument.document || ifrm.contentDocument;
	ifrm.document.open();
	ifrm.document.write(lang_loading);
	ifrm.document.close();
}

function diagrammlink(elementid){
	window.open(document.getElementById(elementid).src, '_blank');
}

function embedding(iframeid){
	alert('<iframe height='+document.getElementById(iframeid).offsetHeight+' width='+document.getElementById(iframeid).offsetWidth + ' src="'+document.getElementById(iframeid).src+'"></iframe>' );
}

function printlink(elementid){
	loading(elementid)
	url = document.getElementById(elementid).src
	if(url.includes('&print=1')){url = url.replace('&print=1','')}else{url += '&print=1'}
	document.getElementById(elementid).src = url
}

var switchLogScale = function(elementid){
	loading(elementid)
	url = document.getElementById(elementid).src
	if(url.includes('&scale=log')){url=url.replaceAll('&scale=log','')}else{url+='&scale=log'}
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
+'<td>'+lang_metadata+'</td>'
+'<td>'+lang_textcorpus+'</td>'
+'<td><a href="../characters">'+lang_characters+'</a></td>'
+'<td>'+lang_word+'</td>'
+'<td>'+lang_connection+'</td>'
+'<td>'+'SpoznajRec'+'</td>'
//+'<td>'+'Entitäten'+'</td>'
+'<td><a href="'+ctsurl+'?request=GetCapabilities">CTS Link</a></td>'
+'</tr>'
+'<tr style="text-align:center;">'
+'<td>'
+'<a href="../metadataauthor">'+lang_author+'</a> | '
+'<a href="../metadatadochierarchy">'+lang_dochierarchy+'</a>'
+'</td>'

+'<td>'
+'<a href="../docreferences/">'+lang_docreferences+'</a> | '
+'<a href="../stats/">'+lang_statistics+'</a> | '
+'<a href="../tokenrec/">'+lang_coverage+'</a> | '
+'<a href="../bwtime/">'+lang_genesis_disappear+'</a>'
+'</td>'
+'<td>'
+'</td>'
+'<td>'
+'<a href="../bwlemma/">'+lang_timeline+'</a> | '
+'<a href="../lemmavariation/">'+lang_variation+'</a> | '
+'<a href="../lemmaeval/">'+lang_evaluation+'</a> | '
+'<a href="../profile/">'+lang_profile+'</a>'
+'</td>'
+'<td>'
+'<a href="../collocation/">'+lang_collocation+'</a> | '
+'<a href="../ngram/?n=3">Trigramme</a>'
+'</td>'
+'<td>'
+'<a href="../langdetect/?n=3">Rozeznaś</a> | <a href="../langrec/?n=3">Gódaś Rec</a> | '
+'<a href="../langsep/">Zelenje Rec</a>'
+'</td>'
//+'<td>'
//+'<a href="../ner_place/">Orte</a>'
//+'<a style="color:white;"  href="../ner_person/">Personen</a>'
//+'</td>'
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
+'<a href="../../">'+lang_projectsite+'</a>'
+'</td>'
+'<td>'
+'<a href="../../../">'+lang_hubarea+'</a>'
+'</td>'
+'</tr>'
+'</table>' 
+'</div>'
return str
}
