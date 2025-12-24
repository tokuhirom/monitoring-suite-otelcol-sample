# Monitoring Suite otelcol Samples

さくらのクラウドのモニタリングスイートに [OpenTelemetry Collector（otelcol）](https://opentelemetry.io/docs/collector/) でログ･メトリクスを送信するため設定ファイルのサンプルです｡

## OpenTelemetry Collector（otelcol）とは？

OpenTelemetry Collector（通称 otelcol）は、様々な形式のメトリクスやログ、トレースデータを受け取り、変換・集約・エクスポートできるOSSのデータコレクターです。
クラウドやオンプレミス環境での監視・observability を実現するための中心的なコンポーネントです。

このリポジトリは、さくらのクラウドのモニタリングスイートと連携するための設定例や、テスト用のデータ送信スクリプトを含みます。

## 依存ツール

- docker-compose

## セットアップ手順

### `.env` ファイルの作成

.env を設定します｡

メトリクスの設定情報は以下のように取得してください｡

![alt text](metrics-settings.png)

ログの設定情報は以下のように取得してください｡

![alt text](logs-settings.png)

`.env` ファイルの中身は以下のように記述します｡

```ini
SAKURA_MONITORINGSUITE_METRICS_ENDPOINT=https://***.metrics.monitoring.global.api.sacloud.jp/prometheus
SAKURA_MONITORINGSUITE_METRICS_CREDENTIALS=met-***-***

SAKURA_MONITORINGSUITE_LOGS_ENDPOINT=***.logs.monitoring.global.api.sacloud.jp
SAKURA_MONITORINGSUITE_LOGS_CREDENTIALS=log-***-***
```
