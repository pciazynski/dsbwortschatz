<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/metadata.db');
$query = 'SELECT author,title,date FROM docmeta WHERE author NOT NULL';

(isset($_GET['sort'])) ? $query .= ' ORDER BY date ASC' : NULL;

$tab = "\t";
$nl = "\n";
$res = '';

foreach($PDO->query($query.';') as $row){
	$res.=$row['author'].$tab.$row['date'].$tab.$row['title'].$nl;
}
print($res);

?>
