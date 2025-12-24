# メモ

## otelcol 自体のデバッグログを出させる方法

以下のように書くと良い｡

```yaml
service:
  telemetry:
    logs:
      level: debug
```

