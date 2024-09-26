<?php
header('Content-Type: text/plain');

$token = "";
$tag = "";

if (isset($_GET['tag'])){
	$tag = $_GET['tag'];
}

$PDO = new PDO('sqlite:../data/entities'.$tag.'.db');
$query = 'SELECT urn, frequency FROM tokenurndatecount';
if (isset($_GET['token'])){
	$query .= ' WHERE token = "'.$_GET['token'].'"';
}

if (isset($_GET['sort'])){
	$query .= ' ORDER BY date ASC';
}

$result = $PDO->query($query.";");
foreach($result as $row){
	print($row['urn']."\t".$row['frequency']."\n");
}
?>
