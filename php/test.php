<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$lemma = "TEJ";
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT token, type, frequency FROM tokenlemmanormtypesubtypedatefrequency';
	if (isset($_GET['inclusive'])){
		$lemma = str_replace(',','|%" OR lemma LIKE "%|',$_GET['lemma']);
		$query .= ' WHERE lemma LIKE "%|'.$lemma.'|%"';
	}
	else{
		$lemma = str_replace(',','|" OR lemma = "|',$_GET['lemma']);
		$query .= ' WHERE lemma = "|'.$lemma.'|"';
	}
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY frequency DESC';
	}
	
	$tab = "\t";
	$nl = "\n";
	foreach($PDO->query($query.';') as $row){
		print($row['lemma'].$tab.$row['token'].$tab.$row['frequency'].$nl);
	}
}
?>
