## Simple Progress Tracker v1.0.1

A lightweight, self-contained project timeline tracker — single HTML file, no build step required.

**Live demo:** https://dannydin.github.io/simple-progress-tracker/

---

## Features

- **Visual phase timeline** — cards arranged in a responsive timeline layout
- **Status-aware coloring**:
  - 🟢 Green — current phase, N days remaining
  - 🟡 Yellow — current phase, ≤2 days remaining (warning)
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

### 3. Deploy

Upload `index.html` to any static host:

- **GitHub Pages** — push to a `gh-pages` branch
- **Netlify / Vercel** — drop the folder
- **Any web server** — just serve the file

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

---

## Customization

To rename phases or change dates, always edit `schedule.md` and re-run `sync-progress.py`. Direct edits to `index.html` will be overwritten on next sync.