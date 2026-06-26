## Simple Progress Tracker v1.0.3

A lightweight, self-contained project timeline tracker — single HTML file, no build step required.

### Changelog
- **v1.0.3**: 加入 ✎ 編輯模式——可直接在頁面新增 / 刪除 / 修改任務名稱與日期，並透過 Flask server (`server.py`) 持久化至 `progress.json`。無 server 時自動降級為唯讀展示頁（GitHub Pages / `file://` 適用）。
- **v1.0.2**: 當某任務被選為當前階段時，之前的任務顯示『完成 ✓』樣式


Live demo: https://dyctalopia.github.io/simple-progress-tracker/

---

## Features

- **Visual phase timeline** — cards arranged in a responsive timeline layout
- **Status-aware coloring**:
  - 🟢 Green — current phase, N days remaining
  - � Yellow — current phase, ≤2 days remaining (warning)
  - 🔴 Red — overdue
  - ⬜ Gray — completed or pending
- **Interactive progress** — click a card to mark that phase as "done"; progress persists in `localStorage`
- **Dark theme** — low-eye-strain dark UI
- **Date-driven** — no manual status editing; the JS computes everything from `startDate` / `endDate`

---

## File Structure

```
simple-progress-tracker/
├── index.html          # Full application (HTML + CSS + JS, all-in-one)
├── schedule.md         # Phase data source (edit this, then run sync)
├── sync-progress.py    # Script to sync schedule.md → index.html
└── README.md
```

---

## Usage

### 1. Edit phases

Open `schedule.md` and update the phase list:

```
[*] Phase 1    startDate: 5/22    endDate: 5/23
[ ] Phase 2    startDate: 5/28    endDate: 6/15
```

- `[*]` marks the current (active) phase
- `[ ]` marks upcoming phases
- Dates use `M/D` format; the current year is inferred automatically

### 2. Sync to HTML

```bash
python sync-progress.py
```

This injects the updated title and phase data into `index.html`.

### 3. Deploy (GitHub Pages — static read-only mode)

When served from GitHub Pages or any plain static host, the page automatically detects that no local server is available and falls back to the built-in default phases defined inside `index.html` (see `CONFIG.phases`). The Edit button is disabled in this mode.

```bash
git push origin main
```

Visit `https://<your-username>.github.io/simple-progress-tracker/` to see the live demo.

### 4. Local editable mode (optional)

For local use with the ✎ editor enabled:

```bash
python server.py
# then open http://localhost:5000
```

The server serves `index.html` and exposes `/data` (read) and `/save`, `/reset` (write) endpoints that persist to `progress.json` in the repo root. The editor lets you add, remove, rename, and re-date phases from the page.

---

## How it works

The tracker reads the current date, compares it to each phase's `startDate`/`endDate`, and classifies each phase:

| Condition | Status |
|-----------|--------|
| Phase is before the checked index | `done` (gray) |
| `today` is within phase dates, >2 days left | `current` (green) |
| `today` is within phase dates, ≤2 days left | `warning` (yellow) |
| Phase end date has passed | `urgent` (red) |
| Phase is after the checked index | `pending` (gray) |

State is saved to `localStorage` under the key `simple-progress-tracker-checked`, so closing the tab won't lose your position.

> **v1.0.3 note:** The Edit-mode UI relies on `localStorage` (`tnl-oral-edit-mode`, `tnl-oral-edit-draft`) for in-progress edits and falls back to the in-page default when no `progress.json` is reachable.

---

## Customization

There are two ways to update the visible phases:

1. **Quick demo / static deploy**: edit `CONFIG.phases` in `index.html` and re-deploy.
2. **Local editable workflow**: run `python server.py`, then click ✎ Edit and persist via Save → `progress.json`.

For bulk updates from a markdown spec, edit `schedule.md` and re-run `sync-progress.py`.
