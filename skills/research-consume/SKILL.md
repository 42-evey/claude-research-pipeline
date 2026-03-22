---
name: research-consume
description: Use when research documents need processing into verified meta-knowledge. Triggers when raw docs accumulate or at each work cycle. Reads docs, verifies claims, merges into meta-research, archives originals.
---

# Research Consume — Process Raw Docs Into Meta-Knowledge

Consume research documents into verified, growing meta-research papers. Every claim gets verified. Originals get archived. Meta-docs are the living knowledge base.

## Before Starting

Check if config exists at `${CLAUDE_PLUGIN_DATA}/config.json`. If not, or if `research_dirs` is empty:

1. Ask the user: "Which directories contain research documents to process?"
2. Default to current working directory if they don't specify
3. Set `meta_dir` to `./research/meta` (relative to cwd)
4. Set `archive_dir` to `./research/archive`
5. Set `reviews_dir` to `./research/reviews`
6. Create all dirs that don't exist
7. Save config to `${CLAUDE_PLUGIN_DATA}/config.json`

All paths should be relative to the current working directory unless the user specifies absolute paths.

## The Process

For each raw doc (max 3 per cycle):

### Step 1: Read & Extract
Read the full document. Extract:
- Title, date, category
- 3-5 key factual claims (specific, verifiable statements)
- Quality scores: depth (1-10), accuracy (1-10), actionability (1-10)
- Summary (2-3 sentences)

### Step 2: Verify Every Claim
For EACH key claim, verify it:
- Use WebSearch to find corroborating sources
- Use WebFetch to read authoritative pages
- Search academic papers on arXiv/Semantic Scholar if technical
- Assign status:

| Status | Criteria | Confidence |
|--------|----------|------------|
| VERIFIED | 2+ independent sources confirm | >= 0.8 |
| LIKELY | 1 authoritative source confirms | 0.6-0.8 |
| UNVERIFIED | No sources found | 0.3-0.6 |
| DISPUTED | Sources contradict | < 0.3 |
| OUTDATED | Was true, may no longer be | needs check |

### Step 3: Merge Into Meta-Doc
Check if a meta-doc exists for this theme at `research/meta/[category].md`:
- **If exists**: Read it, incorporate new verified findings, update claims table
- **If not**: Create new meta-doc with structure below

Meta-doc structure:
```markdown
# Meta-Research: [Theme]
Last updated: [date]
Sources consumed: [count]

## Core Findings
[Verified, synthesized knowledge]

## Claims & Verification
| Claim | Status | Confidence | Source |
[table of all claims with verification status]

## Actionable Insights
[What to do with this knowledge]

## Gaps & Next Research
[What's still unknown]
```

### Step 4: Archive Original
After merging into meta-doc:
- Move original to `research/archive/` (zip by date)
- Update any index or tracking files
- The meta-doc is now the canonical source

## Per-Cycle Workflow (FOLLOW THIS EXACTLY)

### 1. Index & Categorize
Run the indexer or manually list raw docs and group them by category:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/index.py
```
Or list docs and mentally categorize them.

### 2. Batch by Category
Pick ONE category with the most raw docs. Process up to 3 docs from that SAME category together. This is critical — docs in the same category merge into the SAME meta-doc.

### 3. Read Existing Meta-Doc FIRST (before touching raw docs)
Check if `meta/[category].md` already exists:
- If YES: **Read it fully FIRST.** Understand what you already know. What claims are verified? What gaps exist? What's the current structure? You are building ON TOP of this.
- If NO: You will create it fresh after reviewing the raw docs.

This is the most important step. The meta-doc is your existing knowledge. The raw docs are new information to integrate. You MUST know what you have before you read what's new.

### 4. THEN Read Each Raw Doc (max 3 in the batch)
For each raw doc in the category:
a) Read the full raw doc
b) Compare against what's already in the meta-doc — what's genuinely NEW?
c) Extract 3-5 key factual claims that ADD to or CORRECT the meta-doc
d) Verify the top 3 new claims via WebSearch
e) Note contradictions with existing meta-doc claims

### 5. Write/Update the Meta-Doc
- If updating: APPEND new sections, UPDATE the claims table, INCREMENT the sources count
- If creating: Use the template structure below
- ALWAYS: Include the claims verification table with statuses
- ALWAYS: Update "Last updated" date and "Sources consumed" count

### 6. Archive Each Consumed Raw Doc
- Zip each original to `archive/[category]-[date].zip`
- Delete the original from the research dir
- The meta-doc is now the canonical source

### 7. Log
Note what you consumed in the cycle log.
```

## Rules
- Max 3 docs per cycle (~100K tokens budget)
- VERIFY every main claim — don't skip this
- Meta-docs GROW over time — append, don't replace
- Archive originals after consuming — dirs should shrink
- If a claim can't be verified, mark it UNVERIFIED not VERIFIED
- Re-verify meta-doc claims every 14 days
