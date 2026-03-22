---
name: research-consume
description: Use when research documents need processing into verified meta-knowledge. Triggers when raw docs accumulate or at each work cycle.
---

# Research Consume — Process Raw Docs Into Meta-Knowledge

<overview>
Consume research documents into verified, growing meta-research papers. Every claim gets verified. Originals get archived. Meta-docs are the living knowledge base.
</overview>

<setup>
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
</setup>

<workflow>
## Per-Cycle Workflow (FOLLOW THIS EXACTLY)

### Step 1: Index & Categorize
List all raw `.md` docs across configured research directories. Group them by category (ai-models, infrastructure, revenue, agent, iot-protocols, social-media, etc.).

### Step 2: Pick ONE Category
Choose the category with the most unprocessed raw docs. You will process up to 3 docs from this SAME category. All docs in a batch go into the SAME meta-doc.

### Step 3: Read Existing Meta-Doc FIRST
<critical>
BEFORE reading any raw doc, check if `meta/[category].md` exists.
- If YES: Read it fully FIRST. Understand what you already know. What claims are already verified? What gaps exist? What's the current structure? You are building ON TOP of this.
- If NO: You will create it fresh after reviewing the raw docs.

This is the most important step. The meta-doc is your existing knowledge. The raw docs are new information to integrate. You MUST know what you have before you read what's new.
</critical>

### Step 4: Read Raw Docs (max 3)
For each raw doc in the selected category:

<per-document>
a) Read the full raw doc
b) Compare against what's already in the meta-doc — what's genuinely NEW?
c) Extract 3-5 key factual claims that ADD to or CORRECT the meta-doc
d) Verify the top 3 new claims:
   - Use WebSearch to find corroborating sources
   - Use WebFetch to read authoritative pages if needed
   - Search academic papers if the claim is technical/scientific
e) Note contradictions with existing meta-doc claims
</per-document>

<verification-states>
Assign each claim a status:

| Status | Criteria | Confidence |
|--------|----------|------------|
| VERIFIED | 2+ independent sources confirm | >= 0.8 |
| LIKELY | 1 authoritative source confirms | 0.6-0.8 |
| UNVERIFIED | No sources found | 0.3-0.6 |
| DISPUTED | Sources contradict each other | < 0.3 |
| OUTDATED | Was true, may no longer be | needs re-check |
| RETRACTED | Confirmed false, kept for audit | 0.0 |
</verification-states>

### Step 5: Update Meta-Doc
<meta-doc-rules>
- If UPDATING existing: APPEND new sections, UPDATE claims table, INCREMENT sources count, UPDATE "Last updated" date
- If CREATING new: Use the template below
- NEVER delete existing verified content — only add, correct, or mark outdated
- Resolve contradictions: keep the better-sourced claim, note the conflict
- Compress: high-value information density, no filler
</meta-doc-rules>

<template>
```markdown
# Meta-Research: [Theme]

**Last updated**: [date]
**Sources consumed**: [count] ([list filenames])
**Status**: Growing

---

## Core Findings
[Compressed, verified, high-value knowledge]

## Claims & Verification
| Claim | Status | Confidence | Source |
|-------|--------|------------|--------|
[all claims with verification status]

## Actionable Insights
[What to do with this knowledge — specific to our stack/goals]

## Gaps & Next Research
[What's still unknown, what needs deeper investigation]
```
</template>

### Step 6: Archive Originals
For each consumed raw doc:
- Zip to `archive/[category]-[date].zip`
- Delete the original from the research dir
- The meta-doc is now the canonical source

### Step 7: Log
Note what you consumed in the cycle log.
</workflow>

<rules>
## Rules
- Max 3 docs per cycle (~100K tokens budget)
- ALWAYS batch by category — same-theme docs go into same meta-doc
- ALWAYS read existing meta-doc before raw docs
- VERIFY every main claim — don't skip this step
- Meta-docs GROW over time — append, don't replace
- Archive originals after consuming — research dirs should SHRINK
- If a claim can't be verified, mark it UNVERIFIED not VERIFIED
- Re-verify meta-doc claims every 14 days
- When dispatching agents: include the meta-doc content AND raw doc content in the prompt
</rules>
