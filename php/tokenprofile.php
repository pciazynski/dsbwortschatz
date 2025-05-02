<?php
header('Content-Type: text/plain');

if(isset($_GET['token'])){
	
	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$query = 'SELECT Min(date) as mindate, Max(date) as maxdate FROM tokendatecount WHERE token='.$_GET['token'];

	$tab = "\t";
	$nl = "\n";
	$res = '';

	foreach($PDO->query($query.';') as $row){
		$res.=$row['mindate'].$tab.$row['maxdate'].$nl;
	}
	print($res);
}
?>
