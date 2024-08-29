## Hostsファイル用 Tailscaleホストデータ出力用スクリプト

### 何をしている?

1. まず、"tailscale status"でネットワーク上のtailscaleホスト一覧を抽出。
2. 抽出したリストに記載のホストのIP Addressを"tailscale whois"で問い合わせし、サブネットルーターのsite-idを特定
3. "tailscale debug"でそのsite-idに所属する特定のローカルIPアドレス(10.0.64.108等)のtailscale ipv6アドレスを抽出。
4. 抽出したtailscale ipv6アドレスとホスト名をhostsファイルのフォーマットに合わせて表示

