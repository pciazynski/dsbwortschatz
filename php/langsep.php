<?php
header('Content-Type: text/plain');

(isset($_GET['n']))?$n=$_GET['n']:$n=3;

(isset($_GET['groupBy']))?$query = 'SELECT '.$_GET['groupBy'].',SUM(frequency) as frequency FROM tokenurnyearpassagestructureelementfrequency WHERE TRUE':$query = 'SELECT token,docurn,urn,year,structureelement,frequency FROM tokenurnyearpassagestructureelementfrequency WHERE TRUE';
(isset($_GET['token']))?$query.=' AND token="'.$_GET['token'].'"':NULL;
if(isset($_GET['urn'])){
	$urn=$_GET['urn'];
	(str_ends_with($urn,":"))?NULL:$urn.=".";
	$query.=' AND urn LIKE "'.$_GET['urn'].'%"';
}
(isset($_GET['year']))?$query.=' AND year'.$_GET['year']:NULL;
(isset($_GET['structureelement']))?$query.=' AND structureelement="'.$_GET['structureelement'].'"':NULL;

(isset($_GET['groupBy']))?$query .=' GROUP BY '.$_GET['groupBy']:NULL;
$query .=' ORDER BY frequency DESC';

$nl = "\n";
$tab = "\t";
$res = '';

$PDO = new PDO('sqlite:../data/langDeu'.$n.'.db');
foreach($PDO->query($query.';') as $row){
	foreach(array_keys($row) as $key){
		(!is_int($key)) ? $res.=$row[$key].$tab:NULL;
	}
	$res = trim($res).$nl;
}

print($res);
?>
