<?php
header('Content-Type: text/plain');

if (isset($_GET['lemma'])){
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	function _sqliteRegexp($pattern,$string) {
		if(preg_match("/^".$pattern."$/", $string)) {
			return true;
		}
		return false;
	}
	$PDO->sqliteCreateFunction('regexp', '_sqliteRegexp', 2);

	$query = 'SELECT lemma, sum(frequency) as sumfreq FROM tokenlemmanormtypesubtypedatefrequency WHERE lemma REGEXP "\|'.$_GET['lemma'].'\|" GROUP BY lemma ';

	(isset($_GET['sort'])) ? $query .= ' ORDER BY sumfreq DESC' : NULL;

	$tab = "\t";
	$nl = "\n";
	$res = '';

	$result = $PDO->query($query.";");
	foreach($result as $row){
		$res.=$row['lemma'].$tab.$row['sumfreq'].$nl;
	}
	print($res);
}
?>
