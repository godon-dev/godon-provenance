<!--
Copyright (c) 2026 Matthias Tafelmeier.

godon provenance tooling is free software: you can redistribute it and/or
modify it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. See LICENSE.
-->
# godon-provenance

Provenance organs for the godon-dev org: contract, gate, sweep, notes.
Dependency-free by ruling: stdlib Python and git only. Nothing installs,
nothing phones home, nothing needs the network at scan time.

Scope is PROVENANCE ONLY: origin of our code is known and declared.
Credentials are deliberately out of scope — that lane belongs to the
platform (org secret scanning + push protection) and to the auth skill.

## Organs

- `contract.md` — generation-side rules for agents working on org repos.
  Compulsory via the mind-chime pointer. Law lives here; mind-chime cites.
- `triage.md` — what counts as a hit, and the only allowed dispositions.
- `.github/workflows/daily-scan.yaml` — the primary instrument: daily
  GitHub-hosted runner scan per org repo. ScanCode (license, copyright,
  packages), Trivy (vulns, dep licenses), GitHub-native SBOM export.
  Language-agnostic by ruling. Pull-based: no per-repo wiring anywhere.
- `scripts/runner_summary.py` — the policy check over runner outputs.
- `.github/workflows/weekly-scorecard.yaml` — OpenSSF Scorecard posture pass.
- `scripts/gate_scan.py` — optional per-PR marker gate (second speed,
  unwired; ride via `.github/workflows/gate.yaml` + a ruleset if wanted).
- `scripts/sweep.py` — local marker baseline (manual/emergency lane;
  mind-chime is local-only and stays in this lane).
- `notes/` — the provenance record. One file per repo per sweep.

Install doctrine: nothing installs on agent machines. The heavy engine
(ScanCode) lives and dies on ephemeral GitHub runners — free for public
repos. Snippet pass against dependency-source corpora is the workflow's
phase 2 (jscpd or scancode-detect; language-agnostic either way).

## Usage

Gate on a diff, from inside any org repo:

    python3 scripts/gate_scan.py --base origin/main

Baseline sweep (reads `config` for the repo list):

    python3 scripts/sweep.py

## Standing rules enforced here

- Own license is AGPL-3.0-or-later: own AGPL headers are expected and
  allowed. Foreign copyleft (GPL-2-only, CDDL, SSPL, BSL, Commons Clause)
  is the target class.
- Dependencies declared in manifests only. Vendored source is a finding.
- Confirmed hit → rewrite the passage, same day. Never annotate-over,
  never relabel.
