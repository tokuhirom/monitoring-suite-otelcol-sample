# metrics-otlp

OTLP 経由で取得したメトリクスを送信するサンプルです｡

## 実行方法

```sh
dotenv -f ../.env run docker compose up
```

## 出力例

python script からおくった `heartbeat` メトリクスが保存されています｡

![alt text](metrics-otlp-output.png)
