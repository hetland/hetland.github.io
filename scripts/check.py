#!/usr/bin/env python3
"""Validate generated links and bibliography without a browser or network."""
import json
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'dist'
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for key in ('href','src'):
            if a.get(key):self.links.append(a[key])

errors=[]
files=list(OUT.rglob('*.html'))
cache={}
for path in files:
    if 'archive' in path.relative_to(OUT).parts:continue
    parser=Links();parser.feed(path.read_text());cache[path]=parser
for path,parser in cache.items():
    for url in parser.links:
        u=urllib.parse.urlsplit(url)
        if u.scheme or u.netloc:continue
        target = OUT/u.path.lstrip('/') if u.path.startswith('/') else path.parent/u.path
        if not u.path:target=path
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{path.relative_to(OUT)} -> missing {url}')
        elif u.fragment and 'archive' not in target.relative_to(OUT).parts:
            dest=cache.get(target)
            if dest and u.fragment not in dest.ids:errors.append(f'{path.relative_to(OUT)} -> missing fragment {url}')
papers=json.loads((ROOT/'content/publications.json').read_text())
page=(OUT/'publications/index.html').read_text()
assert page.count('class="publication"')==len(papers)
assert len(list((OUT/'publications/bib').glob('*.bib')))==len(papers)
assert all(p['url'] in page for p in papers)
assert (OUT/'archive/2026-11-17/index.html').exists()
if errors:raise SystemExit('\n'.join(errors))
print(f'OK: {len(cache)} generated pages, {len(papers)} DOI-linked papers, individual BibTeX files, and local links.')
