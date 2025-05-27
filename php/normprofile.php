<?php
header('Content-Type: text/plain');

if(isset($_GET['norm'])){
	
	$norm = $_GET['norm'];
	$res = '';
	$tab = "\t";
	$nl = "\n";

	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	
	$query = 'SELECT Min(date) as mindate, Max(date) as maxdate FROM tokenlemmanormtypesubtypedatefrequency WHERE norm = "|'.$norm.'|"';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['mindate'].$tab.$row['maxdate'].$nl;
	}
	$res=trim($res,$tab).$nl;

	$query = 'SELECT DISTINCT token tokenlemmanormtypesubtypedatefrequency WHERE norm = "|'.$norm.'|"';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['token'].$tab;
	}
	$res=trim($res,$tab).$nl;
	
	print($res);
}
?>
