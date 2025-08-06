# monitoring-suite-otelcol-sample

さくらのクラウドのモニタリングスイートに [OpenTelemetry Collector（otelcol）](https://opentelemetry.io/docs/collector/) でログ･メトリクスを送信するため設定ファイルのサンプルです｡

## OpenTelemetry Collector（otelcol）とは？

OpenTelemetry Collector（通称 otelcol）は、様々な形式のメトリクスやログ、トレースデータを受け取り、変換・集約・エクスポートできるOSSのデータコレクターです。
クラウドやオンプレミス環境での監視・observability を実現するための中心的なコンポーネントです。

このリポジトリは、さくらのクラウドのモニタリングスイートと連携するための設定例や、テスト用のデータ送信スクリプトを含みます。

---

## 目次

- [monitoring-suite-otelcol-sample](#monitoring-suite-otelcol-sample)
  - [OpenTelemetry Collector（otelcol）とは？](#opentelemetry-collectorotelcolとは)
  - [目次](#目次)
  - [依存ツール](#依存ツール)
  - [セットアップ手順](#セットアップ手順)
    - [1. Docker で実行（推奨）](#1-docker-で実行推奨)
    - [2. ローカル実行（macOS/Linux, amd64/arm64 対応）](#2-ローカル実行macoslinux-amd64arm64-対応)
  - [サンプルスクリプトの使い方](#サンプルスクリプトの使い方)
    - [Dockerログのシミュレーター](#dockerログのシミュレーター)
    - [OTLPメトリクス送信スクリプト](#otlpメトリクス送信スクリプト)
  - [otelcolの設定例](#otelcolの設定例)
  - [LICENSE](#license)
  - [FAQ](#faq)
    - [Q. resourcedetection processor は使わないのですか？](#q-resourcedetection-processor-は使わないのですか)

---

## 依存ツール

- Make
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [uv](https://docs.astral.sh/uv/)（Pythonパッケージ管理・実行ツール）

## セットアップ手順

1. **`.env` ファイルの作成**

   認証情報を記載した `.env` ファイルをプロジェクトルートに設置してください。
   認証は Basic 認証方式です。header の値は以下のように生成します。

   例:
   ユーザー名: `m123456`
   パスワード: `12345678-1234-5678-9abc-123456789abc`

   ```sh
   echo -n "m123456:12345678-1234-5678-9abc-123456789abc" | base64
   # => bTEyMzQ1NjoxMjM0NTY3OC0xMjM0LTU2NzgtOWFiYy0xMjM0NTY3ODlhYmM=
   ```

   `.env` ファイル例:

   ```
   LOG_AUTH=bTEyMzQ1NjoxMjM0NTY3OC0xMjM0LTU2NzgtOWFiYy0xMjM0NTY3ODlhYmM=
   LOG_RESOURCE_ID=000000000000

   METRIC_AUTH=bTEyMzQ1NjoxMjM0NTY3OC0xMjM0LTU2NzgtOWFiYy0xMjM0NTY3ODlhYmM=
   METRIC_RESOURCE_ID=000000000000
   ```


otelcol-contrib の起動方法は2通りあります。どちらでも動作します。

2. **otelcol の実行方法（推奨: Docker, またはクロスプラットフォームスクリプト）**

otelcol-contrib の起動は Docker を推奨します。ローカル実行したい場合はクロスプラットフォーム対応の `otelcol-contrib-launcher.sh` を用意しています。

### 1. Docker で実行（推奨）

さくらのクラウドが提供するイメージ [ghcr.io/sacloud/sacloud-otel-collector](https://github.com/sacloud/sacloud-otel-collector) を使う場合:

```sh
docker run --rm \
  --env-file .env \
  -v $(pwd)/otelcol-config.yaml:/etc/otelcol-contrib/config.yaml \
  ghcr.io/sacloud/sacloud-otel-collector:v0.2.1
```

`.env` ファイルを `--env-file` で渡すことで、必要な認証情報などが環境変数としてコンテナ内に渡されます。

### 2. ローカル実行（macOS/Linux, amd64/arm64 対応）

`otelcol-contrib-launcher.sh` を使うと、OS/アーキテクチャに応じて自動でバイナリをダウンロードし、.env を読み込んで起動します。

```sh
./otelcol-contrib-launcher.sh
```

> Windows の場合は WSL2 など Linux 環境での利用を推奨します。

---

## サンプルスクリプトの使い方

### Dockerログのシミュレーター

Docker の JSON ログ形式でログファイルを自動生成するスクリプトです。
テスト用のログファイルを作りたい場合に利用できます。

```sh
python3 docker_log_simulator.py
```

### OTLPメトリクス送信スクリプト

OpenTelemetry Protocol (OTLP) でメトリクスを送信するサンプルスクリプトです。
otelcol へのメトリクス送信テストに利用できます。

```sh
./otlp_send_metrics.py --insecure --port=4319
```
（`--port` は otelcol 側の設定に合わせて変更してください）

---

## otelcolの設定例

otelcol の設定ファイル例は [otelcol-config.yaml](otelcol-config.yaml) を参照してください。

---

## LICENSE

See LICENSE file.

---

## FAQ

### Q. resourcedetection processor は使わないのですか？

A. 本サンプルでは resourcedetection processor は利用していません。
理由は、resourceprocessor で環境変数（例: `LOG_RESOURCE_ID` や `METRIC_RESOURCE_ID` など）を直接参照してリソース属性を付与できるためです。
resourcedetection processor を使わなくても、必要なリソース情報は環境変数経由で柔軟に設定できます。

```yaml
  # resourcedetection でホスト名などの基本的な attribute を追加可能｡
  # system と env を使うだけなら､'resource' を使うなら "${HOSTNAME}" などから拾っても良い｡
  # https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/README.md
  resourcedetection:
    detectors:
      # OTEL_RESOURCE_ATTRIBUTES 変数の値を attribute に展開します
      - env
      # os.type, host.name を付与してくれる｡
      # https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/internal/system/documentation.md
      # https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/README.md#system-metadata
      - system
    timeout: 2s
    override: false
```
