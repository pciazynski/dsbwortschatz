<?php
header('Content-Type: text/plain');

if (isset($_GET['token'])){
	$token = $_GET['token'];
}
if (strlen($token)>=1){
	$nl = "\n";
	$PDO = new PDO('sqlite:../data/psedcytas.db');
	$query = 'SELECT url FROM urls';
	$query .= ' WHERE url LIKE "'.$token.'%" LIMIT 1';
	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['url'].$nl);
	}
}
?>
