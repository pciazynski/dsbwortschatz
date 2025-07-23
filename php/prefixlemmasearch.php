<?php
header('Content-Type: text/plain');

(isset($_GET['lemma'])) ? $lemma = $_GET['lemma'] : NULL;

if (strlen($lemma)>=1){
	(isset($_GET['limit'])) ? $limit = $_GET['limit'] : $limit = 100;
	(isset($_GET['cutoff'])) ? $cutoff = ' GROUP BY SUBSTRING(lemma,1,'.strlen($lemma)+$_GET['cutoff'].')' : $cutoff = '';
	(isset($_GET['ambig'])) ? $dbname = 'lemmafrequency':$dbname = 'lemmanonambig';
	
	$query = 'SELECT DISTINCT lemma FROM '.$dbname.' WHERE lemma LIKE "|'.$lemma.'%"'.$cutoff.' ORDER BY frequency DESC LIMIT '.$limit;

	$nl = "\n";
	$res = '';
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	foreach($PDO->query($query.';') as $row){
		$res.=trim($row['lemma'],"|").$nl;
	}
	print($res);
}
?>
