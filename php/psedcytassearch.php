<?php
header('Content-Type: text/plain');

if (isset($_GET['token'])){
	$token = $_GET['token'];
	$token = str_replace(array("ł","ć","č","ė","é","ě","ź","ž","ś","š","ŕ","ó"),array("l4","c1","c2","e1","e1","e2","z1","z2","s1","s2","r1","o1"),$token);
	$token = str_replace(',','-%" OR url LIKE "',$token);

	$PDO = new PDO('sqlite:../data/psedcytas.db');
	$query = 'SELECT url FROM urls';
	$query .= ' WHERE url LIKE "'.$token.'-%" LIMIT 1';
	
	foreach($PDO->query($query.';') as $row){
		print($row['url']);
	}
}
?>
