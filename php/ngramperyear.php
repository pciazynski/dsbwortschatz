<?php
header('Content-Type: text/plain');

$n = $_GET['n'];
$PDO = new PDO('sqlite:../data/ngram'.$n.'.db');
$query = 'SELECT * FROM ngramdatecount WHERE true';
if (isset($_GET['filter'])){
	$filter = str_replace('_','\_',$_GET['filter']);
	$query .= ' AND ngram LIKE "%\_'.$filter.'\_%" escape "\"';
}

if (isset($_GET['year'])){
	$query .= ' AND date = '.$_GET['year'];
}


if (isset($_GET['sort'])){
	$query .= ' ORDER BY date ASC';
}

$result = $PDO->query($query.";");
$nl = "\n";
$tab = "\t";

foreach($result as $row){
	print($row['ngram'].$tab.$row['date'].$tab.$row['frequency'].$nl);
}

?>
