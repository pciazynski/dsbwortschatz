<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/lemmamapping.db');
$query = 'SELECT DISTINCT lemma,token,norm,type,subtype FROM tokenlemmanormtypesubtypedatefrequency';


if (isset($_GET['token'])){
	$query .= ' WHERE token = "'.$_GET['token'].'"';

	$tab = "\t";
	$nl = "\n";
	foreach($PDO->query($query.';') as $row){
		print($row['lemma'].$tab.$row['token'].$tab.$row['norm'].$tab.$row['type'].$tab.$row['subtype'].$nl);
	}
}
?>
