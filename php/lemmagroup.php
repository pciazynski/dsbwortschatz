<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/lemmamapping.db');
$query = 'SELECT lemma, SUM(frequency) as sumfreq FROM tokenlemmanormtypesubtypedatefrequency';
$lemma = $_GET['lemma'];

if (isset($_GET['lemma'])){
	$query .= ' WHERE lemma LIKE "%|'.$lemma.'|%"';
}

$query.=' GROUP BY lemma ';

if (isset($_GET['sort'])){
	$query .= ' ORDER BY sumfreq DESC';
}

$tab = "\t";
$nl = "\n";

foreach($PDO->query($query.';') as $row){
	print($row['lemma'].$tab.$row['sumfreq'].$nl);
}

?>
