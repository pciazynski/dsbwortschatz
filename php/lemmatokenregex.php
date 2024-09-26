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

	$query = 'SELECT token, lemma, frequency FROM lemmatokenfrequency';
	$query .= ' WHERE lemma REGEXP "\|'.$_GET['lemma'].'\|"';
	if (isset($_GET['sort'])){
		$query .= ' ORDER BY frequency DESC';
	}
	$result = $PDO->query($query.";");
	
	$tab = "\t";
	$nl = "\n";
	
	foreach($result as $row){
		print($row['lemma'].$tab.$row['token'].$tab.$row['frequency'].$nl);
	}
}
?>
