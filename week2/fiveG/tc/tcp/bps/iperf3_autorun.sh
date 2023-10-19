#!/bin/bash

# スクリプトを100回実行するループ
for ((i=1; i<=100; i++)); do
  timestamp=$(date +"%Y%m%d%H%M%S")
  result_file="iperf3_result_${timestamp}.txt"
  iperf3 -c 192.168.110.6 -p 5207 --get-server-output > "$result_file"
done

