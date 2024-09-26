<?php
header('Content-Type: text/plain');

$n = $_GET['n'];
$PDO = new PDO('sqlite:../data/ngram'.$n.'.db');
$query = 'SELECT * FROM ngramdatecount';
if (isset($_GET['filter'])){
	$filter = str_replace('_','\_',$_GET['filter']);
	$query .= ' WHERE ngram LIKE "%\_'.$filter.'\_%" escape "\"';
}

if (isset($_GET['sort'])){
	$query .= ' ORDER BY date ASC';
}

$result = $PDO->query($query.";");
foreach($result as $row){
	print($row['ngram']."\t".$row['date']."\t".$row['frequency']."\n");
}

?>
