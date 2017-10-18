#!/bin/sh
a=`free -g | grep Mem | awk -F" " {'print $4'}`
b=`ps aux | grep  scrapyd.runner | grep -v grep |  wc -l`

if [ $a -gt 10 ] && [ $b -lt 130 ] 
then 
   echo `date`." healthy free".$a." running".$b 
else
   echo `date`." badly free".$a."  runing".$b
   /usr/bin/python /root/seCrawler/test.py
fi
