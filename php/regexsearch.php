<?php
header('Content-Type: text/plain');

if (isset($_GET['token'])){
	$token = $_GET['token'];
}

if (strlen($token)>=1){
	$query = 'SELECT DISTINCT * FROM tokendatecount WHERE token REGEXP "'.$token.'" LIMIT 1000';
	$PDO = new PDO('sqlite:../data/bagofwords.db');
	function _sqliteRegexp($pattern,$string) {
		if(preg_match("/^".$pattern."$/", $string)) {
			return true;
		}
		return false;
	}
	$PDO->sqliteCreateFunction('regexp', '_sqliteRegexp', 2);
	$result = $PDO->query($query.";");
	$tab = "\t";
	$nl = "\n";
	foreach($result as $row){
		print($row['token'].$tab.$row['date'].$tab.$row['frequency'].$nl);
	}
}
?>
