# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Integration tests for the local web app notarius/webapp.py (AD-93):
a real server on an ephemeral localhost port, real HTTP requests.

Run: python3 tests/test_webapp.py
"""

import json
import sys
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.webapp import Handler   # noqa: E402


class TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)   # port 0 = ephemeral
        cls.port = cls.httpd.server_address[1]
        cls.t = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.t.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def _post(self, path, obj):
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            data=json.dumps(obj).encode(), method="POST",
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read().decode())

    def test_page_served(self):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/", timeout=5) as r:
            self.assertEqual(r.status, 200)
            self.assertIn(b"NOTARIUS", r.read())

    def test_compare_amount_swap(self):
        st, res = self._post("/api/compare",
                             {"reference": "amount: 1000", "received": "amount: 9000"})
        self.assertEqual(st, 200)
        self.assertFalse(res["identical"])
        self.assertEqual(res["findings"][0]["category"], "VALUE_SUBSTITUTION")

    def test_compare_identical(self):
        st, res = self._post("/api/compare",
                             {"reference": "same", "received": "same"})
        self.assertTrue(res["identical"])

    def test_scan_invisible(self):
        st, res = self._post("/api/scan", {"text": "pay​able"})
        self.assertEqual(res["hidden"]["risk"], "ALARM")

    def test_bad_path_404(self):
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/api/nope",
            data=b"{}", method="POST", headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=5)
            self.fail("expected 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
