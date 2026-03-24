<?php
header('Content-Type: text/plain');

if (isset($_GET['author'])){
	$PDO = new PDO('sqlite:../data/authors.db');
	$query = 'SELECT * FROM authors WHERE author ="'.$_GET['author'].'"';
	(isset($_GET['year'])) ? $query .= ' AND year ='.$_GET['year'] : NULL;
	$tab = "\t";
	$nl = "\n";
	$res = '';

	foreach($PDO->query($query.';') as $row){
		$res.=$row['urn'].$tab.$row['title'].$tab.$row['year'].$tab.$row['coauthors'].$nl;
	}
	print($res);
}

?>
