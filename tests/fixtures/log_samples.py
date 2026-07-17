@@ -0,0 +1,15 @@
+# Hand-written representative log lines for independent parser fixtures
+json_log_line = '{"timestamp": "2023-10-01T12:00:00Z", "level": "INFO", "service": "app", "message": "User logged in"}'
+text_log_line = '2023-10-01 12:00:00 INFO [app] User logged in'
+nginx_log_line = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
+malformed_log_line = 'This is not a valid log line'

--- a/tests/test_log_parser.py