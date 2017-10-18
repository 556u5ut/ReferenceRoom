<?php
	//链接数据库
    include("/root/workspace/regularjob/conf_li.php");
	$link = mysqli_connect($conf_li['mysql_host'],$conf_li['mysql_user'],$conf_li['mysql_pass'],$conf_li['mysql_db']) or die("Error " . mysqli_error($link)); 
	$link -> query('set names utf8');
