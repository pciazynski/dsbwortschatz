<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	if(isset($_GET['year'])){
		$query = 'SELECT DISTINCT (token), SUM(frequency) as sumfreq FROM tokenlemmanormtypesubtypedatefrequency WHERE date '.$_GET['year'];
	}else{
		$query = 'SELECT token, SUM(frequency) as sumfreq FROM lemmatokenfrequency WHERE true';
	}
	if(isset($_GET['exact'])){
		$query .= ' AND lemma = "|'.$_GET['lemma'].'|"';	
	}
	else{
		$query .= ' AND lemma LIKE "|%'.$_GET['lemma'].'%|"';	
	}
	$query.= ' GROUP BY token';
	
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY sumfreq DESC, token';
	}
	$tab = "\t";
	$nl = "\n";

	foreach($PDO->query($query.';') as $row){
		print($row['token'].$tab.$row['sumfreq'].$nl);
	}
}
?>
