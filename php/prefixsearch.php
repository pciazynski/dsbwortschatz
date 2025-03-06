<?php
header('Content-Type: text/plain');

(isset($_GET['token'])) ? $token = $_GET['token'] : NULL;

if (strlen($token)>=1){
	(isset($_GET['limit'])) ? $limit = $_GET['limit'] : $limit = 100;
	(isset($_GET['cutoff'])) ? $cutoff = ' GROUP BY SUBSTRING(token,0,'.strlen($token)+$_GET['cutoff'].')' : $cutoff = "";

	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$query = 'SELECT DISTINCT token FROM tokendatecount WHERE token LIKE "'.$token.'%"'.$cutoff.' ORDER BY frequency DESC LIMIT '.$limit;

	$nl = "\n";
	$res = '';
	
	foreach($PDO->query($query.';') as $row){
		$res.=$row['token'].$nl;
	}
	print($res);
}
?>
