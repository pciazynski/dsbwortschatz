<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){

	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT token, lemma, frequency FROM lemmatokenfrequency';
	if (isset($_GET['inclusive'])){
		$lemma = str_replace(',','|%" OR lemma LIKE "%|',$_GET['lemma']);
		$query .= ' WHERE lemma LIKE "%|'.$lemma.'|%"';
	}
	else{
		$lemma = str_replace(',','|" OR lemma = "|',$_GET['lemma']);
		$query .= ' WHERE lemma = "|'.$lemma.'|"';
	}
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY frequency DESC, token';
	}
	$result = $PDO->query($query.";");
	
	$tab = "\t";
	$nl = "\n";
	
	foreach($result as $row){
		print($row['lemma'].$tab.$row['token'].$tab.$row['frequency'].$nl);
	}
}
?>
