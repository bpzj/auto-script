#!/usr/bin/env bash

modify=`stat /root/sync/ |grep Modify`
while [[ "$modify" == "" ]]; do

done