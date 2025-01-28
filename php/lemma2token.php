<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT DISTINCT (token), SUM(frequency) as sumfreq FROM tokenlemmanormtypesubtypedatefrequency';
	$query .= ' WHERE lemma LIKE "%|'.$_GET['lemma'].'|%" GROUP BY token';
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY sumfreq DESC, token';
	}
	$result = $PDO->query($query.";");
	
	$tab = "\t";
	$nl = "\n";
	
	foreach($result as $row){
		print($row['token'].$tab.$row['sumfreq'].$nl);
	}
}
?>
