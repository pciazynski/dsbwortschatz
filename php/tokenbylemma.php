<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){

	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT DISTINCT token FROM lemmatokenfrequency WHERE lemma = LIKE "%|'.$_GET['lemma'].'|%"';
	echo($query);

	$result = $PDO->query($query.";");
	$nl = "\n";
	
	foreach($result as $row){
		print($row['token'].$nl);
	}
}
?>
