<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT DISTINCT (token), lemma FROM tokenlemmanormtypesubtypedatefrequency';
	$query .= ' WHERE lemma = "|'.$_GET['lemma'].'|" GROUP BY token';
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY token';
	}
	$result = $PDO->query($query.";");
	
	$tab = "\t";
	$nl = "\n";
	
	foreach($result as $row){
		print($row['token'].$tab.$row['lemma'].$nl);
	}
}
?>
