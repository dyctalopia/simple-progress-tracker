# Project Timeline v1.0.4

Lightweight, self-contained project timeline tracker — supports multiple projects in a single page, with optional Flask persistence for tri-and-edit workflows.

Live demo (read-only, GitHub Pages): https://dyctalopia.github.io/simple-progress-tracker/

## Features

- **Multiple projects in one view** — add, remove, rename and re-date projects and their phases side by side; the timeline visually highlights overlapping windows across projects.
- **Date-driven status** — current phase, ≤2 days left, overdue, completed, and pending states are computed automatically from each phase's `startDate` / `endDate`.
- **Inline editor** — click **✎ Edit** to add / remove / rename / re-date phases. Persist back to `progress.json` via the included Flask server.
- **Dark theme** — minimal dark UI designed for long-running dashboards.
- **Pure HTML + JS** — no build step, no framework, no client-side bundle. Runs from `file://`, GitHub Pages, or behind the bundled Flask server.

## File structure

```
simple-progress-tracker/
├── index.html            # Front-end page (rename from progress-tracker.html)
├── server.py             # Flask server — reads/writes progress.json
├── tracker.bat           # One-click launcher (Windows)
├── progress.json         # Data file (rewritten by server)
└── README.md
```

## Usage

### Option A — Static / read-only (GitHub Pages or `file://`)

Open `index.html` directly. The page loads the built-in default project (defined inside the `CONFIG` block in `index.html`). Editing is supported but writes only persist in `localStorage`; for cross-session persistence set up the Flask server below.

### Option B — Editable with persistence (local Flask server)

```bash
python server.py
# or, on Windows, double-click tracker.bat
```

The server binds to `http://127.0.0.1:5050/` by default (override with `--port NNNN`) and serves:

- `GET /progress.json` — read current progress
- `POST /save` — persist the editor payload to `progress.json`

Open the page in your browser, click **✎ Edit**, modify phases, click **💾 Save**, and the server writes the changes straight to `progress.json` on disk. Refresh the page to confirm.

## Status

| Condition | Visual |
|-----------|--------|
| Phase before the checked index | Gray, ✓ Done |
| `<= 2` days from end date | Yellow, "Left: N" |
| Active phase, more than 2 days from end | Green, "Left: N" |
| Past end date, not yet checked as complete | Red, "Overdue: N" |
| After the checked index | Gray, "Planned: N days" |

Click a card to set/clear it as the current phase; the choice persists in `localStorage` per browser profile.

## Requirements

- Python 3.9+
- Flask (`pip install flask`)

## License

MIT — see repo for full text.
