<?php 
$ip = $_SERVER['REMOTE_ADDR'];
$now = date('Y.m.d, H:i');
$agent = $_SERVER['HTTP_USER_AGENT'];
$file = $_SERVER['SCRIPT_NAME'];
$dsn = "sqlite:data/data.sqlite3";
$conn = new PDO ($dsn);
$abfrage = $conn->query('select * from logs order by id desc;');
$current_state = $abfrage->fetch();
$new_id = (int)$current_state['id'];
$new_id = $new_id + 1;
$conn->exec('insert into logs(id,date,file,ip,agent) values('.$new_id.',"'.$now.'","'.$file.'","'.$ip.'","'.$agent.'");');
?>
