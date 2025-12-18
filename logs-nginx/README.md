# logs-nginx

nginx のアクセスログを､さくらのクラウドのモニタリングスイートに送信するサンプルです｡

## 実行

このディレクトリの `Dockerfile` から nginx イメージがビルドされます。

```sh
dotenv -f ../.env run docker compose up --build
```

## 実行結果

このようにログの内容を確認できます｡

![alt text](screenshot-20251218T182830@2x.png)
