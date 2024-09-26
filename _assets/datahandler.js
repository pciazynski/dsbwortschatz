function readTextFile(file){
	textstr=""
	rawFile = new XMLHttpRequest();
	rawFile.open("GET", dataurl+file+".txt", false);
	rawFile.onreadystatechange = function (){
		if(rawFile.readyState === 4){
			if(rawFile.status === 200 || rawFile.status == 0)
			{textstr = rawFile.responseText;}
		}}
	rawFile.send(null);
	return textstr
}

function ctsrequest(url){
	textstr=""
	rawFile = new XMLHttpRequest();
	rawFile.open("GET", url, false);
	rawFile.onreadystatechange = function (){
		if(rawFile.readyState === 4){
			if(rawFile.status === 200 || rawFile.status == 0)
			{textstr = rawFile.responseText;}
		}}
	rawFile.send(null);
	return textstr
}

function loadGeojson(jsonfile, design){
	let xhr = new XMLHttpRequest();
	xhr.open('GET', geourl+jsonfile);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.responseType = 'json';
	xhr.onload = function() {
		if (xhr.status !== 200) return
		geojson = L.geoJSON(xhr.response,design);
		geojson.addTo(mymap);
		mymap.fitBounds(geojson.getBounds());
	};
	xhr.send();
}
function readPHP(file){
	text=""
	rawFile = new XMLHttpRequest();
	rawFile.open("GET", phpurl+file, false);
	rawFile.onreadystatechange = function (){
		if(rawFile.readyState === 4){
			if(rawFile.status === 200 || rawFile.status == 0)
			{
				text = rawFile.responseText;
			}
		}
	}
	rawFile.send(null);
	return text.trim()
}

function getQueryVariable(variable) {
	var query = window.location.search.substring(1);
	var vars = query.split("&");
	for (var i=0;i<vars.length;i++) {
		var pair = vars[i].split("=");
		if (pair[0] == variable) {
			return decodeURIComponent(pair[1]);
		}
	} 
	return ""
}



