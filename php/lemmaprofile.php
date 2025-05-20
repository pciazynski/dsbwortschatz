<?php
header('Content-Type: text/plain');

if(isset($_GET['lemma'])){
	
	$lemma = $_GET['lemma'];
	$res = '';
	$tab = "\t";
	$colon = ":";
	$nl = "\n";

	$PDO = new PDO('sqlite:../data/lemmamapping.db');

	if (strlen($lemma)>0){
		$query = 'SELECT Min(date) as mindate, Max(date) as maxdate FROM tokenlemmanormtypesubtypedatefrequency WHERE lemma = "|'.$lemma.'|"';
		foreach($PDO->query($query.';') as $row){
			$res.=$row['mindate'].$tab.$row['maxdate'].$nl;
		}
	}
	$res=trim($res,$tab).$nl;
	print($res);
}
?>
