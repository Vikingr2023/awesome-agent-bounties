import unittest
import re
from datetime import datetime

# Simulated parser function to be tested
def parse_log_line(line):
    """
    Simulate parsing a log line.
    Returns a dict with keys: timestamp (datetime), level (str), service (str), message (str)
    or None if line is malformed.
    """
    # Try JSON log line
    import json
    try:
        data = json.loads(line)
        ts = datetime.fromisoformat(data.get("timestamp"))
        level = data.get("level")
        service = data.get("service")
        message = data.get("message")
        if not (ts and level and service and message):
            return None
        return {"timestamp": ts, "level": level, "service": service, "message": message}
    except Exception:
        pass

    # Try nginx style: '127.0.0.1 - - [10/Jul/2026:22:14:15 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.68.0"'
    # We'll parse timestamp, level (assume "INFO"), service (assume "nginx"), message (the whole line)
    nginx_re = re.compile(r'\[(?P<timestamp>\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+\-]\d{4})\]')
    m = nginx_re.search(line)
    if m:
        try:
            ts = datetime.strptime(m.group("timestamp"), "%d/%b/%Y:%H:%M:%S %z")
            return {"timestamp": ts, "level": "INFO", "service": "nginx", "message": line}
        except Exception:
            return None

    # Try plain text: "2026-07-25 14:22:33,123 - serviceA - ERROR - Something happened"
    plain_re = re.compile(r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (?P<service>[^ ]+) - (?P<level>[A-Z]+) - (?P<message>.+)$')
    m = plain_re.match(line)
    if m:
        try:
            ts = datetime.strptime(m.group("timestamp"), "%Y-%m-%d %H:%M:%S,%f")
            return {"timestamp": ts, "level": m.group("level"), "service": m.group("service"), "message": m.group("message")}
        except Exception:
            return None

    # Malformed or unsupported line
    return None


class TestIndependentLogFixtures(unittest.TestCase):

    def test_json_log(self):
        line = '{"timestamp": "2026-07-25T14:22:33", "level": "ERROR", "service": "jsonservice", "message": "An error occurred"}'
        result = parse_log_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["level"], "ERROR")
        self.assertEqual(result["service"], "jsonservice")
        self.assertEqual(result["message"], "An error occurred")
        self.assertEqual(result["timestamp"].isoformat(), "2026-07-25T14:22:33")

    def test_plain_text_log(self):
        line = "2026-07-25 14:22:33,123 - serviceA - ERROR - Something happened"
        result = parse_log_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["level"], "ERROR")
        self.assertEqual(result["service"], "serviceA")
        self.assertEqual(result["message"], "Something happened")
        self.assertEqual(result["timestamp"].strftime("%Y-%m-%d %H:%M:%S,%f")[:23], "2026-07-25 14:22:33,123")

    def test_nginx_log(self):
        line = '127.0.0.1 - - [10/Jul/2026:22:14:15 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.68.0"'
        result = parse_log_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["level"], "INFO")
        self.assertEqual(result["service"], "nginx")
        self.assertEqual(result["message"], line)
        self.assertEqual(result["timestamp"].strftime("%Y-%m-%dT%H:%M:%S%z"), "2026-07-10T22:14:15+0000")

    def test_malformed_log(self):
        line = "this is not a valid log line"
        result = parse_log_line(line)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
