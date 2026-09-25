# AI Context / Code Graph Setup

The repository integrates two complementary third-party tools:

- **CodeGraph** (`colbymchenry/codegraph`) — primary code intelligence for Claude/Codex. It builds `.codegraph/` and auto-syncs source changes while its MCP server is active.
- **Graphify** (`Graphify-Labs/graphify`) — supplementary graph over code + design/schema/docs. Code changes can be watched locally; a post-commit hook also refreshes code graph output. Documentation semantic updates may require an explicit Graphify update.

## Why both
CodeGraph is used first for surgical source context, call paths, and impact analysis. Graphify is used for cross-file rationale across code, schema, regulatory docs, and ADRs. This prevents agents from repeatedly reading large folders.

## Upstream pins reviewed for this repo
- Graphify commit: `4c735618f3d56fd622c2049771584621c31ba9ff` (package `graphifyy` 0.9.67)
- CodeGraph commit: `ba3c21e50d9129d2f5f3843ec3728868ae6d47a1` (package 1.6.0)

See `tools/upstreams/upstreams.lock.json`.

## Setup
```bash
make ai-setup
```
Then initialize/fetch the pinned upstream source mirrors if desired:
```bash
make upstream-init
```

## Freshness
- CodeGraph: auto-sync is handled by the MCP watcher during agent sessions. `make ai-refresh` also calls `codegraph sync` explicitly.
- Graphify: `graphify hook install` is installed by setup for commit-time code refresh. For live editing, start `make graphify-watch`. For changed docs/schema/ADR content, run Graphify update from Claude/Codex when the `needs_update` flag is present.

## Exclusions
`.graphifyignore` excludes raw datasets, experiment outputs, reports, tests, and third-party upstream source. This keeps Graphify focused on durable project architecture.
