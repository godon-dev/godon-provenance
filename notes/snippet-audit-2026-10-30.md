# Snippet audit — one-shot deep check — 2026-10-30

Method: per repo, all dependency sources fetched from crates.io per
Cargo.lock (e.g. cli: 167 crates, robots: 212), unpacked as corpus; jscpd
token comparison of every repo file against every corpus file at
function-grade threshold (min-tokens 70); pairs filtered to repo-vs-corpus
only (corpus-internal echo excluded).

Run: godon-provenance snippet-audit 41054245011, all eight jobs green.
Artifacts kept per repo.

Result: repo-vs-corpus clones: 0 — in every repository.

Reading: the abstraction invariant holds, measured. Our code shares no
function-grade token sequence with any declared dependency's source.
Expected zero by architecture (holder's own argument 2026-10-29: clean
API-boundary abstraction means least duplication in exactly this
pairing); measured zero 2026-10-30. Expected-zero audits that read green
are conclusions.

Limits, stated: covers declared dependencies only (cargo lane); threshold
70 tokens; near-verbatim matches only — paraphrase is invisible to token
compare (and mostly irrelevant in law). Not a standing organ: re-run
on demand after major dependency changes or on suspicion.
