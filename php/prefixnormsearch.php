<?php
header('Content-Type: text/plain');

(isset($_GET['norm'])) ? $norm = $_GET['norm'] : NULL;

if (strlen($norm)>=1){
	$PDO = new PDO('sqlite:../data/normmapping.db');
	(isset($_GET['limit'])) ? $limit = $_GET['limit'] : $limit = 100;
	(isset($_GET['cutoff'])) ? $cutoff = ' GROUP BY SUBSTRING(norm,1,'.strlen($norm)+$_GET['cutoff'].')' : $cutoff = '';
	
	$query = 'SELECT DISTINCT norm FROM normfrequency WHERE norm LIKE "|'.$norm.'%"'.$cutoff.' ORDER BY frequency DESC LIMIT '.$limit;

	$nl = "\n";
	$res = '';
	foreach($PDO->query($query.';') as $row){
		$res.=trim($row['norm'],"|").$nl;
	}
	print($res);
}
?>
