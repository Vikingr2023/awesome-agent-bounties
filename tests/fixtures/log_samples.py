@@ -0,0 +1,10 @@
+# Hand-written representative log lines for independent parser fixtures
+json_log_line = '{"timestamp": "2023-10-01T12:00:00Z", "level": "INFO", "service": "app", "message": "User logged in"}'
+text_log_line = "2023-10-01 12:00:00 INFO [app] User logged in"
+nginx_log_line = '127.0.0.1 - - [01/Oct/2023:12:00:00 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0"'
+malformed_log_line = 'This is not a valid log line'

--- a/tests/test_log_parser.py