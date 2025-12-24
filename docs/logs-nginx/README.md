# nginx のログを送信する

nginx のアクセスログを､さくらのクラウドのモニタリングスイートに送信するサンプルです｡

## nginx の設定

`log_format` の設定を行い､JSON 形式でログを出力することにより､モニタリングスイートで扱いやすくすることが出来ます｡`http_` prefix の項目名は､モニタリングスイートで予約されている名前であり､マニュアルの [ログの構造化](https://manual.sakura.ad.jp/cloud/appliance/monitoring-suite/about.html#monitoring-suite-log-structure) セクションにまとまっています｡

```
--8<-- "logs-nginx/nginx.conf"
```

## otelcol の設定

```yaml
--8<-- "logs-nginx/otelcol-config.yaml"
```

## 実行

このディレクトリの `Dockerfile` から nginx イメージがビルドされます。

```sh
dotenv -f ../.env run docker compose up --build
```

## 実行結果

このようにログの内容を確認できます｡

![alt text](screenshot-20251218T182830@2x.png)
