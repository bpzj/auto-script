#!/bin/bash


src=/root
#/usr/local/bin/inotifywait -mrq --timefmt '%d/%m/%y %H:%M' --format '%T %w%f%e' -e modify,delete,create,attrib $src |  while read file
#do
#      /usr/bin/rsync -arzuq --delete --progress $src 192.168.136.128::www/
#      echo "  ${file} was rsynced" >>/tmp/rsync.log 2>&1
#done

inotifywait -mrq --timefmt '%d/%m/%y %H:%M' --format '%T %w%f%e' -e modify,create $src | while read file
do
      echo "  ${file} was rsynced" >> /root/demo.log 2>&1
done