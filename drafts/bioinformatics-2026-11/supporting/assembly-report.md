# Assembly report

Date: 2026-11-09. Draft: /home/guarracino/git/impg-paper/drafts/bioinformatics-2026-11.

## Build

`./build.sh` (pdflatex, bibtex, pdflatex, pdflatex) exited 0 on the first run, before any edit.
After the two fixes below it still exits 0.
`pdfinfo main.pdf` reports 17 pages, page size 708.661 x 1000.63 pts.
The References heading starts on page 9, and "Supplementary Material" starts on page 11, so the main text and references fill pages 1 to 10 and the supplement fills pages 11 to 17.

## Fixes made

1. `sections/07.availability.tex:14`: `\texttt{s3://human-pangenomics/pangenomes/freeze/release2/}` became `\url{...}`. The `\texttt` path could not break and gave an overfull hbox of 33.33617pt in the main text. After the change, the log has no overfull box from this paragraph. Meaning unchanged.
2. `main.tex`, supplement block: added `\renewcommand{\theHfigure}{S\arabic{figure}}` and `\renewcommand{\theHtable}{S\arabic{table}}` after the existing `\thefigure`/`\thetable` redefinitions. Before, Supplementary Table S1 got the hyperref anchor `table.1`, which Table 1 already used, and pdfTeX logged "destination with the same identifier (name{table.1}) has been already used, duplicate ignored", so the link to Table S1 jumped to Table 1. After, the anchor is `table.S1` and the warning is gone.

## Citations and cross-references

- 51 distinct `\cite` keys in the section files and main.tex, 0 missing from bibliography.bib (script check), 0 "Citation ... undefined" in main.log, bibtex `warning$ -- 0`.
- 14 distinct `\ref` targets, 26 `\label`s, 0 refs without a label, 0 "Reference ... undefined" in main.log, 0 "??" in `pdftotext main.pdf`.
- 12 labels are never referenced (sec:availability, sec:discussion, sec:introduction, sec:release, sec:res-local, sec:res-partition, sec:res-reach, sec:res-refine, sec:res-release, sec:res-sparse, sec:res-tpa, sec:results). Harmless.
- On a clean build (no aux files, copy in scratchpad freshbuild/), the third pdflatex pass still logs "Label(s) may have changed". The aux of pass 2 and pass 3 differ only in page numbers inside hyperref labels and in the order of `\citation` lines. The aux of pass 3 and pass 4 are identical, and `pdftotext` of the pass 3 and pass 4 PDFs is identical. The draft uses no `\pageref`, so the PDF from build.sh is correct. A fourth pass in build.sh would silence the warning; build.sh was not edited because the task allows edits only to section files and main.tex.

## Overfull boxes

- Main text paragraphs: 3 overfull boxes of 2.29929pt each, in sections/05.results.tex at lines 93-109, 224-236 and 298-306 (the three figure environments). All are under 20pt, left as they are.
- 10 boxes of 252.0pt "while \output is active", one per page shipout. A minimal document with bioinfo.cls and plain text (scratchpad minbuild/t.tex, 4 pages) logs 3 of the same 252.0pt boxes, so they come from the class page header, not from the draft.

## Other warnings left

- Font substitutions (`LY1/ptm/m/sc`, `LY1/phb/m/n`, `LY1/phb/b/n`, `OT1/cmr` sizes) come from bioinfo.cls fonts.
- hyperref "Difference (3) / (2) between bookmark levels" comes from `\paragraph` headings in sections/08b.supplement-experiments.tex (input lines 8 and 18) under unnumbered parents. Bookmarks only.

## \pending IDs

54 `\pending` calls. Counts by ID: E2 11, E1 7, E4 6, E6 5, E3 5, E5 5, C1 4, E9 4, E10 3, E1b 1, E8 1, E7 1, C14 1.

- E1 to E10 all appear in supporting/plan.md as experiments.
- E1b (sections/04.release.tex:28) is the bidirectional vs `--unidirectional` arm of E1 at plan.md:325 and the claim row at plan.md:212.
- C1 (4 calls: sections/00.abstract.tex:22, sections/07.availability.tex:6 twice and :10) and C14 (sections/07.availability.tex:12) are code-fix IDs (plan.md:618 and plan.md:631), not experiment IDs. They name real plan items (tag, Zenodo DOI, container; benchmark harness), so I left them. The authors may prefer a separate macro for release items.

`\authornote` calls: 28 (introduction 1, model 1, implementation 1, release 7, results 4, discussion 4, availability 3, supplement model 3, supplement experiments 4).

## Word counts

Method: strip LaTeX comments, `\label`, `\ref` and `\cite` commands, run `detex -n`, count tokens with a letter or digit. Math is dropped by detex. Float environments (figure, figure*, table*, algorithm) are counted apart. Column "slot" counts each `\pending{ID}{text}` as one word, since each will become one number; column "full" counts the placeholder text. The abstract count excludes the Contact and Supplementary information lines. Script: scratchpad wc2.py.

| Section | Budget (plan.md section 5) | Full | Slot | Floats |
| --- | ---: | ---: | ---: | ---: |
| Abstract | 143 (plan abstract) | 133 | 120 | 0 |
| 1 Introduction | 500 | 532 | 532 | 0 |
| 2 Model | 450 | 532 | 499 | 94 |
| 3 Implementation | 600 | 761 | 661 | 792 |
| 4 HPRC r2 release | 350 | 394 | 366 | 1,039 |
| 5 Results (total) | 2,500 | 2,506 | 2,271 | 640 |
| 5 lead paragraph | none | 98 | 98 | 0 |
| 5.1 Tracepoint vs CIGAR projection | 200 | 228 | 205 | 0 |
| 5.2 Indexing and querying the release | 450 | 486 | 434 | 279 |
| 5.3 Reach and reference dependence | 400 | 380 | 351 | 0 |
| 5.4 Sparse alignment sets | 400 | 337 | 302 | 0 |
| 5.5 Gene-level accuracy and Shredtools | 400 | 358 | 309 | 223 |
| 5.6 Local graphs and restriction | 300 | 300 | 289 | 0 |
| 5.7 Locus refinement | 200 | 208 | 185 | 138 |
| 5.8 Partition work units on yeast | 150 | 111 | 98 | 0 |
| 6 Discussion | 500 | 613 | 572 | 0 |
| 7 Availability (section body) | 100 | 86 | 76 | 0 |
| Funding, conflict, acknowledgements | none | 62 | 62 | 0 |
| Main text sum (1 to 7 body) | 5,000 | 5,424 | 4,977 | 2,565 |
| Supplement 08a (Notes S1 to S4) | | 2,137 | 2,095 | 0 |
| Supplement 08b (Note S5, Table S1) | | 1,857 | 1,857 | 0 |
| Supplement sum | 2,500 | 3,994 | 3,952 | 0 |

Over budget with full counts: Introduction (532 vs 500), Model (532 vs 450), Implementation (761 vs 600), Release (394 vs 350), Results (2,506 vs 2,500), Discussion (613 vs 500), main text sum (5,424 vs 5,000), supplement (3,994 vs 2,500).
With slot counts the main text sum is 4,977 vs 5,000, but Model (499 vs 450), Implementation (661 vs 600), Release (366 vs 350) and Discussion (572 vs 500) stay over.
Table S1 in 08b is not a float, so its command rows count as supplement body.
Plan.md:149 states that whether legends count toward the 5,000 words is unknown. The 2,565 float words are not in the main text sum.
