<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/bagofwords.db');
$query = 'SELECT * FROM tokendatecount';
$token = str_replace(",",'" OR token LIKE "',$_GET['token']);


if (isset($_GET['token'])){
	$query .= ' WHERE token LIKE "'.$token.'"';
}

if (isset($_GET['sort'])){
	$query .= ' ORDER BY date ASC';
}

$tab = "\t";
$nl = "\n";
foreach($PDO->query($query.';') as $row){
	print($row['token'].$tab.$row['date'].$tab.$row['frequency'].$nl);
}

?>
