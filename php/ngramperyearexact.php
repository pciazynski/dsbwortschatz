<?php
header('Content-Type: text/plain');

if (isset($_GET['filter'])){
	$n = $_GET['n'];
	$PDO = new PDO('sqlite:../data/ngram'.$n.'.db');
	$query = 'SELECT * FROM ngramdatecount WHERE ngram = "_'.$_GET['filter'].'_"';
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY date ASC';
	}

	$result = $PDO->query($query.";");
	$nl = "\n";
	$tab = "\t";

	foreach($result as $row){
		print($row['ngram'].$tab.$row['date'].$tab.$row['frequency'].$nl);
	}

}



?>
