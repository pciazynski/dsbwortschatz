<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/metadata.db');
$query = 'SELECT urn,title,date,author,restricted FROM docmeta WHERE True ';

(isset($_GET['author'])) ? $query .= ' AND author ="'.$_GET['author'].'"' : NULL;
(isset($_GET['restricted'])) ? $query .= ' AND restricted ="'.$_GET['restricted'].'"' : NULL;
(isset($_GET['year'])) ? $query .= ' AND date ="'.$_GET['year'].'"' : NULL;
(isset($_GET['sort'])) ? $query .= ' ORDER BY date ASC' : NULL;

$tab = "\t";
$nl = "\n";
$res = '';

foreach($PDO->query($query.';') as $row){
	$res.=$row['urn'].$tab.$row['title'].$tab.$row['date'].$tab.$row['author'].$tab.$row['restricted'].$nl;
}
print($res);

?>
