# Provenance note — godon-charts — 2026-10-29

- scanned: HEAD 6d453ec (main, dirty)
- tracked files: 33 | text-scanned: 30
- dependencies: 11
- findings: 4 (4 block, 0 note)
- status: review: 4 (4 block)

- [BLOCK] secret:private-key — .github/workflows/charts--smoke-tests.yaml:197 — -----BEGIN RSA PRIVATE KEY-----
- [BLOCK] secret:private-key — .github/workflows/charts--smoke-tests.yaml:750 — printf 'name: "smoke-test-ssh-key"\ncredentialType: "ssh_private_key"\ndescription: "SSH key for smoke testing"\ncontent
- [BLOCK] secret:private-key — .github/workflows/charts--smoke-tests.yaml:817 — printf 'name: "test-cred-special"\ncredentialType: "ssh_private_key"\ndescription: "Testing special character handling"\
- [BLOCK] secret:private-key — .github/workflows/charts--smoke-tests.yaml:1335 — printf 'name: "stress-test-cred-%d-%s"\ncredentialType: "ssh_private_key"\ncontent: "-----BEGIN RSA PRIVATE KEY----- tes

dependencies: alloy, cherusk, grafana, loki, opentelemetry-collector, postgresql, prometheus, prometheus-pushgateway, promtail, windmill, yugabyte

disposition: pending triage per triage.md
