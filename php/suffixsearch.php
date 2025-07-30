<?php
header('Content-Type: text/plain');

(isset($_GET['token'])) ? $token = $_GET['token'] : NULL;

if (strlen($token)>=1){
	(isset($_GET['limit'])) ? $limit = $_GET['limit'] : $limit = 100;

	$PDO = new PDO('sqlite:../data/bagofwords.db');
	$query = 'SELECT DISTINCT token FROM tokencount WHERE token LIKE "%'.$token.'" ORDER BY token LIMIT '.$limit;

	$nl = "\n";
	$res = '';
	
	foreach($PDO->query($query.';') as $row){
		$res.=$row['token'].$nl;
	}
	print($res);
}
?>
