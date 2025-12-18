# metrics-otlp

OTLP 経由で取得したメトリクスを送信するサンプルです｡

## 実行方法

環境変数は以下のように取得してください｡

![alt text](../metrics-settings.png)

必要な環境変数は外部から渡してください。

```
export SAKURA_MONITORINGSUITE_METRICS_ENDPOINT=...   # 監視スイートのエンドポイントのホスト名
export SAKURA_MONITORINGSUITE_METRICS_CREDENTIALS=...   # 認証情報
docker compose up -d
```

## 出力例

python script からおくった `heartbeat` メトリクスが保存されています｡

![alt text](metrics-otlp-output.png)
