# ファイル内容
ほとんど生のデータをパースしただけのデータをcsv形式にしたファイルが格納されています。
- 注意点: 
  - receiverの方のcsvファイルに`total_time`というカラムが作成されていますが、そこに`>=11.00`という値が格納されている行に関して、記録に残っているデータが11.00secを超えている場合は`total_time`よりも右側のセルに10.00-11.00以降のデータが格納されています。ただし`total_time`より右側のカラムに関しては秒数が大小の順に並んでいるわけではないので**要注意**です。
  - `total_time`のカラムに`>=11.00`という値が格納されているにもかかわらずそれより右側に値が格納されていない場合、ちょうど11.00secで記録が終了したことを表しています。

***
- `tc_`から始まるファイル: 制御下での測定
  - tcpの場合: `tc_tcp_${制御の種類}_${receiver or sender}.csv`
  - udpの場合: `tc_udp_${制御の種類}_${帯域幅}_${receiver or sender}.csv`
  - 制御の種類
    - bps: 帯域制御(50mbit)
    - delay: 遅延制御(50ms)
  - 帯域幅
    - hundred: 100Mbps
    - twoHundred: 200Mbps
- `tcp_`から始まるファイル: `tcp_${receiver or sender}.csv`
- `udp_`から始まるファイル: `udp_${帯域幅}_${receiver or sender}.csv`
  - 帯域幅
    - hundred: 100Mbps
    - twoHundred: 200Mbps
- `upperDown_`から始まるファイル: Reverse モードで測定
  - tcpの場合: `upperDown_tcp_${receiver or sender}.csv`
  - udpの場合: `upperDown_udp_${帯域幅}_${receiver or sender}.csv`
  - 帯域幅
    - hundred: 100Mbps
    - twoHundred: 200Mbps