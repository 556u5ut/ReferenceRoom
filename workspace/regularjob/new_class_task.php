<?php
    /*定时执行脚本---论坛
    */
    include('/root/workspace/regularjob/conf_li.php');
    $h=fopen('/root/workspace/regularjob/my_cront_log','a');
    $text=date("Y-m-d H:i:s",time())."  class爬虫  \r\n";
    fwrite($h,$text);
    fclose($h);

    $gc = new GearmanClient();
    $gc->addServer($conf_li['gearman_host'],$conf_li['gearman_port']);

    $request = $gc->do('class_spider',json_encode(''));

?>