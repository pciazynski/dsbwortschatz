<?php
header('Content-Type: text/plain');

$limit = 100;
$cutoff = 0;

if (isset($_GET['limit'])){
	$limit = $_GET['limit'];
}
if (isset($_GET['token'])){
	$token = $_GET['token'];
}
$n=3;
if (isset($_GET['n'])){
	$n = $_GET['n'];
}

if (strlen($token)>=1){
	$cutoff = "";
	if (isset($_GET['cutoff'])){
		$cutoff = ' GROUP BY SUBSTRING(ngram,0,'.(1+strlen($token)+$_GET['cutoff']).')';
	}
	$query = 'SELECT DISTINCT SUBSTRING(ngram,2,LENGTH(ngram)-2) as ngram FROM ngramcount';
	$PDO = new PDO('sqlite:../data/ngram'.$n.'.db');
	$query .= ' WHERE ngram LIKE "\_'.$token.'%" escape "\"'.$cutoff.' ORDER BY ngram LIMIT '.$limit;
	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['ngram']."\n");
	}
}
?>
