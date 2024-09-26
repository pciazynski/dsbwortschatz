<?php
header('Content-Type: text/plain');

$n = $_GET['n'];
$PDO = new PDO('sqlite:../data/ngram'.$n.'.db');
$frequency = 0;

if (isset($_GET['frequency'])){
	$frequency = $_GET['frequency'];
}

$query = 'SELECT ngram, frequency FROM ngramcount WHERE frequency >='.$frequency;
if (isset($_GET['filter'])){
	$filter = str_replace('_','\_',$_GET['filter']);
	$query .= ' AND ngram LIKE "%\_'.$filter.'\_%" escape "\" ';
}

if (isset($_GET['sort'])){
	$query .= ' ORDER BY frequency DESC';
}

$result = $PDO->query($query.";");
foreach($result as $row){
	print($row['ngram']."\t".$row['frequency']."\n");
}

?>
