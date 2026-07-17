@@ -1,6 +1,11 @@
 from tools.log_aggregator import parse_log_line
+from tests.fixtures.log_samples import (
+    json_log_line,
+    text_log_line,
+    nginx_log_line,
+    malformed_log_line,
+)

-def test_parser():
-    # Existing tests using parser-generated samples
-    pass
+def test_parser_fixtures():
+    assert parse_log_line(json_log_line) == {
+        "timestamp": "2023-10-01T12:00:00Z", "level": "INFO", "service": "app", "message": "User logged in"
+    }
+    assert parse_log_line(text_log_line) == {
+        "timestamp": "2023-10-01 12:00:00", "level": "INFO", "service": "app", "message": "User logged in"
+    }
+    assert parse_log_line(nginx_log_line) == {
+        "timestamp": "01/Oct/2023:12:00:00 +0000", "request": "GET / HTTP/1.1", "status": "200", "size": "612", "referrer": "-", "user_agent": "Mozilla/5.0"
+    }
+    assert parse_log_line(malformed_log_line) is None
```

These changes add independent fixtures for JSON, plain text, and nginx-style log lines and include tests to verify parser output. The malformed log line ensures the parser handles unsupported input gracefully.