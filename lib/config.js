var diagramfont = {'family':'Times New Roman', 'size':'14'}
var defNodeFont = "8"
var defNodeCol="gray"
var dataurl="../../data/"
var phpurl="../../php/"
var geourl="../../geojson/"
var sep="\t"
var decicount = 3
var minDate = 1574
var maxDate = 2023
document.title = "DSB Tekst Mining"
var colorseed = "dolnoserbski"

var ctsurl = "https://urncts.eu/cts/dsb/cts/"
today = new Date();
dd = String(today.getDate()).padStart(2, '0');
mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
yyyy = today.getFullYear();
today = dd + '.' + mm + '.' + yyyy;

var wm_title = window.location.hostname+"/"+window.location.pathname.split("/")[1]+'. Accessed ' +today

var getColor = function(code){
	code = code.toLowerCase()+colorseed
	colortmp = stringToColour(code)
	if (typeof colortmp === "undefined"){colortmp="black"}
	return colortmp
}

var stringToColour = function(getcolortmp) {
  var hash = 0;
  for (var i = 0; i < getcolortmp.length; i++) {
    hash = getcolortmp.charCodeAt(i) + ((hash << 5) - hash);
  }
  var colour = '#';
  for (var i = 0; i < 3; i++) {
    var value = (hash >> (i * 8)) & 0xFF;
    colour += ('00'+value.toString(16)).substr(-2);
  }
  return colour;
}

if (typeof Plotly !== "undefined"){
	var markersize = function(entriecount){
		ms = 4
		if(entriecount < 10){return ms*3}
		if(entriecount < 100){return ms*2}
		if(entriecount < 1000){return ms*1.5}
		return ms
	}
	
	var watermarke = function(){
		wm = getQueryVariable("hidewatermark")
		if(wm.length==0){
			watermark = '<span style="color:gray;"> Quelle: '+wm_title+'</span>'
			return [{
				xref:'paper',
				x:0,
				yref:'paper',
				y:1,
				xanchor:'left',
				yanchor:'bottom',
				'text': watermark,
				font : diagramfont, 
				showarrow: false
			}]}
		else{return ""}
	}

	var plotlyconfiguration={
		editable:true,
		modeBarButtonsToAdd: [{
		name: 'SVG',
		icon: Plotly.Icons.camera,
		click: function(gd) {
			Plotly.downloadImage(gd, {format: 'svg'})
	}}]}
}