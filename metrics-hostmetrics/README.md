# metrics-samples

メトリクスを送信するサンプルです｡hostmetrics で送信します｡

## otelcol の起動方法（デモ用）

このディレクトリの `docker-compose.yml` は、さくらのクラウドの OpenTelemetry Collector イメージを使い、`otelcol-config.yaml` をマウントして起動します。

環境変数は以下のように取得してください｡

![alt text](../metrics-settings.png)

必要な環境変数は外部から渡してください。

```
export SAKURA_MONITORINGSUITE_METRICS_ENDPOINT=...   # 監視スイートのエンドポイントのホスト名
export SAKURA_MONITORINGSUITE_METRICS_CREDENTIALS=...   # 認証情報
docker compose up -d
```

## 出力例

otelcol の hostmetrics で取得されたデータが送信されます｡

![alt text](screenshot-20251218T102821@2x.png)
