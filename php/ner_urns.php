<?php
header('Content-Type: text/plain');

(isset($_GET['tag'])) ? $tag = $_GET['tag'] : $tag = "";

$PDO = new PDO('sqlite:../data/entities'.$tag.'.db');
$query = 'SELECT urn, frequency FROM tokenurndatecount';

(isset($_GET['token'])) ? $query .= ' WHERE token = "'.$_GET['token'].'"' : $token = "";
(isset($_GET['sort'])) ? $query .= ' ORDER BY date ASC' : NULL;

$res = '';
foreach($PDO->query($query.";") as $row){
	$res .= $row['urn']."\t".$row['frequency']."\n";
}
print($res);
?>
