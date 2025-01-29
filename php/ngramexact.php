<?php
header('Content-Type: text/plain');

$n = $_GET['n'];
$PDO = new PDO('sqlite:../data/ngram'.$n.'.db');
$frequency = 1;

if (isset($_GET['frequency'])){
	$frequency = $_GET['frequency'];
}

$query = 'SELECT ngram, frequency FROM ngramcount WHERE frequency >='.$frequency;
if (isset($_GET['filter'])){
	$query .= ' AND ngram = "_'.$_GET['filter'].'_"';
}

$result = $PDO->query($query.";");
foreach($result as $row){
	print($row['ngram']."\t".$row['frequency']."\n");
}

?>
