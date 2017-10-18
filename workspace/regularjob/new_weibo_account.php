<?php
    /*定时执行脚本---微博账号
    */
    $h=fopen('/root/workspace/regularjob/my_cront_log','a');
    $text=date("Y-m-d H:i:s",time())."  微博账户爬虫  \r\n";
    fwrite($h,$text);
    fclose($h);
    include("/root/workspace/regularjob/connect_mysql.php");
    include('/root/workspace/regularjob/conf_li.php');
    $gc = new GearmanClient();
    $gc->addServer($conf_li['gearman_host'],$conf_li['gearman_port']);

    //爬取微博账号--账号来自于数据库
    $sql='select url from t_source_used where cate_id=6';
    #$sql='select weibo_id from t_source where cate_id=6';
    $res=mysqli_query($link,$sql);
    var_dump($res);
    while($row=mysqli_fetch_row($res)){
        $param = array('keyword'=>$row[0],'se'=>'weibocontent', 'pages'=>1);
        var_dump($param);
        $request = $gc->do('weibo_spider',json_encode($param));
    }


?>
