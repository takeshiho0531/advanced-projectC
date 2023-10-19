#!/bin/bash

# スクリプトを100回実行するループ
for ((i=1; i<=100; i++)); do
  timestamp=$(date +"%Y%m%d%H%M%S")
  result_file="iperf3_result_${timestamp}.txt"
  iperf3 -c 192.168.0.54 -p 5208 -u -b 200M -R  --get-server-output > "$result_file"
done


