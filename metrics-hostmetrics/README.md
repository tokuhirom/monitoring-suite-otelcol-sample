# metrics-samples

メトリクスを送信するサンプルです｡hostmetrics で送信します｡

## 実行方法

```sh
dotenv -f ../.env run docker compose up
```

## 出力例

otelcol の hostmetrics で取得されたデータが送信されます｡

![alt text](screenshot-20251218T102821@2x.png)

## テスト

Prometheus Remote Write で送信されるメトリクスをローカルで検証するためのテスト環境が用意されています｡

以下のコマンドを実行します｡

```sh
./test.sh
```

