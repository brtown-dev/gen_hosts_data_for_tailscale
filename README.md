## Hostsファイル用 Tailscaleホストデータ出力用スクリプト

### 何をしている?

1. まず、"tailscale status"でネットワーク上のtailscaleホスト一覧を抽出。
2. 抽出したリストに記載のホストのIP Addressを"tailscale whois"で問い合わせし、サブネットルーターのsite-idを特定
3. "tailscale debug"でそのsite-idに所属する特定のローカルIPアドレス(10.0.64.108等)のtailscale ipv6アドレスを抽出。
4. 抽出したtailscale ipv6アドレスとホスト名をhostsファイルのフォーマットに合わせて表示

例外1: JP010-2(10.0.65.108)は出力しません。tailscale debugコマンドで情報抽出し、手動でhostsに追加してください。
例外2: JP043は、Tailscaleネットワークを切り替えて出力してください。

### 使い方
```
usage: gen_hosts.py [-h] [-s HOSTNAME_SUFFIX] [-u TARGET_USER] [-i TARGET_IP]

options:
  -h, --help            show this help message and exit
  -s HOSTNAME_SUFFIX, --suffix HOSTNAME_SUFFIX
  -u TARGET_USER, --user TARGET_USER
  -i TARGET_IP, --ip TARGET_IP
```

Option無しで実行すると、今接続しているTailscaleネットワークに所属するホストの内、「os-node@」でログインしているホスト(jpxxx-via-x)が所属しているネットワークの「10.0.64.108/24」のホストのipV6アドレスを表示。ホスト名は「jpxxx-via-x」から「-via-x」を除いた「jpxxx」で表示。
```
% python gen_hosts.py      
fd7a:115c:a1e0:b1a:0:1:a00:406c jp001
fd7a:115c:a1e0:b1a:0:5:a00:406c jp005
fd7a:115c:a1e0:b1a:0:6:a00:406c jp006
fd7a:115c:a1e0:b1a:0:7:a00:406c jp007
fd7a:115c:a1e0:b1a:0:8:a00:406c jp008
fd7a:115c:a1e0:b1a:0:9:a00:406c jp009
fd7a:115c:a1e0:b1a:0:a:a00:406c jp010-1
fd7a:115c:a1e0:b1a:0:b:a00:406c jp011
fd7a:115c:a1e0:b1a:0:c:a00:406c jp012
:
:
:
```

「全サイトの１号IPカメラ(10.0.64.151/24)でホスト名を「jpxxx-**camera1**」と表示したい場合は以下のようにスクリプトを実行。
```
% python gen_hosts.py  --ip 10.0.64.151/24 --suffix "camera1"
fd7a:115c:a1e0:b1a:0:1:a00:4097 jp001-camera1
fd7a:115c:a1e0:b1a:0:5:a00:4097 jp005-camera1
fd7a:115c:a1e0:b1a:0:6:a00:4097 jp006-camera1
fd7a:115c:a1e0:b1a:0:7:a00:4097 jp007-camera1
fd7a:115c:a1e0:b1a:0:8:a00:4097 jp008-camera1
fd7a:115c:a1e0:b1a:0:9:a00:4097 jp009-camera1
fd7a:115c:a1e0:b1a:0:a:a00:4097 jp010-1-camera1
fd7a:115c:a1e0:b1a:0:b:a00:4097 jp011-camera1
:
:
:
```
