<?php
header('Content-Type: text/plain');

#token,lemma,norm,type,subtype,date,frequency
$token = str_replace(",",'" OR lemma LIKE "%|',$_GET['lemma']);

if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db?mode=ro');
	$query = 'SELECT * FROM tokenlemmanormtypesubtypedatefrequency';
	(isset($_GET['exact'])) ? $query .= ' WHERE lemma = "|'.$token.'|"' : $query .= ' WHERE lemma LIKE "%|'.$token.'|%"';
	(isset($_GET['sort'])) ? $query .= ' ORDER BY date ASC' : NULL;
	
	$tab = "\t";
	$nl = "\n";
	$res = '';

	foreach($PDO->query($query.';') as $row){
		$res.=$row['lemma'].$tab.$row['date'].$tab.$row['frequency'].$tab.$row['token'].$nl;
	}
	print($res);
}
?>
