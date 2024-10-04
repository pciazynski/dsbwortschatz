<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/langDetect'.$_GET['n'].'.db');
$frequency = 0;
$deu = -1;

if (isset($_GET['frequency'])){
	$frequency = $_GET['frequency'];
}

if (isset($_GET['deu'])){
	$deu = $_GET['deu'];
}

$query = 'SELECT ngram, frequency, deu FROM langDetectngram WHERE deu =='.$deu.' AND frequency >='.$frequency;
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
