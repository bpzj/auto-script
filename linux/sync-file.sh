#!/usr/bin/env bash

last=`stat /root/sync/ |grep Modify`
while [[ "" == "" ]]; do
  modify=`stat /root/sync/ |grep Modify`
  if [[ "$modify" == "$last" ]]; then
    echo "same"
  else
    echo "not same"
    echo "should do something"
    last=$modify
  fi

  sleep 5
done
