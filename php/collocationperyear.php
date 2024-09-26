<?php
header('Content-Type: text/plain');
$sep = "\t";

$PDO = new PDO('sqlite:../data/collocation.db');
$frequency = 0;
$year = "";

$leftright = "";
if (isset($_GET['right']) and strlen($_GET['right'])>0){
	$leftright = 'right == "'.$_GET['right'].'"';
}
if (isset($_GET['left']) and strlen($_GET['left'])>0){
	$leftright = 'left == "'.$_GET['left'].'"';
}

if (isset($_GET['year'])){
	$year = $_GET['year'];
}

if (isset($_GET['frequency']) and strlen($_GET['frequency'])>0){
	$frequency = $_GET['frequency'];
}

if(strlen($leftright) > 0 and strlen($year)==4){
	$query = 'SELECT left, right, frequency, date FROM collocationperyear WHERE '.$leftright.' AND date =='.$year.' AND frequency >= '.$frequency;

	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['date'].$sep.$row['left'].$sep.$row['right'].$sep.$row['frequency']."\n");
	}
}
elseif(strlen($leftright) > 0){
	$query = 'SELECT left, right, frequency, date FROM collocationperyear WHERE '.$leftright.' AND frequency >= '.$frequency;

	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['date'].$sep.$row['left'].$sep.$row['right'].$sep.$row['frequency']."\n");
	}
}
elseif(strlen($year)==4){
	$query = 'SELECT left, right, frequency, date FROM collocationperyear WHERE date =='.$year.' AND frequency >= '.$frequency;
	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['date'].$sep.$row['left'].$sep.$row['right'].$sep.$row['frequency']."\n");
	}
}
?>
