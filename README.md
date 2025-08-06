# monitoring-suite-otelcol-sample

さくらのクラウドのモニタリングスイートを otelcol で動かすサンプルです｡

## Dependencies

 * Make
 * [python-dotenv](https://pypi.org/project/python-dotenv/)
 * [uv](https://docs.astral.sh/uv/)

## どうやって動かす

otelcol のダウンローダーが mac 前提になっていますが､それ以外の環境でも otelcol を手動でダウンロードすれば動きます｡

    make

と打てば動きます｡

ログファイルをシミュレートしたい場合､`python3 docker_log_simulator.py` として実行してください｡

## LICENSE

See LICENSE file.

