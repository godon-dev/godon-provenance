#!/usr/bin/env python3
"""Filter jscpd report to repo-vs-corpus clone pairs only.

jscpd reports duplication within the union of scanned paths; we only
care about pairs where one side is our repo and the other is the
dependency corpus. Usage: snippet_filter.py <report.json> <repo-prefix>
"""
import json
import sys


def main():
    path, prefix = sys.argv[1], sys.argv[2]
    data = json.load(open(path))
    dups = data.get("duplicates", [])
    cross = []
    for d in dups:
        a, b = d.get("firstFile", ""), d.get("secondFile", "")
        a_ours = prefix in a
        b_ours = prefix in b
        if a_ours != b_ours:
            cross.append({
                "ours": a if a_ours else b,
                "theirs": b if a_ours else a,
                "lines": d.get("lines"),
                "tokens": d.get("tokens"),
            })
    print("clones total:", len(dups))
    print("repo-vs-corpus clones:", len(cross))
    for c in sorted(cross, key=lambda x: -(x.get("tokens") or 0))[:50]:
        print("CROSS", c.get("tokens"), "tokens |", c.get("ours"), "<->", c.get("theirs"))
    out = path.replace("jscpd-report.json", "cross-pairs.json")
    json.dump(cross, open(out, "w"), indent=2)
    print("written:", out)


if __name__ == "__main__":
    main()
