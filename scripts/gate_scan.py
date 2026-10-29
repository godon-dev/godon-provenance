#!/usr/bin/env python3
"""godon provenance gate — diff scanner for PRs. stdlib only, backslash-free.

Usage:  python3 gate_scan.py [--base origin/main] [--head HEAD] [--json]

Exit 0 = clean or notes only. Exit 1 = BLOCK findings present.
Scans ADDED lines of the diff only. See ../triage.md for classes.
"""
import argparse
import json
import subprocess
import sys

HOUSE_MARKER = "Tafelmeier"

# (kind, case-insensitive substrings, all-of required, allow-if substrings)
BLOCK_MATCHES = [
    ("copyleft:gpl", ["gnu general public license"], [], ["affero", "lesser"]),
    ("copyleft:cddl", ["cddl", "common development and distribution license"], [], []),
    ("copyleft:sspl", ["sspl", "server side public license"], [], []),
    ("copyleft:bsl", ["business source license", "busl-1", "bsl-1.1"], [], []),
    ("copyleft:commons-clause", ["commons clause"], [], []),
    ("secret:private-key", ["private key"], ["begin"], []),
]

MANIFEST_NAMES = ("Cargo.toml", "requirements.txt", "package.json", "Chart.yaml", "pyproject.toml")
VENDORED_PARTS = {"third_party", "vendor", "ext", "bundled"}


def run_git(args):
    return subprocess.run(["git"] + args, capture_output=True, text=True, check=True).stdout


def added_lines(base, head):
    """Yield (path, line_no, text) for each added line in the diff."""
    out = run_git(["diff", "--no-color", "--unified=0", "--diff-filter=ACMR", base + "..." + head])
    path, lineno = None, 0
    for line in out.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
        elif line.startswith("@@"):
            seg = line.split("+", 1)[1] if "+" in line else ""
            digits = ""
            for ch in seg:
                if ch.isdigit():
                    digits += ch
                else:
                    break
            lineno = int(digits) if digits else 0
        elif line.startswith("+") and not line.startswith("+++"):
            yield path, lineno, line[1:]
            lineno += 1


def changed_files(base, head):
    out = run_git(["diff", "--name-only", "--diff-filter=ACMR", base + "..." + head])
    return [f for f in out.splitlines() if f]


def line_has_year(seg):
    return any(seg[j:j + 4].isdigit() for j in range(len(seg) - 3))


def scan_line(path, no, text, findings):
    low = text.lower()
    for kind, any_of, all_of, allow in BLOCK_MATCHES:
        if any(s in low for s in any_of) and all(s in low for s in all_of):
            if not (allow and any(s in low for s in allow)):
                findings.append({"class": "BLOCK", "kind": kind, "file": path, "line": no, "text": text.strip()[:120]})
            return
    idx = low.find("copyright")
    if idx >= 0 and line_has_year(low[idx:idx + 40]) and HOUSE_MARKER not in text:
        findings.append({"class": "NOTE", "kind": "foreign-copyright", "file": path, "line": no, "text": text.strip()[:120]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    findings = []
    for path, no, text in added_lines(args.base, args.head):
        scan_line(path, no, text, findings)

    for f in changed_files(args.base, args.head):
        if any(part in VENDORED_PARTS for part in f.split("/")):
            findings.append({"class": "NOTE", "kind": "vendored-path", "file": f, "line": 0, "text": ""})
        if f.split("/")[-1] in MANIFEST_NAMES:
            findings.append({"class": "NOTE", "kind": "manifest-change", "file": f, "line": 0, "text": ""})

    blocks = [f for f in findings if f["class"] == "BLOCK"]
    if args.json:
        print(json.dumps({"base": args.base, "head": args.head, "blocks": len(blocks), "notes": len(findings) - len(blocks), "findings": findings}, indent=2))
    else:
        for f in findings:
            loc = f["file"] + ":" + str(f["line"]) if f["line"] else f["file"]
            print("[" + f["class"] + "] " + f["kind"].ljust(20) + " " + loc + "  " + f["text"])
        print("--- gate: " + str(len(blocks)) + " block, " + str(len(findings) - len(blocks)) + " note")
    sys.exit(1 if blocks else 0)


if __name__ == "__main__":
    main()
