# Claude Research Pipeline

**Claude Code plugin that consumes research docs into verified meta-knowledge.**

Point it at directories of markdown research docs. It reviews each doc, verifies every key claim via web search, merges findings into growing meta-research documents, and archives the originals. Your research dirs shrink, your knowledge base grows.

## Install

```bash
# Claude Code
claude /install-plugin 42-evey/claude-research-pipeline
```

## Usage

```bash
# First time — configure your research directories
/claude-research-pipeline:research-setup

# Check what needs processing
/claude-research-pipeline:research-status

# Consume docs into meta-research (max 3 per run)
/claude-research-pipeline:research-consume
```

## How It Works

```
Raw Docs (.md files in your research dirs)
    |
    |  /research-consume
    v
Review: Read doc, score quality, extract 3-5 key claims
    |
    v
Verify: Web search + paper search for each claim
    |  VERIFIED (2+ sources) / LIKELY (1 source) / UNVERIFIED / DISPUTED
    v
Merge: Synthesize into meta-doc (research/meta/[theme].md)
    |  Meta-docs GROW over time as more docs are consumed
    v
Archive: Zip original, remove from working set
    |  research/archive/[date].zip
    v
Re-verify: Periodically re-check claims in meta-docs
```

## What's In The Plugin

| Component | Purpose |
|-----------|---------|
| `skills/research-setup` | Configure research directories on first run |
| `skills/research-consume` | Main workflow: read → verify → merge → archive |
| `skills/research-status` | Quick pipeline status check |
| `agents/research-reviewer` | Sonnet subagent for doc review + claim verification |
| `scripts/index.py` | Mechanical indexer (no LLM needed) |

## Claude-Native

No external LLM API needed. Claude does all the thinking:
- **Haiku**: Quick categorization
- **Sonnet**: Document review, web search verification
- **Opus**: Deep synthesis and meta-doc writing

## Config

Stored at `~/.claude/plugins/data/claude-research-pipeline/config.json`:
```json
{
  "research_dirs": ["./research/notes", "./research/specs"],
  "meta_dir": "./research/meta",
  "archive_dir": "./research/archive",
  "reviews_dir": "./research/reviews",
  "max_docs_per_cycle": 3,
  "reverify_days": 14
}
```

## License

MIT — built by [Evey](https://evey.cc)
