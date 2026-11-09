# Venue assessment for the impg paper

Written 2026-11-08 (session clock, MST) for the authors of the impg paper.
It states the venue decision and the evidence behind it, and it lists the decisions that only the authors can make.
I built it from plan.md, opportunities.md, the three proposals, the three judge reports, the phase-1 maps and the two correction files that override the maps.
I read code, saved web pages and saved listings only, ran no impg command, built nothing, and wrote no file other than this one.
The code under study is /home/guarracino/git/impg at HEAD 0987752 (`git describe` v0.5.0-656-g0987752, `impg 0.5.0`).
"Today" in this file means that commit and the files on disk on 2026-11-08.

Path abbreviations used below.

- `SCR` is /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad, a session folder that may not outlive the session.
- `phase1/` and `phase2/` are folders inside `SCR`. Proposal and judge files named without a folder (judge-editor.md, proposal-nm-brief.md and so on) are in `SCR/phase2/`.
- `DRAFT` is /home/guarracino/git/impg-paper/drafts/bioinformatics-2026-11. plan.md and opportunities.md are in `DRAFT/supporting/`, and copies of the release pair data are in `DRAFT/data/`.
- `nm/` is `SCR/phase1/dl_nm/`, the saved Nature Methods author pages.
- `paper.txt` is the Shredtools preprint text, /home/guarracino/git/impg-paper/references/biorxiv-2026-07-03-736354/paper.txt.
- `MOESM3.txt` is the PGGB Peer Review File text, `SCR/phase1/dl_pggb/MOESM3.txt`, and `MOESM1.txt` is the PGGB Supplementary Information text in the same folder.
- Code paths such as src/impg.rs are relative to /home/guarracino/git/impg, and paths that start with references/ are relative to /home/guarracino/git/impg-paper.
- `rev:N` means line N of `SCR/phase1/odgi_review1.txt`, the ODGI round-1 review.
- VERIFY_CORRECTIONS.md and FACTS_CHECKED_BY_ORCHESTRATOR.md are in `SCR/phase1/`.

Status labels follow plan.md, with NOW for code with a test or a stored measurement, NOW-ext for a number or quote from a cited external source, CODE for code without a measurement, EXP for a result that needs an experiment and WIP for research in progress.

## 1. Decision

The paper goes to Bioinformatics (OUP) as an Original Paper in the Genome analysis section, in the ODGI structure (plan.md section 0).
It rests on one claim taken from the Brief Communication proposal, that the indexed pairwise alignments of HPRC release 2 answer base-level regional homology queries for every haplotype without building or loading a whole-genome graph (plan.md section 0).
A Nature Methods Brief Communication presubmission enquiry goes out only if the five flip conditions F1 to F5 meet targets that the authors fix before the runs, and only after the Tier 2 additions are done (plan.md section 2).
A Nature Methods Article is reachable only if a Brief Communication editor offers conversion, as the PGGB editor did (MOESM3.txt:24-26), and the authors add one validated biological result.
No framing can go to any journal today, because every result panel in all three proposals is EXP and no stored number was produced at HEAD on this machine (judge-editor.md section 0, judge-reviewer.md section 0).

### 1.1 Judge scores

Three judges scored the three proposals from 1 to 10 on five axes.
Reviewer risk 10 means low risk, and each total is out of 50 (judge-editor.md section 2, judge-reviewer.md section 3, judge-feasibility.md section 0).

| Judge | Framing | Novelty | Evidence now | Feasibility | Reviewer risk | Venue fit | Total | Judge's verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Editor | Bioinformatics Original Paper | 5 | 3 | 5 | 6 | 9 | 28 | Not a Nature Methods paper, the right home as the fallback |
| Editor | Nature Methods Brief Communication | 6 | 3 | 5 | 5 | 7 | 26 | Send to review once the six minimal experiments have numbers |
| Editor | Nature Methods Article | 7 | 2 | 2 | 3 | 5 | 19 | Reject without review as planned |
| Hostile reviewer | Bioinformatics Original Paper | 5 | 2 | 5 | 6 | 8 | 26 | Most likely to survive, recommended |
| Hostile reviewer | Nature Methods Brief Communication | 6 | 3 | 6 | 5 | 6 | 26 | Survives only with a Minigraph-Cactus and a liftover comparator |
| Hostile reviewer | Nature Methods Article | 7 | 2 | 3 | 3 | 5 | 20 | Long-term extension path |
| Feasibility auditor | Bioinformatics Original Paper | 5 | 3 | 6 | 6 | 8 | 28 | Recommended primary target |
| Feasibility auditor | Nature Methods Brief Communication | 6 | 3 | 5 | 4 | 7 | 25 | Submit only if M1, M2 and M4 meet targets fixed in advance |
| Feasibility auditor | Nature Methods Article | 7 | 2 | 2 | 3 | 6 | 20 | Not feasible as written |

Sums over the three judges, recomputed from the table above.

| Framing | Novelty | Evidence now | Feasibility | Reviewer risk | Venue fit | Sum of totals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Bioinformatics Original Paper | 15 | 8 | 16 | 18 | 25 | 82 |
| Nature Methods Brief Communication | 18 | 9 | 16 | 14 | 20 | 77 |
| Nature Methods Article | 21 | 6 | 7 | 9 | 16 | 59 |

What the scores say, with both numbers in each comparison.

- Bioinformatics leads the Brief in the sum, 82 vs 77. Per judge it scores 28 vs 26 (editor), 26 vs 26 (hostile reviewer, a tie) and 28 vs 25 (feasibility auditor).
- The Brief leads Bioinformatics on novelty, 18 vs 15, and on evidence now, 9 vs 8.
- Bioinformatics leads the Brief on reviewer risk, 18 vs 14, and on venue fit, 25 vs 20.
- Feasibility ties between the two, 16 vs 16.
- The Article leads on novelty, 21 vs 18 for the Brief and 21 vs 15 for Bioinformatics, and trails on feasibility, 7 vs 16 for each of the other two.
- The hostile reviewer broke the 26 vs 26 tie toward Bioinformatics on reviewer risk, 6 vs 5, and on venue fit, 8 vs 6 (judge-reviewer.md section 3.3).
- Two of the three judges recommend Bioinformatics first (the hostile reviewer and the feasibility auditor), and the editor recommends the Brief first.

### 1.2 The editor's case for sending the Brief first

The editor scored the Brief below Bioinformatics, 26 vs 28, and still recommended trying the Brief first (judge-editor.md section 2, last paragraph).
The core of the argument is that the Brief and the Bioinformatics paper share every experiment in the minimal set M1 to M6, so a Brief attempt costs review time, not experimental work (judge-editor.md sections 2 and 7).
The editor gave four more reasons for the Brief (judge-editor.md section 0).

- It makes one claim, that alignments queried transitively are a usable pangenome at HPRC release 2 scale.
- It follows the PGGB precedent from the same group.
- The Brief Communication definition admits "software platforms" (nm/nmeth_content.txt:57).
- Two verified external facts carry it. HPRC release 2 provides its alignment "through IMPG" (phase1/web/hpp_readme.md:151, 183). The Shredtools authors write that "we were unable to compute a comparable index over whole assemblies in HPRCr1 or the larger HPRCr2 collection" with impg (paper.txt:285-287). One measurement can answer that sentence.

The editor also judged that the Bioinformatics framing, as proposed, would come back from Nature Methods without review as a toolkit description, and called Bioinformatics "its right home as the fallback" (judge-editor.md section 0).
The feasibility auditor supports the shared-core part of the argument with "The three framings share one experimental core (section 8), so the venue choice can wait until M1 and M4 have numbers" (judge-feasibility.md section 0).
The editor's route is code must-fix items 1 to 6, then M1 on the workstation, then M2 and M3 on the cluster, then an abstract-only enquiry with the 70-word abstract filled from M2 and a preprint at the same time, then M4 to M6 and a full Brief submission (judge-editor.md section 7).
If Nature Methods declines, the same M1 to M6 plus the partition audit and the refine vignette go to Bioinformatics, without per-file index mode (judge-editor.md section 7).

The shared core is real.
By content, the editor's M1, M3, M4 and M6 match plan.md E1, E3, E4 and E6, M2 matches E2 except its gbz-base arm (plan.md U10) and its cold-cache runs, and M5 matches E5 plus a liftover arm (plan.md U2) (judge-editor.md section 6 compared row by row with plan.md section 7).

### 1.3 Why the plan still starts with Bioinformatics

- The shared set is smaller than the Brief needs. The editor's M5 includes liftOver chain arms (judge-editor.md section 6), the hostile reviewer adds a Minigraph-Cactus regional comparator for any Brief (judge-reviewer.md section 6), and the editor names the coordinate-logging simulation the "first reviewer-request candidate" (judge-editor.md section 6). Bioinformatics Tier 1 needs none of the three, and plan.md lists them as U1, U2 and U3.
- Review time is long at Nature Methods. PGGB took 393 days from receipt on 2023-07-30 to acceptance on 2024-08-26, over 2 review rounds, and the 11 surveyed Nature Methods papers took 232 to 615 days (phase1/pggb-nature-methods.md sections A.1 and C.1).
- Reviews do not travel to Bioinformatics. Nature Methods offers transfer "to a different journal within the Nature Portfolio family" (nm/nmeth_submission-guidelines_editorial-process.txt:72), and Bioinformatics is an OUP journal, so a move there is a new submission.
- The Shredtools sentence has been public since 2026-07-08, 123 days before 2026-11-08 (paper.txt:1, 285-287). A preprint answers it under either order (decision D11), and Nature Methods states that "Posting of preprints is not considered prior publication" (nm/nmeth_editorial-policies_preprints-conference-proceedings.txt:50).
- The enquiry has a timing rule. Nature Methods says enquiries "should not be used to submit a full manuscript" and asks for a full submission once the manuscript is written (nm/nmeth_submission-guidelines_presubmission-enquiries.txt:40). This project is writing a full Bioinformatics manuscript, so an enquiry has to go out when E2 has numbers and before this text is final, or the Brief has to be a full submission (proposed decision D14 in section 8).
- The plan keeps the editor's route open at the cost of one enquiry. The 70-word Brief abstract is ready (phase2/abstract.txt, 70 words by `wc -w`, checked in this step), and F1 to F5 decide whether it goes out (plan.md section 1).

### 1.4 Flip conditions, copied from plan.md section 2

| # | Experiment | Flip condition (target proposed in plan.md, fixed by the authors before the runs, decision D2) |
| --- | --- | --- |
| F1 | E1 | 100% identical sorted rows for TPA exact vs PAF at `-m 1`, on the 1,000 tuning regions and on the 200 held-out regions, and 0 dropped tracepoint hits |
| F2 | E2 | All 466 TPA files index in single mode on one node, the whole-chromosome query finishes, and the median per-query wall time for 10 kb regions at `-x -m 2` (`-t 1`, exact) is at most the Shredtools median on the same 1,000 regions, with both numbers printed |
| F3 | E3b | Median per-region bp recall of held-out partners without reference bridges, at `-m 2`, is at least 0.95 times the recall with bridges, with both numbers printed |
| F4 | E5 | impg gene-copy containment is at least the Shredtools containment on the same genes and haplotypes, and the impg wrong-locus rate is at most the Shredtools rate |
| F5 | E6 | 0 bases whose node class differs between the restricted and the global seqwish graph at `-k 0`, on the 100 tuning loci and on the 20-haplotype C4 holdout |

The Tier 2 additions required before an enquiry are U1 (Minigraph-Cactus regional comparator), U2 (liftover arms), U3 (simulation with a logged coordinate map) and the HPRC r2 PGGB build cost split by stage from the builders (Q3), or the word "unknown" in its place (plan.md section 2).
If F1 fails, the authors choose between fixing the TPA path and moving every run to the 318,372,159,094-byte per-target PAF set on the cluster (decision D1).
If F2 fails because no node holds the build, the paper reports the two reference stars and the largest subset that fits, drops "whole release" from the title and abstract, and stays at Bioinformatics.
If F3 fails, the claim becomes "a reference-anchored implicit pangenome", in the editor's words (judge-editor.md section 3.2), and the venue stays Bioinformatics.

### 1.5 Why not the Article

- All three judges scored it lowest, 19, 20 and 20, against 28, 26 and 28 for Bioinformatics.
- Its biology (copy number at AMY1/AMY2, C4, SMN1/SMN2, LPA, RHD/RHCE, CYP2D6 and HLA class II) repeats the PGR-TK design of 395 genes on 94 haplotypes at a larger haplotype count (judge-editor.md section 3.1).
- At C4 the released GRCh38-target PAF holds 895 records from 465 haplotypes, and for 401 of the 465 haplotypes no GRCh38 base is covered by more than 1 record (median record query span 533,800 bp), so copy counts for those 401 haplotypes cannot come from that file (phase2/judge/c4_depth_out.txt).
- Its "graphs as views" figure contradicts the code, because `query -o gfa` keeps only the merged query intervals and the engine re-aligns them (src/main.rs:12324-12340, plan.md section 4).
- Its "Shredtools premise is false" rebuttal backfires, because Shredtools already wrote "In practice, impg operates over a sparse sampling of the pairwise comparison space" and benchmarked 6% and 17% pair sets (paper.txt:301-312).
- Its 8 "must" experiments need 9 uninstalled external tools, a simulator that does not exist and a read-depth copy-number method that nobody has chosen (judge-feasibility.md section 4.1).

## 2. Nature Methods rules in 2026

The rules below come from https://www.nature.com/nmeth/content, saved as nm/nmeth_content.html on 2026-11-08 at 20:58:13 -0700 and converted to nm/nmeth_content.txt at 20:58:35 -0700, which is 2026-11-09 03:58 UTC (file mtime, and phase1/pggb-nature-methods.md section B).
The aims, presubmission, editorial-process, preparation, reporting and preprint pages under https://www.nature.com/nmeth/ were saved in the same minute range on the same day (phase1/pggb-nature-methods.md section B lists each URL).
Line numbers refer to the saved text files, and a bare line number in the table below refers to nm/nmeth_content.txt.

| Rule | Article | Brief Communication | Resource |
| --- | --- | --- | --- |
| Definition | "a report describing a novel method or tool", with "strong validation data to demonstrate performance, reproducibility, general applicability, and potential for discovering new biology" (:40) | "a concise report describing potentially groundbreaking yet preliminary method or tool developments, highly practical tweaks to an existing method or tool, software platforms, resources of broad interest, and technical critiques of widely used methodologies" (:57) | "a report describing a collection of tools or a large dataset of broad utility, interest and significance to a field of research" (:70) |
| Abstract | up to 150 words, unreferenced (:42) | up to 70 words, unreferenced (:59) | up to 150 words, unreferenced (:72) |
| Main text | 3,000 words, up to 5,000 at editorial discretion, excluding abstract, Methods, references and legends (:43) | 1,200 words, up to 1,600 at editorial discretion, including abstract, references and figure legends (:60) | 3,000 words, up to 5,000 at editorial discretion, excluding abstract, Methods, references and legends (:73) |
| Display items | up to 6 figures or tables (:44) | at most 2, up to 3 at editorial discretion (:62) | up to 6 figures or tables (:74) |
| Structure | Introduction without heading, Results, Discussion, Online Methods, with topical subheadings in Results and Methods and none in the Discussion (:45-50) | no sections or subheadings in the main text, and Online Methods with subheadings (:61, :63) | as the Article (:75-80) |
| References | guideline up to 50 (:51) | guideline up to 20 (:64) | guideline up to 50 (:81) |
| Review and dates | peer reviewed, with received and accepted dates and optional supplementary information (:52-54) | the same (:65-67) | the same (:82-84) |

Rules that hold for all three types.

- Extended Data is optional and capped at "A maximum of ten Extended Data display items" (nm/nmeth_submission-guidelines_preparing-your-submission.txt:48).
- The aims page requires that "the description of the method must be accompanied by strong validation, an application to an important biological question and results illustrating its performance in comparison to available approaches" (nm/nmeth_aims.txt:25).
- Editors send a paper to review based on its advance, the soundness of its conclusions, how well the evidence supports them and their relevance to the readership (nm/nmeth_submission-guidelines_editorial-process.txt:50).
- After review, the usual grounds for decline are insufficient support for the conclusions or a reassessed level of interest or advance (same file, :59).
- A "Code availability" statement is required when custom code is central, deposit in a DOI-minting repository such as Zenodo is called best practice, and Nature journals peer-review central code, which must be shared with editors and reviewers (nm/nmeth_editorial-policies_reporting-standards.txt:156-158).
- Life-science research articles need a Reporting Summary, which is published with the paper (same file, :57-59).
- LLM use must be documented in the Methods (nm/nmeth_submission-guidelines_preparing-your-submission.txt:45).
- A presubmission enquiry is an abstract sent through the manuscript system (nm/nmeth_submission-guidelines_presubmission-enquiries.txt:38) and is not meant for a written manuscript (same file, :40).
- Preprints are encouraged, and "Manuscripts posted on preprint servers will not be taken into account when determining the advance provided by a study under consideration at a Nature Portfolio journal" (nm/nmeth_editorial-policies_preprints-conference-proceedings.txt:50). Whether that sentence also covers a third party's preprint such as Shredtools I don't know, because the page does not say.
- Authors may suggest reviewers and "may also request that the journal excludes one or two individuals or laboratories" (nm/nmeth_editorial-policies_peer-review.txt:157).
- The transfer service for declined manuscripts, which carries the reviewer reports, covers journals "within the Nature Portfolio family" (nm/nmeth_submission-guidelines_editorial-process.txt:72-77).
- No Methods word limit is stated on any saved page (phase1/pggb-nature-methods.md section B.1).
- I could not read the software supplement form, because nm/nr-software-policy.pdf is a dynamic form and its text is a placeholder (nm/nr-software-policy.txt).

How the three types fit impg.

- The Brief Communication definition names "software platforms", and PGGB from the same group is the precedent (section 3.1).
- The Article needs "potential for discovering new biology", and impg has no validated biological result today (section 4).
- A Resource would rest either on the HPRC r2 alignments, which are the consortium's product and are described by the HPRC2 preprint (Lucas et al. 2026, 10.64898/2026.07.21.739710), or on "a collection of tools", which would pull the WIP syng, genotyping, genome-inference and crush subsystems into scope (proposal-nm-brief.md section 0). No proposal recommends it.
- PGGB's published Brief has 1,669 words of abstract, main text and the two legends, more than the 2026 ceiling of 1,600 words, which also counts references (phase1/pggb-nature-methods.md section A.2). Whether the 2023 limits differed I don't know, because only the 2026 page was saved.

Bioinformatics limits for comparison.
The ODGI paper repository gives the Original Paper length as 5,000 words with a hedge word, and recommends at most 150 words for the abstract (/home/guarracino/git/impg-paper/references/odgi-paper/README.md:26-27, which points to https://academic.oup.com/bioinformatics/pages/instructions_for_authors).
The word-limit lines of that README date from 2021-10-30 (commit 10a8d02 "added word limits", `git log -L 26,27:README.md` in `SCR/phase1/odgi_bundle/repo`), and its last edit is 2022-03-15 (commit 692b21b).
No phase read the 2026 OUP page, so both limits are unchecked for 2026.

## 3. Precedents

### 3.1 PGGB, a Brief Communication from the same group

Garrison et al. 2024, "Building pangenome graphs", Nature Methods 21:2008-2012, doi 10.1038/s41592-024-02430-3, is a Brief Communication (`citation_article_type` in phase1/dl_pggb/nm.html).

Dates and process.

- Received 2023-07-30, accepted 2024-08-26 and published 2024-10-21, so 393 days from receipt to acceptance (`<time>` tags in phase1/dl_pggb/nm.html, days recomputed in this step).
- The first decision came on 2023-10-11 with 2 reviewers (MOESM3.txt:14-19), the second on 2024-04-15 (MOESM3.txt:244) and acceptance in principle on 2024-05-22 (MOESM3.txt:408-412).
- The nature.com page showed 17k accesses and 274 citations when it was saved (phase1/dl_pggb/nm.txt:79-81).

Format and display items (phase1/pggb-nature-methods.md sections A.2 and A.3, word counts made in Chrome).

- The main text has 1,334 words in 9 paragraphs without subheadings, the abstract 71 words, the Fig. 1 legend 171 words, the Table 1 legend 93 words and the Methods 2,850 words, with 37 references.
- Fig. 1 has 4 panels, showing the pipeline, a 1D view of a 16-assembly primate chromosome 6 graph, a 2D layout and a phylogeny.
- Table 1 lists 10 pangenome runs from 8 species groups, from 255,615,162 bp (ecoli50) to 36,673,233,537 bp (soy37), with wall time, peak memory, SNV counts and F-scores, all at 48 threads on 378 GB machines.
- Beside them sit 6 Extended Data figures, a Supplementary Information with sections A to H and 9 Supplementary Figures, an accession spreadsheet, a Reporting Summary and a 30-page Peer Review File.

What the reviewers demanded.

- Reviewer 1 opened with "the lack of controls, lack of novelty, and lack of biological results limit enthusiasm" (MOESM3.txt:161-163).
- The same reviewer wrote "The authors must also include comparisons to Minigraph and the Minigraph-Cactus approaches" (MOESM3.txt:173-174), and asked for structural-variant analysis, a measured version of the bias claim, a full description and benchmark of SMOOTHXG, a detailed biological analysis of one pangenome and a justification of each dataset (MOESM3.txt:155-209).
- Reviewer 2 asked what the input must be, whether the method scales to whole genomes instead of chromosomes (MOESM3.txt:228), and how induction and the random-graph heuristic work (MOESM3.txt:211-237).
- The authors built Minigraph-Cactus graphs for every pangenome and reported the share of input sequence they drop, 1.8% (human chr6) to 22.1% (E. coli) (MOESM1.txt:236-238), raised A. thaliana from 7 to 82 genomes and mouse from 17 to 36, and added HiFi DeepVariant benchmarks and openness and phylogeny vignettes (phase1/pggb-nature-methods.md section A.7, from MOESM3.txt:471-505).
- In round 2 reviewer 1 asked why one F-score was the lowest, why sparsification was random instead of a spanning tree, and how to set the other parameters (MOESM3.txt:374-397).
- The F-score answer exposed an MNV normalization bug in the evaluation that "affected the evaluation of all pangenomes" (MOESM3.txt:934-945).
- Reviewer 1 read the documentation and did not run the code in either round (MOESM3.txt:395-396).
- The editor asked for a DOI-minting code deposit, versioning and a licence (MOESM3.txt:114-115).

The Article offer and the impg pointer.

- The editor wrote "We think performing a more detailed biological analysis of one of the pangenomes discussed is optional. If you would like to add this analysis, you could consider reformatting the paper as an Article" (MOESM3.txt:24-26), and the authors kept the Brief (MOESM3.txt:475-480).
- On sparsification the authors answered "We anticipate exploring combinations of these two approaches to reduce the costs of generating very large pangenome graphs and comparative genomic alignments, but reserve this study for future work, possibly focused on implicit pangenome graphs: https://github.com/pangenome/impg." (MOESM3.txt:976-982).
- The published Supplementary H mentions neighbour-joining trees combined with random sampling and does not name impg (MOESM1.txt:1185-1188, opportunities.md section 5.1).

What this precedent means for impg.
The Brief route exists for a software platform from this group.
The decisive demands were a head-to-head with the dominant pipeline, a measured version of the key claim, accuracy against independent truth instead of self-consistency, and some biology.
The deferred sparsification question is one that impg can answer with E4 (homology recall against the fraction of aligned pairs).

### 3.2 PGR-TK, levioSAM2 and the other surveyed Nature Methods papers

The survey covered 11 Nature Methods papers, 9 read in full text and 2 (spliced pangenome graphs, UniAligner) from abstract and figure titles only (phase1/pggb-nature-methods.md section C.1).
Days run from receipt to acceptance.
Dates for PGGB, PGR-TK and levioSAM2 come from the `<time>` tags in `SCR/phase1/dl_nmpapers/`, checked in this step.

| Paper | Type | Days | Main display items, Extended Data, references | Results structure | Comparators | Scale and headline numbers |
| --- | --- | ---: | --- | --- | --- | --- |
| PGGB, Garrison et al. 2024, 21:2008-2012 | Brief Communication | 393 (2023-07-30 to 2024-08-26) | 1 figure and 1 table, 6 ED, 37 | 9 paragraphs, no subheadings | MUMMER4 and HiFi DeepVariant as truth, Minigraph-Cactus 2.7.0 for dropped sequence | 8 species groups, up to 36,673,233,537 bp, human chr6 of 90 haplotypes in 18.46 h with 137.72 GB |
| PGR-TK, Chin et al. 2023, 20:1213-1221, 10.1038/s41592-023-01914-y | Article | 280 (2022-08-10 to 2023-05-17) | 4 figures, 0 ED, 68 | component headings (PGR-TK, SHIMMER index, MAP-graph, principal bundle decomposition, MHC class II, medically relevant amplicon genes) | seqwish, minigraph, minimap2 indexing | HPRC year 1 with 94 haplotypes from 47 samples plus CHM13 v1.1, GRCh38 and hg19, 395 medically relevant genes, index in 18 minutes on an AWS c5.12xlarge, 147 MHC class II sequences graphed in under 5 s against 3.5 min for seqwish and 13 min for minigraph (PMC10406601 text lines 8 and 13) |
| levioSAM2, Chen et al. 2024, 21:41-49, 10.1038/s41592-023-02069-6 | Article | 530 (2022-04-27 to 2023-10-09) | 6 figures, 6 ED, 65 | claim-style headings (for example "Lifting from T2T-CHM13 improves short-read mapping to GRC references") | direct mapping to GRCh37 and GRCh38 with standard pipelines (GATK, DeepVariant) | GIAB samples and CMRG regions, small-variant errors in CMRG reduced by 19.4% to 51.3% for HG002, and the stages other than levioSAM2-lift used at most 35 GB (PMC11610747 text) |
| Personalized pangenome references, Sirén et al. 2024, 21:2017-2023 | Article | 232 | 4 figures, 0 ED, 42 | pipeline, graphs, mapping, small variants, SV genotyping | BWA-MEM on GRCh38, GATK, DeepVariant, vg call, PanGenie | HPRC Minigraph-Cactus graphs, GIAB HG001 to HG005, errors cut by 35% against BWA-MEM-GRCh38 and by 74% against GATK best practice |
| SVPG, Jiang et al. 2026, 23:1984-1993 | Article | 380 | 5 figures, 0 ED, 54 | 6 claim-style subsections | Sniffles, cuteSV, SVIM, DeBreak, Sawfish | GIAB HG002 Tier 1 and Q100, 20 HPRC samples, HG008 and COLO829 |
| Vclust, Zielezinski et al. 2025, 22:1191-1194 | Brief Communication | 279 | 2 figures, 5 ED figures and 2 ED tables, 20 | no subheadings | VIRIDIC, FastANI, skani, anicalc | 15,677,623 viral contigs, 22 vs 210 of 1,188 pairs put below the species threshold (Vclust vs VIRIDIC) |
| Phylogenetic compression, Břinda et al. 2025, 22:692-697 | Article | 615 | 2 figures, 9 ED, 73 | 2 claim-style subsections | XZ, GZip, BZip2, Re-Pair, MBGC, COBS | the 661k assembly collection and 447,833 de Bruijn graphs |
| Jasmine and Iris, Kirsche et al. 2023, 20:408-417 | Article | 567 | 6 figures, 0 ED, 63 | 6 subsections | six SV comparison methods | 31 long-read samples, genotyped in 1,317 samples |
| Winnowmap2, Jain et al. 2022, 19:705-710 | Article | 299 | 6 figures, 0 ED, 51 | 5 subsections | Winnowmap, minimap2, NGMLR | T2T chromosomes and GIAB |
| Spliced pangenome graphs, Sibbesen et al. 2023, 20:239-247 | Article | 528 | 5 figures, 10 ED, 68 | not read | RNA-seq mappers | not read |
| UniAligner, Bzikadze and Pevzner 2023, 20:1346-1354 | Article | 295 | 6 figures, 0 ED, 69 | not read | not read | centromeric tandem repeats |

Patterns across the 11 (phase1/pggb-nature-methods.md section C.1).

- 9 of the 11 are Articles, and the 2 Brief Communications (PGGB, Vclust) each make one claim with 2 main display items and push detail into Extended Data.
- 7 of the 9 papers read in full compare with 3 to 6 named tools on the same inputs (PGR-TK, personalized pangenome references, SVPG, Vclust, phylogenetic compression, Jasmine and Iris, Winnowmap2).
- PGGB, a Brief Communication, compares only dropped sequence against Minigraph-Cactus, and levioSAM2 compares lifted mapping against direct mapping with standard pipelines. The comparators of UniAligner were not read.
- Human tools score accuracy on community truth sets (GIAB Tier 1, Q100, CMRG, HPRC samples).
- The 2024 to 2026 Articles (levioSAM2, phylogenetic compression, SVPG) use claim-style Results headings, while the 2023 PGR-TK Article uses component names.
- Receipt to acceptance took 232 to 615 days.
- The survey found no 2021 to 2026 Nature Methods paper on regional queries of an alignment collection, and PGR-TK, whose `pgr-query` fetches homologous sequence from an index of 94 haplotypes, is the closest.
- FastGA is in Bioinformatics Advances (2025, vbaf238) and Minigraph-Cactus in Nature Biotechnology (2024, 42:663-673), not in Nature Methods.

### 3.3 ODGI and the other Bioinformatics comparables

Days run from receipt to the editorial decision or acceptance in the PMC history of each paper, recomputed in this step from `SCR/phase1/dl_pubmed/PMC*.xml`.

| Paper | Type | Receipt to decision or acceptance | Sections | Display items and references | Evaluation |
| --- | --- | --- | --- | --- | --- |
| ODGI, Guarracino et al. 2022, 38:3319-3326, 10.1093/bioinformatics/btac308 | Original Paper, Genome Analysis | 165 days (received 2021-11-09, revised 2022-03-18, decision 2022-04-23) | 1 Introduction, 2 Model, 3 Implementation, 4 Overview, 5 Results with 5 subsections ending in 5.5 Performance evaluation, 6 Discussion | 4 figures and Algorithm 1, 0 tables, 55 references in PMC | VG v1.37.0 on the 4 operations both toolkits share, threads 1 to 16, haplotypes 1 to 64 of an HPRC chr6 graph, 10 runs, a 28-core 256 GB machine, `odgi extract` 46.87 s and 7.23 GB against `vg chunk` 1838.51 s and 60.37 GB at 16 threads and 64 haplotypes, and `vg find` 0.16 s against `odgi position` 2.58 s at 1 haplotype, a VG win the paper reports |
| seqwish, Garrison and Guarracino 2023, 39:btac743 | Original Paper | 226 days (received 2022-02-14, decision 2022-09-28) | 1 Introduction, 2 Algorithm with 6 subsections, 3 Implementation with 3 subsections, 4 Results, 5 Discussion | 3 figures, 2 tables, 35 references | runtime on 4 pangenomes over identity and `-k`, 100 input-order permutations of yeast chrV against minigraph, 38 human haplotypes (114.627 Gbp) induced in 46,268 s with 347.4983 GB |
| GBZ, Sirén and Paten 2022, 38:5012-5018 | Original Paper | 80 days (received 2022-07-12, accepted 2022-09-30) | body not in the PMC XML, not read | not read | not read |
| Panacus, Parmigiani et al. 2024, 40:btae720 | Applications Note | 239 days (received 2024-04-02, accepted 2024-11-27) | 1 Introduction, 2 Panacus, 3 Results, 4 Conclusion | 1 figure, 2 tables, 14 references | HPRC PGGB graph of 44 samples, `odgi heaps` 24 min plus 5 h of indexing against 55 min for Panacus |
| gaftools, Pani et al. 2026, 42:btag406 | Applications Note | 547 days (received 2024-12-11, accepted 2026-06-11) | 1 Introduction, 2 Methods with 5 subsections, 3 Results, 4 Discussion | 2 figures, 2 tables, 22 references | NA12878 ONT reads at 14X aligned to an HPRC minigraph graph |

nf-core/pangenome (Heumos et al. 2024, Bioinformatics 40:btae609) is a further Bioinformatics paper from the group, whose Discussion names IMPG as the planned route to split, build and lace graphs (phase1/related-work.md section 4.3), and the survey did not profile its structure.
Bioinformatics Original Papers in this set lead with Model or Algorithm and Implementation sections before Results, benchmark against one or two tools of the same ecosystem, and report no biological finding (phase1/pggb-nature-methods.md section C.2).
ODGI's own Discussion says "our presentation is primarily qualitative" (/home/guarracino/git/impg-paper/references/odgi-paper/manuscript/main.tex:571), so ODGI carried 0 accuracy benchmarks.
This draft plans 3 accuracy experiments (E3 to E5).
They score against held-out direct alignments and CAT annotations, which are alignment-derived references, not independent truth (judge-reviewer.md must-fix 8).

## 4. What Nature Methods requires that impg lacks today

Each row names the requirement, where it comes from, the state of impg at HEAD 0987752 and the plan item that closes it.

| # | Requirement | Source of the requirement | impg today | Evidence | Plan item |
| --- | --- | --- | --- | --- | --- |
| 1 | Strong validation against independent truth | nm/nmeth_aims.txt:25, nm/nmeth_content.txt:40 | No test compares a real-data `impg query` result with an independent truth, and no truth-set accuracy exists for any subsystem | phase1/evidence-inventory.md sections 0 and 3 | E3b, E4, E5 (CAT GENCODE38), U3 (the simulator does not exist, judge-feasibility.md section 4.1) |
| 2 | An application to an important biological question | nm/nmeth_aims.txt:25 | No validated biological result. At C4 the released GRCh38-target file maps each GRCh38 base to one record in 401 of 465 haplotypes, so it cannot give copy numbers for those 401 haplotypes | phase2/judge/c4_depth_out.txt | E7 as a gate, U4 or U7 for an Article |
| 3 | Comparison with available approaches on the same inputs | nm/nmeth_aims.txt:25 | No benchmark against an external PGGB, Minigraph-Cactus, vg or odgi run exists. Shredtools, Mumemto, gbz-base, liftOver, paf2chain, halLiftover and Cactus are not installed | phase1/evidence-inventory.md section 0 item 3, plan.md section 7 | E2, E5, U1, U2, U10 |
| 4 | A head-to-head with the dominant graph pipeline | PGGB precedent, MOESM3.txt:173-174 | No Minigraph-Cactus arm in Tier 1 | judge-reviewer.md sections 3.2 and 6 | U1 |
| 5 | Performance measured at release scale with the cited version | nm/nmeth_content.txt:40 | No stored number at HEAD. The only whole-chromosome query on record, at 7bd50a8, was killed after more than 10 min, and the note that records it is untracked in git | plan.md section 9 C3, phase1/VERIFY_CORRECTIONS.md:48 and :301 | E2, C3 |
| 6 | A machine that holds the build | needed for row 5 | A single-index build holds at least 59,163,669,536 bytes at once (field sizes, not run). That is 0.962 times the workstation's 61,478,674,432 bytes of RAM and 3.814 times the 15,510,704,128 bytes available at the 2026-11-08 check, before growth slack and tree construction. The cluster node is unknown | plan.md section 4, judge-feasibility.md section 1.1 | C6, D5, Q6 |
| 7 | Tests for the format the release uses | code peer review, nm/nmeth_editorial-policies_reporting-standards.txt:158 | No `.tpa` or `.1aln` string in tests/*.rs, while all 466 release files are TPA | judge-editor.md V13 | C2, E1 |
| 8 | One tagged, archived release that reviewers can run | nm/nmeth_editorial-policies_reporting-standards.txt:157-158, MOESM3.txt:114-115 | HEAD is 656 commits past v0.5.0, Dockerfile:38 clones the default branch, the release binary was rebuilt at least 5 times on 2026-11-08, and Zenodo holds five records titled v0.5.0 plus one v0.5.1 record without a matching tag | plan.md section 9 C1, phase1/related-work.md section 7 | C1, D6 |
| 9 | A command surface reviewers can read | code peer review | 23 top-level commands with the experimental ones unmarked, internal campaign language in `impg infer --help`, and README examples that the binary rejects | judge-editor.md must-fix 14 and 15, plan.md C12 | C12, D10 |
| 10 | Closure semantics fixed before accuracy runs | strong validation | Strand is set per hop, not composed back to the query, and self-hits are written but not expanded | src/impg.rs:282-286, 2574-2589, src/main.rs:12072-12079 | C7, D3 |
| 11 | An advance beyond "a liftover wrapper" | the editor's reading, judge-editor.md section 2 | No liftover comparator, and the term "implicit pangenome graph" already appears in Yoo et al. 2025 Supplementary Note III | opportunities.md section 5.2 | U2, E6 (Proposition 2) |
| 12 | Reference independence measured in bases | the PGGB reviewer's demand to measure bias, MOESM3.txt:155-209 | At the pair level every non-reference haplotype reaches all 463 others within 2 hops without either reference, but no base-level reach has been measured | DRAFT/data/pairs_out.txt | E3, F3 |
| 13 | Breadth of species | general applicability, nm/nmeth_content.txt:40 | Tier 1 has one non-human species, S. cerevisiae, in two sets (ScRAP 142 in E4 and E9, whose accessions no phase has checked, and the 7-sequence chrV fixture in E6), against 8 species groups in PGGB Table 1 | plan.md section 14 | E4, E9, U11 |
| 14 | Disclosure of who produced the release product | the editor's must-fix, judge-editor.md section 3.2 | The HPRC README does not say who produced the IMPG product | phase1/web/hpp_readme.md:149-191 | Q4 |
| 15 | A Brief that fits 1,600 words and 2 display items | nm/nmeth_content.txt:60-62 | The Brief proposal budgets 1,500 words, and the hostile reviewer judges that the ceiling cannot hold five experiments | proposal-nm-brief.md section 5, judge-reviewer.md section 3.2 | Extended Data, at most 10 items |
| 16 | Reporting Summary and LLM statement | nm/nmeth_editorial-policies_reporting-standards.txt:57-59, nm/nmeth_submission-guidelines_preparing-your-submission.txt:45 | Neither written | none | Availability section |
| 17 | Named haplotype sets | the PGGB reviewer's dataset questions, MOESM3.txt:206 | Sources use 460, 464, 465, 466 and 476 for HPRC r2 | phase1/related-work.md finding 10 | Table S11 |

Row 6 corrects one judge sentence.
The feasibility auditor wrote that the RAM floor "exceeds the 57 GB of the workstation" (judge-feasibility.md section 1.1), but 57 there is `free -g` output in GiB, and 59,163,669,536 bytes is below the 61,478,674,432 bytes of total RAM.
The practical conclusion stands, because the floor is a lower bound and only 15,510,704,128 bytes were free at the 2026-11-08 check.

## 5. Strengths that argue for a high venue

The release fact.

- The HPRC release 2 README lists three pangenome products in its header table, "Minigraph", "Minigraph-Cactus" and "IMPG/PGGB" (phase1/web/hpp_readme.md:21).
- It says the PGGB all-vs-all alignment "is also provided through IMPG (implicit pangenome), which represents the pangenome as a set of assembly-vs-assembly alignments that can be projected and queried on the fly" (phase1/web/hpp_readme.md:151).
- It provides "Alignments ... in PAF format and in IMPG's TPA format (one file per haplotype, 466 total)" (phase1/web/hpp_readme.md:183).
- The TPA set is 466 files and 25,070,431,026 bytes holding 389,234,668 records, all Standard tracepoints with edit distance and max complexity 128 (S3 listing summed in this step from phase2/s3_tpas.xml, record sum recomputed from DRAFT/data/partners.tsv, plan.md section 4).
- The release also ships 466 per-target PAF.gz files of 318,372,159,094 bytes in total and a single all-vs-all PAF of 309,962,462,020 bytes (plan.md section 4, phase1/FACTS_CHECKED_BY_ORCHESTRATOR.md).

The release structure is new knowledge.

- The bidirectional index walks 23,738 of 108,345 unordered haplotype pairs (21.9096%), while the files list 25,221 of 216,690 ordered pairs (11.6392%) (DRAFT/data/pairs_out.txt).
- 1,483 unordered pairs are stored in both files of the pair, and the GRCh38 and CHM13 files each list all 465 other haplotypes (DRAFT/data/pairs_out.txt, DRAFT/data/partner_summary.txt).
- The editor called this "a natural experiment", a sparse haplotype network plus two complete reference stars (judge-editor.md section 3.1).

The Nature Methods history.

- The PGGB authors deferred the spanning-tree sparsification question to "implicit pangenome graphs" with the impg link in their Nature Methods rebuttal (MOESM3.txt:976-982).
- Yoo et al. 2025 (Nature 641:401-418) gives the first peer-reviewed description of impg, in Supplementary Note III, subsection "Implicit pangenome graph (impg)" (phase2/yoo/MOESM1.txt:648, opportunities.md section 5.2).

Published uses, with the authorship check I made in this step.
I counted impg authors (Guarracino, Garrison, Kille) among the Crossref author lists saved in `SCR/phase1/cr/`.

| Paper | Use of impg | impg authors among the paper's authors |
| --- | --- | --- |
| Sorin et al. 2025, Genet Sel Evol 57:61, 10.1186/s12711-025-01012-x | region extraction from a French cattle pangenome with impg v0.2.1 | 0 of 19 |
| Sorin et al. 2026, Genet Sel Evol 58:17, 10.1186/s12711-026-01037-w | `impg -p sample.paf -r 6:69000000-71000000 -x` with impg v0.2.1 on 79 assemblies from 20 breeds | 0 of 9 |
| Downing 2026, Genomics Proteomics Bioinformatics 24:qzag003 (review) | describes impg region extraction | 0 of 1 |
| Shivakumar and Langmead 2026, Shredtools, bioRxiv 10.64898/2026.07.03.736354 | benchmark comparator, impg v0.4.0 | 0 of 3 Crossref author entries (2 people and the HPRC group) |
| Bolognini et al. 2026, COSIGT, Genome Biol 27:286, 10.1186/s13059-026-04242-4 | "an implicit pangenomics approach using impg", with `impg refine` for locus boundaries and `impg query` for BEDPE projection, benchmarked on 326 CMRGs and 265 SV regions and applied to "over 6,000" genomes | 2 of 9 (Guarracino, Garrison) |
| Varki et al. 2025, Genome Res 35:1609-1620, 10.1101/gr.279858.124 | impg v0.2.0 extracts the GRCh38 MHC region | 1 of 7 (Garrison) |
| Heumos et al. 2024, nf-core/pangenome, Bioinformatics 40:btae609 | the Discussion names IMPG as the split-and-lace route | 2 of 10 (Guarracino, Garrison) |
| Yoo et al. 2025, Nature 641:401-418, 10.1038/s41586-025-08816-3 | Supplementary Note III on impg, `impg -p ... -x` for 8p23.1 | 3 of 123 (Guarracino, Kille, Garrison) |
| HPRC release 2 resources | distributes the IMPG PAF and TPA alignments | producer not stated in the README (Q4) |

This check changes one judge statement.
The editor listed Varki et al. 2025 and COSIGT among the "independent users" (judge-editor.md section 3.2), but both list impg authors.
The uses with no impg author are the two cattle papers, the review and the competitor's benchmark.
The uses come from phase1/evidence-inventory.md section 4.4, phase1/related-work.md section 4.3, `SCR/phase1/ft/cosigt.txt` lines 11, 21 and 45-49.

Adoption counters on 2026-11-08 (phase1/evidence-inventory.md section 4, phase1/VERIFY_CORRECTIONS.md:308 and :311).

- GitHub had 114 stars, 16 forks, 7 watchers, 15 issues and 269 pull requests in total.
- GitHub traffic from 2026-10-25 to 2026-11-07 was 378 views by 147 unique visitors and 1,637 clones by 263 unique cloners.
- Bioconda counted 11,161 downloads over 9 versions (0.2.0 to 0.5.0), with no build for v0.3.0, v0.4.0 or v0.4.1.
- Docker Hub `pangenome/impg` counted 4,895 pulls since registration on 2026-03-09.
- The inventory also says 12 of the 15 issues were opened by people other than the two main developers, which the verifier did not check (phase1/VERIFY_CORRECTIONS.md:319).
- No phase collected the same counters for PGGB, Shredtools or PGR-TK, so these numbers carry no ranking.

Other strengths.

- By Shredtools' own numbers, impg v0.4.0 on the 17% sparse set answered a query in 0.21 s with 12 MB, against 0.484 s and 79 MB for Shredtools (paper.txt:308-312). These are their measurements of an older version, cited as theirs.
- Proposition 2 (seqwish on alignments clipped to a closed set equals the global seqwish graph restricted to that set, at seqwish `-k` at most 1) is, in the editor's words, "the one result no explicit-graph tool can offer" (judge-editor.md section 5). It is EXP until E6 runs.
- seqwish, the formal parent of the model, and ODGI are Bioinformatics papers from the same group (section 3.3), and the HPRC r2 PGGB graph of the same alignments is a public control at release scale (GBZ v3 6,398,170,680 bytes, plan.md section 4).

What the strengths do not show.
No strength is a measurement of impg at HEAD.
The release fact shows distribution, not use, and who produced the product is unknown (Q4).
Four of the nine uses in the table list impg authors.
Nature Methods asks for validation, biology and comparisons (section 2), and none of the three exists today (section 4).

## 6. The Shredtools threat and how the plan answers it

### 6.1 What Shredtools is and what it says of impg

- "Navigating the pangenome coordinate system with Shredtools", Shivakumar and Langmead with the Human Pangenome Reference Consortium as group author, bioRxiv 10.64898/2026.07.03.736354, v1 posted 2026-07-08 and not yet published (paper.txt:1-8, phase1/related-work.md section 4.1). Its target venue is unknown.
- It frames its query as a missing primitive and calls it, with a hedge word, "the pangenome analogue of bedtools getfasta" (paper.txt:279).
- It states that "impg involves all-pairs whole-genome alignments" and that "as such, we were unable to compute a comparable index over whole assemblies in HPRCr1 or the larger HPRCr2 collection (N=476), both of which Shredtools was able to index and query" (paper.txt:285-287).
- In the same section it writes "In practice, impg operates over a sparse sampling of the pairwise comparison space" and benchmarks 6% and 17% pair sets (paper.txt:301-312), which is why the plan never calls its premise false.
- It argues that composing pairwise alignments through intermediate genomes leads "to reduced fidelity for genome pairs separated by more intermediate genomes" (paper.txt:56-59).
- It calls impg "a general framework that can operate over different notions of pangenome homology" and suggests integrating multi-MUM coordinates into impg (paper.txt:528-532).

Its benchmark of impg v0.4.0 on 92 HPRCr1 chr19 assemblies, cited as its own numbers.

| Measure | Shredtools | impg as Shredtools ran it | Source |
| --- | --- | --- | --- |
| Index build at 48 threads | 86 times faster, printed with a tilde | includes all-pairs wfmash alignment at 48 threads | paper.txt:299-300, 346-349 |
| Index build at 1 thread | 3.8 times faster with 20 times less memory | all pairs | paper.txt:300-301 |
| Index build against 6% of pairs | Shredtools at 1 thread 2 times faster with 15 times less memory | wfmash on 6% of pairs at 48 threads | paper.txt:302-304 |
| Disk | 252.4 MB | 10.1 GB with all PAF plus index, 630 MB at 6% | paper.txt:304-307 |
| Query, 1,000 random regions | 0.484 s and 79 MB | 4.01 s and 1.66 GB on all pairs, 0.21 s and 12 MB on the 17% set | paper.txt:308-312 |

Where Shredtools wins, stated plainly.

- It needs no alignment, and on its chr19 benchmark its index build beat every impg configuration once alignment time was counted (paper.txt:299-304).
- It serves queries from a browser over HTTP Range requests to S3 (paper.txt:473-489), and impg has no remote-access code (phase1/odgi-shredtools.md section C item 7).
- It merges new genomes through Mumemto without recomputing everything (paper.txt:88-90).
- On HPRCr2 it reports 34,864 of 55,997 genes (62.3%) with perfect bounds, and 4,497 more gene regions with perfect bounds after enhance (paper.txt:381-384, 428-430). Our sum gives 39,361 of 55,997 (70.3%) after enhance, a number the preprint does not print. impg has no genome-wide gene-set evaluation yet.
- Its HPRCr2 merged index is public, `s3://genome-idx/mumemto/hprc/hprcv2_merged.bumbl` of 27,424,443,909 bytes plus a 54,330,664-byte `.bumbl.bi`, 27,478,774,573 bytes together, with a gzipped copy of 11,926,204,592 bytes (phase2/gi_all.xml, parsed in this step).

Where its evidence is thin, stated as fairly.

- It reports bounds, which measure window tightness, and no truth set (phase1/odgi-shredtools.md section B8 item 7).
- It returns one window per genome by construction (phase1/odgi-shredtools.md section B9).
- Its multi-MUM coverage of CHM13 falls from 76% on HPRCr1 to 63% on HPRCr2 (paper.txt:424-426).
- The abstract's "476 human genomes in half a second" (paper.txt:20-21) has no timing in the text, and the Fig. 5 screenshot shows "query 34.7s" with "Sequences: 466/476" (phase1/odgi-shredtools.md section B8 items 2 and 3).
- It gives no impg command line, and the version appears only in reference [6] as v0.4.0 (paper.txt:837-839).

### 6.2 Why it threatens the paper

- It is the only benchmark of impg by another group that the phase-1 search found (phase1/related-work.md section 4.3), and it shows impg losing on build cost when alignment is counted and on the all-pairs query, 4.01 s against 0.484 s.
- Its "unable to compute" sentence has stood in public for 123 days at 2026-11-08 with no answer in print.
- Its authors are likely reviewers of any impg paper, which is the persona the hostile-reviewer judge took (judge-reviewer.md line 4), and the HPRC is a group author of the preprint (paper.txt:7-8).
- Any storage claim fails against their numbers and the release. The TPA set is 3.918 times the GBZ v3 (25,070,431,026 vs 6,398,170,680 bytes), and the Shredtools merged index with its `.bi` (27,478,774,573 bytes) is 1.096 times the TPA set before any impg index is added.
- A Nature Methods editor who sees two tools for the same query will ask what impg adds, and a Brief has 2 main display items to answer it (nm/nmeth_content.txt:62).

### 6.3 How the plan answers it

| Threat | Plan answer | Status |
| --- | --- | --- |
| "Unable to compute" over whole HPRCr2 | E2 indexes all 466 TPA files in single mode and reports build wall time, peak RSS and index bytes, then queries 1,000 regions per size class. F2 sets the median 10 kb query against the Shredtools median on the same regions | EXP |
| Build cost with alignment counted | E5 times alignment, index and query apart at 1, 8, 16 and 48 threads, and the main text says Shredtools wins whenever alignment must be computed. On HPRC r2 the alignment was paid by the PGGB build, at a cost that is unknown unless the builders answer Q3 | EXP, Q3 |
| Same input as their benchmark | E5 runs on HPRC year-1 chr19 and names the set as its own, because the year-1 PGGB graphs hold 90 haplotypes (`-n 90`) and their 92-haplotype list is not in the preprint. Q5 asks them for the list, the impg command lines and the meaning of "17%, the default auto setting" | EXP, Q5 |
| Their "17%, the default auto setting" | E5 writes the `--sparsify auto` pair list with `impg align --format joblist`. The editor computed that `tree:5:2:0.05` keeps 7.6923% to 20.3774% of pairs at n = 92, an inference from code (judge-editor.md V15) | inference, EXP |
| Both tools on released indexes | E2 runs Shredtools on `hprcv2_merged.bumbl` with the same BED as impg | EXP, Shredtools not installed |
| No truth set | E5 scores both tools against the 178 CAT GENCODE38 GFF3 files by containment, flank excess and wrong-locus rate (F4) | EXP |
| Fidelity through intermediate genomes | E3b measures recall of held-out partners with and without the two reference bridges (F3), and E4 measures recall by pair fraction and depth, scored once on the ScRAP 142 holdout | EXP |
| Copies per genome | the paper claims no copy counts until E7 shows separate records, and C4 on GRCh38 already shows depth 1 in 401 of 465 haplotypes | NOW for C4, EXP elsewhere |
| Zoom | E10 compares `impg refine` with enhance and zoom at TERT and IGKV6-21, as opposite trade-offs (refine moves boundaries to keep haplotypes, zoom drops haplotypes to keep boundaries) | EXP |
| Remote access | stated as a limit unless the authors add it (D12) | CODE (absence) |
| Their impg numbers | cited as theirs for impg v0.4.0, never as results of this paper | NOW-ext |
| Storage | no storage claim (plan.md section 11) | NOW (sizes) |
| Tone | the Discussion presents multi-MUMs as complementary and takes up their suggestion to feed them to impg as a homology source (paper.txt:528-532) | text |
| Timing | a preprint with the E2 numbers, which the editor recommends (decision D11) | decision |

Two details the authors should know before E2.
The listing holds two objects named `hprcv2_merged.bumbl`, 27,424,443,909 bytes under `mumemto/hprc/` and 27,424,176,737 bytes under `mumemto/` (phase2/gi_all.xml), and which one the web tool or the preprint used I don't know.
Shredtools' HPRCr2 set has N = 476 and the IMPG release has 466 files, so any shared comparison must use the intersection and name it (judge-reviewer.md must-fix 9).

## 7. Structure this draft borrows

### 7.1 From ODGI (Bioinformatics 2022)

In this table, main.tex is references/odgi-paper/manuscript/main.tex.

| ODGI element | ODGI evidence | Where it goes in this draft |
| --- | --- | --- |
| A Model section that defines the object in one paragraph, V = (N, E, P), 99 words | references/odgi-paper/manuscript/main.tex:145-153, word count in phase1/odgi-shredtools.md section A2 | Section 2 Model, 450 words, with the alignment tuple, the implied graph G(A), projection, the depth-bounded closure H_m, Propositions 1 and 2, and guarantees and non-guarantees (plan.md section 5.2) |
| An Implementation section built on stated properties, with Algorithm 1, 802 words | main.tex:159-229 | Section 3 Implementation, 600 words, Algorithm 1 for the BFS closure and Fig. 1c for the index layout (plan.md section 5.3) |
| An Overview with a full-width command-to-format map, which reviewer 2 found hard to read | main.tex:250-298, odgi_review1.txt:617 | Fig. 1d, a map for the 6 in-scope commands, sized for print |
| Results as vignettes on loci readers know, then a performance section | main.tex:340-519 | Results 5.1 to 5.8 (sections/05.results.tex), each tied to one experiment, and the whole-release cost section 5.2 |
| Benchmark rules: thread and haplotype sweeps, 10 runs, full supplementary tables, competitor wins reported (`vg find` 0.16 s vs `odgi position` 2.58 s) | references/odgi-paper/manuscript/table_position.tex, phase1/odgi-shredtools.md section A4 | E2 and E5 rules, Tables S1 to S8, axes from 0 |
| A worked toy example of the core algorithm | main.tex:695-725 | Fig. S1 from the fixtures in tests/test_transitive_integrity.rs |
| One script per figure and table in a paper repository (17 scripts) | references/odgi-paper/scripts/ | code fix C14 and Table S9 |
| A limits paragraph | main.tex:558-563 | the Discussion limits from plan.md section 11 |
| A coordinate-system comparison with rGFA and minigraph | main.tex:311-318 | Table 2, what each tool guarantees (impg, Shredtools, PGR-TK, liftOver and HAL, odgi and vg) |

ODGI reviewer lessons and the answer in this draft (odgi_review1.txt line numbers from phase1/odgi-shredtools.md section A7).

- Reviewer 2 wrote that the paper was "more a README/subtools manual than a scientific paper" with no benchmarks (odgi_review1.txt:377-383). This draft makes one claim and keeps partition, refine and local graphs as supporting sections that each carry their own measured evidence (plan.md section 0).
- The same passage says the paper "does not clearly state already at the beginning that you need an already computed graph" (odgi_review1.txt:382-383). The abstract here names the inputs, PAF, TPA or 1ALN (plan.md section 3).
- Reviewer 1 asked for y-axes from 0 (odgi_review1.txt:170-171), runtime against haplotype count (rev:176-178) and memory and disk tables (rev:342-356). Fig. 3 and Tables S1 to S8 carry them.
- Reviewer 2 asked "Why working only on chromosome 6 and not on the whole pangenome?" (odgi_review1.txt:637-638). E2 runs the whole release.
- Reviewer 2 asked for non-human data (rev:488-489). E4 and E9 use ScRAP 142.
- Reviewer 2 rejected a panel that claimed more than it showed (rev:765-775) and a wrong statement on other tools (rev:914-922). The must-not-claim list in plan.md section 11 and Table 2 answer both.
- ODGI had no accuracy benchmark (main.tex:571). This draft adds truth-based accuracy (E3 to E5).

### 7.2 From Shredtools (bioRxiv 2026)

- The missing-primitive framing (paper.txt:276-281) goes into the Introduction, with `impg query` as the alignment-backed form of the same primitive, carrying base-level ends and the alignment behind each interval (plan.md section 5.1).
- The genome-wide gene-set evaluation (55,997 genes, OMIM, CMRG, one per-gene number, scatter with marginals in its Fig. 4) becomes E5 and Fig. 4b, scored per gene and haplotype against CAT GENCODE38, a truth that Shredtools did not use.
- Refine against zoom at Shredtools' own loci becomes E10 and Fig. 5b. At IGKV6-21 (CHM13 chr2:89168754-89169041, 15 T2T haplotypes) Shredtools reported bounds of 328,599 bp left and 74,147 bp right, and 0 bp in 13 genomes after it dropped 2 (paper.txt:445-454).
- Case studies that expose data artifacts (the LCL VDJ deletion at IGK, the HG04228 duplication at TERT) become the dropped-haplotype count reported in E10.
- A short index-layout description goes into the Implementation section, as Shredtools did for bumbl.bi (phase1/odgi-shredtools.md section B11).
- This draft does not borrow the scaling-with-N figure built from subsets (its Fig. 1, N = 10 to 400), which plan.md does not include. The authors may add it as a haplotype sweep in E2.

### 7.3 From PGGB (Nature Methods 2024)

- The single claim. PGGB argued one pipeline in 9 paragraphs, and this draft keeps the Brief's one claim with supporting sections (plan.md section 0).
- The release-scale table. PGGB Table 1 gave size, compression, time, memory, SNV count and F-score for 10 runs, with the hardware in the legend. This draft gives Table 1 for datasets and Fig. 3 for cost on the whole release, with hardware, threads and the binary hash for every run (plan.md section 7 rules).
- Peer-review lessons.
  - The Minigraph-Cactus demand (MOESM3.txt:173-174) becomes U1, required before any Nature Methods enquiry.
  - The demand to measure the key claim (bias, answered as dropped sequence) becomes E3, reference dependence measured in bases.
  - Independent truth, not self-consistency, becomes the rule that E8 (concordance with the PGGB graph of the same alignments) is labelled consistency. Accuracy is scored against held-out direct alignments and CAT annotations, which are alignment-derived, and only the U3 simulation gives independent truth (judge-reviewer.md must-fix 8).
  - Dataset documentation with accessions becomes Table 1 and Table S11.
  - The evaluation bug found only in round 2 (MOESM3.txt:934-945) becomes code fix C14, a harness tested on toy data before any run.
  - The sparsification question becomes E4.
  - The code-deposit request (MOESM3.txt:114-115) becomes code fix C1, one tag with a Zenodo version DOI.
  - The whole-genome question from reviewer 2 (MOESM3.txt:228) becomes E2 on the whole release.

## 8. Decisions only the authors can make, and questions for outside parties

### 8.1 Decisions D1 to D14

plan.md section 13 defines D1 to D13, copied here.
D14 is new in this file, raised by the Nature Methods presubmission rule in section 2.

| ID | Decision |
| --- | --- |
| D1 | If E1 fails, fix the TPA path or move every run to the 318,372,159,094-byte per-target PAF set on the cluster |
| D2 | The flip targets for F1 to F5 (values proposed in plan.md section 2) and the E8 Jaccard target, fixed before any run |
| D3 | Compose strand across hops or document per-hop strand, and expand self-hits or document that they are not expanded (C7) |
| D4 | Whether to implement the restriction path (C15) so that `-o gfa` itself induces from clipped alignments |
| D5 | Which cluster node runs E2 and E3b, or whether to fund a lower-memory build if no node exceeds 59,163,669,536 bytes |
| D6 | The tag name, who owns C1 to C14, and how to keep the benchmark binary frozen while other work rebuilds target/release |
| D7 | Bioinformatics first (this plan) or the editor's Brief-first order (section 1.2) |
| D8 | ScRAP 142 (published) or yeast235 (local, 1,039,122,903 bytes, publication unknown) as the yeast set, and the hub strain for the star arm |
| D9 | The POA smoothing default (87 vs 2,224 spurious bp on yeast) before any pggb-engine graph appears (U8) |
| D10 | Whether `impg infer` is labelled experimental or product surface in `--help` |
| D11 | Preprint timing, given that the Shredtools sentence is public since 2026-07-08 |
| D12 | Add remote HTTP access before submission or state it as a limit |
| D13 | Who sends Q1 to Q5 |
| D14 (new) | If F1 to F5 pass, approach Nature Methods with an abstract-only enquiry sent when E2 has numbers and before this manuscript is final, or with a full Brief Communication, because the journal says enquiries are not for written manuscripts (nm/nmeth_submission-guidelines_presubmission-enquiries.txt:40). The same decision covers which reviewers to suggest, and whether to use the option to exclude one or two individuals or laboratories (nm/nmeth_editorial-policies_peer-review.txt:157) |

The order that matters most is D2, D5 and D7 first, because they decide what runs and where, then D3 before E3a strand scoring, and D1 only if E1 fails (plan.md, To decide).

### 8.2 Questions for outside parties Q1 to Q6, copied from plan.md section 12

| ID | To | Question |
| --- | --- | --- |
| Q1 | HPRC builders | Did `impg partition` and `impg lace` build the 7,424 released partition graphs (`partitionN.final.gfa.zst`, a `laced` VCF)? |
| Q2 | HPRC builders | Which pair-selection rule and wfmash settings produced the release network (11.2583% of ordered non-reference pairs)? |
| Q3 | HPRC builders | What did the r2 PGGB build cost, split by alignment, induction and smoothing (CPU hours, peak RAM)? |
| Q4 | HPRC builders | Who produced the IMPG product, so that the paper can disclose it? |
| Q5 | Shredtools authors | The 92-haplotype chr19 list, the impg command lines, and the meaning of "17%, the default auto setting" |
| Q6 | Cluster administrators | Which gemini node has more than 59,163,669,536 bytes of RAM and 63,916,842,350 bytes of scratch, and can jobs drop the page cache? |

Q3 and Q4 also bear on the venue.
Without Q3 the phrase "without building a graph" has no cost denominator at release scale, and the only stage cost on record is seqwish on 38 haplotypes, 46,268 s with 347.4983 GB (PMC9805579 Table 1, judge-editor.md section 3.2).
Without Q4 a reviewer may discount the HPRC distribution as self-produced adoption (proposal-nm-brief.md section 9 item 9).

## 9. Unknowns and where I looked

- The 2026 Bioinformatics author instructions. No phase saved the OUP page, and the only source is the ODGI repository README, whose word-limit lines date from 2021-10-30 (commit 10a8d02).
- Whether the Nature Methods preprint sentence covers third-party preprints. I read nm/nmeth_editorial-policies_preprints-conference-proceedings.txt, which does not say.
- The 2023 Brief Communication word limits. Only the 2026 page was saved (phase1/pggb-nature-methods.md, Open questions).
- Shredtools' target venue and its review status. The bioRxiv record read in phase 1 has no published DOI (`SCR/phase1_research_digest.txt`, Shredtools entry under STRUCTURES).
- Which `hprcv2_merged.bumbl` object the Shredtools web tool and preprint used. phase2/gi_all.xml lists two of different sizes.
- Who produced the HPRC r2 IMPG product. phase1/web/hpp_readme.md:149-191 does not say (Q4).
- Whether any experiment in sections 4 to 6 meets its target. Every one is EXP.
- Effort in person-weeks for the Tier 1 and Tier 2 work. No phase found a basis for an estimate (judge-feasibility.md section 0).
