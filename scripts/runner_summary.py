#!/usr/bin/env python3
"""Summarize scancode + trivy runner outputs against the org policy.

Usage:  runner_summary.py scan.json trivy.json [--count]

Exit 0 = policy clean (own AGPL allowed; foreign copyleft absent).
Exit 1 = foreign copyleft present — run should flag it.
--count prints just the number of policy hits.
Foreign copyleft list mirrors triage.md: GPL-2-only, CDDL, SSPL, BSL/BUSL,
Commons Clause. AGPL (own license) and permissive licenses pass.
"""
import json
import sys

FOREIGN_COPYLEFT = (
    "GPL-2.0-only", "GPL-2.0-or-later", "GPL-2.0", "CDDL", "SSPL-1.0",
    "BSL-1.1", "BUSL-1.1", "commons-clause",
)


def hits_from_scan(path):
    try:
        data = json.load(open(path))
    except (OSError, json.JSONDecodeError):
        return []
    found = []
    for f in data.get("files", []):
        for lic in f.get("licenses", []) or []:
            expr = (lic.get("key") or "") + " " + (lic.get("spdx_license_key") or "")
            for bad in FOREIGN_COPYLEFT:
                if bad.lower() in expr.lower():
                    found.append({"file": f.get("path"), "license": bad})
    return found


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    count_only = "--count" in sys.argv
    hits = []
    for path in args:
        hits.extend(hits_from_scan(path))
    if count_only:
        print(len(hits))
    else:
        for h in hits:
            print(f"FOREIGN-COPYLEFT {h['license']} {h['file']}")
        print(f"--- policy hits: {len(hits)}")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
