# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small Django site for a wedding RSVP: a single scrolling invitation page (`/`) with a guest questionnaire form, a thank-you page, and a live stats/dashboard page for the couple. Russian-language content throughout (models, forms, templates).

## Commands

Activate the venv first (Windows):
```
venv\Scripts\activate
```

Common commands (run from the repo root, same directory as `manage.py`):
```
python manage.py runserver              # dev server at http://127.0.0.1:8000/
python manage.py makemigrations rsvp    # after changing rsvp/models.py
python manage.py migrate                # apply migrations to db.sqlite3
python manage.py createsuperuser        # to use /admin/
python manage.py collectstatic          # populate staticfiles/ (see gotcha below)
python manage.py test rsvp              # run tests (rsvp/tests.py is currently empty)
```

There is no JS build step, linter, or formatter configured — this is plain Django + hand-written CSS/HTML in templates, plus one CDN script (Chart.js) on the stats page.

## Architecture

Single Django app (`rsvp`) inside project `wedding`. Three views, three templates, one model:

- `rsvp/views.py`
  - `index` — renders/handles the RSVP form (`rsvp/forms.py::RSVPForm`, a `ModelForm`). On valid POST, saves a `RSVPResponse` and redirects to `success`.
  - `success` — static thank-you page.
  - `stats` — aggregates `RSVPResponse` rows (counts, per-drink tally) for `rsvp/templates/rsvp/stats.html`, which renders them with Chart.js.
- `rsvp/models.py::RSVPResponse` — `name`, `attendance` (yes/no choice), `drinks` (a **comma-joined string**, not a proper M2M/array field — the form's `CheckboxSelectMultiple` list is joined with `', '` on save in `views.py` and split back on `', '` in `stats`). Keep that join/split convention in sync if you touch either side.
- `rsvp/templates/rsvp/index.html` — the entire invitation page: one `<style>` block, no separate CSS file. Built as a vertical stack of full-bleed `<section>`s, each sized via `aspect-ratio` and a `background-image` static asset (`rsvp/static/images/*.png`) matching a fixed mobile frame (393×852, i.e. iPhone 14/15 Pro), with text absolutely positioned in percentages on top of the photo. When adjusting a section's copy/layout, check the corresponding background PNG first — most positioning is tuned by eyeballing where the photo's blank/sky/cardstock areas are, not from any design tokens.
- `rsvp/templates/rsvp/stats.html` — self-contained dashboard: stat cards + two Chart.js charts (drinks bar chart, attendance doughnut) + a full response table. Chart data reaches the page via Django's `json_script` template filter (`{{ drinks_labels|json_script:"..." }}`), then `JSON.parse`d in inline JS. **Don't `json.dumps()` the context values in `views.py` before passing them** — `json_script` already serializes; double-serializing turns the list into a string that Chart.js then reads character-by-character (see the comment in `views.py::stats`).

## Gotchas specific to this repo

- **Static files under gunicorn vs `runserver`.** `runserver` serves `STATICFILES_DIRS` automatically; a bare gunicorn process does not unless a route is wired up. `wedding/urls.py` adds `staticfiles_urlpatterns()` to `urlpatterns` when `settings.DEBUG` is `True` specifically so gunicorn also serves static assets straight from `rsvp/static/` without needing `collectstatic`. If `DEBUG` is ever turned off for a real deployment, static serving needs a real solution (whitenoise/nginx) — right now nothing else serves `/static/`.
- **`STATIC_ROOT` (`staticfiles/`) can go stale.** It's a `collectstatic` output, gitignored, and not auto-synced when you add/rename files under `rsvp/static/images/`. If something is served from there instead of `runserver`'s live static serving, missing images mean `collectstatic` hasn't been rerun.
- **`requirements.txt` and `.gitignore` are UTF-16-encoded**, not UTF-8 — evidently written by a PowerShell `>` redirect without `-Encoding utf8`. Tools that assume UTF-8 will misread them. When regenerating `requirements.txt` (e.g. `pip freeze`), redirect with explicit UTF-8 encoding or the file will round-trip as UTF-16 again.
- **`db.sqlite3` is gitignored** (along with `venv/`, `__pycache__/`, `*.pyc`, and `staticfiles/`). Real guest RSVP data lives only in this local file; there's no seed/fixture data, so a fresh clone starts with an empty stats page until `migrate` is run and the form is submitted a few times.
