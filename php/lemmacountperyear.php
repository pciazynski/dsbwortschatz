<?php
header('Content-Type: text/plain');

#token,lemma,norm,type,subtype,date,frequency
$token = str_replace(",",'" OR lemma LIKE "%|',$_GET['lemma']);


if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT * FROM tokenlemmanormtypesubtypedatefrequency';
	if (isset($_GET['exact'])){
		$query .= ' WHERE lemma = "|'.$token.'|"';
	}
	else{
		$query .= ' WHERE lemma LIKE "%|'.$token.'|%"';
	}
	
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY date ASC';
	}
	
	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['lemma']."\t".$row['date']."\t".$row['frequency']."\t".$row['token']."\n");
	}
}



?>
