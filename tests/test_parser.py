@@ -1,6 +1,13 @@
 import pytest
 from tools.log_aggregator import parse_log_line

+def test_json_parser(json_log):
+    result = parse_log_line(json_log)
+    assert result['timestamp'] == '2023-10-01T12:00:00Z'
+    assert result['level'] == 'INFO'
+    assert result['service'] == 'api'
+    assert 'message' in result
+
+def test_text_parser(text_log):
+    result = parse_log_line(text_log)
+    assert result['timestamp'] == '2023-10-01 12:00:00'
+    assert result['level'] == 'INFO'
+    assert result['service'] == 'api'
+    assert 'message' in result

 def test_nginx_parser(nginx_log):
     result = parse_log_line(nginx_log)
     assert result['timestamp'] == '01/Oct/2023:12:00:00 +0000'
     assert result['request'] == '"GET /api/user HTTP/1.1"'
     assert result['status'] == '200'
     assert result['bytes_sent'] == '1234'

+def test_malformed_log(malformed_log):
+    result = parse_log_line(malformed_log)
+    assert result is None
```

This patch adds independent fixtures for JSON, plain text, and nginx-style log lines, and includes tests to verify the parser output. It also adds a test for a malformed log line to ensure the parser does not crash.