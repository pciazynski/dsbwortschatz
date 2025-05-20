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
		$query = 'SELECT token, frequency FROM lemmatokenfrequency WHERE lemma = "'.$lemma.'" ORDER BY frequency DESC';
		foreach($PDO->query($query.';') as $row){
			$res.=$row['token'].$colon.$row['frequency'].$tab;
		}
	}
	$res=trim($res,$tab).$nl;
	print($res);
}
?>
