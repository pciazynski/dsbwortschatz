<?php
header('Content-Type: text/plain');

(isset($_GET['n']))?$n=$_GET['n']:$n=3;

(isset($_GET['count']))?$count=$_GET['count']:$count='token';
(isset($_GET['groupBy']))?$groupBy=$_GET['groupBy']:$groupBy='year';

$query = 'SELECT COUNT('.$count.') as summe,'.$groupBy.' FROM tokenurnyearpassagestructureelement WHERE TRUE';
(isset($_GET['token']))?$query.=' AND token="'.$_GET['token'].'"':NULL;
if(isset($_GET['urn'])){
	$urn=$_GET['urn'];
	(str_ends_with($urn,":"))?NULL:$urn.=".";
	$query.=' AND urn LIKE "'.$_GET['urn'].'%"';
}
(isset($_GET['year']))?$query.=' AND year'.$_GET['year']:NULL;
(isset($_GET['structureelement']))?$query.=' AND structureelement="'.$_GET['structureelement'].'"':NULL;

$query.=' GROUP BY '.$groupBy.' ORDER BY '.$groupBy;

$nl = "\n";
$tab = "\t";
$res = '';


$PDO = new PDO('sqlite:../data/langDeu'.$n.'.db');
foreach($PDO->query($query.';') as $row){
	$res.=$row['summe'].$tab.$row[$groupBy].$nl;
}

print($res);
?>
