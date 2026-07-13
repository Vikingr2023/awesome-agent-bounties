@@ -1,5 +1,10 @@
 import pytest
 
 from tools.log_aggregator import LogAggregator
 
 
+@pytest.fixture
def json_log_fixture():
-    return "{\"timestamp\": \"2023-10-27T10:00:00Z\", \"level\": \"INFO\", \"message\": \"User logged in\"}"
+
+@pytest.fixture
def plain_text_log_fixture():
+    return "2023-10-27 10:00:00 INFO User logged in"
+
+@pytest.fixture
def nginx_log_fixture():
+    return '192.168.1.1 - - [27/Oct/2023:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"'
+
+@pytest.fixture
def malformed_log_fixture():
+    return "this is not a log line"
+
 
def test_log_aggregator_json_parsing(tmp_path):
     aggregator = LogAggregator(tmp_path)
     log_data = json_log_fixture()
@@ -10,3 +15,15 @@
     aggregator.process_log_line(log_data)
     assert aggregator.logs[0]['message'] == 'User logged in'
 
+def test_log_aggregator_plain_text_parsing(tmp_path):
+    aggregator = LogAggregator(tmp_path)
+    log_data = plain_text_log_fixture()
+    aggregator.process_log_line(log_data)
+    assert aggregator.logs[0]['message'] == 'User logged in'
+
+def test_log_aggregator_nginx_parsing(tmp_path):
+    aggregator = LogAggregator(tmp_path)
+    log_data = nginx_log_fixture()
+    aggregator.process_log_line(log_data)
+    assert aggregator.logs[0]['service'] == 'nginx'
+
+def test_log_aggregator_malformed_line(tmp_path):
+    aggregator = LogAggregator(tmp_path)
+    log_data = malformed_log_fixture()
+    aggregator.process_log_line(log_data)
+    assert len(aggregator.logs) == 0
