# Log

## 2026-11-08 paper draft session
- impg repo: /home/guarracino/git/impg, version 0.5.0, HEAD 0987752. The paper repo submodule impg is older (7bd50a8).
- Paper repo already has a Bioinformatics Applications Note draft (sections/*.tex, uncommitted changes from 2026-09-19) and a cover letter for a Nature Methods Brief Communication.
- Phase 1 reports go to the session scratchpad phase1/ directory.
- Removed workgraph from the paper repo: .wg (34M), .wg-worktrees (54M, 3 worktrees), branches wg/agent-1, wg/agent-5, wg/agent-6 (all 88 branch files were identical in the working tree), .agents (empty), AGENTS.md, IMPG-WORKGRAPH-PROMPT.md, research/graph-view-filtering.md, the wg sections of CLAUDE.md, and the .wg and .workgraph lines of .gitignore. Backups of CLAUDE.md and .gitignore are in the session scratchpad.
- Removed outside the repo on user request: cargo uninstall workgraph (~/.cargo/bin/wg), ~/.wg (24K), ~/.claude/skills/wg (48K).
- Removed on user request: ~/git/wg (1.7G clone of graphwork/wg, clean, 0 unpushed commits) and the dead PATH line for ~/git/workgraph/target/release in ~/.zshrc (backup in the session scratchpad).
- Phase 1 result: broad features, weak quantitative evidence. No external comparator run (every "PGGB control" is impg's internal gfa:pggb engine). No alignment-backend scaling receipt at HEAD. Genotyping and genome inference are research in progress (infer mosaic bug, days per genome). Syng misses reverse-complement homologs (possible w vs w+1 seqhash cause, src/syng.rs:2204).
- Adoption: 114 GitHub stars, 16 forks, 11,160 Bioconda downloads, 4,895 Docker pulls; 6 papers use or cite impg (COSIGT, Genome Biology 27:286, 2026). HPRC r2 ships IMPG alignments (all-vs-all PAF 309,962,462,020 bytes, 466 TPA files) as one of three pangenome products.
- Shredtools preprint benchmarks impg v0.4.0 on 92 HPRCr1 chr19 haplotypes and says impg could not index whole HPRCr1 or HPRCr2.
- Nature Methods 2026 rules (read 2026-11-09 by agent): Article 150-word abstract, 3,000 words (5,000 at discretion), 6 display items; Brief Communication 70-word abstract, 1,200 words, 2 display items. PGGB was a Brief Communication.
- Phase 1 reports: session scratchpad phase1/*.md, corrections in phase1/VERIFY_CORRECTIONS.md.
- Phase 2 result: judges (editor, hostile reviewer, feasibility) total out of 50: Bioinformatics 28, 26, 28; Nature Methods Brief 26, 26, 25; Nature Methods Article 19, 20, 20. No framing can be submitted today: every result panel needs an experiment at a tagged release.
- New release facts (two agents agree): 466 TPA files, 25,070,431,026 bytes, 389,234,668 records; 25,221 of 216,690 ordered haplotype pairs (11.6392%); 23,738 of 108,345 unordered (21.9096%); without GRCh38 and CHM13 every haplotype reaches all 463 others within 2 hops.
- At C4 the released GRCh38 PAF has 895 records from 465 haplotypes, and 401 of 465 haplotypes have record depth 1, so copy-number claims need a check first (E7).
- target/release/impg was rebuilt at least 5 times on 2026-11-08 by another process: benchmarks need a frozen tagged binary.
- A phase-2 judge agent published its report by mistake as a private artifact: https://claude.ai/artifact/9eVLRc3v3JpcjNCNe8zwyk. Not deleted; the user decides.
- Phase 3+4 result: draft builds (17 pages). Bibliography 90 keys, 78 DOIs checked with Crossref or DataCite (77 of 78 titles matched; the 78th had a Crossref footnote, fixed). impg HEAD moved to 4008ae1 during the run; line numbers in the draft refer to 0987752.
- Committed draft, notes and workgraph removal as 832da96 on new branch draft/bioinformatics-2026-11, pushed to origin. Pre-existing user changes (sections, main.tex, build files, impg submodule, references/, research/) left uncommitted.
