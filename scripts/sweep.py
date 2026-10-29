#!/usr/bin/env python3
"""godon provenance sweep — local marker baseline over tracked files.

Usage:  python3 sweep.py [--date YYYY-MM-DD]

Reads ../config for the repo list. For each repo: scans tracked text
files at HEAD, inventories dependencies from manifests, writes
notes/<repo>-<date>.md and rebuilds notes/INDEX.md. Read-only toward the
scanned repos. stdlib only, backslash-free by necessity (output pipeline
doubles backslashes — do not reintroduce them).
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from gate_scan import BLOCK_MATCHES, HOUSE_MARKER, line_has_year  # noqa: E402

TEXT_EXT = (".py", ".rs", ".sh", ".md", ".yaml", ".yml", ".toml", ".json", ".txt", ".js", ".ts", ".html", ".css", ".go", ".nix", ".conf", ".service", ".xml", ".svg", ".cfg", ".ini", ".lock", ".mod", ".sum", ".tf")
MAX_FILE = 1000000
MANIFEST_NAMES = ("Cargo.toml", "requirements.txt", "package.json", "Chart.yaml", "pyproject.toml", "Cargo.lock")
NL = chr(10)
NUL = bytes([0])


def read_config():
    cfg = {}
    for line in open(os.path.join(ROOT, "config")):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            cfg[k.strip()] = v.strip()
    return cfg


def git(repo, args):
    return subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True, check=True).stdout


def is_text(path):
    ext = os.path.splitext(path)[1]
    if ext not in TEXT_EXT and ext != "":
        return False
    try:
        with open(path, "rb") as fh:
            return NUL not in fh.read(8192)
    except OSError:
        return False


def classify_line(text):
    low = text.lower()
    for kind, any_of, all_of, allow in BLOCK_MATCHES:
        if any(s in low for s in any_of) and all(s in low for s in all_of):
            if not (allow and any(s in low for s in allow)):
                return ("BLOCK", kind)
    idx = low.find("copyright")
    if idx >= 0 and line_has_year(low[idx:idx + 40]) and HOUSE_MARKER not in text:
        return ("NOTE", "foreign-copyright")
    return None


def collect_deps(full, name):
    out = set()
    try:
        text = open(full, errors="replace").read()
    except OSError:
        return out
    if name == "Cargo.toml":
        section = ""
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("[") and s.endswith("]"):
                header = s[1:-1]
                if header == "dependencies":
                    section = "deps"
                elif header.startswith("dependencies."):
                    out.add(header.split(".", 1)[1].split(" ")[0])
                    section = ""
                else:
                    section = ""
            elif section == "deps" and "=" in line and not s.startswith("#"):
                out.add(line.split("=", 1)[0].strip())
    elif name == "Cargo.lock":
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("name = ") and '"' in s:
                out.add(s[s.find('"') + 1:s.rfind('"')])
    elif name == "requirements.txt":
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            cut = len(s)
            for ch in "=<>!~[ #":
                pos = s.find(ch)
                if pos >= 0:
                    cut = min(cut, pos)
            out.add(s[:cut])
    elif name == "package.json":
        try:
            pkg = json.loads(text)
            for key in ("dependencies", "devDependencies"):
                out.update((pkg.get(key) or {}).keys())
        except json.JSONDecodeError:
            pass
    elif name == "Chart.yaml":
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("- name:"):
                rest = s[len("- name:"):].strip()
                if rest:
                    out.add(rest.split()[0])
    return out


def scan_repo(path, repo):
    head = git(path, ["rev-parse", "--short", "HEAD"]).strip()
    branch = git(path, ["rev-parse", "--abbrev-ref", "HEAD"]).strip()
    dirty = bool(git(path, ["status", "--porcelain"]).strip())
    files = git(path, ["ls-files"]).splitlines()

    hits, scanned, deps = [], 0, set()
    for rel in files:
        full = os.path.join(path, rel)
        base = rel.split("/")[-1]
        if base.upper() in ("LICENSE", "COPYING", "NOTICE"):
            continue  # canonical license text is expected content, exempt
        if any(part in ("third_party", "vendor", "ext", "bundled") for part in rel.split("/")):
            hits.append({"class": "NOTE", "kind": "vendored-path", "file": rel, "line": 0, "text": ""})
        if not (os.path.isfile(full) and os.path.getsize(full) <= MAX_FILE and is_text(full)):
            continue
        scanned += 1
        if base in MANIFEST_NAMES:
            deps.update(collect_deps(full, base))
        try:
            with open(full, errors="replace") as fh:
                for no, line in enumerate(fh, 1):
                    got = classify_line(line)
                    if got:
                        hits.append({"class": got[0], "kind": got[1], "file": rel, "line": no, "text": line.strip()[:120]})
        except OSError:
            continue

    return {"repo": repo, "head": head, "branch": branch, "dirty": dirty,
            "tracked": len(files), "scanned": scanned, "hits": hits, "deps": sorted(deps)}


def write_note(res, date, notes_dir):
    blocks = [h for h in res["hits"] if h["class"] == "BLOCK"]
    notes = [h for h in res["hits"] if h["class"] == "NOTE"]
    status = "clean" if not res["hits"] else ("review: " + str(len(res["hits"])) + " (" + str(len(blocks)) + " block)")
    lines = ["# Provenance note — " + res["repo"] + " — " + date, "",
             "- scanned: HEAD " + res["head"] + " (" + res["branch"] + (", dirty" if res["dirty"] else "") + ")",
             "- tracked files: " + str(res["tracked"]) + " | text-scanned: " + str(res["scanned"]),
             "- dependencies: " + str(len(res["deps"])),
             "- findings: " + str(len(res["hits"])) + " (" + str(len(blocks)) + " block, " + str(len(notes)) + " note)",
             "- status: " + status, ""]
    for h in res["hits"]:
        loc = h["file"] + ":" + str(h["line"]) if h["line"] else h["file"]
        lines.append("- [" + h["class"] + "] " + h["kind"] + " — " + loc + " — " + h["text"])
    if res["deps"]:
        lines += ["", "dependencies: " + ", ".join(res["deps"])]
    lines += ["", "disposition: pending triage per triage.md" if res["hits"] else "disposition: none needed"]
    path = os.path.join(notes_dir, res["repo"] + "-" + date + ".md")
    open(path, "w").write(NL.join(lines) + NL)
    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()
    cfg = read_config()
    root = cfg["projects_root"]
    notes_dir = os.path.join(ROOT, "notes")
    os.makedirs(notes_dir, exist_ok=True)

    rows = []
    for repo in cfg["sweep_repos"].split():
        path = os.path.join(root, repo)
        if not os.path.isdir(path):
            rows.append((repo, "-", "-", "-", "missing"))
            continue
        res = scan_repo(path, repo)
        status = write_note(res, args.date, notes_dir)
        rows.append((repo, str(res["scanned"]), str(len(res["deps"])), str(len(res["hits"])), status))
        print("swept " + repo + ": " + str(res["scanned"]) + " files, " + str(len(res["deps"])) + " deps, " + str(len(res["hits"])) + " findings")

    idx = ["# Provenance index — " + args.date, "", "| repo | files | deps | findings | status |", "|---|---|---|---|---|"]
    for r in rows:
        idx.append("| " + " | ".join(r) + " |")
    open(os.path.join(notes_dir, "INDEX.md"), "w").write(NL.join(idx) + NL)
    print("index written: notes/INDEX.md (" + str(len(rows)) + " repos)")


if __name__ == "__main__":
    main()
