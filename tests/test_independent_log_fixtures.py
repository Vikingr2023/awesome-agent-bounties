import unittest
import json
import re
from datetime import datetime
from tools.log_aggregator import parse_log_line

class TestIndependentLogFixtures(unittest.TestCase):
    def test_json_log_line(self):
        # Independent JSON log line fixture (hand-written)
        line = '{"timestamp": "2026-07-25T12:34:56Z", "level": "INFO", "service": "auth", "message": "User login successful", "user_id": 12345}'
        result = parse_log_line(line)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("level"), "INFO")
        self.assertEqual(result.get("service"), "auth")
        self.assertEqual(result.get("message"), "User login successful")
        self.assertEqual(result.get("user_id"), 12345)
        # Timestamp parse check (ISO 8601)
        self.assertTrue(re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", result.get("timestamp", "")))

    def test_plain_text_log_line(self):
        # Independent plain text log line fixture (hand-written)
        line = "2026-07-25 12:34:56,789 [ERROR] [payment] Payment failed: insufficient funds"
        result = parse_log_line(line)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("level"), "ERROR")
        self.assertEqual(result.get("service"), "payment")
        self.assertTrue(result.get("message").startswith("Payment failed"))
        # Timestamp parse check (YYYY-MM-DD HH:MM:SS,ms)
        self.assertTrue(re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}", result.get("timestamp", "")))

    def test_nginx_log_line(self):
        # Independent nginx-style log line fixture (hand-written)
        line = '127.0.0.1 - - [25/Jul/2026:12:34:56 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"'
        result = parse_log_line(line)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("format"), "nginx")
        self.assertEqual(result.get("status"), 200)
        self.assertEqual(result.get("method"), "GET")
        self.assertEqual(result.get("path"), "/index.html")
        # Timestamp parse check (Apache log format)
        self.assertTrue(re.match(r"\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4}", result.get("timestamp", "")))

    def test_malformed_log_line(self):
        # Malformed log line that should not crash parsing
        line = "this is not a valid log line"
        result = parse_log_line(line)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
