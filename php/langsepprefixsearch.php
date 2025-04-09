<?php
header('Content-Type: text/plain');

(isset($_GET['token'])) ? $token = $_GET['token'] : NULL;
(isset($_GET['n']))?$n=$_GET['n']:$n=3;

if (strlen($token)>=1){
	(isset($_GET['limit'])) ? $limit = $_GET['limit'] : $limit = 100;
	(isset($_GET['cutoff'])) ? $cutoff = ' GROUP BY SUBSTRING(token,0,'.strlen($token)+$_GET['cutoff'].')' : $cutoff = "";

	$query = 'SELECT DISTINCT token FROM tokenurnyearpassagestructureelementfrequency WHERE token LIKE "'.$token.'%"'.$cutoff.' ORDER BY frequency DESC LIMIT '.$limit;

	$nl = "\n";
	$res = '';
	$PDO = new PDO('sqlite:../data/langDeu'.$n.'.db');

	foreach($PDO->query($query.';') as $row){
		$res.=$row['token'].$nl;
	}
	print($res);
}
?>
