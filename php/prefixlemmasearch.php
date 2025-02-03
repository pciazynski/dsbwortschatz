<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$lemma = $_GET['lemma'];
}
if (strlen($lemma)>=1){
	$limit = 100;
	if (isset($_GET['limit'])){
		$limit = $_GET['limit'];
	}
	$nl = "\n";
	$cutoff = "";
	
	if (isset($_GET['cutoff'])){
		$cutoff = ' GROUP BY SUBSTRING(lemma,0,'.strlen($lemma)+$_GET['cutoff'].')';
	}
	
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT DISTINCT lemma FROM lemmafrequency';
	$query .= ' WHERE lemma LIKE "'.$lemma.'%"'.$cutoff.' ORDER BY frequency DESC LIMIT '.$limit;

	$nl = "\n";
	foreach($PDO->query($query.';') as $row){
		print($row['lemma'].$nl);
	}
}
?>
