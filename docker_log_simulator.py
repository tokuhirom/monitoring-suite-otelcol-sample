#!/usr/bin/env python3
import json
import time
import random
from datetime import datetime, timezone
import uuid
from pathlib import Path

# ログメッセージ用の単語リスト
WORDS = [
    # アプリケーション関連
    "application",
    "server",
    "client",
    "database",
    "connection",
    "request",
    "response",
    "service",
    "api",
    "endpoint",
    "handler",
    "middleware",
    "controller",
    "model",
    # 動作関連
    "starting",
    "stopping",
    "processing",
    "connecting",
    "disconnecting",
    "loading",
    "saving",
    "updating",
    "creating",
    "deleting",
    "sending",
    "receiving",
    "parsing",
    # 状態関連
    "success",
    "failed",
    "error",
    "warning",
    "info",
    "debug",
    "completed",
    "timeout",
    "ready",
    "busy",
    "idle",
    "active",
    "inactive",
    "pending",
    "cancelled",
    # 技術用語
    "http",
    "https",
    "tcp",
    "ssl",
    "tls",
    "json",
    "xml",
    "yaml",
    "config",
    "cache",
    "session",
    "token",
    "auth",
    "login",
    "logout",
    "user",
    "admin",
    # 数値・識別子
    "id",
    "uuid",
    "hash",
    "key",
    "value",
    "count",
    "size",
    "length",
    "port",
    "version",
    "build",
    "release",
    "commit",
    "branch",
    "tag",
    # エラー関連
    "exception",
    "stack",
    "trace",
    "panic",
    "crash",
    "abort",
    "retry",
    "fallback",
    "circuit",
    "breaker",
    "health",
    "check",
    "monitor",
    "alert",
    "notification",
]

# ログレベル別のメッセージテンプレート
LOG_TEMPLATES = {
    "info": [
        "Server started on port {port}",
        "Processing request {id}",
        "Database connection established",
        "User {user} logged in successfully",
        "Cache hit for key {key}",
        "API endpoint {endpoint} called",
        "Configuration loaded from {file}",
        "Health check passed",
        "Session {session} created",
        "Background job {job} started",
    ],
    "warning": [
        "High memory usage detected: {percent}%",
        "Slow query detected: {time}ms",
        "Rate limit approaching for {ip}",
        "Cache miss for key {key}",
        "Retry attempt {attempt} for {operation}",
        "Connection pool nearly exhausted",
        "Disk space low: {space}GB remaining",
        "SSL certificate expires in {days} days",
        "Deprecated API endpoint {endpoint} used",
        "Queue size growing: {size} items",
    ],
    "error": [
        "Database connection failed: {error}",
        "Authentication failed for user {user}",
        "API request timeout after {timeout}s",
        "Failed to parse JSON: {error}",
        "Permission denied for {resource}",
        "Service {service} unavailable",
        "Out of memory error",
        "Network connection lost",
        "File not found: {file}",
        "Invalid configuration: {config}",
    ],
}


def generate_random_message():
    """ランダムなログメッセージを生成"""
    # 50% info, 30% warning, 20% error の比率
    level = random.choices(["info", "warning", "error"], weights=[50, 30, 20])[0]

    template = random.choice(LOG_TEMPLATES[level])

    # テンプレートの変数を置換
    replacements = {
        "port": random.randint(3000, 9999),
        "id": str(uuid.uuid4())[:8],
        "user": f"user{random.randint(1, 1000)}",
        "key": f"cache_key_{random.randint(1, 999)}",
        "endpoint": f"/api/v{random.randint(1, 3)}/{random.choice(['users', 'orders', 'products', 'auth'])}",
        "file": f"{random.choice(['config', 'settings', 'database'])}.{random.choice(['yaml', 'json', 'conf'])}",
        "session": str(uuid.uuid4())[:12],
        "job": f"job_{random.randint(1, 100)}",
        "percent": random.randint(70, 95),
        "time": random.randint(1000, 5000),
        "ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "attempt": random.randint(1, 5),
        "operation": random.choice(
            ["database_query", "api_call", "file_write", "cache_update"]
        ),
        "space": random.randint(1, 10),
        "days": random.randint(1, 30),
        "size": random.randint(100, 1000),
        "error": random.choice(
            [
                "connection_refused",
                "timeout",
                "invalid_credentials",
                "permission_denied",
            ]
        ),
        "timeout": random.randint(5, 30),
        "resource": f"/{random.choice(['admin', 'api', 'data'])}/{random.choice(['users', 'files', 'config'])}",
        "service": random.choice(
            ["database", "cache", "auth", "notification", "payment"]
        ),
        "config": random.choice(["database.url", "api.key", "ssl.cert", "cache.size"]),
    }

    try:
        message = template.format(**replacements)
    except KeyError:
        # フォーマットに失敗した場合は単語をランダムに組み合わせ
        message = generate_word_based_message()

    return f"[{level.upper()}] {message}"


def generate_word_based_message():
    """単語ベースのランダムメッセージを生成"""
    num_words = random.randint(1, 5)
    words = random.sample(WORDS, min(num_words, len(WORDS)))
    return " ".join(words)


def generate_docker_log_entry():
    """Docker JSON ログエントリを生成"""
    # stdout または stderr をランダムに選択
    stream = random.choice(["stdout", "stderr"])

    # メッセージを生成（改行文字付き）
    message = generate_random_message() + "\n"

    # 現在時刻をISO形式で取得
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    return {"log": message, "stream": stream, "time": timestamp}


def main():
    # コンテナIDを生成（実際のDockerコンテナIDっぽく）
    container_id = "".join(random.choices("0123456789abcdef", k=64))

    # ログディレクトリを作成（mkdir -p 相当）
    log_dir = Path("logs/containers") / container_id
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file_path = log_dir / f"{container_id}-json.log"

    print(f"Created directory: {log_dir}")
    print(f"Writing Docker JSON logs to: {log_file_path}")
    print("Press Ctrl+C to stop...")

    try:
        with open(log_file_path, "w") as log_file:
            while True:
                # ログエントリを生成
                log_entry = generate_docker_log_entry()

                # JSON形式で書き込み
                json_line = json.dumps(log_entry, separators=(",", ":"))
                log_file.write(json_line + "\n")
                log_file.flush()  # すぐにファイルに書き込み

                # コンソールにも表示
                print(f"[{log_entry['stream']}] {log_entry['log'].strip()}")

                # 1秒待機
                time.sleep(1)

    except KeyboardInterrupt:
        print(f"\nStopped. Log file saved to: {log_file_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
