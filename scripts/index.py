#!/usr/bin/env python3
"""Index research directories — reads config from plugin data dir."""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

def load_config():
    """Load config from plugin data dir or skill dir."""
    for p in [
        Path(os.environ.get("CLAUDE_PLUGIN_DATA", "")) / "config.json",
        Path(__file__).parent.parent / "skills" / "research-consume" / "config.json",
        Path.cwd() / "config.json",
    ]:
        if p.exists():
            return json.loads(p.read_text())
    print("No config found. Run /claude-research-pipeline:research-setup first.")
    return None

CATEGORIES = {
    "ai-models": ["model", "llm", "gpt", "benchmark", "training", "inference"],
    "iot-protocols": ["mqtt", "iot", "zigbee", "ble", "coap", "broker"],
    "translation": ["translation", "multilingual", "speech", "nllb"],
    "social-media": ["social", "viral", "moltbook", "twitter", "marketing"],
    "revenue": ["revenue", "product", "sell", "pricing", "monetiz"],
    "infrastructure": ["docker", "cloudflare", "worker", "pwa", "server"],
    "agent": ["agent", "hermes", "plugin", "memory", "delegation"],
    "security": ["security", "auth", "encrypt", "vulnerability"],
}

def categorize(title, preview):
    text = (title + " " + preview).lower()
    scores = {cat: sum(1 for kw in kws if kw in text) for cat, kws in CATEGORIES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"

def scan(config):
    raw, meta, archives = [], [], []
    for d in config.get("research_dirs", []):
        dp = Path(d)
        if not dp.exists():
            continue
        for f in sorted(dp.glob("*.md")):
            if f.name.startswith(("research-log", "MEMORY", "RESEARCH-")):
                continue
            try:
                content = f.read_text(errors="replace")
                m = re.search(r'^#\s+(.+)', content, re.MULTILINE)
                title = m.group(1).strip() if m else f.stem.replace("-", " ").title()
                raw.append({"path": str(f), "title": title, "size": f.stat().st_size,
                           "category": categorize(title, content[:500])})
            except Exception as e:
                print(f"  Error: {f}: {e}")

    md = Path(config.get("meta_dir", ""))
    if md.exists():
        for f in sorted(md.glob("*.md")):
            meta.append({"path": str(f), "title": f.stem, "size": f.stat().st_size})

    ad = Path(config.get("archive_dir", ""))
    if ad.exists():
        archives = list(ad.glob("*.zip"))

    by_cat = defaultdict(int)
    for d in raw:
        by_cat[d["category"]] += 1

    print("Research Pipeline Status")
    print("=" * 40)
    print(f"  Raw docs:    {len(raw)} ({sum(d['size'] for d in raw) / 1024:.0f} KB)")
    print(f"  Meta docs:   {len(meta)} ({sum(d['size'] for d in meta) / 1024:.0f} KB)")
    print(f"  Archives:    {len(archives)}")
    if by_cat:
        print("\nRaw docs by theme:")
        for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
            print(f"  {cat:20} {count:3}")
    if raw:
        print("\nNext to consume:")
        for d in sorted(raw, key=lambda x: -x["size"])[:3]:
            print(f"  {d['size']/1024:.1f}KB  {d['title'][:60]}")

if __name__ == "__main__":
    config = load_config()
    if config:
        scan(config)
