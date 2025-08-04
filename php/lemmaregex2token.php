<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	function _sqliteRegexp($pattern,$string) {
		(preg_match("/^".$pattern."$/", $string)) ? $hit = true : $hit =  false;
		return $hit;
	}
	$PDO->sqliteCreateFunction('regexp', '_sqliteRegexp', 2);
	$query = 'SELECT lemma, token, SUM(frequency) as sumfreq FROM tokenlemmanormtypesubtypedatefrequency WHERE lemma REGEXP "\|'.$_GET['lemma'].'\|"  LIMIT 2100000';
	(isset($_GET['year'])) ? $query .= ' AND date '.$_GET['year'] : NULL;
	$query.=' GROUP BY token,lemma';
	(isset($_GET['sort'])) ? $query .= ' ORDER BY sumfreq DESC' : NULL;
	$tab = "\t";
	$nl = "\n";
	$res = '';

	foreach($PDO->query($query.";") as $row){
		$res.=$row['lemma'].$tab.$row['token'].$tab.$row['sumfreq'].$nl;
	}
	print($res);
}
?>
