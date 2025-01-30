<?php
header('Content-Type: text/plain');

#token,lemma,norm,type,subtype,date,frequency
$token = $_GET['lemma'];


if (isset($_GET['lemma'])){
	function _sqliteRegexp($pattern,$string) {
		if(preg_match("/^".$pattern."$/", $string)) {
			return true;
		}
		return false;
	}
	$PDO = new PDO('sqlite:../data/lemmamapping.db');
	$query = 'SELECT * FROM tokenlemmanormtypesubtypedatefrequency WHERE lemma REGEXP "\|'.$token.'\|"';

	$PDO->sqliteCreateFunction('regexp', '_sqliteRegexp', 2);
	$result = $PDO->query($query.";");

	$tab = "\t";
	$nl = "\n";
	foreach($result as $row){
		print($row['lemma'].$tab.$row['date'].$tab.$row['frequency'].$tab.$row['token'].$nl);
	}
}



?>
