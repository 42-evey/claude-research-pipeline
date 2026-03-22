---
name: research-consume
description: Use when research documents need processing into verified meta-knowledge. Triggers when raw docs accumulate or at each work cycle.
---

# Research Consume — Process Raw Docs Into Meta-Knowledge

<overview>
Consume research documents into verified, growing meta-research papers. Every claim gets verified. Originals get archived. Meta-docs are the living knowledge base.

Based on the Karpathy autoresearch pattern (verified: Fortune, VentureBeat, 26K GitHub stars):
- **Editable asset**: The meta-doc is the asset that improves with each cycle
- **Scalar metric**: Claims verified count, depth/accuracy scores, compression ratio (raw bytes consumed vs meta-doc growth)
- **Time box**: Max 3 docs per cycle, ~100K tokens budget, 8 min per doc

Each cycle: read what you know (meta-doc) → consume what's new (raw docs) → verify claims → improve the asset → archive consumed inputs. The meta-docs compound over time — each cycle makes them more verified, more compressed, more useful.
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

**TIME-SENSITIVE CLAIMS**: Any claim about pricing, free tiers, model availability, API limits, user counts, or market size MUST include the verification date: `VERIFIED (2026-03-22)`. These decay fast — re-verify every 7 days, not 14.
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
| Claim | Status | Confidence | Verified | Source |
|-------|--------|------------|----------|--------|
[all claims — time-sensitive ones MUST have date in Verified column]

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
</rules>

<agent-dispatch>
## Agent Dispatch Rules

**ONE agent per meta-doc. No exceptions.**

When dispatching subagents to consume docs:
- Each agent works on exactly ONE meta-doc (one category)
- If you have 3 docs across 3 categories → dispatch 3 separate agents
- If you have 3 docs in the SAME category → dispatch 1 agent for all 3
- Never have one agent update multiple meta-docs — they will conflict

Each agent's prompt MUST include:
1. The full text of the EXISTING meta-doc (so it knows what's already known)
2. The full text of the raw doc(s) to consume
3. The verification states table
4. The output path for the updated meta-doc
5. The archive commands to run after writing

## Model Tier Strategy (min-max efficiency)

The consume agent MUST be **Opus** — it reads 700+ line meta-docs, synthesizes new findings, resolves contradictions. This is deep reasoning work.

The Opus agent should dispatch its own sub-agents for mechanical tasks:
- **Haiku sub-agents**: Categorize docs, extract basic metadata, format tables
- **Sonnet sub-agents**: Run WebSearch verification, fetch paper abstracts, check URLs
- **Opus (self)**: Read existing meta-doc, compare with new findings, write synthesis, resolve contradictions

This means: dispatch the main consume agent as `model: "opus"`. That agent can internally use the Agent tool to spawn Haiku/Sonnet helpers for the grunt work (web search, data extraction) while it focuses on the thinking.

```
Opus (main agent)
  ├── reads existing meta-doc
  ├── reads raw docs
  ├── dispatches Sonnet → WebSearch verification (parallel)
  ├── dispatches Haiku → format/extract claims (parallel)
  ├── waits for sub-results
  ├── synthesizes everything into updated meta-doc
  └── archives originals
```

**NEVER dispatch the main consume agent as Sonnet or Haiku.** Always Opus.
</agent-dispatch>
