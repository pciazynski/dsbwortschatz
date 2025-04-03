<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){

	$PDO = new PDO('sqlite:../data/lemmamapping.db?mode=ro');
	$query = 'SELECT DISTINCT token FROM lemmatokenfrequency WHERE lemma = LIKE "%|'.$_GET['lemma'].'|%"';

	$nl = "\n";
	foreach($PDO->query($query.';') as $row){
		print($row['token'].$nl);
	}
}
?>
