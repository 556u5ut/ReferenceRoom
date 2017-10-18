<?php
    /*定时执行脚本---突发事件相关信息
    */
    $h=fopen('/root/workspace/regularjob/my_cront_log','a');
    $text=date("Y-m-d H:i:s",time())."  微博搜索爬虫  \r\n";
    fwrite($h,$text);
    fclose($h);
    include("/root/workspace/regularjob/connect_mysql.php");
    include('/root/workspace/regularjob/conf_li.php');
    $gc = new GearmanClient();
    $gc->addServer($conf_li['gearman_host'],$conf_li['gearman_port']);

    $sql="SELECT keyword FROM cnpc_geo_ps_dev.key_words where type=0;";
    $res=mysqli_query($link,$sql);
    while($row=mysqli_fetch_array($res)){
        $keyword=$row[0];
        var_dump($keyword);
        //元数据爬取
        #$param = array('keyword'=>$keyword,'se'=>'baidu','pages'=>5,'sleep'=>5);
        #$request = $gc->do('keyword_spider',json_encode($param));

        //微博搜索
        $param = array('keyword'=>$keyword,'se'=>'weibosearch','pages'=>1,'sleep'=>5);
        $request = $gc->do('weibo_spider',json_encode($param));

        //论坛爬取
        #$param = array('keyword'=>$keyword,'se'=>'','pages'=>5,'sleep'=>5);//{'msg':'www.ttlsa.com', 'sleep':5}
        #$request = $gc->do('bbs_spider',json_encode($param));

        //博客爬取
        #$param = array('keyword'=>$keyword,'se'=>'sogoublog','pages'=>5,'sleep'=>5);//
        #$request = $gc->do('blog_spider',json_encode($param));
    }
?>
