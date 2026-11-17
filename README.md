# Rob Hetland’s website

A small, fast static website. Content is separate from design. There is no framework, JavaScript package installation, Ruby, database, subscription, or theme to maintain. Python 3.9+ builds the pages using its standard library. All research content is readable without JavaScript; JavaScript adds publication filtering, citation copying, and printing.

## Update your CV

1. Open [`content/cv.json`](content/cv.json) on GitHub and click the pencil.
2. Edit an entry or copy an existing entry to add one. Keep commas between entries and double quotes around text.
3. Commit to `master`. GitHub Actions builds and publishes the site automatically.

The online CV and printable CV use this **same file**. Publications are appended automatically when printing the CV. On the CV page choose **Print / save CV as PDF**, then select **Save as PDF** in your browser; turn browser headers and footers off for a clean result. Print layout includes contact details and the complete peer-reviewed publication list.

Example CV entry:

```json
{"dates":"2021–present","title":"Earth Scientist","organization":"Pacific Northwest National Laboratory"}
```

## Add a publication

The only publication source is [`content/publications.json`](content/publications.json). The site sorts it automatically, creates every DOI link, updates the homepage’s recent publications, and generates individual and combined BibTeX downloads. You do not edit HTML or duplicate entries in the CV.

### Recommended: import a DOI

After confirming this is a full peer-reviewed paper, run:

```sh
python3 scripts/add-publication.py 10.5194/gmd-19-10321-2026 --reviewed
```

The importer retrieves publisher-deposited Crossref metadata, rejects duplicate DOIs, checks Hetland is in the deposited author list, and rejects nonarticle types and obvious editorial/correction entries. It needs an internet connection. **You still confirm peer review**: DOI registration and a journal-article label do not by themselves establish it. Inspect the imported title, authors, publication year, and journal before committing.

Then commit `content/publications.json` and push `master`. The website rebuilds automatically.

### Or edit directly in GitHub

Copy a record in `content/publications.json` and fill in the fields. At minimum:

```json
{
  "title": "Full paper title",
  "authors": ["Hetland, Robert D.", "Surname, Given Name"],
  "year": 2026,
  "date": "2026-11-01",
  "journal": "Journal name",
  "doi": "10.xxxx/example",
  "url": "https://doi.org/10.xxxx/example",
  "type": "journal-article",
  "peer_reviewed": true
}
```

Replace the illustrative DOI with a real one. Optional fields: `volume`, `issue`, `pages`, `source_urls`, `correction_url`. Dates are `YYYY-MM-DD` strings. Use `proceedings-article` only for a full paper with confirmed manuscript peer review. Exclude AGU/EGU meeting abstracts, preprints, reports, datasets, and editorials. Publication data and DOI validation must pass before a new version deploys; a failed build leaves the existing live site in place.

## Other changes

| What | Edit |
| --- | --- |
| Bio, contact, affiliation, professional links | `content/profile.json` |
| Detailed project descriptions | `content/projects.json` (simple Markdown links supported) |
| Publication selection notes | `content/publication-notes.html` |
| Typography, colors, responsive and print styles | `assets/style.css` |
| Page structure | `scripts/build.py` |
| Portrait | Replace `assets/rob.jpeg` |

The project descriptions were carried forward from the old website. The CV was updated from the owner-supplied research interests, service, awards, and affiliations on November 17, 2026. Research interests and the homepage focus list can be edited in `content/profile.json`.

## Preview locally

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Rebuild and reload after changing content. Never edit `dist/` directly: it is generated. Build and link checks run in `.github/workflows/publish.yml`; Pages serves the resulting artifact. No API keys or secrets are required. Only `master` publishes; pull requests build and check without deploying.

## Publishing configuration

GitHub repository Settings → Pages → Build and deployment → Source is **GitHub Actions**. The `github-pages` environment must allow deployment from `master`. The canonical public website remains https://hetland.github.io/.

The `.openai/hosting.json` manifest is for the additional private Sites review copy. GitHub Pages does not use it, and future GitHub pushes update the public site independently of that copy.

## Archive and rollback

Before the redesign (November 17, 2026), the default branch was `master` but the live Pages source was `reduce-cruft`. Both were preserved:

- `archive/pre-redesign-2026-11-17`: exact pre-redesign default branch, `818f34261b4373715c66f25a1f28c58a78a60f86`.
- `archive/live-site-2026-11-17`: exact live source, `a8faa22d6528d74f28db73a0a6bc4af4ee6de6bb`.
- `/archive/2026-11-17/`: browsable snapshot of the live site with local assets and original HTML, plus a timestamp/hash manifest. Linked from every page footer. The archive is intentionally excluded from the new site’s sitemap.

To restore the previous live site, change Pages Source back to **Deploy from a branch**, select `archive/live-site-2026-11-17` and `/ (root)`, and Save. The redesign remains in Git history. No force push is necessary.

The publication audit is in `content/publication-audit.md`. The current bibliography contains 103 reviewed papers from 1998–2026, reconciled with all 192 records visible on Google Scholar on November 17, 2026. The old report/book/chapter entries remain in the browsable archive; they are excluded from the current peer-reviewed research list where review status could not be established.
