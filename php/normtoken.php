<?php
header('Content-Type: text/plain');

if (isset($_GET['norm'])){
	$PDO = new PDO('sqlite:../data/normmapping.db');
	$query = 'SELECT token, norm, frequency FROM normtokenfrequency';
	(isset($_GET['exact']) and $_GET['exact']==1) ? $query .= ' WHERE norm = "|'.str_replace(',','|" OR norm = "|',$_GET['norm']).'|"' : $query .= ' WHERE norm LIKE "%|'.str_replace(',','|%" OR norm LIKE "%|',$_GET['norm']).'|%"';
	
	(isset($_GET['sort'])) ? $query .= ' ORDER BY frequency DESC, token' : NULL;
	
	$tab = "\t";
	$nl = "\n";
	$res = '';

	foreach($PDO->query($query.';') as $row){
		$res.=$row['norm'].$tab.$row['token'].$tab.$row['frequency'].$nl;
	}
	print($res);
}
?>
