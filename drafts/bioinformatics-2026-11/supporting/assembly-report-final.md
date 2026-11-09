# Final assembly report

Date: 2026-11-09. Draft: /home/guarracino/git/impg-paper/drafts/bioinformatics-2026-11. This report replaces supporting/assembly-report.md, whose word counts predate the 09:17 to 09:25 section edits.

## Build

`./build.sh` (pdflatex, bibtex, pdflatex, pdflatex) exited 0 before any edit and after every edit below.
No preamble change was needed, and main.tex is unchanged.
`pdfinfo main.pdf` reports 17 pages, page size 708.661 x 1000.63 pts.
Sections 1 to 7 fill pages 1 to 9, References start on page 9 and end on page 10, and "Supplementary Material" fills pages 11 to 17.
main.log has no "Rerun" or "Label(s) may have changed" warning and no "destination with the same identifier" warning. bibtex reports `warning$ -- 0`.

## Checks

| Check | Result |
| --- | --- |
| `\cite` keys | 52 distinct keys in sections/*.tex, 0 missing from bibliography.bib, 0 "Citation ... undefined" in main.log |
| `\ref` targets | 14 distinct targets, 26 labels, 0 duplicate labels, 0 refs without a label, 0 "Reference ... undefined", 0 "??" in pdftotext |
| Unreferenced labels | 12 section labels (sec:availability, sec:discussion, sec:introduction, sec:release, sec:res-local, sec:res-partition, sec:res-reach, sec:res-refine, sec:res-release, sec:res-sparse, sec:res-tpa, sec:results). Harmless |
| Overfull boxes in paragraphs | 3, each 2.29929pt, at sections/05.results.tex lines 95-111, 228-240 and 302-310 (the three figure placeholders). All under 20pt, left |
| Overfull boxes during output | 9 of 252.0pt from the bioinfo.cls page header (earlier report reproduced 3 of them on a plain 4-page bioinfo.cls file) and 1 of 1.12001pt on page 1. Under 20pt or class-made, left |
| Other warnings | bioinfo.cls font substitutions, and hyperref bookmark-level warnings from `\paragraph` under `\subsection*` in 08b. Left |
| `\pending` IDs | 54 calls: E2 11, E1 7, E4 6, E3 5, E5 5, E6 5, C1 4, E9 4, E10 3, E1b 1, E7 1, E8 1, C14 1 |
| `\authornote` calls | 32 |

`\pending` IDs against plan.md and experiment-plan.md.
- E1 to E10 are experiments in plan.md section 7 and each has a section in experiment-plan.md section 3.
- E1b is the reciprocal-pair arm of E1 (plan.md E1 block and section 5.4 claim row; experiment-plan.md E1 Data, Compared, Metrics rows and its E1b command block).
- C1 (sections/00.abstract.tex:22, sections/07.availability.tex twice on line 6 and once on line 10) and C14 (sections/07.availability.tex:12) are code-fix IDs, not experiment IDs. Both have rows in plan.md section 9 and experiment-plan.md section 5. I left them, because they name release items that a later step fills. The authors may prefer a separate macro for them.
- No `\pending` lacks a row in experiment-plan.md.

## Fixes made

All edits keep the meaning, add no fact and touch only section files.

1. sections/03.implementation.tex:177. `\pending{E2}{whether query output is identical at -t 1, 4 and 16}` now ends "-t 1, 4, 16 and 48". Results 5.2 line 59, Fig. 3d, Note S5 and experiment-plan.md correction 15 all use 1, 4, 16 and 48 threads.
2. Release 1 naming. The draft used "HPRC year-1" 11 times, "HPRC release 1" twice and "HPRC r1" twice for the same release. Now all four outliers read "HPRC year-1": sections/01.introduction.tex:45, sections/05.results.tex:190, sections/06.discussion.tex:49 and the Table 1 row name at sections/04.release.tex:85. Quotes of the Shredtools preprint keep "HPRCr1".
3. sections/01.introduction.tex:31, HG00272 authornote. The list of places that call the TPA files the alignment behind the PGGB graph named only the abstract and the introduction. It now also names 04.release.tex line 4 and Table 1, and 05.results.tex lines 17 and 61. Its semicolon became a full stop.
4. sections/05.results.tex:61, vg authornote. "needs a recent vg" became "needs ``a recent release of vg'' without naming a version". The quote is hpp_readme.md:159 verbatim. The style rules forbid "recent" without a date or number.

## Word counts

Method: strip comments, `\label`, `\ref` and `\cite`, then `detex -n`, then count tokens with a letter or digit. Math is dropped. Floats (figure, table, algorithm) are counted apart. The abstract count stops before "Contact:". "With notes" counts `\authornote` text, which the final text will not have. "Slot" counts each `\pending` as one word. Script: /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/final/wc_final.py, output in wc.tsv in the same folder.

| Section | Budget (plan.md 3 and 5) | With notes | Without notes | Without notes, slot | Float words |
| --- | ---: | ---: | ---: | ---: | ---: |
| Abstract (headings included) | 143 (journal maximum 150) | 172 | 150 | 137 | 0 |
| 1 Introduction | 500 | 681 | 599 | 599 | 0 |
| 2 Model | 450 | 622 | 583 | 547 | 94 |
| 3 Implementation | 600 | 813 | 785 | 684 | 821 |
| 4 HPRC r2 release | 350 | 449 | 400 | 372 | 1,038 |
| 5 Results (total) | 2,500 | 2,589 | 2,511 | 2,276 | 643 |
| 5 lead paragraph | none | 100 | 83 | 83 | 0 |
| 5.1 Tracepoint vs CIGAR projection | 200 | 228 | 228 | 205 | 0 |
| 5.2 Indexing and querying the release | 450 | 529 | 496 | 444 | 284 |
| 5.3 Reach and reference dependence | 400 | 394 | 370 | 341 | 0 |
| 5.4 Sparse alignment sets | 400 | 346 | 346 | 311 | 0 |
| 5.5 Gene-level accuracy and Shredtools | 400 | 368 | 364 | 315 | 223 |
| 5.6 Local graphs and restriction | 300 | 299 | 299 | 288 | 0 |
| 5.7 Locus refinement | 200 | 214 | 214 | 191 | 138 |
| 5.8 Partition work units on yeast | 150 | 111 | 111 | 98 | 0 |
| 6 Discussion | 500 | 699 | 635 | 594 | 0 |
| 7 Availability | 100 | 83 | 83 | 63 | 0 |
| Main text sum (1 to 7) | 5,000 | 6,936 | 5,596 | 5,135 | 2,596 |
| Supplement 08a (Notes S1 to S4) | | 2,208 | 2,141 | 2,099 | 0 |
| Supplement 08b (Note S5, Table S1) | | 2,050 | 2,007 | 2,007 | 0 |
| Supplement sum | 2,500 | 4,258 | 4,148 | 4,106 | 0 |

Without notes and with slots, these stay over budget: Introduction (599 vs 500), Model (547 vs 450), Implementation (684 vs 600), Release (372 vs 350), Discussion (594 vs 500), main text sum (5,135 vs 5,000) and supplement (4,106 vs 2,500).
Subsections 5.1 (205 vs 200) and 5.2 (444 vs 450) sit at their budgets with slots, and 5.2 is over without slots (496 vs 450).
The abstract has 150 words without notes and 137 with slots, against the plan's 143 and the journal's 150.
plan.md section 5 states that it is unknown whether legends count toward the 5,000 words. The 2,596 float words are not in the main-text sum.

## Completeness against plan.md

Present and matching the plan: title; structured abstract; the claims of plan.md sections 5.1 to 5.7; Algorithm 1; Table 1; Table 2; Fig. 1; Fig. 2 panels a to c; placeholders for Figs. 3, 4 and 5 with full planned captions; Results 5.1 to 5.8 with experiments E1 to E10; Notes on proofs, sparsification and partition termination; the command and version table; and the must-not-claim list. I found no "every copy", no "reference-free", no "premise", no "exactly equivalent", and no subgraph or view claim for `-o gfa` (grep of non-comment text).

Missing or changed against plan.md section 6 and 5.8 (each needs data, a figure or an author choice, so I did not add them).
1. Fig. 2d (bp reached per depth with and without reference bridges, E3b) is absent. Fig. 2b now plots file size against records instead of the plan's undirected degree with the 1,483 reciprocal pairs. Fig. 2c shows pair-level reach, and the plan's panel c (the two reference stars) is absent. sections/05.results.tex 5.3 carries an authornote on the missing panel.
2. Fig. 1d is an output example for `query`. The plan's command-to-format map for index, query, refine, partition, align and stats is absent.
3. Fig. S1 (worked toy example) is text only, as Supplementary Note S1. No figure exists.
4. Supplementary Figs. S2 (E1), S3 (E8) and S4 (E9) are cited in Results 5.1, 5.2 and 5.8, but the supplement has no figure or placeholder for them. Fig. S5 (E7, copy representation) is neither cited nor present. The Discussion cites only `\pending{E7}`.
5. Supplementary Tables S1 to S8 (benchmark grids, EXP) are absent. The plan's Table S9 (commands, versions, binary hashes) exists as Supplementary Table S1. Table S10 (feature and test matrix) and Table S11 (haplotype sets: 466 files, Shredtools N = 476, HPRC2 abstract 460, graph 464, and their intersection) are absent. plan.md section 5.4 places the Shredtools N = 476 intersection in Table S11, so that claim has no home.
6. Supplementary Note numbers differ from the plan. The plan has Note S1 proofs, S2 sparsification and S3 partition, while the draft has S1 worked example, S2 proofs, S3 sparsification, S4 partition and S5 benchmark protocol. All in-text references follow the draft numbering, which is consistent.
7. plan.md section 5.4 lists equal TPA and PAF record counts for 3 files (550,678, 1,082,733 and 8,916,633). Only the 8,916,633 count of the GRCh38 file is in the draft.
8. The Discussion names the open syng bugs but not the open genotyping bugs that plan.md section 10 lists (the GFA backend ignores candidate filters, and the mosaic span bug). It says only that genotyping has no benchmark against COSIGT calls.

## Consistency checks that passed

These match across sections and supporting files. Thread counts are E2 1, 4, 16 and 48 and E5 1, 8, 16 and 48. Seeds 1 to 10 match between Note S5 and experiment-plan.md. Region counts are 1,000 plus 200 held out for E1, E2 and E3a, 100 per haplotype with 20 held out for E3b, and 100 loci for E6. Query defaults are `-m` 2, 101 bp minimum hop and 10 bp snapping. Refine uses 1,000 bp steps, 1,000 bp end spans and half the locus. Subset sets are random 6%, random 17%, auto, star and all pairs. The AGC slot is 3.70 GB with 8 slots by default. The 32-bit limit is 2,147,483,647 bp. The storage ratios 3.918, 4.433 and 0.840 match the byte counts. The 13.1849% and 11.2583% (24,291 of 215,760) figures check out. The pair counts 23,738 of 108,345 and 25,221 of 216,690 match. The seqwish version v0.7.11-35-gaab5bee matches.
I checked against the scratchpad S3 listings: the CHM13 TPA (455,391,474 bytes), the CHM13 PAF.gz (5,590,178,237 bytes) and hprcv2_enhanced_merged (31,371,728,522 + 54,339,192 = 31,426,067,714 bytes).
Results 5.5 cites the Shredtools 86-fold factor at 48 threads, and the Discussion cites the 3.8-fold factor and 20-fold memory for a serial build. Both are in paper.txt:299-301, so the two sentences do not conflict.
Table 2 says partition fragments under 3,000 bp join a neighbouring interval (`--min-missing-size`). Implementation says closures extend to sequence ends closer than 3,000 bp (`--min-boundary-distance`). Both options default to 3000 in `impg partition --help`, so these are two facts, not one fact stated twice.

## Left for the authors or a later step

- Cut the main text by 135 words with slots, or by 596 without them, and the supplement by 1,606 with slots. Introduction, Model, Implementation and Discussion carry most of the excess.
- Decide whether `\pending{C1}` and `\pending{C14}` should use their own macro.
- Add the missing display items in the list above, or drop their citations (Supplementary Figs. S2 to S4).
- Five prose source lines exceed 25 words by my token count (flags and line numbers count as words): 02.model.tex:51 (27), 05.results.tex:107 (29, Fig. 3c legend), 08a.supplement-model.tex:153 (29), 08b.supplement-experiments.tex:31 (27) and 59 (27). I did not split them, because the task asked only for build fixes and consistency fixes.
- 32 `\authornote` items remain, as the earlier phases placed them.
