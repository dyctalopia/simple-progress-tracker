#!/usr/bin/env python3
"""
Sync schedule.md → index.html

Usage:
    python sync-progress.py
    python sync-progress.py --watch   # watch for changes and auto-sync
"""

import re
import sys
from pathlib import Path

SCHEDULE_MD = Path(__file__).parent.parent / "schedule.md"
HTML_FILE   = Path(__file__).parent.parent / "index.html"


def extract_title_and_phases(md_path: Path):
    """Parse title and phases from schedule.md."""
    text = md_path.read_text(encoding="utf-8")

    # Extract first # heading as page title
    h1_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    page_title = h1_match.group(1).strip() if h1_match else "Project Timeline"

    # Parse phases: [*] Phase name    startDate: 5/22    endDate: 5/23
    phases = []
    for line in text.splitlines():
        m = re.search(
            r"\[\s*(\*| )\]\s*(.+?)\s+startDate:\s*(\S+)\s+endDate:\s*(\S+)",
            line
        )
        if m:
            checked, title = m.group(1), m.group(2).strip()
            phases.append({
                "title": title,
                "startDate": m.group(3),
                "endDate": m.group(4),
            })

    return page_title, phases


def phases_to_js(phases):
    """Generate phases JavaScript array content."""
    items = []
    for p in phases:
        items.append(f'        {{ title: "{p["title"]}", startDate: "{p["startDate"]}", endDate: "{p["endDate"]}" }}')
    return ",\n".join(items)


def sync(html_path: Path, title: str, phases_js: str):
    """Inject title and phases into index.html."""
    content = html_path.read_text(encoding="utf-8")

    # 1. Inject PAGE_TITLE
    content = re.sub(
        r"var\s+PAGE_TITLE\s*=\s*['\"][^'\"]*['\"]",
        f'var PAGE_TITLE = "{title}"',
        content
    )

    # 2. Update CONFIG.phases block
    content = re.sub(
        r"<!-- PHASES_START -->.*?<!-- PHASES_END -->",
        f"<!-- PHASES_START -->\n        {phases_js.strip()}\n        <!-- PHASES_END -->",
        content,
        flags=re.DOTALL
    )

    html_path.write_text(content, encoding="utf-8")
    print(f"[sync]  ✓  Title: {title}")
    print(f"[sync]  ✓  Phases: {len(phases_js.splitlines())} items")


def main():
    title, phases = extract_title_and_phases(SCHEDULE_MD)
    phases_js = phases_to_js(phases)
    sync(HTML_FILE, title, phases_js)


if __name__ == "__main__":
    main()