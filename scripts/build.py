#!/usr/bin/env python3
"""Build the complete static website using only Python's standard library."""
import html
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
E = lambda value: html.escape(str(value), quote=True)
def load(name):
    return json.loads((ROOT / 'content' / f'{name}.json').read_text())

profile, cv, projects, publications = [load(x) for x in ('profile', 'cv', 'projects', 'publications')]
publications.sort(key=lambda p: (p['year'], p.get('date', str(p['year'])), p['title']), reverse=True)
seen = set()
for paper in publications:
    assert paper['title'] and paper['authors'] and paper['journal'], 'Incomplete publication'
    assert paper.get('peer_reviewed') is True, f"Peer-review confirmation required: {paper['title']}"
    assert re.fullmatch(r'10\.\d{4,9}/\S+', paper['doi'], re.I), f"Invalid DOI: {paper['doi']}"
    assert paper['url'] == 'https://doi.org/' + paper['doi'], 'Use a canonical DOI link'
    assert paper['doi'].lower() not in seen, f"Duplicate DOI: {paper['doi']}"
    seen.add(paper['doi'].lower())

def inline(text):
    value = E(text)
    return re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', r'<a href="\2">\1</a>', value)

def paras(text):
    return ''.join(f'<p>{inline(p)}</p>' for p in re.split(r'\n\s*\n', text.strip()))

def initials(name):
    if ',' not in name:
        return name
    family, given = name.split(',', 1)
    return family + ', ' + ' '.join(w if re.fullmatch(r'(?:[A-Z]\.){1,5}', w) else ' '.join(c+'.' for c in w) if re.fullmatch(r'[A-Z]{2,5}', w) else w[0] + '.' for w in given.strip().split() if w)

def authors(paper, markup=False):
    names = [initials(n) for n in paper['authors']]
    if markup:
        return ', '.join(f'<strong>{E(n)}</strong>' if n.startswith('Hetland,') else E(n) for n in names)
    return ', '.join(names)

def citation(p):
    extra = p.get('volume', '')
    if p.get('issue'):
        extra += '(' + p['issue'] + ')'
    if p.get('pages'):
        extra += ', ' + p['pages']
    return f"{authors(p)} ({p['year']}). {p['title']}. {p['journal']}" + (f', {extra}' if extra else '') + f". {p['url']}"

def key(p):
    return re.sub('[^a-zA-Z0-9]+', '-', p['doi']).strip('-')

def bibtex(p):
    fields = {'title':p['title'], 'author':' and '.join(p['authors']), 'year':p['year'], 'journal':p['journal'], 'volume':p.get('volume'), 'number':p.get('issue'), 'pages':p.get('pages'), 'doi':p['doi'], 'url':p['url']}
    is_proceedings = p.get('type') == 'proceedings-article'
    if is_proceedings:
        fields['booktitle'] = fields.pop('journal')
    return '@' + ('inproceedings' if is_proceedings else 'article') + '{' + key(p) + ',\n' + ',\n'.join('  ' + k + ' = {' + str(v).replace('{','').replace('}','') + '}' for k,v in fields.items() if v) + '\n}\n'

MARK = '<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true"><path d="M3 12C12 0 24 24 37 9M3 21C12 9 24 33 37 18M3 30C12 18 24 42 37 27" fill="none" stroke="currentColor" stroke-width="2.5"/></svg>'
def social():
    return f'<div class="socials"><a href="{E(profile["scholar"])}">Google Scholar ↗</a><a href="{E(profile["orcid"])}">ORCID ↗</a><a href="{E(profile["github"])}">GitHub ↗</a></div>'

def shell(title, active, body, description=None):
    description = description or profile['bio']
    nav = ''.join(f'<a href="{url}"' + (' aria-current="page"' if active == name else '') + f'>{name}</a>' for name,url in [('Research','/'),('Projects','/projects/'),('Publications','/publications/'),('CV','/cv/')])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} · Rob Hetland</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#163c42"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css"><script src="/assets/site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="Rob Hetland home">{MARK}Rob Hetland<span style="color:var(--orange)">.</span></a><nav class="nav" aria-label="Main navigation">{nav}<a class="contact-link" href="mailto:{E(profile['email'])}">Get in touch ↗</a></nav></div></header>
<main id="main">{body}</main><div class="wrap"><section class="contact-band" aria-label="Contact"><div><h2>Let’s connect.</h2><p>{E(profile['organization'])} · {E(profile['location'])}</p></div><div><p style="margin-bottom:16px"><a href="mailto:{E(profile['email'])}">{E(profile['email'])} ↗</a></p>{social()}</div></section></div><footer class="site-footer"><div class="wrap footer-inner"><span>Rob Hetland · Coastal ocean science</span><div><a href="/archive/2026-11-17/">Previous website ↗</a><a href="https://github.com/hetland/hetland.github.io">Website source ↗</a></div></div></footer></body></html>'''

def paper_html(p, short=False):
    ref = citation(p)
    correction = f' <a href="{E(p["correction_url"])}">Published correction ↗</a>' if p.get('correction_url') else ''
    return f'''<article class="publication" data-year="{p['year']}"><div><h3><a href="{E(p['url'])}">{E(p['title'])}</a></h3><p class="authors">{authors(p,True)}</p><p class="journal">{E(p['journal'])} · {p['year']}{correction}</p>''' + ('' if short else f'''<details class="citation"><summary>Citation &amp; DOI</summary><p>{E(ref)}</p><button class="copy-button" data-copy="{E(ref)}">Copy citation</button></details>''') + f'''</div><div class="paper-actions"><a href="{E(p['url'])}" aria-label="Read {E(p['title'])}">Read ↗</a>''' + ('' if short else f'<a href="/publications/bib/{key(p)}.bib" download aria-label="Download BibTeX for {E(p["title"])}">.bib ↓</a>') + '</div></article>'

def ocean():
    paths = []
    import math
    for k in range(27):
        points = []
        for i in range(161):
            x = -45 + i * 3.8
            y = 35 + k * 16 + 27 * math.sin(x / 98 + k * .09) + 50 * math.exp(-((x-270)/120)**2) * math.sin(k*.24)
            points.append(f'{x:.1f},{y:.1f}')
        paths.append(f'<polyline points="{" ".join(points)}" stroke="{["#517a75","#6f9a8d","#adbd9f","#d1c89c"][k//7%4]}" opacity=".75"/>')
    return '''<figure class="ocean-figure"><svg viewBox="0 0 500 478" role="img" aria-labelledby="ocean-title ocean-desc"><title id="ocean-title">A conceptual coastal flow field</title><desc id="ocean-desc">Curved contour lines and an eddy illustrate the interaction of coastal circulation and mixing. This is a conceptual illustration, not observational data.</desc><defs><clipPath id="plot"><rect width="500" height="478" rx="3"/></clipPath><radialGradient id="glow"><stop stop-color="#448778" stop-opacity=".35"/><stop offset="1" stop-color="#153c40" stop-opacity="0"/></radialGradient></defs><g clip-path="url(#plot)"><rect width="500" height="478" fill="#153c40"/><circle cx="290" cy="230" r="260" fill="url(#glow)"/><g fill="none" stroke-width=".9">''' + ''.join(paths) + '''</g><path d="M-30 20C110 100 128 88 140 170S115 274 165 310S180 390 120 500L-30 500Z" fill="#d3d9bd"/><path d="M-30 20C110 100 128 88 140 170S115 274 165 310S180 390 120 500" fill="none" stroke="#f1e4b9" stroke-width="2"/><g fill="none" stroke="#b5cba9" stroke-width="1" opacity=".85"><ellipse cx="320" cy="245" rx="91" ry="58" transform="rotate(-35 320 245)"/><ellipse cx="320" cy="245" rx="72" ry="44" transform="rotate(-35 320 245)"/><ellipse cx="320" cy="245" rx="51" ry="30" transform="rotate(-35 320 245)"/><ellipse cx="320" cy="245" rx="29" ry="17" transform="rotate(-35 320 245)"/></g><g fill="#e7e8cc" font-family="sans-serif" font-size="9" letter-spacing="1.5"><text x="29" y="35">COASTAL DYNAMICS</text><text x="26" y="442" fill="#163c42">LAND</text><text x="388" y="442">OPEN OCEAN</text></g><g stroke="#d9e2cc" stroke-width="1"><path d="M450 34v32m-5-26 5-7 5 7"/><path d="M232 395h60m-7-4 7 4-7 4"/></g><text x="446" y="83" fill="#d9e2cc" font-size="9" font-family="sans-serif">N</text><circle cx="320" cy="245" r="3" fill="#e5b780"/></g></svg><figcaption><span>Circulation · fronts · mixing</span><span>Conceptual illustration</span></figcaption></figure>'''

def home():
    summaries = [
        'Coupling the atmosphere, lakes, and watersheds to understand how freshwater coasts respond to a changing climate.',
        'Connecting coastal development, hydrology, and biogeochemistry through integrated models and rigorous comparisons.',
        'Resolving how near-inertial motions, submesoscale fronts, and turbulence exchange water in the upper ocean.'
    ]
    cards = ''.join(f'<article class="project-card"><span class="number">0{i+1} / RESEARCH PROJECT</span><h3>{E(p["title"])}</h3><p>{summaries[i]}</p><a class="text-link" href="/projects/#{["compass-glm","icom","sunrise"][i]}">Explore project <span>↗</span></a></article>' for i,p in enumerate(projects))
    return shell('Coastal ocean science', 'Research', f'''<div class="wrap"><section class="hero"><div><div class="eyebrow">Coastal ocean science</div><h1>Understanding<br>a changing<br><span>coastal ocean.</span></h1><p class="hero-intro">I’m Rob Hetland. I use analytical and numerical models to understand how water moves, mixes, and shapes coastal ecosystems.</p><div class="buttons"><a class="button primary" href="/publications/">Explore publications <span>↗</span></a><a class="button" href="/projects/">Research projects <span>↗</span></a></div><div class="person"><img src="/assets/rob.jpeg" alt="Rob Hetland" width="52" height="52"><div><strong>{E(profile['name'])}</strong><small>{E(profile['role'])}<br>Pacific Northwest National Laboratory</small></div></div></div>{ocean()}</section><div class="topic-strip"><b>RESEARCH FOCUS</b><span>Estuaries &amp; river plumes</span><span>Transport &amp; mixing</span><span>Coastal ecology</span><span>Numerical modeling</span></div><section class="section research-overview"><div><div class="eyebrow">A connected coast</div><h2>From physical processes<br>to coastal ecosystems.</h2></div><p>{E(profile['bio'])}</p></section></div><section class="tint"><div class="wrap section"><div class="section-heading"><div><div class="eyebrow">Research in practice</div><h2>Projects &amp; collaborations</h2></div><a class="text-link" href="/projects/">View all projects <span>↗</span></a></div><div class="project-grid">{cards}</div></div></section><div class="wrap section"><div class="section-heading"><div><div class="eyebrow">Recent work</div><h2>Latest publications</h2></div><a class="text-link" href="/publications/">All {len(publications)} publications <span>↗</span></a></div>{''.join(paper_html(p,True) for p in publications[:3])}</div>''')

def publications_page():
    groups = defaultdict(list)
    for p in publications:
        groups[p['year']].append(p)
    years = ''.join(f'<option value="{year}">{year}</option>' for year in groups)
    rows = ''.join(f'<section class="publication-year" aria-labelledby="year-{year}"><h2 id="year-{year}">{year}</h2><div>{"".join(paper_html(p) for p in papers)}</div></section>' for year,papers in groups.items())
    return shell('Publications','Publications',f'''<div class="wrap"><header class="page-head"><div class="eyebrow">Research library</div><h1>Publications</h1><p>Peer-reviewed research on coastal circulation, mixing, and the ecosystems they sustain.</p><div class="buttons"><a class="button" href="/publications/publications.bib" download>Download all BibTeX ↓</a><a class="button" href="{E(profile['scholar'])}">Google Scholar ↗</a></div></header><div class="filters"><label for="publication-search">Search publications<input type="search" id="publication-search" placeholder="Title, author, journal, or keyword…" autocomplete="off"></label><label for="publication-year">Year<select id="publication-year"><option value="">All years</option>{years}</select></label><button class="button" id="clear-filters">Clear filters</button></div><div class="results-meta"><span id="result-count" role="status" aria-live="polite">{len(publications)} publications</span><p>Newest first · {min(groups)}–{max(groups)} · Every paper links to its DOI</p></div><p class="no-results" id="no-results" hidden>No publications match. Try another keyword or clear the filters.</p>{rows}<p class="note">This list includes peer-reviewed journal articles and reviewed proceedings papers. Meeting abstracts, preprints, editorials, and reports are excluded. DOI metadata checked November 17, 2026. <a href="/publications/sources.html">Sources &amp; selection notes</a>.</p></div>''')

def projects_page():
    labels = ['Great Lakes · Coupled climate systems','Integrated coastal modeling · Model evaluation','Gulf of Mexico · Fronts & turbulence']
    ids = ['compass-glm','icom','sunrise']
    rows = ''.join(f'<article class="project-detail" id="{ids[i]}"><div><span class="project-label">0{i+1} / {E(labels[i])}</span><h2>{E(p["title"])}</h2></div><div class="project-copy">{paras(p["body"])}</div></article>' for i,p in enumerate(projects))
    return shell('Projects','Projects',f'<div class="wrap"><header class="page-head"><div class="eyebrow">Research in practice</div><h1>Projects &amp; collaborations</h1><p>Connecting fundamental coastal physics with the models we use to understand and predict environmental change.</p></header>{rows}</div>')

def cv_page():
    links, sections = [], []
    for i,(name,entries) in enumerate(cv.items()):
        links.append(f'<a href="#cv-{i}">{E(name)}</a>')
        rows = ''.join(f'<div class="cv-entry"><time>{E(p["dates"])}</time><div><h3>{E(p["title"])}</h3><p>{E(p["organization"])}</p><small>{E(p.get("detail",""))}</small></div></div>' for p in entries)
        sections.append(f'<section class="cv-section" id="cv-{i}"><h2>{E(name)}</h2>{rows}</section>')
    return shell('Curriculum vitae','CV',f'''<div class="wrap"><header class="page-head"><div class="eyebrow">Background &amp; experience</div><h1>Curriculum vitae</h1><p>{E(profile['name'])}<br>{E(profile['role'])}<br>{E(profile['organization'])}</p><p class="cv-print-header">{E(profile['email'])} · hetland.github.io · ORCID 0000-0001-9531-2119</p><div class="buttons"><button class="button primary" data-print>Print / save CV as PDF ↓</button><a class="button" href="/publications/">Peer-reviewed publications ↗</a></div></header><div class="cv-layout"><aside class="cv-aside" aria-label="CV sections">{''.join(links)}<a href="/publications/">Publications ↗</a></aside><div>{''.join(sections)}</div></div><section class="cv-publications"><h2>Peer-reviewed publications</h2><ol>{''.join('<li>'+E(citation(p))+'</li>' for p in publications)}</ol></section></div>''')

def write(path, data):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(data)

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT/'assets', OUT/'assets')
    if (ROOT/'archive').exists():
        shutil.copytree(ROOT/'archive',OUT/'archive')
    write('.nojekyll','')
    write('index.html',home())
    write('publications/index.html',publications_page())
    write('projects/index.html',projects_page())
    write('cv/index.html',cv_page())
    write('publications/publications.bib','\n'.join(bibtex(p) for p in publications))
    for p in publications:
        write(f'publications/bib/{key(p)}.bib',bibtex(p))
    # A machine-readable copy supports reuse without client-side rendering.
    write('publications/publications.json',json.dumps(publications,ensure_ascii=False,indent=2)+'\n')
    note = (ROOT/'content/publication-notes.html').read_text() if (ROOT/'content/publication-notes.html').exists() else ''
    write('publications/sources.html',shell('Publication sources','Publications','<div class="wrap"><header class="page-head"><div class="eyebrow">Research library</div><h1>Sources &amp; selection</h1></header><div class="plain-content">'+note+'</div></div>'))
    for alias,target in {'about':'/','about.html':'/','projects.html':'/projects/','publications.html':'/publications/','resume':'/cv/','resume.html':'/cv/','cv.html':'/cv/'}.items():
        path = alias if '.' in alias else alias+'/index.html'
        write(path,f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Rob Hetland</title><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="https://hetland.github.io{target}"><a href="{target}">Continue to Rob Hetland’s website</a></html>')
    write('404.html',shell('Page not found','', '<div class="wrap"><header class="page-head"><div class="eyebrow">404</div><h1>A little off course.</h1><p>The page you’re looking for may have moved. You can return to the research overview or explore the previous website.</p><div class="buttons"><a class="button primary" href="/">Back to research ↗</a><a class="button" href="/archive/2026-11-17/">Previous website ↗</a></div></header></div>'))
    write('robots.txt','User-agent: *\nAllow: /\nDisallow: /archive/\nSitemap: https://hetland.github.io/sitemap.xml\n')
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://hetland.github.io'+p+'</loc></url>' for p in ['/','/projects/','/publications/','/cv/'])+'</urlset>')
    print(f'Built {len(publications)} linked publications and all pages in {OUT}')

if __name__ == '__main__':
    build()
