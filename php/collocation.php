<?php
header('Content-Type: text/plain');
$sep = "\t";
$PDO = new PDO('sqlite:../data/collocation.db');
$frequency = 0;
$condition = '';

if (isset($_GET['frequency']) and strlen($_GET['frequency'])>0){
	$frequency = $_GET['frequency'];
}



if (isset($_GET['right']) and strlen($_GET['right'])>0){
	$condition = 'WHERE right == "'.$_GET['right'].'" AND frequency >='.$frequency;
}

if (isset($_GET['left']) and strlen($_GET['left'])>0){
	$condition = 'WHERE left == "'.$_GET['left'].'" AND frequency >='.$frequency;
}
if(strlen($condition) == 0){
	if($frequency==0){
		$frequency=10;
	}
	$condition = ' WHERE frequency >= '.$frequency;
}

if (isset($_GET['logdice']) and strlen($_GET['logdice'])>0){
	if(str_contains($_GET['logdice'],"-")){
		$tmp = explode("-",$_GET['logdice']);
		$condition .= ' AND logdice BETWEEN '.$tmp[0].' AND '.$tmp[1].'.99999999999999999';
	}
	else{
		$condition .= ' AND logdice >= '.$_GET['logdice'];
	}
}

$query = 'SELECT * FROM collocation '.$condition;
if(isset($_GET['sortBy'])){
	$sortBy = $_GET['sortBy'];
	if($sortBy == "logdice" or $sortBy == "frequency"){
		$query.=' ORDER BY '.$_GET['sortBy'].' DESC';
	}
}


$result = $PDO->query($query.";");
foreach($result as $row){
	print($row['left'].$sep.$row['right'].$sep.$row['frequency'].$sep.$row['logdice']."\n");
}
?>
