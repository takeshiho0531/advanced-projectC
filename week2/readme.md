# week2
応用プロジェクト3A1のweek2の結果が格納されてるフォルダです。

## フォルダ構成
```
.
├── fiveG: Local5Gの場合
│   ├── tc
│   │   ├── tcp
│   │   │   ├── bps
│   │   │   └── delay
│   │   └── udp
│   │       ├── hundred
│   │       │   ├── bps
│   │       │   └── delay
│   │       └── twoHundred
│   │           └── bps
│   ├── tcp
│   ├── udp
│   │   ├── hundred
│   │   └── twoHundred
│   └── upperDown
│       ├── tcp
│       └── udp
│           ├── hundred
│           └── twoHundred
└── wifi
    ├── tc
    │   ├── tcp
    │   │   └── bps
    │   └── udp
    │       ├── hundred
    │       │   └── bps
    │       └── twoHundred
    │           └── bps
    ├── tcp
    ├── udp
    │   ├── hundred
    │   └── twoHundred
    └── upperDown
        ├── tcp
        └── udp
            ├── hundred
            └── twoHundred
```
- 各フォルダに入ってるshell scriptが書かれたファイルの中のコマンドを見てもらうのが一番確かです。
- 結果は全てテキストファイルに格納されています。`iperf_result_`以下はtimestamp(実行した時刻)になってます
- 帯域/遅延制御下で汚染されてしまったファイルが`tc/`以外に含まれてしまっている可能性があります...(最悪timestamp的に判断できる)
***

- `ping.txt`: `ping 192.168.110.6` の実行結果
- `pingRTT.txt`: `ping 192.168.110.6 -c 15` の実行結果
- `traceroute.txt`: `traceroute 192.168.110.6` の実行結果

- `tc/`: それ以下のファイル・フォルダはtcコマンド関連
  - `bps/` は次の帯域制御下で行った;
  `sudo tc qdisc add dev eth0 root handle 10:0 tbf rate 50mbit burst 200kb limit 2000kb`
  - `delay`　は次の遅延制御下で行った;
  `sudo tc qdisc add dev eth0 root handle 1:0 netem delay 50ms`
  - `tcp/`
    - `bps/`: `iperf3 -c 192.168.110.6 -p 5207 --get-server-output` の実行結果 (port番号は必ずしも一致しない)
    - `delay/`: `iperf3 -c 192.168.110.6 -p 5207 --get-server-output` の実行結果 (port番号は必ずしも一致しない)
  - `udp/`:
    - -b 200Mは帯域制御のみ行った
    - `hundred/`
      - `bps/`: `iperf3 -c 192.168.110.6 -p 5209 -u -b 100M  --get-server-output` の実行結果 (port番号は必ずしも一致しない)
      - `delay/`: `iperf3 -c 192.168.110.6 -p 5209 -u -b 100M  --get-server-output` の実行結果 (port番号は必ずしも一致しない)
    - `twoHundred/`
      - `bps/`: `iperf3 -c 192.168.110.6 -p 5201 -u -b 200M  --get-server-output` の実行結果 (port番号は必ずしも一致しない)

- `tcp/`: `iperf3 -c 192.168.110.6 -p 5205 --get-server-output` の実行結果 (port番号は必ずしも一致しない)

- `udp/`
  - `hundred/`: `iperf3 -c 192.168.110.6 -p 5204 -u -b 100M  --get-server-output` の実行結果 (port番号は必ずしも一致しない)
  - `twoHundred/`: `iperf3 -c 192.168.110.6 -p 5210 -u -b 200M  --get-server-output` の実行結果 (port番号は必ずしも一致しない)

- `upperDown/`: iperf3の-Rオプション
  - `tcp/`: `iperf3 -c 192.168.110.6 -p 5209 -R --get-server-output` の実行結果 (port番号は必ずしも一致しない)
  - `udp/`
    - `hundred/`: `iperf3 -c 192.168.110.6 -p 5203 -u -b 100M -R  --get-server-output` の実行結果 (port番号は必ずしも一致しない)
    - `twoHundred/`: `iperf3 -c 192.168.110.6 -p 5202 -u -b 200M -R  --get-server-output` の実行結果 (port番号は必ずしも一致しない)
