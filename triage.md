<!--
Copyright (c) 2026 Matthias Tafelmeier. AGPL-3.0-or-later, see LICENSE.
-->
# Triage rules

Read before acting on any finding from gate or sweep.

## Hit classes

BLOCK — merge-stopping in the gate:
- foreign copyleft license markers in added lines: plain GPL (no Affero,
  no Lesser), CDDL, SSPL, BSL/BUSL, Commons Clause
- private key blocks (BEGIN ... PRIVATE KEY) in added lines

NOTE — review items, never auto-merge-stopping:
- copyright lines naming anyone other than the house holder
- files added under third_party/, vendor/, ext/ paths
- new or changed entries in dependency manifests (inventory, not verdict)

## Dispositions

The only disposition for confirmed foreign code: REWRITE THE PASSAGE.
Same day. Never annotate-over, never relabel, never patch a license
header onto foreign code — labeling someone else's code as ours is a
second violation on top of the first.

A BLOCK hit means: stop, rewrite the passage fresh from the problem,
re-run the gate. A NOTE hit means: a human looks once, then either
rewrites or records why it stands (declared dependency, own historical
file, false positive).

## On being challenged externally

Any external provenance challenge (issue, notice, takedown): same-day
removal of the challenged passage, then rewrite. Innocence survives
discovery; it does not survive refusal. The session trail plus the
provenance notes are the standing evidence of process.

## Scope limits, stated honestly

The sweep matches markers and known-corpus patterns. It cannot see
private, unindexed code; no scanner can. What it certifies is "no match
against the marker classes above" — a process record, not a certificate
of originality. Never present it as more.
