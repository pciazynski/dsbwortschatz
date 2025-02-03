<?php
header('Content-Type: text/plain');
$PDO = new PDO('sqlite:../data/ctstm.db');
$query = 'SELECT DISTINCT date FROM tokendatecount ORDER BY date ASC';

$nl = "\n";
foreach($PDO->query($query.';') as $row){
	print($row['date'].$nl);
}

?>
