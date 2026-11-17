#!/usr/bin/env python3
"""Import a reviewed paper by DOI; no third-party packages required."""
import argparse
import datetime
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('doi', help='DOI or https://doi.org URL')
parser.add_argument('--reviewed', action='store_true', help='Confirm that this is a full peer-reviewed paper, not an abstract or editorial')
args = parser.parse_args()
if not args.reviewed:
    parser.error('Check the publisher confirms peer review, then add --reviewed.')
doi = re.sub(r'^https?://(?:dx\.)?doi\.org/','',args.doi.strip(),flags=re.I)
if not re.fullmatch(r'10\.\d{4,9}/\S+',doi,re.I):
    parser.error('A valid DOI is required.')
path = Path(__file__).resolve().parents[1] / 'content/publications.json'
papers = json.loads(path.read_text())
if any(p['doi'].lower() == doi.lower() for p in papers):
    parser.error('This DOI is already in the list.')
url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi,safe='')
req = urllib.request.Request(url,headers={'User-Agent':'HetlandWebsite/1.0 (https://hetland.github.io)'})
with urllib.request.urlopen(req,timeout=45) as response:
    m = json.load(response)['message']
if m['type'] not in ('journal-article','proceedings-article'):
    parser.error('This DOI is not a journal or proceedings article.')
if not any('hetland' in a.get('family','').lower() for a in m.get('author',[])):
    parser.error('Crossref does not list Hetland as an author. Inspect the publisher record and add manually if its metadata is incomplete.')
clean = lambda s: html.unescape(re.sub('<[^>]+>','',s))
title = clean(m['title'][0])
if re.search(r'^(editorial|correction|corrigendum|erratum|thank|acknowledg)',title,re.I):
    parser.error('This appears to be an editorial or correction; link it from the original paper instead.')
dates = m.get('published-print',m.get('published',m.get('published-online',{}))).get('date-parts',[[datetime.date.today().year]])[0]
paper = {'title':title, 'authors':[a.get('family','')+', '+a.get('given','') for a in m.get('author',[])], 'year':dates[0], 'date':'-'.join(str(n).zfill(4 if i==0 else 2) for i,n in enumerate(dates)), 'journal':clean(m.get('container-title',[''])[0]), 'volume':m.get('volume',''), 'issue':m.get('issue',''), 'pages':m.get('page',m.get('article-number','')), 'doi':m['DOI'], 'url':'https://doi.org/'+m['DOI'], 'type':m['type'], 'peer_reviewed':True, 'source_urls':[url]}
papers.append(paper)
papers.sort(key=lambda p:(p['year'],p.get('date',''),p['title']),reverse=True)
tmp = path.with_suffix('.tmp')
tmp.write_text(json.dumps(papers,ensure_ascii=False,indent=2)+'\n')
tmp.replace(path)
print(f"Added: {title}\nReview content/publications.json, then commit and push. The website and printable CV rebuild automatically.")
