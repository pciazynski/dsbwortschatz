<?php
header('Content-Type: text/plain');

#token,lemma,norm,type,subtype,date,frequency
$token = str_replace(",",'" OR lemma LIKE "%|',$_GET['lemma']);


if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT DISTINCT(token) FROM tokenlemmanormtypesubtypedatefrequency WHERE date '.$_GET['year'];
	if (isset($_GET['exact'])){
		$query .= ' AND lemma = "|'.$token.'|"';
	}
	else{
		$query .= ' AND lemma LIKE "%|'.$token.'|%"';
	}

	if (isset($_GET['sort'])){
		$query .= ' ORDER BY token';
	}
	
	$nl = "\n";

	foreach($PDO->query($query.';') as $row){
		print($row['token'].$nl);
	}
}



?>
