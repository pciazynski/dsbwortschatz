<?php
header('Content-Type: text/plain');

$PDO = new PDO('sqlite:../data/lemmamapping.db');
$query = 'SELECT DISTINCT lemma,token,norm,type,subtype FROM tokenlemmanormtypesubtypedatefrequency';


if (isset($_GET['token'])){
	$query .= ' WHERE token = "'.$_GET['token'].'"';
	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['lemma']."\t".$row['token']."\t".$row['norm']."\t".$row['type']."\t".$row['subtype']."\n");
	}
}
?>
