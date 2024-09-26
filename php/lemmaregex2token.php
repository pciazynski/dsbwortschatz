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
	$query = 'SELECT DISTINCT (token), SUM(frequency) as sumfreq FROM tokenlemmanormtypesubtypedatefrequency WHERE lemma REGEXP "\|'.$_GET['lemma'].'\|" GROUP BY token';
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY sumfreq DESC';
	}
	
	$tab = "\t";
	$nl = "\n";
	
	$result = $PDO->query($query.";");
	foreach($result as $row){
		print($row['token'].$tab.$row['sumfreq'].$nl);
	}
}
?>
