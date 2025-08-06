# monitoring-suite-otelcol-sample

さくらのクラウドのモニタリングスイートを otelcol で動かすサンプルです｡

[otelcol-config.yaml](otelcol-config.yaml) を見てください｡

## Dependencies

 * Make
 * [python-dotenv](https://pypi.org/project/python-dotenv/)
 * [uv](https://docs.astral.sh/uv/)

## どうやって動かす

`.env` ファイルを設置してください｡

認証のための情報です｡basicauth なので､以下のようにして header の値を生成する必要があります｡｡

例えば､username: `m123456`, password: `12345678-1234-5678-9abc-123456789abc` の場合は以下のようにします｡

    $ echo -n "m123456:12345678-1234-5678-9abc-123456789abc" | base64
    bTEyMzQ1NjoxMjM0NTY3OC0xMjM0LTU2NzgtOWFiYy0xMjM0NTY3ODlhYmM=

.env ファイルは以下のようになります｡

```
LOG_AUTH=bTEyMzQ1NjoxMjM0NTY3OC0xMjM0LTU2NzgtOWFiYy0xMjM0NTY3ODlhYmM=
LOG_RESOURCE_ID=000000000000

METRIC_AUTH=bTEyMzQ1NjoxMjM0NTY3OC0xMjM0LTU2NzgtOWFiYy0xMjM0NTY3ODlhYmM=
METRIC_RESOURCE_ID=000000000000
```


otelcol のダウンローダーが mac 前提になっていますが､それ以外の環境でも otelcol を手動でダウンロードすれば動きます｡

    make

と打てば動きます｡

docker の json ログ形式でログを生成するスクリプトを同梱しています｡
ログファイルをシミュレートしたい場合､`python3 docker_log_simulator.py` として実行してください｡

メトリクスを otlp で送信するスクリプトを同梱しています｡
`./otlp_send_metrics.py --insecure --port=4319` などとして実行してください｡

## LICENSE

See LICENSE file.

