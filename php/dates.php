<?php
header('Content-Type: text/plain');
$PDO = new PDO('sqlite:../data/ctstm.db');
$query = 'SELECT DISTINCT date FROM tokendatecount ORDER BY date ASC';

$result = $PDO->query($query.";");
foreach($result as $row){
	print($row['date']."\n");
}

?>
