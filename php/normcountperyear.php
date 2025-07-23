<?php
header('Content-Type: text/plain');

#token,lemma,norm,type,subtype,date,frequency

if (isset($_GET['norm'])){
	$token = str_replace(",",'|%" OR norm LIKE "%|',$_GET['norm']);
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT * FROM tokenlemmanormtypesubtypedatefrequency';
	(isset($_GET['exact'])) ? $query .= ' WHERE norm = "|'.$token.'|"' : $query .= ' WHERE norm LIKE "%|'.$token.'|%"';
	(isset($_GET['sort'])) ? $query .= ' ORDER BY date ASC' : NULL;
	
	$tab = "\t";
	$nl = "\n";
	$res = '';

	foreach($PDO->query($query.';') as $row){
		$res.=$row['norm'].$tab.$row['date'].$tab.$row['frequency'].$tab.$row['token'].$nl;
	}
	print($res);
}
?>
