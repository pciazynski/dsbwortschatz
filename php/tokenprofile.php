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

	$query = 'SELECT frequency FROM tokencount WHERE token="'.$token.'"';
	foreach($PDO->query($query.';') as $row){
		$frequency = $row['frequency'];
	}
	
	$query = 'SELECT COUNT(*) as rank FROM tokencount WHERE frequency>'.$frequency.'';
	foreach($PDO->query($query.';') as $row){
		$rank=$row['rank'];
	}
	
	$res .= $frequency.$tab.($rank+1).$nl;

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
		$lemma.=$row['lemma'];
	}
	$res.=$lemma.$nl;


	if (strlen($lemma)>0){
		$query = 'SELECT token, frequency FROM lemmatokenfrequency WHERE lemma LIKE "%'.$lemma.'%" ORDER BY frequency DESC';
		foreach($PDO->query($query.';') as $row){
			$res.=$row['token'].$colon.$row['frequency'].$tab;
		}
	}
	$res=trim($res,$tab).$nl;

	$query = 'SELECT DISTINCT norm FROM tokenlemmanormtypesubtypedatefrequency WHERE token = "'.$token.'"';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['norm'].$tab;
	}
	$res=trim($res,$tab).$nl;
	
	$query = 'SELECT type, SUM(frequency) as c FROM tokenlemmanormtypesubtypedatefrequency WHERE token = "'.$token.'" GROUP BY type';
	foreach($PDO->query($query.';') as $row){
		(strlen(trim($row['type']))>0) ? $res.=$row['type'].$colon.$row['c'].$tab:NULL;
	}
	$res=trim($res,$tab).$nl;
	
	$PDO = new PDO('sqlite:../data/collocation.db');
	$query = 'SELECT left,CAST(logdice AS INT) as c FROM collocation WHERE right = "'.$token.'" ORDER BY logdice DESC LIMIT 10';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['left'].$colon.$row['c'].$tab;
	}
	$res=trim($res,$tab).$nl;
	$query = 'SELECT right,CAST(logdice AS INT) as c  FROM collocation WHERE left = "'.$token.'" ORDER BY logdice DESC LIMIT 10';
	foreach($PDO->query($query.';') as $row){
		$res.=$row['right'].$colon.$row['c'].$tab;
	}
	$res=trim($res,$tab).$nl;
	
	print($res);
}
?>
