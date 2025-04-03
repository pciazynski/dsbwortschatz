<?php
header('Content-Type: text/plain');

$token = "";
$tag = "";

(isset($_GET['tag'])) ? $tag = $_GET['tag'] : NULL;

(isset($_GET['token'])) ? $query .= ' WHERE stemming = "'.$_GET['token'].'"' : NULL;
(isset($_GET['sort'])) ? $query .= ' ORDER BY length(mapping)' : NULL;

$PDO = new PDO('sqlite:../data/entities'.$tag.'.db?mode=ro');
$query = 'SELECT * FROM stemmingmapping';

$nl = "\n";
$res = '';

foreach($PDO->query($query.';') as $row){
	$res.=$row['mapping'].$nl;
}
print($res);
?>
