# Docker の JSON ログを送信する

Docker の json ログを､さくらのクラウドのモニタリングスイートに送信するサンプルです｡

## otelcol 設定例

```yaml
--8<-- "logs-docker/otelcol-config.yaml"
```

## 実行

```sh
dotenv -f ../.env run docker compose up
```

## 実行結果

このようにログの内容を確認できます｡

![alt text](screenshot-20251218T114415@2x.png)
