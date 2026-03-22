---
name: research-status
description: Use to check the state of the research pipeline — how many raw docs, meta-docs, verified claims, what needs processing next.
disable-model-invocation: true
---

# Research Status

Check the research pipeline state. Run the indexer, show what needs work.

## Quick Check

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/index.py
```

This scans all configured research directories and shows:
- Total raw docs (need consuming)
- Meta-docs (living knowledge base)
- Archives (consumed originals)
- Breakdown by theme

## What To Do Next

Pick the theme with the most raw docs and run `/claude-research-pipeline:research-consume` to process 3 of them.
