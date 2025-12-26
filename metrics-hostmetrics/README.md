# ホストメトリクスを送信する

モニタリングスイートにホストメトリクスを送信するサンプルです｡

## otelcol 設定例

今回はサンプルなので､docker container の中の procfs を見た結果を送信していますが､実際にはホスト側の `/proc` をマウントして実装する必要があります｡

```yaml
--8<-- "metrics-hostmetrics/otelcol-config.yaml"
```

## 実行方法

```sh
dotenv -f ../.env run docker compose up
```

## 出力例

otelcol の hostmetrics で取得されたデータが送信されます｡

![alt text](screenshot-20251218T102821@2x.png)
