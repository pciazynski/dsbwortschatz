<?php
header('Content-Type: text/plain');

(isset($_GET['n']))?$n=$_GET['n']:$n=3;

$query = 'SELECT token,docurn,urn,year,structureelement FROM tokenurnyearpassagestructureelement WHERE TRUE';
(isset($_GET['token']))?$query.=' AND token="'.$_GET['token'].'"':NULL;
if(isset($_GET['urn'])){
	$urn=$_GET['urn'];
	(str_ends_with($urn,":"))?NULL:$urn.=".";
	$query.=' AND urn LIKE "'.$_GET['urn'].'%"';
}
(isset($_GET['year']))?$query.=' AND year'.$_GET['year']:NULL;
(isset($_GET['structureelement']))?$query.=' AND structureelement="'.$_GET['structureelement'].'"':NULL;

$nl = "\n";
$tab = "\t";
$res = '';

$PDO = new PDO('sqlite:../data/langDeu'.$n.'.db');
foreach($PDO->query($query.';') as $row){
	$res.=$row['token'].$tab.$row['docurn'].$tab.$row['urn'].$tab.$row['year'].$tab.$row['structureelement'].$nl;
}

print($res);
?>
