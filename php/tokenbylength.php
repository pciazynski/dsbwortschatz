<?php
header('Content-Type: text/plain');

if(isset($_GET['length'])){

	(isset($_GET['limit']))?$limit=$_GET['limit']:$limit=50;
	(isset($_GET['random']))?$order="random()":$order="token";

	#SUBSTR(token,1,1) and GROUP BY sub make sure that the words are not very similar
	$query = 'SELECT SUBSTR(token,1,1) as sub , token FROM tokencount WHERE LENGTH(token)=='.$_GET['length'].' GROUP BY sub ORDER BY '.$order.' DESC LIMIT '.$limit;

	$nl = "\n";
	$res = '';

	$PDO = new PDO('sqlite:../data/bagofwords.db');
	foreach($PDO->query($query.';') as $row){
		$res.=$row['token'].$nl;
	}

	print($res);
}
?>
