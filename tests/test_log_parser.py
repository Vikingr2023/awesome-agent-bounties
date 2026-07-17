@@ -1,6 +1,10 @@
 from tools.log_aggregator import parse_log_line
+from tests.fixtures.log_samples import (
+    json_log_line,
+    text_log_line,
+    nginx_log_line,
+    malformed_log_line
+)

-def test_parser():
-    # Existing tests using parser-generated samples
-    pass
+def test_parser_fixtures():
+    assert parse_log_line(json_log_line) == {'timestamp': '2023-10-01T12:00:00Z', 'level': 'INFO','service': 'app','message': 'User logged in'}
+    assert parse_log_line(text_log_line) == {'timestamp': '2023-10-01 12:00:00', 'level': 'INFO','service': 'app','message': 'User logged in'}
+    assert parse_log_line(nginx_log_line) == {'timestamp': '10/Oct/2000:13:55:36 -0700', 'level': None,'service': None,'message': '127.0.0.1 - frank "GET /apache_pb.gif HTTP/1.0" 200 2326'}
+    assert parse_log_line(malformed_log_line) is None
```

This patch adds independent fixtures for JSON, plain text, and nginx-style log lines and includes a test to verify parser output. It also includes a malformed log line to ensure the parser does not crash on unsupported input.