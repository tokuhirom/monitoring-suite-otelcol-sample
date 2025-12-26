# ｢さくらのクラウドのモニタリングスイートにotelcolで送信する本｣のサンプルコード集

[さくらのクラウドのモニタリングスイートにotelcolで送信する本](https://zenn.dev/tokuhirom/books/7c2c7820b2c36c) のサンプルコードです｡

## 依存ツール

- docker-compose
- dotenv

## セットアップ手順

### `.env` ファイルの作成

.env を設定します｡

メトリクスの設定情報は以下のように取得してください｡

![alt text](images/metrics-settings.png)

ログの設定情報は以下のように取得してください｡

![alt text](images/logs-settings.png)

ファイルの中身は以下のように記述します｡

```ini
SAKURA_MONITORINGSUITE_METRICS_ENDPOINT=https://***.metrics.monitoring.global.api.sacloud.jp/prometheus
SAKURA_MONITORINGSUITE_METRICS_CREDENTIALS=met-***-***

SAKURA_MONITORINGSUITE_LOGS_ENDPOINT=***.logs.monitoring.global.api.sacloud.jp
SAKURA_MONITORINGSUITE_LOGS_CREDENTIALS=log-***-***
```

## 実装済みのサンプル

現在､以下のようなサンプルコードが設置されています｡

- metrics-hostmetrics: hostmetrics を送信する例
- metrics-otlp: OTLP で受信したメトリクスを送信する例
- logs-docker: Docker のログを転送する例
- logs-nginx: nginx のログを転送する例

## LICENSE

See LICENSE file.
