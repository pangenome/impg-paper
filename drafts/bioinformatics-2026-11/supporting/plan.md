# impg paper plan (phase 2 synthesis)

Written 2026-11-08 (session clock) from three proposals, the opportunity map and three judges, all in /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase2, and from the phase-1 knowledge base in /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase1.
VERIFY_CORRECTIONS.md overrides the phase-1 map texts, and the judges' measurements override the proposals where they disagree.
Code is /home/guarracino/git/impg at HEAD 0987752 (`git describe` v0.5.0-656-g0987752, `impg 0.5.0`).
I ran only `impg <cmd> --help`, `--version`, `--help` of installed external tools, read-only git and file commands, and small Python sums over the saved S3 listings.
I edited, built and deleted nothing in /home/guarracino/git/impg or /home/guarracino/git/impg-paper, and I ran no workgraph command.
Status labels: NOW = in code and covered by a test or a stored measurement (NOW-ext = a number or quote from a cited external source); CODE = in code, not measured; EXP = needs a new experiment; WIP = research in progress, not product-ready.
Paths without a leading slash are relative to /home/guarracino/git/impg unless they start with phase1/ or phase2/, which are relative to the scratchpad.

## 0. Decision

Venue: Bioinformatics (OUP), Original Paper, section Genome analysis, in the ODGI structure (Introduction, Model, Implementation, Results as vignettes plus a performance section, Discussion).
The paper rests on one claim, taken from the Nature Methods Brief proposal: the pairwise alignments of a genome collection, indexed, answer base-level regional homology queries for every haplotype of HPRC release 2 without building or loading a whole-genome graph.
Partition, refine and local graphs are supporting sections, and each one carries its own measured evidence or leaves the paper.
Upgrade path: a Nature Methods Brief Communication presubmission enquiry, sent only if the flip conditions in section 2 are met with targets fixed before the runs.
A Nature Methods Article is reachable only by editor conversion after a reviewed Brief Communication, with a biological result that needs a property of the implicit model.

## 1. Rationale with the judges' scores

Scores are 1 to 10 per axis, reviewer risk 10 means low risk, totals are out of 50.

| Framing | Editor | Hostile reviewer | Feasibility auditor | Sum of 3 totals |
| --- | ---: | ---: | ---: | ---: |
| Bioinformatics Original Paper | 28 | 26 | 28 | 82 |
| Nature Methods Brief Communication | 26 | 26 | 25 | 77 |
| Nature Methods Article | 19 | 20 | 20 | 59 |

Per axis, summed over the three judges (Bioinformatics vs Brief vs Article): novelty 15 vs 18 vs 21; evidence now 8 vs 9 vs 6; feasibility 16 vs 16 vs 7; reviewer risk 18 vs 14 vs 9; venue fit 25 vs 20 vs 16.
Sources: judge-editor.md section 2, judge-reviewer.md section 3, judge-feasibility.md section 0.

Why Bioinformatics and not the Brief first.
- Bioinformatics has the higher total for every judge but one tie: 28 vs 26 (editor), 26 vs 26 (reviewer), 28 vs 25 (feasibility).
- Two of three judges recommend Bioinformatics first; the reviewer breaks the 26 vs 26 tie on reviewer risk (6 vs 5) and venue fit (8 vs 6), and the feasibility auditor ranks it 28 vs 25.
- The editor recommends the Brief first while scoring it lower (26 vs 28), on the argument that both papers share the minimal experiment set, so a Brief attempt costs review time, not work (judge-editor.md section 7).
- That argument does not hold in full: the Brief needs comparators that Bioinformatics does not (a Minigraph-Cactus regional comparator and liftover arms, judge-reviewer.md section 6; judge-editor.md section 3.2), and the PGGB Brief took 393 days and 2 review rounds from receipt to acceptance (phase1_research_digest.txt, PGGB SUMMARY).
- The plan keeps the editor's route open at the cost of one presubmission enquiry: the Brief abstract (70 words by `wc -w` on phase2/abstract.txt) is ready, and the flip conditions in section 2 decide whether to send it.
- No framing can go to any journal today: every result panel in all three proposals is EXP, and no stored number was produced at HEAD on this machine (judge-editor.md section 0; evidence-inventory.md section 0 items 1-4).

Why not the Article.
- All three judges score it lowest (19, 20, 20).
- Its biology (copy number at AMY1/AMY2, C4, SMN1/SMN2, LPA, RHD/RHCE, CYP2D6, HLA class II) repeats the PGR-TK design of 395 genes on 94 haplotypes at larger N (judge-editor.md section 3.1).
- At C4 the released GRCh38-target PAF holds 895 records from 465 haplotypes, and for 401 of 465 haplotypes no GRCh38 base is covered by more than 1 record (median record query span 533,800 bp), so copy counts cannot come from that file (phase2/judge/c4_depth_out.txt).
- Its "graphs as views" figure contradicts the code, because `query -o gfa` keeps only the merged intervals and the engine re-aligns them (src/main.rs:12326-12339, checked in this step).
- Its "Shredtools premise is false" rebuttal backfires: Shredtools already wrote "In practice, impg operates over a sparse sampling of the pairwise comparison space" and benchmarked 6% and 17% sets (impg-paper/references/biorxiv-2026-07-03-736354/paper.txt:301-312, quoted in judge-reviewer.md section 1).

Grafts from the losing framings and the opportunity map.

| From | Idea | Where it goes |
| --- | --- | --- |
| NM Article | The HPRC r2 release audit (466 files, 389,234,668 records, all Standard tracepoints, partner census), extended with the undirected density and the reciprocal pairs the judges measured | Section 4, Fig. 2a-c, Table 1 |
| NM Article | Reach and recall measured without GRCh38 and CHM13 as bridges, at base level | E3, Fig. 2d, Fig. 4c |
| NM Article | TPA vs PAF exact identity on the local GRCh38 star as the gate for every TPA number | E1 |
| NM Article | The "what the paper must not claim" list, carried into the Discussion as stated limits | Section 11, Discussion |
| NM Article | The semantics table (what impg guarantees and what it does not, against Shredtools, PGR-TK, liftOver/HAL, odgi/vg) | Table 2 |
| NM Article | liftOver chains (direct and chained), halLiftover and a simulation with a logged coordinate map | U2, U3 (Tier 2, required for the upgrade) |
| NM Article | The concession that Shredtools multi-MUMs are complementary, as its authors suggest (paper.txt:528-532) | Discussion |
| NM Brief | One claim, the explicit refusal of a storage claim with both ratios | Thesis, Section 4, Discussion |
| NM Brief | CAT GENCODE38 annotations on HPRC year 1 (178 GFF3 files) as gene truth | E5 |
| NM Brief | ScRAP 142 yeast strains as a published holdout never used for tuning | E4, E9 |
| NM Brief | Single-index mode for every benchmark; questions to the HPRC builders | Code fix C6, section 12 |
| NM Brief | A benchmark harness with fixed seeds, `/usr/bin/time -v` and output validators, tested on toy data first | Code fix C14 |
| Bioinformatics | Formal Model section, Algorithm 1, worked toy example from the test fixtures | Section 2, Fig. S1 |
| Bioinformatics | Query comparison on both tools' released HPRC r2 indexes (Shredtools hprcv2_merged.bumbl, 27,424,443,909 bytes) | E2, E10 |
| Bioinformatics | ODGI benchmark rules: thread and haplotype sweeps, replicates, competitor wins in the main text, axes from 0 | E2, E5 |
| Bioinformatics | refine vs Shredtools zoom at TERT and IGKV6-21 | E10 |
| Opportunity map | Proposition 1 (closedness) and Proposition 2 (restriction), with the yeast restriction test | Section 2, E6, Note S1 |
| Feasibility judge | Held-out direct pairs taken from the release itself, scored with and without the reference bridges | E3b |

## 2. Upgrade path to Nature Methods

The decision flips from Bioinformatics to a Nature Methods Brief Communication presubmission enquiry only if all five Tier 1 results below meet targets that the authors fix before the runs (proposed values, decision D2), and the four Tier 2 additions are done.

| # | Experiment | Flip condition (proposed target) |
| --- | --- | --- |
| F1 | E1 | 100% identical sorted rows, TPA exact vs PAF, at `-m 1` on the 1,000 tuning regions and on the 200 held-out regions, and 0 dropped tracepoint hits |
| F2 | E2 | All 466 TPA files index in single mode on one node; the whole-chromosome query finishes; median per-query wall time for 10 kb regions at `-x -m 2` (`-t 1`, exact) is at most the Shredtools median on the same 1,000 regions, with both numbers printed |
| F3 | E3b | Median per-region bp recall of held-out partners without reference bridges, at `-m 2`, is at least 0.95 times the recall with bridges, with both numbers printed |
| F4 | E5 | impg gene-copy containment is at least the Shredtools containment on the same genes and haplotypes, and the impg wrong-locus rate is at most Shredtools' rate |
| F5 | E6 | 0 bases whose node class differs between the restricted and the global seqwish graph at `-k 0`, on the 100 tuning loci and on the 20-haplotype C4 holdout |

Tier 2 additions required before the enquiry: U1 (Minigraph-Cactus regional comparator, required by PGGB reviewer 1 per judge-reviewer.md section 3.2), U2 (liftover arms), U3 (simulation with a logged coordinate map, the editor's "first reviewer-request candidate", judge-editor.md section 6), and the HPRC r2 PGGB build cost split by stage from the builders (question Q3), or the word "unknown" in its place.
If F1 fails, stop, then choose between fixing the TPA path and moving every run to the per-target PAF set on the cluster (318,372,159,094 bytes); this choice is decision D1.
If F2 fails because no node holds the build (RAM floor 59,163,669,536 bytes, section 4), the paper reports the two reference stars and the largest subset that fits, drops "whole release" from the title and abstract, and stays at Bioinformatics.
If F3 fails, the claim becomes "a reference-anchored implicit pangenome", as the editor wrote (judge-editor.md section 3.2), and the venue stays Bioinformatics.
Nature Methods Article: only if a Brief Communication editor offers conversion, as the PGGB editor did (MOESM3.txt:24-26, judge-editor.md V19), and the authors add one validated biological result that needs the implicit model's own property; the two candidates are U7 (homology across acrocentric short arms without a reference frame) and U4 (copy number) gated on E7 and on orthogonal read-depth validation.
Preprint timing is decision D11; the Shredtools "unable to compute" sentence is public since 2026-07-08 (paper.txt:285-287), so the editor recommends posting a preprint with the E2 numbers (judge-editor.md section 7).

Nature Methods Brief Communication text for the enquiry (70 words by `wc -w` on phase2/abstract.txt, limit 70, nmeth_content.txt Brief Communication section):

> Pangenome graphs are costly to build and update. We present impg, which treats the pairwise alignments of a genome collection as an implicit pangenome graph. An interval index projects any region of any assembly through the alignments, transitively and at base level, and builds sequences, graphs or variants only for that region. On the 389,234,668 alignments released by the Human Pangenome Reference Consortium, impg queries 466 haplotypes in [T] seconds.

## 3. Title, advance, abstract, thesis

Title: **impg: querying pangenomes through their pairwise alignments**

One-sentence advance: impg indexes the pairwise alignments of a genome collection as an implicit pangenome graph, so that any interval of any assembly is projected at base level, directly and through intermediate genomes, to every haplotype of HPRC release 2 without inducing, storing or loading a whole-genome graph.

Structured abstract, 143 words by `wc -w` on /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase2/plan_abstract_bioinf.txt (Motivation 45, Results 88, Availability 10, headings included); the recommended maximum is 150 (impg-paper/references/odgi-paper/README.md:27).
Each bracketed placeholder counts as one word and is filled from E2; no sentence states a result before the experiment.

> Motivation: Pangenome graph tools build a whole-genome graph before one locus can be studied, and a new sample set needs a rebuild. The Human Pangenome Reference Consortium release 2 (HPRC r2) distributes the pairwise alignments behind its PGGB graph in the tracepoint format of impg.
>
> Results: impg treats pairwise alignments (PAF, TPA or 1ALN) as an implicit pangenome graph. It indexes each alignment in both directions, projects an interval of any sequence at base level through the overlapping alignments, and follows homology transitively through other genomes. On the 389,234,668 HPRC r2 alignments, impg builds its index in [H] h with [G] GB of memory and answers a 10 kb query across 466 haplotypes in [T] s. We report recall against held-out alignments and gene annotations, and cost against Shredtools and the released graph.
>
> Availability and implementation: Rust, MIT license, https://github.com/pangenome/impg; archived release [DOI].

Abstract claims and status: HPRC r2 distributes the PGGB alignments as IMPG TPA files (NOW-ext, phase1/web/hpp_readme.md:151, 183); 389,234,668 records (NOW, sum of the 466 TPA headers, phase2/nm_article/partners.tsv, recomputed in this step); both directions (NOW, src/impg.rs:1686-1712, tests/test_transitive_integrity.rs:226-290); [H], [G], [T] (EXP, E2); recall and cost (EXP, E3-E5, E2); MIT license (NOW, LICENSE in /home/guarracino/git/impg); archived release (EXP, code fix C1).

Thesis.
For regional analysis a pangenome does not need to be a graph.
The alignments from which a graph would be induced can be indexed by target interval and queried lazily, and a depth-bounded transitive search supplies the homology that graph induction computes up front.
The paper must show four things with measurements: that tracepoint projection is exact against PAF (E1), that the whole HPRC r2 release can be indexed and queried on stated hardware (E2), how much transitive projection recovers against held-out direct alignments and annotation, with and without the two reference stars (E3-E5), and that a local graph induced from the clipped alignments equals the matching part of the global seqwish graph under stated settings (E6).
The thesis does not claim smaller storage: the TPA set is 3.918 times the released GBZ v3 (25,070,431,026 vs 6,398,170,680 bytes), and TPA plus AGC is 28,365,501,759 bytes, 0.840 times the GBZ v1 (33,768,296,600 bytes), before any impg index is added (my arithmetic on the S3 sizes, phase2/s3/tpas.tsv, phase2/s3/pggb_wg.tsv).

## 4. Facts used by the plan and checked in this step

| Fact | Value | Status | Evidence |
| --- | --- | --- | --- |
| Release TPA set | 466 files, 25,070,431,026 bytes, min 33,955,770, median 51,401,828 (middle values 51,399,166 and 51,404,490), max 560,062,985 | NOW | recomputed from phase2/s3/tpas.tsv in this step |
| Release per-target PAF.gz set | 466 files, 318,372,159,094 bytes, median 654,912,957.5 (middle values 654,751,523 and 655,074,392) | NOW | recomputed from phase2/s3/pafs.tsv in this step; judge-feasibility.md used the lower middle value |
| Records | 389,234,668 in total; GRCh38 file 8,916,633; CHM13 file 7,149,766 | NOW | sum of phase2/nm_article/partners.tsv column 2, recomputed; judge-feasibility.md section 1 |
| Encoding | all 466 TPA headers version 1, Standard tracepoints, edit distance, max complexity 128 | NOW | phase2/s3/tpa_headers.tsv; judge-feasibility.md section 1 |
| Composition | 460 hprc_r2 files from 230 samples (HG00272 included), HG06807 mat and pat, HG002 v1.1 mat and pat, GRCh38, CHM13; 232 samples and 464 assembly haplotypes | NOW | judge-feasibility.md section 1; proposal-bioinf-original.md section 2.1 |
| AGC membership | the 466 AGC sample names equal the 466 TPA stems | NOW | judge-feasibility.md section 1 (`agc listset`) |
| Directed network | 25,221 of 216,690 ordered pairs (11.6392%); assembly files list 35 to 74 partners, median 52 | NOW | phase2/nm_article/partner_summary.txt; cross-checked on 2 files by streamed PAF |
| Undirected network | 23,738 of 108,345 unordered pairs (21.9096%); without references 22,809 of 107,416 (21.2343%); 2,966 ordered pairs stored in both files (1,483 unordered) | NOW | phase2/judge/pairs_out.txt |
| Degree and reach | non-reference degree 74 to 123, median 98; every non-reference haplotype reaches all 463 others within 2 hops without either reference (pair graph only, not bases) | NOW | phase2/judge/pairs_out.txt |
| References | GRCh38 and CHM13 files list all 465 others; 45 of 464 assembly files list GRCh38#0 as a query and 51 list CHM13#0 | NOW | phase2/judge/pairs_out.txt |
| C4 in the GRCh38 file | 895 records from 465 haplotypes; 401 haplotypes with depth 1, 59 with 2, 5 with 3; median record query span 533,800 bp | NOW | phase2/judge/c4_depth_out.txt |
| Single-index build RAM floor | 389,234,668 x 56 + 778,469,336 x 48 = 59,163,669,536 bytes held at once (field sizes, not run) | CODE (inference) | judge-feasibility.md section 1.1; recomputed in this step |
| Full-release disk | 61,427,685,951 to 63,916,842,350 bytes for TPA, AGC and index, by three index estimates | estimate | judge-feasibility.md section 3 |
| Explicit `-i` forces single mode; 100 or more files switch to per-file | `IndexMode::Auto` returns single when `alignment.index.is_some()` | CODE | src/main.rs:11277-11291, read in this step |
| Self-hits | written but not expanded ("Only consider for next depth if it's a different sequence") | CODE | src/impg.rs:2574-2589, read in this step |
| Strand across hops | frontier ranges stored with start <= end; BED strand set per row | CODE (derived, not run) | src/impg.rs:282-286, src/main.rs:12072-12079, read in this step |
| Local graphs | `-o gfa` keeps only merged query intervals and calls `dispatch_gfa_engine`, which re-aligns them | CODE | src/main.rs:12324-12340, read in this step |
| `-o paf` rows | full sequence names and lengths, `gi:f`, `bi:f`, `cg:Z`, `an:Z` | CODE | src/main.rs:12240-12295, read in this step |
| Released PGGB files | GBZ v3 6,398,170,680; GBZ v1 33,768,296,600; `.gbz.db` 61,240,860,672; GFA.zst 107,950,343,211 bytes; built with `-p 98 -k 311` | NOW / NOW-ext | phase2/s3/pggb_wg.tsv; phase1/web/hpp_readme.md:155 |
| Shredtools public HPRC r2 index | hprcv2_merged.bumbl 27,424,443,909 + .bi 54,330,664 = 27,478,774,573 bytes | NOW | phase2/gi_all.xml via judge-feasibility.md section 1 |
| HPRC year-1 chr19 PGGB graph | chr19.hprc-v1.0-pggb.gfa.gz, 345,202,999 bytes, built with `-n 90` | NOW | judge-feasibility.md section 1 (freeze1 README) |
| Local data | GRCh38 TPA 560,062,985; GRCh38 PAF.gz 6,532,446,867; AGC 3,295,070,733; existing TPA `.impg` has magic IMPGIDX3, which HEAD rejects | NOW | `ls -la` in this step; judge-feasibility.md section 1; src/impg.rs:1897-1898 |
| Local resources at the 2026-11-08 check | 16 CPUs; 61,478,674,432 bytes RAM, 15,510,704,128 available; 42,340,347,904 bytes free on `/`; `/tmp` tmpfs 978,358,272 bytes free | NOW | `nproc`, `free -b`, `df -B1` in this step |
| Binary provenance | target/release/impg mtime 2026-11-08 22:10:17 -0700 (rebuilt at least 5 times this session, judge-reviewer.md section 1); help of index, query, align, graph, refine, partition, stats is byte-identical to phase2/help | NOW | `stat`, `cmp` in this step |
| Paper-repo submodule | impg-paper records impg at f773342, the checkout is at 7bd50a8 (v0.5.0 tag) with a modified tests/test_pipeline_integration.rs, and HEAD of the separate clone is 0987752, 656 commits later | NOW | `git ls-tree`, `git -C impg rev-parse`, `git rev-list --count` in this step |
| Workgraph | impg-paper/notes/tasks.md:5 records workgraph as removed on user request; impg-paper/CLAUDE.md has 0 matches for "workgraph" or "wg "; `wg` is not on PATH | NOW | `grep`, `command -v` in this step |

## 5. Outline with word budgets and claims

Main text budget 5,000 words ("approximately 5,000 words", impg-paper/references/odgi-paper/README.md:26), abstract 143 words counted apart, supplement 2,500 words; whether legends count toward the 5,000 is unknown (the README line says only "approximately 5,000 words").

### 5.1 Introduction (500 words)

Purpose: the problem, the release fact, the competitor landscape and the contributions, with no tool tour.

| Claim | Status | Source |
| --- | --- | --- |
| PGGB built a 90-haplotype human chr6 graph (15,508,376,475 bp) in 18.46 h with 137.72 GB on 48 threads | NOW-ext | PGGB Nat Methods 21:2008-2012 Table 1 (proposal-bioinf-original.md section 5.1) |
| seqwish induced 38 human haplotypes (114.627 Gbp) in 46,268 s with 347.4983 GB of memory | NOW-ext | PMC9805579 Table 1 (opportunities.md section 3.2 item 2) |
| After a graph exists, odgi extract took 46.87 s and 7.23 GB and vg chunk 1838.51 s and 60.37 GB at 16 threads on 64 HPRC chr6 haplotypes | NOW-ext | ODGI table_extract.tex (phase1_research_digest.txt, COMPETITOR FACTS) |
| HPRC r2 lists "IMPG/PGGB" as a pangenome product, provided "through IMPG (implicit pangenome)", as PAF and "IMPG's TPA format (one file per haplotype, 466 total)" | NOW-ext | phase1/web/hpp_readme.md:151, 183 |
| Shredtools wrote that it was "unable to compute a comparable index over whole assemblies in HPRCr1 or the larger HPRCr2 collection (N=476)" with impg | NOW-ext | paper.txt:285-287 |
| Shredtools also wrote that impg "operates over a sparse sampling" and benchmarked 6% and 17% pair sets; the paper answers only the whole-collection sentence | NOW-ext | paper.txt:301-312 |
| Shredtools returns one window per genome bounded by multi-MUMs, with bounds and no truth set | NOW-ext | paper.txt p.4 and p.13 (phase1_research_digest.txt, COMPETITOR FACTS) |
| PGR-TK surveyed 395 medically relevant genes across 94 HPRC haplotypes | NOW-ext | phase1_research_digest.txt, PGGB LESSONS |
| liftOver chains are pairwise, HAL needs a Cactus alignment, levioSAM2 lifts reads through chains | NOW-ext | Kent 2003 (10.1073/pnas.1932072100); Hickey 2013 (10.1093/bioinformatics/btt128); Chen 2024 (10.1038/s41592-023-02069-6) |
| COSIGT uses `impg query` and `impg refine` as its locus extractor | NOW-ext | Bolognini 2026 Genome Biol 27:286 (10.1186/s13059-026-04242-4); related-work.md section 5 |
| The term "implicit pangenome graph (impg)" appears in Yoo et al. 2025 Supplementary Note III; the paper cites it and does not repeat its unmeasured "exactly equivalent" sentence | NOW-ext | opportunities.md section 5.2 (MOESM1.txt:648, 669-670) |
| The PGGB authors deferred the spanning-tree sparsification question to "implicit pangenome graphs" with the impg link | NOW-ext | phase1/dl_pggb/MOESM3.txt:976-982 |
| Contributions: model, index, closure, the release audit, release-scale evaluation, restriction property | EXP for the scale and accuracy parts | E1-E6 |

### 5.2 Model (450 words, Algorithm 1, Note S1)

Purpose: define the object and its operations formally, as ODGI defined V = (N, E, P), with guarantees and non-guarantees.

| Claim | Status | Source |
| --- | --- | --- |
| An alignment is (q, [qs, qe), t, [ts, te), strand, CIGAR over =, X, I, D, M); other ops panic at query time | CODE | src/impg.rs:81-89 (opportunities.md section 1.1) |
| The implied variation graph G(A) is the seqwish induction of A, and a PGGB graph is G(A) after filtering, smoothing, normalization and sorting | NOW-ext | PMC9805579 induction passage (opportunities.md section 1.2) |
| Each non-self alignment is also inserted as its inverse; self-alignments once | NOW | src/impg.rs:1686-1712; tests/test_transitive_integrity.rs:226-290 |
| Projection pi_a(I) is one CIGAR walk; pure insertions and deletions project to nothing | NOW | src/impg.rs:2791-2929; 9 unit tests at src/impg.rs:3012-3187 |
| The closure H_m has depth m (default 2, 0 unbounded), minimum hop length 101 bp and snapping distance 10 bp | NOW (BFS on synthetic tests) | src/impg.rs:2379-2628; impg query --help; VERIFY_CORRECTIONS.md:46 |
| Self-hits are written but not expanded, so an intra-contig copy propagates one hop | CODE | src/impg.rs:2574-2589; decision D3 |
| BED strand is per hop, not composed back to the query | CODE (derived, not run) | src/impg.rs:282-286; src/main.rs:12072-12079; decision D3 |
| Proposition 1: with the default bidirectional index, m = 0, hop length at most 1, snapping 0 and no filters, the closure is closed under alignment columns between different sequences | CODE (derived) | opportunities.md section 1.6; tested indirectly by E6 |
| Proposition 2: seqwish on the alignments clipped to a closed set equals the global seqwish graph restricted to that set when seqwish `-k` is at most 1 | EXP | opportunities.md section 1.6; E6 |
| Guarantees: every reported interval is linked to the query by at most m alignments and has base-level ends; non-guarantees: completeness depends on the aligned pairs, orthology is not asserted | CODE | odgi-shredtools.md B9; Table 2 |

### 5.3 Implementation (600 words, Fig. 1)

| Claim | Status | Source |
| --- | --- | --- |
| One coitrees BasicCOITree per target; a record holds coordinates, a strand bit (63), a REVERSED bit (62) and a file offset, never a CIGAR or sequence | NOW | src/impg.rs:164-211, 226, 498-508; 11 of 13 tests in tests/test_transitive_integrity.rs index and query |
| IMPGIDX2 layout (header, sequence table, one blob per target, trailing ForestMap); a query decodes only touched trees | NOW (indirect integration coverage) | src/impg.rs:1758-1954; VERIFY_CORRECTIONS.md:288 (G8 correction) |
| TPA and 1ALN inputs rebuild only the CIGAR of segments overlapping the query, with WFA2 and the sequences | CODE (no fixture, no test) | src/impg.rs:1206-1362; E1 |
| `--approximate` interpolates tracepoints for bed and bedpe output only | CODE (no test, no timing) | impg query --help; notes/FAST_MODE_IMPLEMENTATION.md:788 claims a speedup with no timing (VERIFY_CORRECTIONS.md:20); E1 |
| Sequences come from FASTA or AGC behind one trait; one AGC decompressor slot costs 3.70 GB on the HPRC archive, 8 slots by default | NOW (7 AGC tests); CODE (slot cost from a code comment) | tests/test_agc_integration.rs; src/agc_index.rs:61, 87-100 |
| BFS processes each depth in parallel and applies results in a fixed order | NOW for bed on PAF; EXP at scale | src/impg.rs:2379-2628; E2 thread arm |
| Outputs bed, bedpe, paf, fasta, gfa, vcf; only bed and gfa have alignment-backend tests | CODE | VERIFY_CORRECTIONS.md:15-16; code fix C11 |
| `-o gfa` re-aligns the extracted intervals; the paper calls these graphs "built from the homologous intervals", not views of the global graph | CODE | src/main.rs:12324-12340; src/lib.rs:926-951 |
| A single-index build holds every record and interval entry at once: at least 59,163,669,536 bytes for the release | CODE (inference) | src/main.rs:11621-11760; src/impg.rs:1657-1735; judge-feasibility.md section 1.1 |
| Per-file mode is not used in the paper | CODE (0 tests, different BFS) | src/multi_impg.rs:757-780, 813-952; code fix C6 |
| Coordinates are i32 | CODE (limit) | src/impg.rs:164-174, 1669-1694 |

### 5.4 The HPRC r2 implicit pangenome as released (350 words, Table 1, Fig. 2a-c)

| Claim | Status | Source |
| --- | --- | --- |
| 466 TPA files, 25,070,431,026 bytes, 389,234,668 records, all Standard tracepoints with edit distance and max complexity 128 | NOW | section 4 |
| File composition and the 466-file haplotype set, named in every number, with its intersection with Shredtools' N = 476 in Table S11 | NOW for the 466; EXP for the intersection | section 4; judge-reviewer.md must-fix 9 |
| Directed: 25,221 of 216,690 ordered pairs (11.6392%), 35 to 74 partners per assembly file, median 52 | NOW | phase2/nm_article/partner_summary.txt |
| As the bidirectional index walks it: 23,738 of 108,345 unordered pairs (21.9096%), non-reference degree 74 to 123, median 98 | NOW | phase2/judge/pairs_out.txt |
| 1,483 unordered pairs are stored in both files, so their alignments enter the index twice per direction | NOW (pairs); EXP (records) | phase2/judge/pairs_out.txt; E1b |
| Every assembly aligns to GRCh38 and CHM13, and at the pair level every non-reference haplotype reaches all 463 others within 2 hops without either reference, so reference dependence must be measured in bases | NOW (pair graph); EXP (bases) | phase2/judge/pairs_out.txt; E3 |
| The pair-selection rule of the release is unknown: 10 ln(n)/n is 13.1849% at n = 466 against 11.2583% observed among non-reference files | unknown | judge-editor.md V8; question Q2 |
| Who produced the IMPG product is not stated in the release README | unknown | phase1/web/hpp_readme.md:149-191; question Q4 |
| TPA vs PAF record counts are equal for 3 files (550,678; 1,082,733; 8,916,633); content identity is E1 | NOW (counts); EXP (content) | proposal-nm-brief.md section 2 |
| Storage is not a claim: TPA is 3.918 times GBZ v3, TPA plus AGC is 0.840 times GBZ v1 before the index; Shredtools hprcv2_merged.bumbl plus .bi is 27,478,774,573 bytes | NOW (sizes, arithmetic) | section 4 |

### 5.5 Results (2,500 words)

| Subsection | Words | Experiment | Display |
| --- | ---: | --- | --- |
| 5.5.1 Tracepoint projection equals CIGAR projection | 200 | E1 | Fig. S2 |
| 5.5.2 Indexing and querying the whole release | 450 | E2, E8 | Fig. 3, Fig. S3 |
| 5.5.3 Reach and reference dependence on the release | 400 | E3 | Fig. 2d, Fig. 4c |
| 5.5.4 Sparse alignment sets and transitive error | 400 | E4 | Fig. 4a |
| 5.5.5 Gene-level accuracy and Shredtools on the same input | 400 | E5 | Fig. 4b |
| 5.5.6 Local graphs as restrictions of the implied graph | 300 | E6 | Fig. 5a |
| 5.5.7 Locus refinement | 200 | E10 | Fig. 5b |
| 5.5.8 Disjoint work units on yeast | 150 | E9 | Fig. S4 |

Claims per subsection (all numbers are slots filled by the named experiment, written so that either direction can be reported).

| Claim | Status | Source |
| --- | --- | --- |
| TPA exact rows equal PAF rows at `-m` 0, 1 and 2; dropped tracepoint hits are counted; `--approximate` boundary deltas and speed are reported, not tuned | EXP | E1 |
| impg indexes the 466 files in [H] h with [G] GB peak RSS into a [B]-byte index on [node] | EXP | E2 |
| Per-query median and p95 wall and peak RSS at 1 kb, 10 kb, 100 kb and 1 Mb, `-m` 1 and 2, exact and approximate, for impg, vg chunk on GBZ v3 and Shredtools on hprcv2_merged.bumbl, with the competitor's wins in the main text | EXP | E2 |
| Output is identical across `-t` 1, 4 and 16 | EXP | E2 |
| Concordance with the PGGB graph of the same alignments is consistency, not truth, with a target fixed in advance because `-k 311` drops matches shorter than 311 bp | EXP | E8; phase1/web/hpp_readme.md:155 |
| bp reached and bp recall of held-out partners at `-m` 1 to 4 and 0, with and without GRCh38 and CHM13 as bridges | EXP | E3b |
| GRCh38 to CHM13 projection through haplotypes after removing the direct pair, against the direct projection and a public chain | EXP | E3a |
| bp recall, precision and exact-boundary rate at 0, 10 and 100 bp against held-out direct alignments by pair fraction and depth, tuned on chr19, scored once on ScRAP 142 | EXP | E4 |
| `--sparsify auto` is `tree:5:2:0.05` above 50 genomes and keeps 7.6923% to 20.3774% of pairs at n = 92 (bounds), so Shredtools' "17%, the default auto setting" plausibly is impg's auto | CODE (sweepga 4713ce0 knn_graph.rs:427-451); inference | judge-editor.md V14-V15; checked by the joblist step of E5 |
| `giant:<p>` is a k-nearest-neighbour rule with k = 2 at p = 0.99 for n = 7, 235, 1,000 and 10,000, not Erdős-Rényi | CODE | VERIFY_CORRECTIONS.md:91-92 |
| Per gene and haplotype containment, flank excess and wrong-locus rate against CAT GENCODE38 for impg (all pairs, 17%, 6%, auto, CHM13 star) and Shredtools on the same FASTA, with alignment, index and query cost apart | EXP | E5 |
| Shredtools' own numbers for impg v0.4.0 (4.01 s and 1.66 GB all pairs; 0.21 s and 12 MB sparse; 0.484 s and 79 MB Shredtools) are cited as theirs, not as impg results | NOW-ext | paper.txt:308-312 |
| Restricted and global seqwish graphs agree base by base at `-k 0`; the gap at `-k 23`, at CLI closure defaults and for today's `-o gfa` path is reported | EXP | E6 |
| refine keeps [n] haplotypes spanning both ends at TERT and IGKV6-21 with [bp] extension; Shredtools zoom kept 0 bp bounds at IGKV6-21 by dropping 2 of 15 T2T haplotypes | EXP; NOW-ext | E10; paper.txt:445-454 |
| refine has 1 unit test and no CLI test | CODE | partition-regional.md G5; code fix C11 |
| On ScRAP 142 the alignment-backed partition has [n] partitions, 0 uncovered bp and 0 bp owned twice, or reports the counts it finds | EXP | E9 |
| The only exact-once audit on record is the syng-backed yeast235 run at 295bca9 (19,421 partitions, 3,336,976,856 bp, 0 uncovered, 0 owned twice), on a backend outside the paper, with 11 partition-related commits since | NOW (out of scope backend) | VERIFY_CORRECTIONS.md:72-73 |

### 5.6 Discussion (500 words)

| Claim | Status | Source |
| --- | --- | --- |
| The main cost of an implicit pangenome is the alignment; HPRC r2 paid it for PGGB, and impg adds an index and per-query work; the PGGB build cost is [stage split] or unknown | NOW-ext; EXP | phase1/web/hpp_readme.md:151; question Q3 |
| Stated limits from section 11 (storage, alignment cost, giant, partitioned memory, re-aligned local graphs, self-hits, strand, paralogs reported but not classified) | CODE | section 11 |
| No remote access: impg has no HTTP code, and Shredtools serves queries by HTTP Range requests | CODE (absence); NOW-ext | odgi-shredtools.md C item 7; phase1_research_digest.txt COMPETITOR FACTS |
| Shredtools multi-MUMs are complementary and could feed impg as a homology source, as its authors suggest | NOW-ext | paper.txt:528-532 |
| The syncmer backend, genotyping and genome inference are future work, with their open bugs named | WIP | section 10 |
| Copy-level statements depend on whether the alignments store each copy as its own record, which E7 measures | NOW (C4 on GRCh38); EXP (other loci) | phase2/judge/c4_depth_out.txt; E7 |

### 5.7 Availability (100 words)

| Claim | Status | Source |
| --- | --- | --- |
| impg is MIT licensed | NOW | /home/guarracino/git/impg/LICENSE |
| The paper's release has a tag, a Zenodo version DOI and a container built from the tag | EXP (not cut) | code fix C1; Dockerfile:38 clones the default branch |
| One script per figure and table in the paper repository, with commands, versions and the binary sha256 in Table S9 | EXP | code fix C14 |

### 5.8 Supplement (2,500 words)

Fig. S1 worked toy example from test fixtures (CODE to NOW); Note S1 proofs of Propositions 1 and 2 (CODE, derived); Note S2 sparsification definitions (CODE, sweepga 4713ce0); Note S3 partition termination for `-w` at least 1 (CODE, src/commands/partition.rs:297, 945-948, 981-996); Tables S1-S8 benchmark grids (EXP); Table S9 commands, versions and binary hashes (EXP); Table S10 feature and test matrix (partly NOW, evidence-inventory.md section 3); Table S11 haplotype sets (466 files, Shredtools N = 476, HPRC2 abstract 460, graph 464) and their intersection (partly NOW); Figs. S2-S5 from E1, E8, E9, E7.

## 6. Display items

| ID | Title | Panels | Data status |
| --- | --- | --- | --- |
| Fig. 1 | The implicit pangenome graph | a, sequences as coordinate spaces and alignments as edges, projection of an interval through one CIGAR; b, bidirectional entries and a 2-hop closure with visited sets, depth m, hop length 101 bp and snapping 10 bp; c, on-disk index (IMPGIDX2 header, sequence table, per-target blobs, ForestMap) and lazy loading; d, command-to-format map for index, query, refine, partition, align and stats | CODE (schematic from src/impg.rs:164-211, 1686-1712, 1758-1954, 2379-2628) |
| Algorithm 1 | Depth-bounded transitive projection | BFS over frontier ranges with per-sequence SortedRanges | CODE (src/impg.rs:2379-2628) |
| Table 1 | Datasets | HPRC r2 composition (466 files by group, bytes, records), HPRC year-1 chr19 set, ScRAP 142, yeast chrV fixture, CAT GENCODE38, accessions and URLs | NOW for HPRC r2 and the fixture; EXP for the chr19 set and ScRAP sizes |
| Table 2 | What each tool guarantees | impg, Shredtools, PGR-TK, liftOver/HAL, odgi/vg: inputs, coordinate system, guarantees, copies, remote access, update model | NOW-ext and CODE (odgi-shredtools.md B9) |
| Fig. 2 | The HPRC r2 implicit pangenome as released | a, directed partners per file (35 to 74, median 52); b, undirected degree (74 to 123, median 98) with the 1,483 reciprocal pairs; c, the two reference stars; d, bp reached per depth from non-reference regions with and without the reference bridges | a-c NOW; d EXP (E3b) |
| Fig. 3 | Cost on the whole release | a, index build wall, peak RSS and bytes; b, per-query wall and RSS by region size for impg exact, impg approximate, vg chunk on GBZ v3 and Shredtools on bumbl; c, bytes on disk of PAF.gz, TPA, impg index, GBZ v1, GBZ v3, `.gbz.db`, bumbl; d, thread sweep 1 to 48 and output identity; axes from 0 | c NOW except the impg index bar; a, b, d EXP (E2) |
| Fig. 4 | What transitive projection recovers | a, bp recall and exact-boundary rate vs pair fraction and depth, chr19 tuning and ScRAP 142 holdout; b, gene-copy containment, flank excess and wrong-locus rate vs CAT for impg and Shredtools; c, held-out partner recall on the release with and without reference bridges, and GRCh38 to CHM13 against the public chain | EXP (E4, E5, E3) |
| Fig. 5 | Local graphs and locus boundaries | a, bases with a differing node class between restricted and global seqwish graphs at `-k 0`, `-k 23`, CLI closure defaults and today's `-o gfa`; b, refine vs Shredtools zoom at TERT and IGKV6-21, haplotypes kept vs interval length | EXP (E6, E10) |
| Fig. S1 | Worked toy example | every coordinate of a projection, a REVERSED inversion and a 2-hop closure | NOW (fixtures in tests/test_transitive_integrity.rs) |
| Fig. S2 | TPA vs PAF and approximate mode | identity per region and depth; boundary delta CDF; speed | EXP (E1) |
| Fig. S3 | Consistency with the released PGGB graph | per region and haplotype bp Jaccard by segmental duplication, satellite and other | EXP (E8) |
| Fig. S4 | Alignment-backed partition audit on ScRAP 142 | partitions, member intervals, uncovered bp, bp owned twice, cross-chromosome partitions | EXP (E9) |
| Fig. S5 | Copy representation in the released alignments | records per haplotype and per-base record depth at C4, AMY1, SMN1/SMN2, LPA, CYP2D6 in 5 target files | C4 on GRCh38 NOW; rest EXP (E7) |

## 7. Experiments

Rules for every run.
- One tagged impg build (`$IMPG`), never the target/release binary that other work rebuilds; record `sha256sum $IMPG`, `$IMPG --version`, the commit, host, threads and `/usr/bin/time -v` output next to each result (code fix C1).
- Single-index mode for every benchmark: always pass `-i <file>`, which forces single mode (src/main.rs:11277-11291).
- Fixed seeds for every region set; the 200-region holdouts and ScRAP 142 are never used to choose `-d`, `-m`, `--min-transitive-len`, `--min-distance-between-ranges` or subset fractions; report tuning and holdout scores side by side.
- Local scratch in /home/guarracino/git/impg-paper/experiments/<name>/ on `/` (42,340,347,904 bytes free), never in `/tmp` (978,358,272 bytes free); cluster scratch in /scratch/aguarracino/impg-paper/<name>/.
- `IMPG_AGC_DECOMPRESSOR_SLOTS` set so that slots x 3.70 GB fits the free RAM (2 slots on the workstation at the 15,510,704,128 available bytes measured on 2026-11-08; src/agc_index.rs:61, 87-100).
- Only impg flags printed by `impg <cmd> --help` are used (phase2/help, byte-identical to the help of the binary with mtime 2026-11-08 22:10:17 -0700); external tool flags come from their local `--help` (seqwish v0.7.11-35-gaab5bee, odgi v0.9.4-82-g34c461ff, vg v1.76.1, wfmash with `-T` and `--pairs-file`, bedtools v2.31.1); Shredtools, Mumemto, gbz-base, liftOver, paf2chain, halLiftover and Cactus are not installed, so their commands are not written and their flags are unknown.
- Scripts named below (`subset_pairs.py`, `compare_classes.py`, `bp_metrics.py`, `exact_once_audit.py`, `chunk_paths_to_bed.py`, `locus_depth.py`) do not exist yet; each is part of the harness (code fix C14) and is validated on toy data first.

Common variables used below.

```
IMPG=/path/to/impg-<tag>/target/release/impg        # one tagged build, hashed per run
D=/home/guarracino/git/impg/data/hprcv2
P38=$D/GCA_000001405.15_GRCh38_no_alt_analysis_set.PanSN.merged.paf.gz
T38=$D/GCA_000001405.15_GRCh38_no_alt_analysis_set.PanSN.merged.edit-distance.128.tpa
AGC=$D/HPRC_r2_assemblies_0.6.1.agc
X=/home/guarracino/git/impg-paper/experiments      # local
S=/scratch/aguarracino/impg-paper                  # cluster
R2=s3://human-pangenomics/pangenomes/freeze/release2
```

### Tier 1 (required for the Bioinformatics Original Paper)

#### E1. TPA projection equals PAF projection (local, gate)

- Question: does exact TPA projection give the same rows as PAF projection of the same alignments, how many tracepoint hits are dropped, and what does `--approximate` change?
- Dataset: GRCh38 star on disk (TPA 560,062,985 bytes; PAF.gz 6,532,446,867 bytes; AGC 3,295,070,733 bytes); 1,000 random 10 kb GRCh38 regions plus 200 held out (seed 1). E1b: two assembly TPA files that list each other (one of the 1,483 reciprocal pairs, chosen from phase2/judge/pairs_out.txt inputs), their two per-target PAF.gz files (median 654,912,957.5 bytes each).
- Compared: impg PAF exact vs impg TPA exact vs impg TPA `--approximate`; E1b bidirectional vs `--unidirectional`.
- Metrics: identical sorted rows (%), rows only in one output, max start and end delta (bp), dropped-hit count (after C2), index bytes, wall, peak RSS; E1b index entries vs 2 x records and merged-BED identity.
- Commands:
```
mkdir -p $X/e1 && cd $X/e1
export IMPG_AGC_DECOMPRESSOR_SLOTS=2
/usr/bin/time -v $IMPG index -a $P38 -i paf.impg -f -t 16 -v 1 2> paf.index.time
/usr/bin/time -v $IMPG index -a $T38 -i tpa.impg -f -t 16 -v 1 2> tpa.index.time   # -f: existing .impg is IMPGIDX3
$IMPG stats -a $P38 -i paf.impg --list-sequences > grch38.seqs.tsv
awk -F'\t' '$1 ~ /^GRCh38#0#chr[0-9XY]+$/ {print $1"\t"$2}' grch38.seqs.tsv > g38.genome
bedtools random -l 10000 -n 1200 -seed 1 -g g38.genome > r1200.bed      # random order; split before sorting
head -n 1000 r1200.bed | sort -k1,1 -k2,2n > tune.bed; tail -n 200 r1200.bed | sort -k1,1 -k2,2n > hold.bed
for b in tune hold; do for m in 0 1 2; do
  /usr/bin/time -v $IMPG query -a $P38 -i paf.impg -b $b.bed --no-merge -x -m $m -o bedpe -O paf.$b.m$m -t 16 2> paf.$b.m$m.time
  /usr/bin/time -v $IMPG query -a $T38 -i tpa.impg -b $b.bed --no-merge -x -m $m --sequence-files $AGC -o bedpe -O tpa.$b.m$m -t 16 -v 2 2> tpa.$b.m$m.time
  /usr/bin/time -v $IMPG query -a $T38 -i tpa.impg -b $b.bed --no-merge -x -m $m --approximate -o bedpe -O apx.$b.m$m -t 16 2> apx.$b.m$m.time
done; done
python3 -I bp_metrics.py --mode identity paf.tune.m1.bedpe tpa.tune.m1.bedpe   # likewise for every b, m and for apx
# E1b: A.tpa and B.tpa list each other
$IMPG index -a A.tpa B.tpa -i ab.bi.impg -f -t 16
$IMPG index -a A.tpa B.tpa -i ab.uni.impg -f --unidirectional -t 16
$IMPG query -a A.tpa B.tpa -i ab.bi.impg -b ab.bed -d 0 -x -m 2 --sequence-files $AGC -o bed -O ab.bi -t 16
$IMPG query -a A.tpa B.tpa -i ab.uni.impg -b ab.bed -d 0 -x -m 2 --sequence-files $AGC -o bed -O ab.uni -t 16
```
- Compute: workstation; 0 bytes to download for E1, two TPA files (median 51,401,828 bytes) and two PAF.gz files for E1b; two indexes of 757,392,357 to 814,414,241 bytes each by the sizes of the older indexes on disk; wall time unknown.
- Blockers: C1 (tag), C2 (TPA fixtures and dropped-hit counter), C4 (file-list binding), C5 (stats on a fresh index; here the index is written first); `--min-result-identity` stays unset (C2).
- Feeds: Fig. S2, section 5.5.1, flip condition F1; gates every TPA number in E2-E10.

#### E2. Index and query the whole release (cluster)

- Question: can impg index all 389,234,668 released alignments on one node in single mode, and what does a query cost against the released graph and against Shredtools' released index?
- Dataset: `$R2/impg/tpas/` (466 files, 25,070,431,026 bytes), AGC (3,295,070,733 bytes, copied from the workstation), GBZ v3 `$R2/pggb/gfas/whole-genome/20250930_hprc25272.p98-k311.tmp.fix.v3.gbz` (6,398,170,680 bytes), Shredtools `s3://genome-idx/mumemto/hprc/hprcv2_merged.bumbl` and `.bumbl.bi` (27,478,774,573 bytes); regions: 1,000 random regions per size class (1 kb, 10 kb, 100 kb, 1 Mb) on non-reference haplotypes and 1,000 on GRCh38, seed 2, 200 per class held out; one whole-chromosome query.
- Compared: impg exact and `--approximate`; vg v1.76.1 `chunk` on GBZ v3; Shredtools v0.1.0 extract on hprcv2_merged.bumbl; gbz-base on the `.gbz.db` only if installed (optional arm).
- Metrics: index wall, CPU time, peak RSS, index bytes; per query median and p95 wall and peak RSS, 5 replicates, warm cache (cold cache only if the cluster allows dropping the page cache, unknown); batch throughput with `-b`; whole-chromosome wall and RSS; output identity across `-t` 1, 4 and 16; dropped-hit count; where each competitor wins.
- Commands:
```
mkdir -p $S/e2/tpas $S/e2/q $S/e2/vg $S/e2/cons && cd $S/e2
aws s3 cp --no-sign-request --recursive $R2/impg/tpas/ tpas/
ls $PWD/tpas/*.tpa | sort > tpa466.list && sha256sum tpas/*.tpa > tpa466.sha256
/usr/bin/time -v $IMPG index --alignment-list tpa466.list -i r2.impg -t 32 -v 1 2> r2.index.time
$IMPG stats --alignment-list tpa466.list -i r2.impg > r2.stats
$IMPG stats --alignment-list tpa466.list -i r2.impg --list-sequences > r2.seqs.tsv
awk -F'\t' '$1 !~ /^(GRCh38|CHM13)#/ {print $1"\t"$2}' r2.seqs.tsv > nonref.genome
awk -F'\t' '$1 ~ /^GRCh38#0#chr[0-9XY]+$/ {print $1"\t"$2}' r2.seqs.tsv > g38.genome
for L in 1000 10000 100000 1000000; do bedtools random -l $L -n 1200 -seed 2 -g nonref.genome > nr.$L.bed; done   # first 1,000 tuning, last 200 held out
bedtools random -l 10000 -n 1200 -seed 2 -g g38.genome > g38.10000.bed
for L in 1000 10000 100000 1000000; do for m in 1 2; do for rep in 1 2 3 4 5; do
  while read c b e n; do
    /usr/bin/time -v $IMPG query --alignment-list tpa466.list -i r2.impg -r "$c:$b-$e" -d 0 -x -m $m --sequence-files $AGC -o bedpe -O q/ex.$L.$m.$rep.$n -t 1 2> q/ex.$L.$m.$rep.$n.time
    /usr/bin/time -v $IMPG query --alignment-list tpa466.list -i r2.impg -r "$c:$b-$e" -d 0 -x -m $m --approximate -o bedpe -O q/ap.$L.$m.$rep.$n -t 1 2> q/ap.$L.$m.$rep.$n.time
  done < <(head -n 1000 nr.$L.bed)
done; done; done
for t in 1 4 16; do $IMPG query --alignment-list tpa466.list -i r2.impg -b nr.10000.bed -d 0 -x -m 2 --sequence-files $AGC -o bedpe -O batch.t$t -t $t; done
/usr/bin/time -v $IMPG query --alignment-list tpa466.list -i r2.impg -r 'CHM13#0#chr1' -d 0 -o bed -O chr1 -t 16 2> chr1.time
aws s3 cp --no-sign-request $R2/pggb/gfas/whole-genome/20250930_hprc25272.p98-k311.tmp.fix.v3.gbz .
while read c b e n; do /usr/bin/time -v vg chunk -x 20250930_hprc25272.p98-k311.tmp.fix.v3.gbz -p "$c:$b-$e" -c 0 -O gfa -t 1 > vg/$n.gfa 2> vg/$n.time; done < <(head -n 1000 g38.10000.bed)
# Shredtools extract on hprcv2_merged.bumbl with the same BED: not written (not installed, flags unknown)
```
- Compute: cluster node with more than 59,163,669,536 bytes of RAM (build floor) and 61,427,685,951 to 63,916,842,350 bytes of scratch plus 33,877,515,253 bytes for GBZ v3 and bumbl; downloads 25,070,431,026 + 6,398,170,680 + 27,478,774,573 bytes; wall unknown; node size of gemini unknown (decision D5).
- Blockers: C1-C6, C9, C14; vg v1.76.1 help says "graph or XG index", so whether it reads the released v3 GBZ is unknown; GBZ path names (PanSN form assumed); Shredtools and Mumemto install; the bedtools genome file for non-reference haplotypes is built from r2.seqs.tsv.
- Feeds: Fig. 3, section 5.5.2, abstract [H] [G] [T], flip condition F2.

#### E3. Reach and reference dependence (E3a local, E3b cluster)

- Question: how much of what a query reaches depends on GRCh38 and CHM13, measured in bases, and how well does transitive projection recover a held-out direct alignment?
- Dataset: E3a, the GRCh38 star on disk plus the CHM13 per-target PAF.gz (`$R2/impg/pafs/all-vs-1/chm13v2.0_maskedY_rCRS.fa.PanSN.merged.paf.gz`, 5,590,178,237 bytes), 1,200 random 1 kb GRCh38 regions (seed 3, 200 held out), the public UCSC GRCh38-to-CHM13 chain (file name and provenance to record). E3b, the E2 index; 10 non-reference query haplotypes Q_i (seed 4) each with one partner P_i whose records are stored only in Q_i's file (non-reciprocal pair), Q_i's per-target PAF.gz (10 files, 6,549,129,575 bytes at the median size), 100 random 10 kb regions per Q_i (20 held out).
- Compared: E3a, direct GRCh38-to-CHM13 projection vs 2-hop projection through haplotypes after removing the direct pair vs the public chain; E3b, direct projection Q_i to P_i on the full index vs transitive projection on the held-out index, each with and without the two references as bridges.
- Metrics: bp recall and precision per region and target haplotype, exact-boundary rate at 0, 1, 10 and 100 bp, strand agreement, haplotypes and bp reached per depth.
- Commands:
```
mkdir -p $X/e3a && cd $X/e3a
aws s3 cp --no-sign-request $R2/impg/pafs/all-vs-1/chm13v2.0_maskedY_rCRS.fa.PanSN.merged.paf.gz chm13.paf.gz
pigz -dc $P38 | awk -F'\t' -v OFS='\t' '!($1 ~ /^CHM13#/)' | bgzip -@ 8 > g38.noCHM13.paf.gz
pigz -dc chm13.paf.gz | awk -F'\t' -v OFS='\t' '!($1 ~ /^GRCh38#/)' | bgzip -@ 8 > chm13.noGRCh38.paf.gz
$IMPG index -a $P38 chm13.paf.gz -i full.impg -f -t 16
$IMPG index -a g38.noCHM13.paf.gz chm13.noGRCh38.paf.gz -i held.impg -f -t 16
bedtools random -l 1000 -n 1200 -seed 3 -g g38.genome | sort -k1,1 -k2,2n > g38.1k.bed
$IMPG query -a $P38 chm13.paf.gz -i full.impg -b g38.1k.bed -d 0 -o bedpe -O direct -t 16
for m in 2 3; do $IMPG query -a g38.noCHM13.paf.gz chm13.noGRCh38.paf.gz -i held.impg -b g38.1k.bed -d 0 -x -m $m -o bedpe -O held.m$m -t 16; done
# chain arm: liftOver is not installed; lift g38.1k.bed with the public chain, then bp_metrics.py
mkdir -p $S/e3b && cd $S/e3b
awk '$1 !~ /^(GRCh38|CHM13)#/ {print $1}' ../e2/r2.seqs.tsv > nonref_contigs.txt     # subset list: every non-reference contig
while read q; do awk -F'\t' -v q="$q#" 'index($1,q)==1 {print $1"\t"$2}' ../e2/r2.seqs.tsv > $q.genome; bedtools random -l 10000 -n 100 -seed 4 -g $q.genome; done < q10.txt > q10.bed   # q10.txt: the 10 Q_i as SAMPLE#HAP
for m in 1 2 3 4 0; do
  $IMPG query --alignment-list ../e2/tpa466.list -i ../e2/r2.impg -b q10.bed -d 0 -x -m $m --sequence-files $AGC -o bedpe -O refs.m$m -t 16
  $IMPG query --alignment-list ../e2/tpa466.list -i ../e2/r2.impg -b q10.bed -d 0 -x -m $m --subset-sequence-list nonref_contigs.txt --sequence-files $AGC -o bedpe -O norefs.m$m -t 16
done
# held-out index: Q_i's TPA replaced by Q_i's per-target PAF without P_i's records
pigz -dc Qi.paf.gz | awk -F'\t' -v p="$Pi#" 'index($1,p)!=1' | bgzip -@ 8 > Qi.held.paf.gz    # once per Q_i
grep -v -F -f q10_tpa_stems.txt ../e2/tpa466.list > held.list && ls $PWD/*.held.paf.gz >> held.list   # 456 TPA + 10 filtered PAF
/usr/bin/time -v $IMPG index --alignment-list held.list -i held.impg -f -t 32 2> held.index.time   # 456 TPA + 10 filtered PAF
$IMPG query --alignment-list ../e2/tpa466.list -i ../e2/r2.impg -b q10.bed -d 0 -o bedpe -O truth.direct -t 16
for m in 1 2 3 4 0; do
  $IMPG query --alignment-list held.list -i held.impg -b q10.bed -d 0 -x -m $m --sequence-files $AGC -o bedpe -O held.refs.m$m -t 16
  $IMPG query --alignment-list held.list -i held.impg -b q10.bed -d 0 -x -m $m --subset-sequence-list nonref_contigs.txt --sequence-files $AGC -o bedpe -O held.norefs.m$m -t 16
done
```
- Compute: E3a on the workstation, 5,590,178,237 bytes to download, filtered copies of 6,532,446,867 and 5,590,178,237 bytes at most, two indexes; E3b on the cluster after E2, 6,549,129,575 bytes to download at the median size, one more single-index build with the E2 RAM floor; wall unknown.
- Blockers: C2 must add a mixed PAF and TPA index test, because the held-out index mixes formats (CODE, untested, opportunities.md section 2); C7 (strand and self-hit decision) before strand agreement is scored; the subset filter keeps the query target and matches PanSN at haplotype or sample level (VERIFY_CORRECTIONS.md:18), so the list holds every non-reference contig; `-m 0` on the release may not finish (unknown), and is then reported as not finished; liftOver install and chain provenance.
- Feeds: Fig. 2d, Fig. 4c, section 5.5.3, flip condition F3.

#### E4. Sparse alignment sets and transitive error (tuning chr19 from E5, holdout ScRAP 142)

- Question: as the fraction of aligned pairs falls, how much homology does transitive projection recover against direct all-pairs projection, by depth?
- Dataset: tuning, the all-pairs chr19 alignments of E5; holdout, ScRAP 142 S. cerevisiae assemblies (O'Donnell et al. 2023, Nat Genet 55:1390-1399, 10.1038/s41588-023-01459-y; accessions and download path not checked), one bgzipped FASTA per strain with PanSN names; 1,000 random 10 kb regions on non-hub strains (seed 5).
- Compared: impg on subsets (random 0.06, random 0.17, the `--sparsify auto` pair list, a star to one strain fixed in advance) vs direct projection on the all-pairs index.
- Metrics: pairs aligned, alignment CPU time, bp recall, bp precision, exact-boundary rate at 0, 10 and 100 bp, haplotypes reached, per `-m` 1, 2, 3, 4 and 0; tuning and holdout reported side by side.
- Commands:
```
mkdir -p $X/e4 && cd $X/e4      # ScRAP FASTAs in $X/e4/scrap142/*.fa.gz (bgzip + samtools faidx)
$IMPG align --sequence-files scrap142/*.fa.gz --format joblist --sparsify auto -o jobs_auto
/usr/bin/time -v $IMPG align --sequence-files scrap142/*.fa.gz --wfmash --format paf --sparsify none -o y_all -t 16 2> y_all.align.time
python3 -I subset_pairs.py --paf y_all/alignments.paf --mode random --fraction 0.06 --seed 1 > r006.paf
python3 -I subset_pairs.py --paf y_all/alignments.paf --mode random --fraction 0.17 --seed 1 > r017.paf
python3 -I subset_pairs.py --paf y_all/alignments.paf --mode joblist --jobs jobs_auto > auto.paf
python3 -I subset_pairs.py --paf y_all/alignments.paf --mode star --hub "$HUB" > star.paf
cp y_all/alignments.paf all.paf
for s in all r006 r017 auto star; do bgzip -f -@ 8 $s.paf; $IMPG index -a $s.paf.gz -i $s.impg -f -t 16; done
$IMPG query -a all.paf.gz -i all.impg -b y_r1000.bed -d 0 -o bedpe -O truth.direct -t 16
for s in r006 r017 auto star; do for m in 1 2 3 4 0; do
  $IMPG query -a $s.paf.gz -i $s.impg -b y_r1000.bed -d 0 -x -m $m -o bedpe -O $s.m$m -t 16
done; done
```
- Compute: workstation for index and query; the all-pairs wfmash run over 10,011 pairs (n = 142) has unknown wall time, so it may move to the cluster; ScRAP download size unknown (the PGGB scerevisiae142 input is 1,702,093,905 bp, PGGB Table 1, and whether it is the same set is unknown).
- Blockers: ScRAP accessions; the hub strain (decision D8); `random:` pair hashing uses `DefaultHasher`, so pairs are drawn by the harness with a fixed seed, not by `impg align` (partition-regional.md G27); per-genome FASTA because FastGA on one FASTA ignores the pair set (src/commands/align.rs:485-500); C14.
- Feeds: Fig. 4a, section 5.5.4.

#### E5. Gene-level accuracy and Shredtools on the same input (cluster)

- Question: on HPRC year-1 chr19, how often does each tool return the annotated copy of a gene per haplotype, with what flank, and at what alignment, index and query cost?
- Dataset: chr19 paths of `s3://human-pangenomics/pangenomes/freeze/freeze1/pggb/chroms/chr19.hprc-v1.0-pggb.gfa.gz` (345,202,999 bytes, 90 haplotypes from `-n 90`); truth, the 178 CAT GENCODE38 GFF3 files under `s3://human-pangenomics/submissions/FC7E9302-5A35-4A4F-9D4A-B3E957118E36--Y1_CAT_ANNOTATION_GENCODE38/`; the gene BED on CHM13 chr19 from the same annotation; 1,000 random regions (seed 6) for latency. The set is named as ours, because Shredtools' 92-haplotype list is not in the preprint (paper.txt:283-312) and the year-1 graphs hold 90 (judge-feasibility.md section 1).
- Compared: impg tag on all pairs, random 0.17, random 0.06, the `auto` pair list and a CHM13 star (filtered from all pairs); Shredtools v0.1.0 with Mumemto on the same per-haplotype FASTA.
- Metrics: per stage (alignment, index, query) wall, CPU time and peak RSS at 1, 8, 16 and 48 threads; bytes of PAF and index; per gene and haplotype containment of the CAT interval, flank excess bp, wrong-locus rate, copies returned; per-query median and p95; the number of pairs that `--sparsify auto` selects at this n (tests whether Shredtools' "17%" is impg's auto).
- Commands:
```
mkdir -p $S/e5/hap && cd $S/e5
aws s3 cp --no-sign-request s3://human-pangenomics/pangenomes/freeze/freeze1/pggb/chroms/chr19.hprc-v1.0-pggb.gfa.gz .
zcat chr19.hprc-v1.0-pggb.gfa.gz > chr19.gfa
odgi build -g chr19.gfa -o chr19.og -t 48
odgi paths -i chr19.og -f > chr19.paths.fa
python3 -I split_by_haplotype.py chr19.paths.fa hap/      # one bgzipped, faidx-indexed FASTA per PanSN haplotype
$IMPG align --sequence-files hap/*.fa.gz --format joblist --sparsify auto -o jobs_auto
/usr/bin/time -v $IMPG align --sequence-files hap/*.fa.gz --wfmash --format paf --sparsify none -o aln_all -t 48 2> align.all.time
cp aln_all/alignments.paf all.paf
python3 -I subset_pairs.py --paf all.paf --mode random --fraction 0.17 --seed 1 > r017.paf
python3 -I subset_pairs.py --paf all.paf --mode random --fraction 0.06 --seed 1 > r006.paf
python3 -I subset_pairs.py --paf all.paf --mode joblist --jobs jobs_auto > auto.paf
python3 -I subset_pairs.py --paf all.paf --mode star --hub 'CHM13#' > star.paf
for s in all r017 r006 auto star; do
  bgzip -f -@ 16 $s.paf
  for t in 1 8 16 48; do /usr/bin/time -v $IMPG index -a $s.paf.gz -i $s.t$t.impg -f -t $t 2> $s.index.t$t.time; done
  $IMPG query -a $s.paf.gz -i $s.t48.impg -b cat_genes_chm13_chr19.bed -d 0 -x -m 2 -o bedpe -O genes.$s -t 16
  while read c b e n; do /usr/bin/time -v $IMPG query -a $s.paf.gz -i $s.t48.impg -r "$c:$b-$e" -d 0 -x -m 2 -o bed -O lat/$s.$n -t 1 2> lat/$s.$n.time; done < rand1000.bed
done
python3 -I bp_metrics.py --mode genes --truth cat/ --calls genes.all.bedpe   # likewise per subset and for Shredtools
# Shredtools and Mumemto on hap/*.fa.gz: not written (not installed, flags unknown)
```
- Compute: cluster at 48 threads (Shredtools' setting, paper.txt:346-349); for the alignment, the pair count is 4,005 at n = 90 (my arithmetic, 90 x 89 / 2) and the wall time is unknown; CAT download size unknown (one file is 95,737,432 bytes).
- Blockers: CAT seqids must be joined to PanSN contig names (not checked); the haplotypes with CAT files vs the 90 graph paths (overlap unknown); Shredtools and Mumemto install; question Q5 to the Shredtools authors; C14.
- Feeds: Fig. 4b, section 5.5.5, Table S1-S4, flip condition F4.

#### E6. Local graphs as restrictions of the implied graph (local)

- Question: does seqwish on the alignments clipped to a closed interval set give the same node classes as the global seqwish graph restricted to that set (Proposition 2), and how far are the CLI defaults and today's `-o gfa` path from it?
- Dataset: tuning, tests/test_data/yeast.chrV.fa.gz (7 sequences, 4,029,392 bp), 100 random 10 kb loci (seed 7); holdout, the C4 region (GRCh38#0#chr6:31891045-32123783) for 20 haplotypes (seed 8) extracted from the AGC.
- Compared: restricted seqwish graph vs global seqwish graph at `-k 0`; the same at `-k 23`; closure at CLI defaults (`-m 2`, 101, 10); today's `impg query -o gfa --gfa-engine seqwish`.
- Metrics: bases of C whose node class differs (count and fraction), per locus and in total.
- Commands:
```
mkdir -p $X/e6 && cd $X/e6
Y=/home/guarracino/git/impg/tests/test_data/yeast.chrV.fa.gz
$IMPG align --sequence-files $Y --wfmash --format paf --sparsify none -o aln -t 16
seqwish -p aln/alignments.paf -s $Y -g global.k0.gfa -k 0 -t 16
seqwish -p aln/alignments.paf -s $Y -g global.k23.gfa -k 23 -t 16
bgzip -c aln/alignments.paf > aln.paf.gz && $IMPG index -a aln.paf.gz -i aln.impg -f -t 16
while read c b e n; do
  $IMPG query -a aln.paf.gz -i aln.impg -r "$c:$b-$e" -x -m 0 --min-transitive-len 0 --min-distance-between-ranges 0 --no-merge -o paf -O C.$n -t 16
  seqwish -p C.$n.paf -s $Y -g R.$n.k0.gfa -k 0 -t 16
  seqwish -p C.$n.paf -s $Y -g R.$n.k23.gfa -k 23 -t 16
  $IMPG query -a aln.paf.gz -i aln.impg -r "$c:$b-$e" -x --no-merge -o paf -O D.$n -t 16      # CLI closure defaults
  seqwish -p D.$n.paf -s $Y -g RD.$n.k0.gfa -k 0 -t 16
  $IMPG query -a aln.paf.gz -i aln.impg -r "$c:$b-$e" -x -m 0 --min-transitive-len 0 --min-distance-between-ranges 0 -d 0 -o gfa --gfa-engine seqwish --sequence-files $Y -O T.$n -t 16
  python3 -I compare_classes.py --global global.k0.gfa --local R.$n.k0.gfa --closure C.$n.paf > cmp.$n.k0.tsv
done < loci100.bed
# C4 holdout: 20 haplotypes (seed 8) from the E1 star index and the AGC, then the same steps on c4_20.fa
$IMPG query -a $P38 -i ../e1/paf.impg -r 'GRCh38#0#chr6:31891045-32123783' -d 0 --subset-sequence-list c4_20_contigs.txt --sequence-files $AGC -o fasta -O c4_20 -t 16
```
- Compute: workstation, 0 bytes to download for the tuning set; the C4 holdout reads 20 sequences from the AGC; wall unknown.
- Blockers: `-o paf` has no test on the alignment backend (VERIFY_CORRECTIONS.md:15-16), and the reverse-strand CIGAR slice in PAF rows must be checked on a fixture first; `compare_classes.py` must be validated on a 3-sequence toy where the answer is known; whether seqwish accepts the gzipped FASTA (to check; else decompress); the `-o gfa` arm applies impg's own normalization, so it measures distance, not equality; C14.
- Feeds: Fig. 5a, section 5.5.6, Note S1, flip condition F5.

#### E7. Copy representation in the released alignments (local, gate for any copy statement)

- Question: do the released alignments store gene copies as separate records, per haplotype, at multi-copy loci?
- Dataset: GRCh38 PAF.gz on disk; CHM13 PAF.gz from E3a; 3 assembly-target PAF.gz files (seed 9, 1,964,738,872.5 bytes at the median size); loci C4 (GRCh38#0#chr6:31891045-32123783, done on GRCh38), AMY1, SMN1/SMN2, LPA, CYP2D6 with coordinates from GENCODE records written to loci.bed.
- Compared: none (audit).
- Metrics: records per haplotype; maximum per-base record depth per haplotype; fraction of haplotypes with depth at least 2; query contigs per haplotype; record query span.
- Commands:
```
mkdir -p $X/e7 && cd $X/e7
for f in $P38 ../e3a/chm13.paf.gz a1.paf.gz a2.paf.gz a3.paf.gz; do
  while read c b e n; do
    pigz -dc -p 4 "$f" | cut -f1-12 | awk -F'\t' -v c="$c" -v b="$b" -v e="$e" '$6==c && $8<e && $9>b' > $(basename $f .paf.gz).$n.tsv
    python3 -I locus_depth.py --start $b --end $e $(basename $f .paf.gz).$n.tsv >> depth.tsv
  done < loci.$(basename $f .paf.gz).bed      # locus coordinates in each target's own coordinates
done
```
- Compute: workstation; the C4 extraction on the GRCh38 file took 221 s (judge-reviewer.md section 1); downloads 1,964,738,872.5 bytes at the median size plus the CHM13 file of E3a.
- Blockers: locus coordinates on the 3 assembly targets (from a projection in E3a or E2); `locus_depth.py` generalizes phase2/judge/c4_depth.py.
- Feeds: Fig. S5, Discussion, the gate for U4.

#### E8. Consistency with the released PGGB graph (cluster, supplement)

- Question: per region and haplotype, how much do impg intervals and the paths of the PGGB graph built from the same alignments overlap?
- Dataset: E2 index; GBZ v3; 1,000 random 10 kb regions on GRCh38 and 1,000 on non-reference haplotypes (seed 10); segmental duplication and satellite strata (annotation source to choose); target bp Jaccard fixed before the run (decision D2).
- Compared: impg `-x -m 2` vs `vg chunk` path intervals.
- Metrics: per region and haplotype bp Jaccard, haplotypes found by one method only, boundary deltas, per stratum.
- Commands:
```
cd $S/e2
$IMPG query --alignment-list tpa466.list -i r2.impg -b cons.bed -d 0 -x -m 2 --sequence-files $AGC -o bed -O cons.impg -t 16
while read c b e n; do vg chunk -x 20250930_hprc25272.p98-k311.tmp.fix.v3.gbz -p "$c:$b-$e" -c 0 -O gfa -t 1 > cons/$n.gfa; done < cons.bed
python3 -I chunk_paths_to_bed.py cons/ > cons.vg.bed
python3 -I bp_metrics.py --mode jaccard cons.impg.bed cons.vg.bed --strata strata.bed
```
- Compute: cluster after E2; 0 extra bytes beyond E2.
- Blockers: E2; vg reading v3 GBZ (unknown); `chunk_paths_to_bed.py` validated on a toy graph; `-k 311` drops matches shorter than 311 bp, so 100% is not expected (phase1/web/hpp_readme.md:155).
- Feeds: Fig. S3, section 5.5.2 (labelled consistency).

#### E9. Alignment-backed partition audit on ScRAP 142 (local)

- Question: does `impg partition` on the alignment backend cover every base exactly once, and how many partitions join material from different chromosomes?
- Dataset: the E4 all-pairs ScRAP PAF and index; parameters fixed in advance from the syng-backed yeast235 run (`-w 10000 -d 1000 --selection-mode haplotype`, VERIFY_CORRECTIONS.md:72), default rehoming.
- Compared: none (audit), plus the counts of the syng-backed yeast235 run as context only.
- Metrics: partitions counted from the BED files (the log count can exceed them, VERIFY_CORRECTIONS.md:88), member intervals, uncovered bp (must be 0), bp owned more than once (must be 0), partitions spanning more than one S288C chromosome, wall, peak RSS.
- Commands:
```
cd $X/e4
/usr/bin/time -v $IMPG partition -a all.paf.gz -i all.impg -w 10000 -d 1000 --selection-mode haplotype -o bed --output-folder part -t 16 2> part.time
python3 -I exact_once_audit.py --bed-dir part --fai scrap142/*.fa.gz.fai > part.audit.tsv
```
- Compute: workstation after E4; wall unknown; the per-window clone of the mask map grows with the masked ranges (src/impg.rs:2182, 2399-2401), measured here at yeast scale only.
- Blockers: E4; port of the audit in docs/syng-gmem-bwt/observation-registry-repair.md to the alignment backend; C11 (`-w 0` never advances; the partition test passes a nonexistent `--reference-fai`).
- Feeds: Fig. S4, section 5.5.8.

#### E10. Locus refinement vs Shredtools zoom (cluster)

- Question: at TERT and IGKV6-21, how many haplotypes span both ends after `impg refine`, with what extension, compared with Shredtools enhance plus zoom?
- Dataset: E2 index; IGKV6-21 at CHM13 chr2:89168754-89169041 (paper.txt:445) and TERT at the coordinates Shredtools used (to copy from its text); the 15 T2T haplotypes of the Shredtools example where present in the 466-file set (subset list), and all 466.
- Compared: impg refine vs Shredtools enhance and zoom on hprcv2_merged.bumbl.
- Metrics: haplotypes spanning both ends before and after, extension bp per side, haplotypes dropped by zoom, wall.
- Commands:
```
cd $S/e2
$IMPG refine --alignment-list tpa466.list -i r2.impg -b tert_igk.bed -d 10k -x -m 2 --pansn-mode haplotype --span-bp 1000 --max-extension 0.5 --extension-step 1000 --support-output refine.support.bed --sequence-files $AGC -t 16 > refine.tsv
$IMPG refine --alignment-list tpa466.list -i r2.impg -b tert_igk.bed -d 10k -x -m 2 --pansn-mode haplotype --span-bp 1000 --max-extension 0.5 --extension-step 1000 --subset-sequence-list t2t15.txt --support-output refine15.support.bed --sequence-files $AGC -t 16 > refine15.tsv
# Shredtools enhance and zoom: not written (not installed, flags unknown)
```
- Compute: cluster after E2; wall unknown.
- Blockers: E2; Shredtools install; C11 (refine CLI test); non-transitive refine ignores `--approximate` (src/commands/refine.rs:213, 527-535), so approximate mode is not used.
- Feeds: Fig. 5b, section 5.5.7.

### Tier 2 (upgrade to the Nature Methods Brief, or optional)

| ID | Experiment | Why | Status of tools and data | Feeds |
| --- | --- | --- | --- | --- |
| U1 | Minigraph-Cactus regional comparator: `vg chunk -x <MC GBZ> -p <path:start-end> -c 0 -O gfa -t 1` on the E2 and E5 regions | PGGB reviewer 1 required MC comparisons (judge-reviewer.md section 3.2) | vg installed; HPRC r2 MC GBZ file name and size not checked | Fig. 3b, Fig. 4b |
| U2 | Liftover arms on the E5 alignments: UCSC liftOver with chains from paf2chain, direct and chained through one intermediate genome; halLiftover if a HAL exists | Answers "a liftover wrapper" (judge-editor.md section 3.2) | liftOver, paf2chain, halLiftover not installed; HAL availability unknown | Fig. 4b |
| U3 | Simulation with a logged coordinate map: tens of 10 Mbp genomes from a CHM13 chr20 slice with SNVs, indels, inversions, tandem and dispersed duplications, scored by event class, strand and hop count 1 to 4 | The only truth independent of any aligner (judge-reviewer.md must-fix 8) | Simulator does not exist (judge-feasibility.md section 4.1) | Fig. 4 new panel |
| U4 | AMY1 copies per haplotype against Bolognini et al. 2024 (10.1038/s41586-024-07911-1) on shared assemblies; read-depth validation on 1000 Genomes CRAMs only for an Article | Biology for a conversion | Gated on E7; sample overlap unknown; no read-depth method chosen | Article Fig. 6 |
| U5 | Incremental growth: add files to a per-file index and check byte identity of old answers against a single-index rebuild | Opportunity 4 (opportunities.md section 3.2) | Needs MultiImpg FIFO BFS, self-hits, eviction and a single-vs-per-file equality test (C6 second part) | ED or supplement |
| U6 | Whole HPRC r2 partition on the alignment backend; compare with the 7,424 released partitions if Q1 is yes | Scale claim for partition | Mask-map clone cost unmeasured (src/impg.rs:2182, 2399-2401) | Supplement |
| U7 | Homology across acrocentric short arms without a reference frame | Article conversion biology (judge-editor.md section 7) | Short-arm completeness in HPRC r2 unknown | Article |
| U8 | Local pggb-engine graphs at 5 loci against the released partition graphs (path spelling, segment bp, cost) | Locus graph vignette | After the POA smoothing default decision (87 vs 2,224 spurious bp on yeast, .claude/runs/poa-score/pggb_yeast.out:1-2) | Supplement |
| U9 | E5 rerun at impg v0.4.0 to bound version drift against Shredtools' printed numbers | judge-reviewer.md section 5 | v0.4.0 tag build needed | Table S4 |
| U10 | gbz-base on the `.gbz.db` (61,240,860,672 bytes) as a third E2 comparator | Released query path for the graph | Not installed | Fig. 3b |
| U11 | A. thaliana 69 accessions (Shredtools' second set) | Second non-human set | No released alignments; accessions not checked | Supplement |

## 8. Order of work and gates

1. Code gate on the workstation: C1-C8 and C14 (section 9); then E1 and E1b.
2. If E1 fails, stop and take decision D1.
3. Local, in parallel with cluster setup: E6, E7, E3a.
4. Ask the outside questions before cluster work (section 12) and name the node (decision D5).
5. Cluster: E2, then E3b, E8 and E10 on the E2 index.
6. Cluster and local: E5 (needs Shredtools, CAT), then E4 (tuning on E5 alignments, holdout ScRAP 142), then E9.
7. Decision point: compare F1-F5 with the targets fixed in step 1; if all pass, run U1-U3 and send the Nature Methods Brief presubmission enquiry; otherwise write the Bioinformatics paper from Tier 1.
8. Preprint when E2 and E3 have numbers, if the authors choose (decision D11).

## 9. Code fixes before benchmarking

| ID | Fix | Why it blocks | Evidence |
| --- | --- | --- | --- |
| C1 | Cut one tag, archive it with a Zenodo version DOI, build the container from the tag, point the paper-repo submodule at the tag, record the binary sha256 in every run, and stop rebuilding the benchmark binary | HEAD is 656 commits past v0.5.0; the Dockerfile clones the default branch; the binary mtime moved from 18:53:01 to 22:10:17 on 2026-11-08; the paper repo records f773342 while its checkout is 7bd50a8 | `git describe`; Dockerfile:38; judge-reviewer.md section 1; section 4 |
| C2 | TPA path: Standard-type TPA and 1ALN fixtures with exact-vs-PAF identity tests on both strands and on a mixed PAF+TPA index; count and warn on dropped tracepoint hits; return an error, not an index panic, for FastgaNoDiff and Variable records; one identity-filter span for PAF and tracepoints, or keep `--min-result-identity` out | The release is TPA and no test touches tracepoint projection | no `.tpa` or `.1aln` in tests/*.rs (judge-editor.md V13); src/impg.rs:1230-1236, 1247-1254, 1330-1338, 1436-1442, 1453-1460; src/tpa_parser.rs:202-224; src/impg.rs:832; src/impg.rs:1277-1281 vs 1386-1390 |
| C3 | Merge a bounded tree cache and the coitrees clone fix | A whole-chr1 query was killed after more than 10 min at 7bd50a8; c03ea0e, cfa20d5, c6e85dd and e2d093a are not in HEAD; Cargo.lock pins stock coitrees 0.4.0 | notes/IMPG_MEMORY_PROFILING_REPORT.md:212 (untracked, not citable as a result); VERIFY_CORRECTIONS.md:48 |
| C4 | Store the ordered alignment file list (paths, sizes) and the build direction in the index header and refuse a mismatch; skip the IMPGIDX3 magic at the next format bump | A reordered list reads CIGARs from the wrong file without an error; an IMPGIDX3 file exists in user data | src/main.rs:11778-11798 vs src/impg.rs:1657-1663; src/impg.rs:1897-1898 |
| C5 | Keep in-memory trees non-evictable in `impg stats` | `stats` on a fresh in-memory index plausibly panics through `File::open("")` | src/impg.rs:1827-1832; src/main.rs:13300-13303, 13369-13374 |
| C6 | Benchmark only in single mode with `-i`; either a node above the RAM floor or a lower-memory build; MultiImpg FIFO BFS, self-hits, eviction and an equality test only for U5 | 466 files select the untested per-file path under `auto`; the single build needs at least 59,163,669,536 bytes | src/main.rs:11277-11291; src/multi_impg.rs:757-780, 813-821, 876-882, 933-952; judge-feasibility.md section 1.1 |
| C7 | Decide and test the closure semantics: compose strand across hops or document per-hop strand (with a two-reverse-hop fixture), and expand self-hits or document that they are not expanded | Strand agreement in E3a and any duplicated-locus count depend on it | src/impg.rs:282-286, 2574-2589; src/main.rs:12072-12079 |
| C8 | Measure the 1,483 reciprocal pairs: index entries vs 2 x records, BEDPE and PAF duplicate rows, merged BED identity with `--unidirectional` | Duplicate entries inflate index size and unmerged rows | phase2/judge/pairs_out.txt; E1b |
| C9 | Fail when an AGC fetch returns a length other than end minus start | Archives appended with agc older than 3.2.2 return wrong ranges silently; the local agc is 3.2.1 | src/agc_index.rs:383-407; notes/bug-agc-appended-sample-range.md |
| C10 | Enforce `--min-transitive-len` in approximate transitive mode; pass `--approximate` through non-transitive refine or reject it there | The flag only warns; refine ignores it | src/main.rs:10581-10595; src/commands/refine.rs:213, 527-535 |
| C11 | Tests for bedpe and paf output on the alignment backend, a refine CLI test, a fixed `test_partition_window_separation`, and `-w 0` rejected | Every command and format in the paper needs a test; `-w 0` never advances | VERIFY_CORRECTIONS.md:8, 15-16, 92; tests/test_transitive_integrity.rs:595-643 |
| C12 | README and help: `--min-identity` (README.md:137), refine examples without `-d` (README.md:214-226), "compact deltas" (README.md:30-33), `--approximate` ".1aln only" (README.md:142), `--syng-min-chain-fraction` default (README.md:434), `giant` described as k-nearest (README.md:586, 595); mark experimental subcommands in `impg --help` and remove campaign language from `impg infer --help` | Reviewers run the README and `--help` | VERIFY_CORRECTIONS.md:92, 297; src/main.rs:5217-5227 |
| C13 | Error on sequences longer than 2,147,483,647 bp and on PAF without `cg:Z` at index time | Silent wrap and a query-time panic | src/impg.rs:80-109, 164-174, 610-615 |
| C14 | Benchmark harness in impg-paper/experiments/ (region sampler with fixed seeds, `/usr/bin/time -v` wrapper, `subset_pairs.py`, `bp_metrics.py`, `compare_classes.py`, `exact_once_audit.py`, `chunk_paths_to_bed.py`, `locus_depth.py`), each with verbose diagnostics and a toy-data test | The PGGB evaluation bug surfaced only in review round 2 | phase1_research_digest.txt PGGB LESSONS; MOESM3.txt:934-945 |
| C15 | Optional: build local graphs from the projected PAF records instead of re-aligning (the restriction path) | Needed only if the paper wants `-o gfa` itself to equal the restriction | src/main.rs:12324-12340; decision D4 |

## 10. Out of scope

| Item | Reason | Evidence |
| --- | --- | --- |
| syng alignment-free backend (`syng`, `map`, `read-index`, `syng2gfa`, `syng-repair`, `render`, syng query and partition) | WIP: a 20 kb sequence and its reverse complement share 34 of 715 nodes and `query` never reports the copy; the fix rebuilds every index; `impg syng` segfaults on whole GRCh38 chr20; query-time parameters are ignored on syng | notes/log.md:7-11; docs/bug-syng-segfault.md:1-12; src/lib.rs:515-607 |
| Genotyping (`genotype cos`, `genotype-infer`, `project`) | WIP: no truth-set accuracy; the GFA backend ignores candidate filters; the mosaic bug writes 230,529,097 bp for a 33,944,167 bp region | src/main.rs:8413-8426; notes/bug-infer-mosaic-path-span.md:7 |
| Genome inference (`impg infer`, 28 subcommands) | WIP: stopped at 2,189 of 5,844 territories (37.5%); receipts need environment switches the CLI does not set | docs/syng-gmem-bwt/datasheet-runtime.md:7-13, 52; VERIFY_CORRECTIONS.md:238 |
| `crush` | 553,585 vs 234,524 segment bp, 36:53 vs 13:38 wall, 100.8 vs 64.3 GB against impg's own pggb engine; 5 tests ignored | docs/crush-vs-pggb-comparison.md:9-15, 64-91; tests/test_crush_integration.rs:755, 861, 943, 1024, 1425 |
| `similarity` | 0 tests | partition-regional.md G4 |
| Whole-genome graph construction as a headline (`impg graph ENGINE:WINDOW`, `partition -o gfa`, `lace`) | No recorded whole-chromosome run; every partition GFA is held, laced, normalized and sorted in memory | src/lib.rs:1276-1319; VERIFY_CORRECTIONS.md:112 |
| Per-file index mode as a benchmark mode | 0 tests, different BFS | src/multi_impg.rs:757-952 |
| Storage advantage | TPA is 3.918 times GBZ v3 | section 4 |
| Remote HTTP access | Not implemented | odgi-shredtools.md C item 7 |
| Whole HPRC r2 partition | Mask-map clone cost unmeasured; moved to U6 | src/impg.rs:2182, 2399-2401 |
| Copy-number survey | Gated on E7; moved to U4 | phase2/judge/c4_depth_out.txt |
| Any number from the untracked impg notes (814,414,241-byte index, 0.51 s and 327.8 MB per 5 kb query) | Raw outputs gone and notes untracked in git; rerun or drop | VERIFY_CORRECTIONS.md:301; judge-feasibility.md must-fix 11 |
| The relayed request to remove workgraph | Recorded as done in impg-paper/notes/tasks.md:5 and notes/log.md:7-9; this step did not touch it and uses no `wg` command | section 4 |

## 11. What the paper must not claim

- That impg removes alignment cost; it removes whole-genome graph induction, and the HPRC alignments were paid for by the PGGB build.
- A storage advantage over GBZ v3 (3.918 times) or over the `.gbz.db` once an index is added.
- That `giant:<p>` is an Erdős-Rényi guarantee; it is k-nearest with k = 2 at p = 0.99, and the Erdős-Rényi code is not compiled (VERIFY_CORRECTIONS.md:91-92).
- That partitioned graph building caps peak memory (VERIFY_CORRECTIONS.md:59, 112).
- That a local graph from `-o gfa` is a view or subgraph of the global graph; only E6's restricted seqwish graph carries that statement, under its stated settings.
- "Every copy" or copy number per haplotype, unless E7 shows separate records and C7 settles self-hits.
- "Reference-free" reach, unless E3 shows it in bases without the two stars.
- That the Shredtools premise is false; the paper answers only the whole-collection sentence (paper.txt:285-287) with E2 and cites Shredtools' own impg numbers as theirs.
- "Exactly equivalent" (Yoo et al. 2025) without Propositions 1 and 2 and E6.
- Any syng, genotyping, genome-inference or crush result.
- Any directional abstract clause before the experiment, such as a fold speedup over odgi or vg extraction.

## 12. Questions for outside parties

- Q1 (HPRC builders): did `impg partition` and `impg lace` build the 7,424 released partition graphs (`partitionN.final.gfa.zst`, a `laced` VCF)?
- Q2 (HPRC builders): which pair-selection rule and wfmash settings produced the release network (11.2583% of ordered non-reference pairs)?
- Q3 (HPRC builders): what did the r2 PGGB build cost, split by alignment, induction and smoothing (CPU hours, peak RAM)?
- Q4 (HPRC builders): who produced the IMPG product, so that the paper can disclose it?
- Q5 (Shredtools authors): the 92-haplotype chr19 list, the impg command lines and the meaning of "17%, the default auto setting".
- Q6 (cluster admins): which gemini node has more than 59,163,669,536 bytes of RAM and 63,916,842,350 bytes of scratch, and can jobs drop the page cache?

## 13. Decisions only the authors can make

- D1: if E1 fails, fix the TPA path or move every run to the 318,372,159,094-byte PAF set on the cluster.
- D2: the flip targets F2-F4 (proposed values in section 2) and the E8 Jaccard target, fixed before any run.
- D3: compose strand across hops or document per-hop strand; expand self-hits or document their non-expansion (C7).
- D4: whether to implement the restriction path (C15) so that `-o gfa` itself induces from clipped alignments.
- D5: which cluster node runs E2 and E3b, or whether to fund a lower-memory build if none exceeds 59,163,669,536 bytes.
- D6: the tag name, who owns C1-C14, and how to keep the benchmark binary frozen while other work rebuilds target/release.
- D7: Bioinformatics first (this plan) or the editor's Brief-first order.
- D8: ScRAP 142 (published) or yeast235 (local, 1,039,122,903 bytes, publication unknown) as the yeast set, and the star hub strain.
- D9: the POA smoothing default (87 vs 2,224 spurious bp on yeast) before any pggb-engine graph appears (U8).
- D10: whether `impg infer` is labelled experimental or product surface in `--help` (src/commands/genome_infer.rs:1 vs commit c63b405).
- D11: preprint timing.
- D12: add remote HTTP access before submission or state it as a limit.
- D13: who sends Q1-Q5.

## 14. Unknowns and where I looked

- Cluster CPU, RAM, disk and page-cache policy: no phase measured them; the impg docs name a 256-core, 1,005 GiB box and a 192-thread box without saying whether either is gemini (judge-feasibility.md section 1).
- Whether vg v1.76.1 reads the released v3 GBZ: `vg chunk --help` names "graph or XG index" only; not run.
- ScRAP 142 accessions, download path and size: not checked in any phase.
- The overlap between CAT GENCODE38 haplotypes and the 90 chr19 graph paths, and the CAT seqid join: not checked.
- Shredtools commands and flags: not installed; the preprint prints none (paper.txt p.4-5, p.12-14).
- Whether `-m 0` on the whole release finishes: not run.
- Whether seqwish v0.7.11-35-gaab5bee reads a gzipped FASTA for `-s`: its help says "FASTA, FASTQ, .seq, .agc"; not run.
- Effort in person-weeks for any item: no basis found (judge-feasibility.md section 0).

## To decide

- D2 targets, D5 node and D7 venue order first, because they decide what runs and where.
- D3 closure semantics before E3a strand scoring.
- D1 only if E1 fails.

## Changed

- Wrote /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase2/PLAN.md, the abstract file /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase2/plan_abstract_bioinf.txt (143 words) and help dumps plan_help_*.txt in the same folder.
- Nothing in /home/guarracino/git/impg or /home/guarracino/git/impg-paper; code.md, notes/tasks.md, notes/log.md, notes/memory.md: none, because this step is read-only for both repositories.

## Found

- The three judges' totals rank Bioinformatics first in the sum (82 vs 77 vs 59), and two of three recommend it first.
- The per-target PAF median is 654,912,957.5 bytes (middle values 654,751,523 and 655,074,392); one judge used the lower value.
- The paper repo records impg at f773342 and checks out 7bd50a8, while the code under study is 0987752, 656 commits later, so three code versions are in play.
- The workgraph removal the user asked for is already recorded as done (impg-paper/notes/tasks.md:5), and impg-paper/CLAUDE.md (mtime 2026-11-08 21:29) has 0 matches for "workgraph".
- The `-o paf` writer emits full names, lengths and `cg:Z` per projected hop (src/main.rs:12240-12295), which is what E6 needs to induce restricted graphs with standalone seqwish.
