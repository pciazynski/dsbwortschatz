<?php
header('Content-Type: text/plain');

if(isset($_GET['token'])){
	
	$token = $_GET['token'];
	$res = '';
	$tab = "\t";
	$colon = ":";
	$nl = "\n";
	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$lemma = "";

	$query = 'SELECT Min(date) as mindate, Max(date) as maxdate FROM tokendatecount WHERE token="'.$token.'"';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['mindate'].$tab.$row['maxdate'].$nl;
	}
	
	if(strlen(trim($res))==0){
		print("NULL");
		exit();
	}
	$PDO = new PDO('sqlite:../data/lemmamapping.db');

	$query = 'SELECT DISTINCT lemma FROM lemmatokenfrequency WHERE token = "'.$token.'"';
	foreach($PDO->query($query.';') as $row){
		$lemma=$row['lemma'];
	}
	$res.=$lemma.$nl;

	if (strlen($lemma)>0){
		$query = 'SELECT token FROM lemmatokenfrequency WHERE lemma LIKE "%'.$lemma.'%"';
		foreach($PDO->query($query.';') as $row){
			$res.=$row['token'].$tab;
		}
	}
	$res=trim($res,$tab).$nl;

	$query = 'SELECT DISTINCT norm FROM tokenlemmanormtypesubtypedatefrequency WHERE token = "'.$token.'"';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['norm'].$tab;
	}
	$res=trim($res,$tab).$nl;
	
	$query = 'SELECT DISTINCT type FROM tokenlemmanormtypesubtypedatefrequency WHERE token = "'.$token.'"';
	foreach($PDO->query($query.';') as $row){
		(strlen(trim($row['type']))>0) ? $res.=$row['type'].$tab:NULL;
	}
	$res=trim($res,$tab).$nl;
	
	$PDO = new PDO('sqlite:../data/collocation.db');
	$query = 'SELECT left FROM collocation WHERE right = "'.$token.'" ORDER BY logdice DESC LIMIT 10';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['left'].$tab;
	}
	$res=trim($res,$tab).$nl;
	$query = 'SELECT right FROM collocation WHERE left = "'.$token.'" ORDER BY logdice DESC LIMIT 10';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['right'].$tab;
	}
	$res=trim($res,$tab).$nl;
	
	$PDO = new PDO('sqlite:../data/ngram5.db');
	$query = 'SELECT ngram FROM ngramcount WHERE ngram LIKE "%\_'.$token.'\_%" escape "\" ORDER BY frequency DESC LIMIT 5';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['ngram'].$tab;
	}
	$res=trim($res,$tab).$nl;

	print($res);
}
?>
