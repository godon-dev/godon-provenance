# Provenance note — godon-test-infra — 2026-10-29

- scanned: HEAD 360e4b0 (main, dirty)
- tracked files: 13 | text-scanned: 11
- dependencies: 0
- findings: 7 (7 block, 0 note)
- status: review: 7 (7 block)

- [BLOCK] copyleft:gpl — .github/nix_config/ci-runner/configuration.nix:7 — ## it under the terms of the GNU General Public License as published by
- [BLOCK] copyleft:gpl — .github/nix_config/ci-runner/configuration.nix:14 — ## GNU General Public License for more details.
- [BLOCK] copyleft:gpl — .github/nix_config/ci-runner/configuration.nix:16 — ## You should have received a copy of the GNU General Public License
- [BLOCK] secret:private-key — testing/infra/credentials/ssh/id_rsa:1 — -----BEGIN OPENSSH PRIVATE KEY-----
- [BLOCK] copyleft:gpl — testing/infra/machines/nix/configuration.nix:7 — ## it under the terms of the GNU General Public License as published by
- [BLOCK] copyleft:gpl — testing/infra/machines/nix/configuration.nix:14 — ## GNU General Public License for more details.
- [BLOCK] copyleft:gpl — testing/infra/machines/nix/configuration.nix:16 — ## You should have received a copy of the GNU General Public License

disposition: id_rsa + id_rsa.pub removed via godon-test-infra PR #5 (rebase-merged 2026-10-29, holder-ruled: VMs decommissioned, key opens nothing; history keeps old bytes). nix GPL headers pending triage — check ScanCode artifact for exact version (GPL-3 = AGPL-compatible, note and close; GPL-2-only = rewrite).
