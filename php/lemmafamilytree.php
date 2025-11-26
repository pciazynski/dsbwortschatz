<?php
header('Content-Type: text/plain');

#token,lemma,norm,type,subtype,date,frequency

if (isset($_GET['lemma'])){
	$lemma = str_replace(",",'|%" OR lemma LIKE "%|',$_GET['lemma']);
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT token,min(date) as mindate,max(date) as maxdate,sum(frequency) as summe FROM tokenlemmatypesubtypedatefrequency';
	(isset($_GET['exact'])) ? $query .= ' WHERE lemma = "|'.$lemma.'|"' : $query .= ' WHERE lemma LIKE "%|'.$lemma.'|%"';
	$query.=' GROUP BY token';
	(isset($_GET['sort'])) ? $query .= ' ORDER BY mindate ASC' : NULL;
	$tab = "\t";
	$nl = "\n";
	$res = '';

	foreach($PDO->query($query.';') as $row){
		$res.=$row['token'].$tab.$row['mindate'].$tab.$row['maxdate'].$tab.$row['summe'].$nl;
	}
	print($res);
}
?>
