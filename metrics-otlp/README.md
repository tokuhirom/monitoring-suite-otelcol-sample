# OTLP で受信したメトリクスを送信する

OTLP を使ってメトリクスを送信するサンプルです｡

ユーザーが取得したメトリクスやサービスメトリクスなどを OTLP で送信する際にはこのサンプルのように実装すると良いでしょう｡

## コード例

以下のように設定します｡OTLP のポートで受信したメトリクスデータは､モニタリングスイートに送信されます｡

```yaml
--8<-- "metrics-otlp/otelcol-config.yaml"
```

## 実行方法

docs/metrics-otlp/ ディレクトリで､以下のようにして実行します｡

```sh
dotenv -f ../.env run docker compose up
```

## 出力例

python script からおくった `heartbeat` メトリクスが保存されています｡

![alt text](./metrics-otlp-output.png)
