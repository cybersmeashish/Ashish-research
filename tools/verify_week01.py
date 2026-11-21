"""Verify saved results against current input hashes and independent local regeneration."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from week01_review import ROOT, WEEK, execute as baseline
from week01_evaluate import execute as evaluation
from week01_worked_example import example

def verify(output):
    output.mkdir(parents=True, exist_ok=True)
    checked = []
    for phase in ("baseline", "evaluation"):
        manifest = json.loads((WEEK / f"evidence/{phase}/source-manifest.json").read_text())
        for path, expected in manifest.items():
            if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
                raise ValueError("Published input differs from recorded evidence: " + path)
            checked.append(path)
    base_rows, _ = baseline(output / "baseline")
    review_rows, report = evaluation(output / "evaluation")
    for folder, name in (("baseline", "baseline-observations.csv"),
                         ("evaluation", "review-results.csv")):
        if (output / folder / name).read_bytes() != (WEEK / name).read_bytes():
            raise ValueError("Saved CSV does not reproduce: " + name)
    stored_example = json.loads((WEEK / "evidence/worked-example.json").read_text())
    if stored_example != example():
        raise ValueError("Worked example differs from current decisions")
    tests = subprocess.run([sys.executable, "-m", "unittest", "discover",
                            "-s", str(ROOT / "tests"), "-p", "test_week01_*.py", "-v"],
                           capture_output=True, text=True, cwd=ROOT)
    (output / "test-results.log").write_text(tests.stdout + tests.stderr)
    if tests.returncode:
        raise ValueError("Regression tests failed; inspect test-results.log")
    count = re.search(r"Ran (\d+) tests", tests.stderr)
    if not count:
        raise ValueError("Regression test count is unavailable")
    link_count = 0
    for document in [ROOT / "README.md", *WEEK.glob("*.md")]:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
            if target.startswith(("https://", "http://", "#")):
                continue
            path = target.split("#", 1)[0]
            if path and not (document.parent / path).is_file():
                raise ValueError(f"Missing local document target: {document.relative_to(ROOT)} -> {target}")
            link_count += 1
    record = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "unique_regression_tests": int(count.group(1)),
        "matching_manifest_entries": len(checked),
        "matching_unique_input_files": len(set(checked)),
        "reproduced_csv_files": ["baseline-observations.csv", "review-results.csv"],
        "worked_example_reproduced": True, "local_document_links": link_count,
        "totals": report["totals"],
        "original_backend_unknown_preserved": next(
            r["original_backend_decidable"] == "no" and r["original_decision"] == "unknown"
            for r in review_rows if r["fixture_id"] == "P02"),
        "scope": "actual standard-library local execution; no network/model/deployment assurance",
    }
    (output / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
    return record

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.out:
        print(json.dumps(verify(args.out), indent=2))
    else:
        with tempfile.TemporaryDirectory(prefix="ashish-week01-") as folder:
            print(json.dumps(verify(Path(folder)), indent=2))
