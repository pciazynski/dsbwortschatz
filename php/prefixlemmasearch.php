<?php
header('Content-Type: text/plain');

(isset($_GET['lemma'])) ? $lemma = $_GET['lemma'] : NULL;

if (strlen($lemma)>=1){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	(isset($_GET['limit'])) ? $limit = $_GET['limit'] : $limit = 100;
	(isset($_GET['cutoff'])) ? $cutoff = ' GROUP BY SUBSTRING(lemma,0,'.strlen($lemma)+$_GET['cutoff'].')' : $cutoff = '';
	
	$query = 'SELECT DISTINCT lemma FROM lemmafrequency WHERE lemma LIKE "'.$lemma.'%"'.$cutoff.' ORDER BY frequency DESC LIMIT '.$limit;

	$nl = "\n";
	$res = '';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['lemma'].$nl;
	}
	print($res);
}
?>
