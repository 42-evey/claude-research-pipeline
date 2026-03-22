---
name: research-setup
description: Use when first installing the research pipeline or adding new research directories to track. Configures paths and creates required directories.
disable-model-invocation: true
---

# Research Pipeline Setup

Initialize or update the research pipeline configuration.

## First-Time Setup

1. Read the config at `${CLAUDE_PLUGIN_DATA}/config.json`
   - If it doesn't exist, create it with the template below
2. Ask the user which directories contain research documents
3. Set the meta, archive, and reviews directories
4. Create all directories that don't exist
5. Run the indexer to catalog existing docs

## Config Template

Write to `${CLAUDE_PLUGIN_DATA}/config.json`:
```json
{
  "research_dirs": [],
  "meta_dir": "",
  "archive_dir": "",
  "reviews_dir": "",
  "max_docs_per_cycle": 3,
  "reverify_days": 14
}
```

## Adding a New Research Directory

1. Read existing config from `${CLAUDE_PLUGIN_DATA}/config.json`
2. Append the new directory path to `research_dirs`
3. Write updated config
4. Run indexer to catalog the new docs

## Required Directory Structure

After setup, these should exist:
- Each path in `research_dirs` (where raw docs live)
- `meta_dir` (where meta-research grows)
- `archive_dir` (where consumed originals get zipped)
- `reviews_dir` (where per-doc reviews are stored)
