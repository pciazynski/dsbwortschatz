<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT DISTINCT token FROM lemmatokenfrequency WHERE lemma LIKE "%|'.$_GET['lemma'].'|%"';
	$result = $PDO->query($query.";");
	$token = "";
	foreach($result as $row){
		$token .= $row['token'].",";
	}
	$token = substr_replace($token,'',-1);

	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$query = 'SELECT urn, date FROM urnwordbag';
	$token = str_replace(",",'|%" OR wordbag LIKE "%|',$token);
	$query .= ' WHERE wordbag LIKE "%|'.$token.'|%"';
	if (isset($_GET['year'])){
		$query .= ' AND date =='.$_GET['year'];
	}
	
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY date ASC';
	}

	$tab = "\t";
	$nl = "\n";
	foreach($PDO->query($query.';') as $row){
		print($row['urn'].$tab.$row['date'].$nl);
	}
}

elseif (isset($_GET['token'])){
	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$query = 'SELECT urn, date FROM urnwordbag';
	$token = str_replace(",",'|%" OR wordbag LIKE "%|',$_GET['token']);
	$query .= ' WHERE wordbag LIKE "%|'.$token.'|%"';
	if (isset($_GET['year'])){
		$query .= ' AND date =='.$_GET['year'];
	}
	
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY date ASC';
	}

	$tab = "\t";
	$nl = "\n";
	foreach($PDO->query($query.';') as $row){
		print($row['urn'].$tab.$row['date'].$nl);
	}
}

?>
