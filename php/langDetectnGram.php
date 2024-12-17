<?php
header('Content-Type: text/plain');

if (isset($_GET['deu']) and strlen($_GET['deu'])>0 and isset($_GET['n']) and strlen($_GET['n'])>0){
	$PDO = new PDO('sqlite:../data/langDetect'.$_GET['n'].'.db');
	$deu = $_GET['deu'];

	$frequency = 1;
	if (isset($_GET['frequency']) and strlen($_GET['filter'])>0){
		$frequency = $_GET['frequency'];
	}
	
	if($deu == 0){
		$query = 'SELECT ngram, frequency FROM langDetectdsbngram WHERE frequency >='.$frequency;
	}else if($deu == $_GET['n']){
		$query = 'SELECT ngram, frequency FROM langDetectdeungram WHERE frequency >='.$frequency;
	}else{
		$query = 'SELECT ngram, frequency FROM langDetectmixngram WHERE deu =='.$deu.' AND frequency >='.$frequency;
	}
	if (isset($_GET['filter']) and strlen($_GET['filter'])>0){
		$filter = str_replace('_','\_',$_GET['filter']);
		$query .= ' AND ngram LIKE "%\_'.$filter.'\_%" escape "\" ';
	}
	
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY frequency DESC';
	}

	if (isset($_GET['count']) and strlen($_GET['count'])>0){
		$query.=' LIMIT '.$_GET['count'];
	}

	$result = $PDO->query($query.";");

	foreach($result as $row){
		print($row['ngram']."\t".$row['frequency']."\n");
	}
}
?>
