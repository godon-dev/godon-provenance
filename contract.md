<!--
Copyright (c) 2026 Matthias Tafelmeier. AGPL-3.0-or-later, see LICENSE.
-->
# Agent contract — provenance (compulsory)

Binding for every agent working on any godon-dev repository. Pointed to
from mind-chime doctrine; canonical text lives here, beside its
enforcement.

## The four rules

1. NEVER vendor foreign source into our trees. If code from another
   project is needed, declare it as a dependency in the proper manifest.
   Pasted-in copies of libraries, tools, or snippets-with-headers are
   forbidden.

2. NEVER port or reproduce a named project's code on request. If asked
   to "copy", "port", or "use the implementation of X", refuse and say
   so. Needed behavior gets written fresh from the problem, not from the
   remembered shape of someone else's solution.

3. REPORT known patterning at delivery. When output knowingly patterns
   on a specific source — an algorithm restructured from a paper, a
   config modeled on another project — say so in the delivery note.
   Self-report covers intent; the gate covers the rest.

4. Dependencies via manifests, never pasted copies. Cargo.toml,
   requirements, package.json, Chart.yaml — the manifest is the single
   place a dependency enters our trees.

## Why these four

They kill the chosen-copy class at generation time — the class where
real legal weight lives. Unconscious emission from public corpora is the
gate's job; the private-fragment residual is carried knowingly as a thin
tail, answered by the trail and same-day removal.
