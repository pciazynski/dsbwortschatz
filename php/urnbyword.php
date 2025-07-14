<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT DISTINCT token FROM lemmatokenfrequency WHERE lemma LIKE "%|'.$_GET['lemma'].'|%"';
	$token = '';
	foreach($PDO->query($query.';') as $row){
		$token .= $row['token'].",";
	}
	$token = substr_replace($token,'',-1);

	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$query = 'SELECT urn, date FROM urnwordbag WHERE wordbag LIKE "%|'.str_replace(",",'|%" OR wordbag LIKE "%|',$token).'|%"';

	(isset($_GET['year'])) ? $query .= ' AND date '.$_GET['year'] : NULL;
	(isset($_GET['sort'])) ? $query .= ' ORDER BY date ASC' : NULL;

	$tab = "\t";
	$nl = "\n";
	$res = '';
	
	foreach($PDO->query($query.';') as $row){
		$res.=$row['urn'].$tab.$row['date'].$nl;
	}
	print($res);
}

elseif (isset($_GET['token'])){
	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$query = 'SELECT urn, date FROM urnwordbag WHERE wordbag LIKE "%|'.str_replace(",",'|%" OR wordbag LIKE "%|',$_GET['token']).'|%"';

	(isset($_GET['year'])) ? $query .= ' AND date '.$_GET['year'] : NULL;
	(isset($_GET['sort'])) ? $query .= ' ORDER BY date ASC' : NULL;

	$tab = "\t";
	$nl = "\n";
	$res = '';
	
	foreach($PDO->query($query.';') as $row){
		$res.=$row['urn'].$tab.$row['date'].$nl;
	}
	print($res);
}

?>
