<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/bagofwords.db');
$query = 'SELECT SUBSTR(token,1,1) as sub , token FROM tokendatecount WHERE LENGTH(token)=='.$_GET['length'].' GROUP BY sub ORDER BY token DESC LIMIT 50';

$result = $PDO->query($query.";");
$nl = "\n";
foreach($result as $row){
	print($row['token'].$nl);
}

?>
