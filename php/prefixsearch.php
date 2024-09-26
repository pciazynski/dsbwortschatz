<?php
header('Content-Type: text/plain');

if (isset($_GET['token'])){
	$token = $_GET['token'];
}
if (strlen($token)>=1){
	$limit = 100;
	if (isset($_GET['limit'])){
		$limit = $_GET['limit'];
	}
	$nl = "\n";
	$cutoff = "";
	if (isset($_GET['cutoff'])){
		$cutoff = ' GROUP BY SUBSTRING(token,0,'.strlen($token)+$_GET['cutoff'].')';
	}
	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$query = 'SELECT DISTINCT token FROM tokendatecount';
	$query .= ' WHERE token LIKE "'.$token.'%"'.$cutoff.' ORDER BY frequency DESC LIMIT '.$limit;
	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['token'].$nl);
	}
}
?>
