# Project Timeline v1.0.4

## Features

- **Multiple projects in one view** — all timelines visible simultaneously; overlap conflicts are computed automatically from date ranges.
- **Date-driven status** — current, warning (≤2 days left), overdue, done, and planned states are computed from each phase's `startDate` / `endDate`.
- **Inline editor** — click **✎ Edit** to add / remove / rename / re-date phases. Persist back to `progress.json` via the bundled Flask server.
- **Dark theme** — minimal dark UI for long-running dashboards.
- **Pure HTML + JS** — no build step, no framework. Runs from `file://`, GitHub Pages, or behind the Flask server.

## File structure

```
simple-progress-tracker/
├── index.html            # Front-end (single file, all-in-one)
├── server.py             # Flask server — serves page, reads/writes progress.json
├── tracker.bat           # One-click launcher (Windows)
├── progress.json         # Data store (written by server)
└── README.md
```

## Usage

### Static / read-only (GitHub Pages or `file://`)

Open `index.html` directly. The page loads the built-in default project (defined in the `CONFIG` block). Editing is disabled in this mode.

### Editable with persistence (local Flask server)

```bash
pip install flask
python server.py
# or double-click tracker.bat (Windows)
```

Server binds to `http://127.0.0.1:5050/`, auto-opens browser.

Endpoints:
- `GET /progress.json` — read current progress
- `POST /save` — persist editor payload to `progress.json`

Click **✎ Edit**, make changes, click **💾 Save**, and the server writes changes to `progress.json` on disk.

## Status rules

| Condition | Visual |
|-----------|--------|
| Before checked index | Gray, ✓ Done |
| ≤2 days from end | Yellow, "Left: N" |
| Active phase, >2 days from end | Green, "Left: N" |
| Past end date, not yet done | Red, "Overdue: N" |
| After checked index | Gray, "Planned: N days" |

## Requirements

- Python 3.9+
- Flask (`pip install flask`)

## License

MIT