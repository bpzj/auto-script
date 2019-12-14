#!/usr/bin/env bash

last=""
while [[ "" == "" ]]; do
  modify=`stat /root/sync/ |grep Modify`
  if [[ "$modify" == "$last" ]]; then
    echo "same"
  else
    echo "not same"
    last=$modify
  fi

  sleep 5
done