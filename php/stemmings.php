<?php
header('Content-Type: text/plain');

$token = "";
$tag = "";

if (isset($_GET['tag'])){
	$tag = $_GET['tag'];
}

$PDO = new PDO('sqlite:../data/entities'.$tag.'.db');
$query = 'SELECT * FROM stemmingmapping';
if (isset($_GET['token'])){
	$query .= ' WHERE stemming = "'.$_GET['token'].'"';
}

if (isset($_GET['sort'])){
	$query .= ' ORDER BY length(mapping)';
}

$nl = "\n";
foreach($PDO->query($query.';') as $row){
	print($row['mapping'].$nl);
}
?>
