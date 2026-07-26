# -*- coding: utf-8 -*-
"""Tests of the supply-chain "injection on the glass" (AD-53)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notarius.supply import ArtifactRegistry, verify_delivery

AUTHENTIC = b"authentic wheel bytes: def notarius(): return 'clean'"
TAMPERED = b"authentic wheel bytes: def notarius(): return 'clean'  # + os.system('rm -rf')"


class TestSupplyChain(unittest.TestCase):

    def _reg(self):
        r = ArtifactRegistry()
        r.register("notarius==0.1.0", AUTHENTIC, "maintainer", "t0")
        return r

    def test_authentic_delivery_matches(self):
        self.assertEqual(verify_delivery(self._reg(), "notarius==0.1.0", AUTHENTIC)["status"],
                         "MATCH")

    def test_injection_on_glass_caught(self):
        r = verify_delivery(self._reg(), "notarius==0.1.0", TAMPERED)
        self.assertEqual(r["status"], "FORGERY_ON_GLASS")
        self.assertNotEqual(r["registry_hash"], r["delivered_hash"])

    def test_unknown_package(self):
        self.assertEqual(verify_delivery(self._reg(), "evil==9.9", AUTHENTIC)["status"],
                         "UNKNOWN_PACKAGE")

    def test_first_wins_later_reregister_ignored(self):
        # the thief tries to re-register the same package_id to THEIR (evil) hash
        r = self._reg()
        r.register("notarius==0.1.0", TAMPERED, "thief", "t9")
        # the original (recorded first) stays the authority
        self.assertEqual(verify_delivery(r, "notarius==0.1.0", AUTHENTIC)["status"], "MATCH")
        self.assertEqual(verify_delivery(r, "notarius==0.1.0", TAMPERED)["status"],
                         "FORGERY_ON_GLASS")

    def test_registry_tamper_detected(self):
        r = self._reg()
        r.register("other==1.0", b"x", "m", "t1")
        r._log[0]["artifact_sha256"] = "0" * 64        # a secret edit of the registry
        self.assertEqual(verify_delivery(r, "notarius==0.1.0", AUTHENTIC)["status"],
                         "REGISTRY_TAMPERED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
