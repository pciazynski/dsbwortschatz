<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/lemmamapping.db?mode=ro');
$query = 'SELECT lemma, SUM(frequency) as sumfreq FROM tokenlemmanormtypesubtypedatefrequency';

(isset($_GET['lemma'])) ? $query .= ' WHERE lemma LIKE "%|'.$_GET['lemma'].'|%"' : NULL;

$query.=' GROUP BY lemma ';

(isset($_GET['sort'])) ? $query .= ' ORDER BY sumfreq DESC' : NULL;

$tab = "\t";
$nl = "\n";
$res = '';

foreach($PDO->query($query.';') as $row){
	$res.=$row['lemma'].$tab.$row['sumfreq'].$nl;
}
print($res);
?>
