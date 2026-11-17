# Historical publication audit

Prepared 2026-11-17 from the website's live publication list, repository `_pages/publications.md`, the author's OpenAlex cluster A5066137424 (156 works, retrieved as `openalex-all.json`), Crossref DOI metadata, and primary author/institution records.

`historical-publications.json` contains 81 items dated 1998–2023: 80 journal articles/reviews and one full peer-reviewed conference proceedings paper (TracPy). Every item has a DOI URL and source URLs; all 81 were checked to contain Hetland in the author list. No abstract, dataset, report, preprint, or editorial is included. The new-publications agent supplies 2024 and later, including Cao 2024 and the final Deb 2024 paper.

Publication years use the volume/print year when supplied by Crossref, which corrects the online-first year in OpenAlex (for example Cole 2016, Xu 2016, Hetland 2017, Qu 2018, Ruiz-Xomchuk 2021). Titles and journal names come from Crossref rather than the shortened paraphrases on the repository page. Full author arrays use `Surname, Given` where deposited.

## Included special cases and corrections

- **TracPy: Wrapping the Fortran Lagrangian trajectory model TRACMASS** (2014), full proceedings paper, pages 79–84, DOI https://doi.org/10.25080/Majora-14bd3278-00d . The SciPy organizers document open peer review and specifically describe the 2014 process with ideally two reviewers signing off: https://scipy-conference.readthedocs.io/ja/latest/manual/committees/proceedings.html . This is a paper, not a meeting abstract.
- **A mechanism for offshore initiation of harmful algal blooms in the coastal Gulf of Maine** is **2003**, not 2002. DOI https://doi.org/10.1093/plankt/25.9.1131 . Crossref deposits only the first author, so the full author list was restored from USGS and the original WHOI-hosted article. https://www.usgs.gov/publications/a-mechanism-offshore-initiation-harmful-algal-blooms-coastal-gulf-maine and https://www2.whoi.edu/staff/dmcgillicuddy/wp-content/uploads/sites/73/2017/06/mcgetal03_jpr.pdf . It is missing from the Hetland OpenAlex author cluster and was added explicitly.
- **The science of hypoxia in the Northern Gulf of Mexico: A review** (2010) is included, DOI https://doi.org/10.1016/j.scitotenv.2009.11.047 . The live list had a malformed DOI with an extra hyphen; the repository's updated list omitted this paper.
- **Sensitivity of hypoxia predictions for the northern Gulf of Mexico to sediment oxygen consumption and model nesting** (2013) is a legitimate additional journal article from the author's OpenAlex/Crossref records, DOI https://doi.org/10.1002/jgrc.20077 . It was absent from the old site and is included.
- The oldest item **Observations of the Eastern Maine Coastal Current and its offshore extensions in 1994** (1998) is included with DOI https://doi.org/10.1029/98JC01625 .
- Crossref erroneously leaves a footnote asterisk in the 2004 idealized estuary article title; removed the trailing asterisk for display.

## Exclusions from the old/current lists

- **Deb et al., Estuarine hurricane wind…**, EGUsphere (2023): preprint excluded. Replaced by the final peer-reviewed **Natural Hazards and Earth System Sciences 24, 2461–2479 (2024)**, DOI https://doi.org/10.5194/nhess-24-2461-2024 ; supplied with new publications.
- **Beal et al. (2022), What's New at JGR-Oceans? Confronting Bias, Burn Out, and Big Data**: editorial, DOI https://doi.org/10.1029/2022JC019539 ; excluded from peer-reviewed research list.
- **Bianchi et al. (2010), Hypoxia in the Northern Gulf of Mexico: Connecting Science with Policy**, EOS Forum: magazine/forum item, excluded; retained in old website archive.
- **Bianchi et al. (2008), Controlling Hypoxia on the U.S. Louisiana Shelf: Beyond the Nutrient-Centric View**, Eos, DOI https://doi.org/10.1029/2008EO260005 : magazine/forum item excluded; retained in archive.
- **Burchard et al. (2008), Physikalische und ökologische Auswirkungen einer Kühlwasserausbreitung im Greifswalder Bodden – Endbericht**: technical report; excluded from peer-reviewed list, retained in archive.
- **Hetland et al. (2011), Integrated bio-physical modeling of Louisiana-Texas (LATEX) Shelf**: BOEMRE report; excluded, retained in archive.
- **Justić et al. (eds., 2017), Modeling Coastal Hypoxia**: edited book; not itself a peer-reviewed research article, retained in archive.
- **Hetland & Zhang (2017), Interannual Variation in Stratification…**; **Rose et al. (2017), Numerical Modeling of Hypoxia and Its Effects…**; **Hetland, Spreading and Mixing in Near-Field River Plumes** (now published 2022); **Hetland & Hsu (2013), Freshwater and Sediment Dispersal in Large River Plumes**: book chapters; individual external peer-review status not established, therefore conservatively excluded from the filtered research list while preserved in archive. DOI links are respectively https://doi.org/10.1007/978-3-319-54571-4_3 , https://doi.org/10.1007/978-3-319-54571-4_15 , https://doi.org/10.1007/978-3-031-09559-7_8 , https://doi.org/10.1017/CBO9781139136853.006 .

## Additional indexed records excluded

OpenAlex can classify nonresearch items as articles. Excluded: JGR reviewer-thanks notices for 2017, 2019, 2020, and 2021; OSTI software/data records; thesis-like records lacking journal and DOI; DTIC reports; all AGU/EGU abstracts and unverified conference papers; a spurious duplicate in `Journal of End-to-End-testing` with DOI `10.1016/s9999-9994(08)20541-6` (the genuine river plume paper uses `10.1016/j.dynatmoce.2008.11.003`).

## Limits

Google Scholar blocks automated retrieval, so exhaustive identity with the live Scholar profile cannot be asserted. This list reconciles every historical peer-reviewed research paper identified on the live old list and adds records found in the author's OpenAlex cluster. DOI registry metadata verifies links and citation identity; article classification plus venue review practices supports inclusion, while known editorial and abstract types are explicitly removed.

# Follow-up Scholar reconciliation

## Add these two full peer-reviewed proceedings papers

`additional-reviewed.json` contains full metadata, author arrays, DOI links and page ranges for:

1. Martin et al. (2005), **Ten years of realtime, near-surface current observations supporting oil spill response**, International Oil Spill Conference Proceedings 2005(1), 541–545. DOI https://doi.org/10.7901/2169-3358-2005-1-541 . Crossref includes a trailing footnote marker 1 in the title; it is removed for display.
2. Chapman, Socolofsky & Hetland (2014), **From blowout to beach: An integrated modeling approach**, International Oil Spill Conference Proceedings 2014(1), 919–932. DOI https://doi.org/10.7901/2169-3358-2014.1.919 .

Evidence: NOAA's repository hosts the conference history **Fifty Years of the International Oil Spill Conference**, which describes the proceedings as a collection of peer-reviewed papers/posters throughout its 50-year history. https://repository.library.noaa.gov/view/noaa/64452/noaa_64452_DS1.pdf . The contemporary API sponsor newsletter also explicitly calls 2014 proceedings papers peer-reviewed: https://www.api.org/~/media/files/ehs/clean_water/oil_spill_prevention/spill-newsletter/dispersant-newsletter-sept2014.pdf . Crossref verifies these as full 5-page and 14-page papers, not AGU-style abstracts.

## Link this correction from its original article

The Forrest et al. (2011) ERL hypoxia paper has a 2012 corrigendum: https://doi.org/10.1088/1748-9326/7/1/019501 . Add a **Correction** link to the existing original article rather than counting it as independent research. Structured data in `forrest-correction.json`. The correction itself is a published journal correction, not a separate research paper.

## Exclude pending individual full-paper review evidence

- **Observing and forecasting coastal currents: Texas Automated Buoy System (TABS)** (2001), https://doi.org/10.1109/OCEANS.2001.968300 , is a full five-page IEEE OCEANS proceedings paper, but I could not establish that the full manuscript received peer review. OCEANS' documented process is review of paper proposals/extended abstracts followed by full-paper submission. Retain in archive/pending audit rather than assert full-paper review.
- **SeaweedPaddock: Initial Modeling and Design for a Sargassum Ranch** (2018), https://doi.org/10.1109/OCEANS.2018.8604848 , is a full six-page IEEE OCEANS proceedings paper, but the 2018 operational manual describes independent expert review of 500–1000-word proposals, followed by later full manuscripts checked for quality/formatting by session chairs. This establishes reviewed proposals and published full papers, but does not establish independent scientific review of the full papers. Coauthor Thyng lists it under Products and Other rather than her journal publications: https://kristenthyng.com/publications.html . Conservative exclusion pending author confirmation is appropriate.
- **Offshore spreading of buoyant bulge from numerical simulations and laboratory experiments** (2014), https://doi.org/10.1109/BALTIC.2014.6887889 , is a full 11-page IEEE proceedings paper included in Soosaar's doctoral thesis. The archived symposium site shows abstract acceptance followed by full paper submission; its instructions do not establish full-manuscript peer review. Therefore do not assert peer review on current evidence. Sources https://baltic2014.msi.taltech.ee/docs.php and https://digikogu.taltech.ee/et/Download/ed32b8f8-1111-4f17-95c8-0c788bf4fcc5 .

Relevant OCEANS primary process source: **OCEANS Conference Operational Policy Manual v9.6 (October 7, 2018)**, sections 6.1–6.4 (proposal review) and 6.9 (session-chair full-paper quality check), https://www.oceansconference.org/wp-content/uploads/2018/12/OCEANS_Conference_Manual_v9.6.pdf . This is deliberately a conservative full-manuscript standard; the user may consider reviewed full proceedings papers eligible even when acceptance is based on extended abstracts, so the above are documented rather than silently discarded.

## Hurricane Ida study

**The Influence of Climate Change on Flooding and Social Inequalities from Remnants of Hurricane Ida** (Li, Wehner, Judi, Hetland) is still identifiable only as a Research Square **posted-content/preprint** record, DOI https://doi.org/10.21203/rs.3.rs-3470345/v1 . Exclude from the peer-reviewed list. An exact-title Crossref search returned that preprint and no final journal record (`ida-crossref-search.json`); the author's OpenAlex cluster similarly classifies it as preprint. Michael Wehner's institutional CV in May 2024 lists it as under review: https://crd.lbl.gov/assets/Uploads/Wehner/publications_051424.pdf . Some secondary bibliographies mislabel the preprint as Nature journals while still linking the preprint DOI; those do not establish publication. No final publisher DOI was found as of this audit.

Google Scholar was subsequently reviewed in the signed-in Chrome browser on 2026-11-17, all 192 visible records. Two additional full peer-reviewed IOSC proceedings papers were identified and added; meeting abstracts, duplicate preprints, data, editorial items, and unconfirmed reviewed proceedings were excluded. Final current bibliography: 103 items (1998–2026).
