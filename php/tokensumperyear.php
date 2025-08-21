<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/bagofwords.db');
$query = 'SELECT sum(frequency) as summe, date FROM tokendatecount GROUP BY date ORDER BY date ASC';

$tab = "\t";
$nl = "\n";
$res = '';

foreach($PDO->query($query.';') as $row){
	$res.=$row['date'].$tab.$row['summe'].$nl;
}
print($res);

?>
