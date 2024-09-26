<?php
header('Content-Type: text/plain');

#token,lemma,norm,type,subtype,date,frequency
$token = str_replace(",",'" OR lemma LIKE "%|',$_GET['lemma']);


if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT lemma, SUM(frequency) as summe, date FROM tokenlemmanormtypesubtypedatefrequency';
	if (isset($_GET['exact'])){
		$query .= ' WHERE lemma = "|'.$token.'|"';
	}
	else{
		$query .= ' WHERE lemma LIKE "%|'.$token.'|%"';
	}
	
	$query.= ' GROUP BY lemma, date ';
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY date ASC';
	}
	
	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['lemma']."\t".$row['date']."\t".$row['summe']."\n");
	}
}



?>
