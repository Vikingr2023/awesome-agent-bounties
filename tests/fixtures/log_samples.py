@@ -0,0 +1,15 @@
+import pytest
+
+# Independent fixtures for parser tests
+@pytest.fixture
+def json_log():
+    return '{"timestamp": "2023-10-01T12:00:00Z", "level": "INFO", "service": "api", "message": "User logged in"}'
+
+@pytest.fixture
+def text_log():
+    return "2023-10-01 12:00:00 INFO [api] User logged in"
+
+@pytest.fixture
+def nginx_log():
+    return '127.0.0.1 - - [01/Oct/2023:12:00:00 +0000] "GET /api/user HTTP/1.1" 200 1234'
+
+@pytest.fixture
+def malformed_log():
+    return 'This is not a valid log line'

--- a/tests/test_parser.py