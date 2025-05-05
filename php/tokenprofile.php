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
	
	$PDO1 = new PDO('sqlite:../data/lemmamapping.db');

	$query = 'SELECT DISTINCT lemma FROM lemmatokenfrequency WHERE token = "'.$token.'"';
	foreach($PDO1->query($query.';') as $row){
		$lemma=$row['lemma'];
	}
	$res.=$lemma.$nl;

	$query = 'SELECT token FROM lemmatokenfrequency WHERE lemma LIKE "%'.$lemma.'%"';
	foreach($PDO1->query($query.';') as $row){
		$res.=$row['token'].$tab;
	}
	$res=trim($res).$nl;

	$query = 'SELECT DISTINCT norm FROM tokenlemmanormtypesubtypedatefrequency WHERE token = "'.$token.'"';
	foreach($PDO1->query($query.';') as $row){
		$res.=$row['norm'].$tab;
	}
	$res=trim($res).$nl;
	
	$query = 'SELECT DISTINCT type FROM tokenlemmanormtypesubtypedatefrequency WHERE token = "'.$token.'"';
	foreach($PDO1->query($query.';') as $row){
		(strlen(trim($row['type']))>0) ? $res.=$row['type'].$tab:NULL;
	}
	$res=trim($res).$nl;
	
	$PDO1 = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT left FROM collocation WHERE token = "'.$token.'" ORDER BY logdice DESC LIMIT 10';
	foreach($PDO1->query($query.';') as $row){
		$lemma=$row['lemma'].$tab;;
	}
	$res.=$lemma.$nl;
	$query = 'SELECT right FROM collocation WHERE token = "'.$token.'" ORDER BY logdice DESC LIMIT 10';
	foreach($PDO1->query($query.';') as $row){
		$lemma=$row['lemma'].$tab;;
	}
	$res.=$lemma.$nl;
	print($res);
}
?>
