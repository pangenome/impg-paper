# Implicit pangenomics: definition, properties, opportunities and limits

Written 2026-11-08 (session date) as the phase-2 conceptual map for the impg paper.
Code read at /home/guarracino/git/impg, HEAD 0987752, `impg 0.5.0`; I ran only `impg <cmd> --help` and read-only git commands there, and I wrote nothing in /home/guarracino/git/impg or /home/guarracino/git/impg-paper.
Inputs are the phase-1 maps, the verifier corrections (which override the maps where they differ) and the orchestrator facts, all under /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase1.
Facts I checked myself for this report are marked "checked here" with the file or command.
Status tags follow the task: NOW (in code and covered by a test or a stored measurement), CODE (in code, not measured), EXP (needs a new experiment), WIP (research in progress, not product-ready), IDEA (not in code).
Paths without a leading slash are relative to /home/guarracino/git/impg.
Every number is copied from its source or computed by me from copied numbers, and computed numbers say so.

## 0. Short answer

An implicit pangenome graph is the variation graph that seqwish would induce from a set of pairwise alignments, kept as an interval index over those alignments and evaluated only where a query touches it.
impg realizes the index, the interval projection through each alignment and a depth-bounded breadth-first closure of that projection (NOW on synthetic tests, and measured on a 465-haplotype HPRC index at v0.5.0).
impg does not realize the induced graph itself: `query -o gfa` drops the projected CIGARs and re-aligns the extracted intervals from scratch (CODE, src/main.rs:12326-12339, src/lib.rs:926-951), so today's local graphs are graphs of new alignments, not pieces of the implied graph.
Section 1 states two properties that make the concept exact: with unbounded depth and no length, snapping or identity filters, the closure is closed under inter-sequence alignment columns (Proposition 1), and seqwish run on the alignments clipped to any closed set gives the same nodes as the global seqwish graph restricted to that set (Proposition 2, which needs seqwish `-k` of at most 1).
Under the CLI defaults (`-m 2`, `--min-transitive-len 101`, `--min-distance-between-ranges 10`) the closure is not closed, self-alignments are reported but never expanded (src/impg.rs:2574-2575), and the BED strand is relative to the parent hop, not composed back to the query (derived from code, not run).
The syng backend is a second homology source (shared closed syncmers in a GBWT) behind the same `ImpgIndex` trait, but the trait silently ignores masks, depth, length, identity and subset parameters on it (src/lib.rs:515-607), and it misses reverse-complement homologs (34 of 715 nodes shared, notes/log.md:7-11).
The four top-ranked opportunities are population-scale regional retrieval without a graph build (NOW), exact lazy materialization by restriction (CODE pieces, EXP), sparse alignment networks with transitive recall (CODE, EXP) and incremental growth by per-file indexes (CODE, EXP).
Checked here: the HPRC release 2 TPA set is 466 files and 25,070,431,026 bytes, against 318,372,159,094 bytes for the 466 all-vs-1 PAF.gz files and 33,768,296,600 bytes for the whole-genome PGGB GBZ (S3 ListObjectsV2 on 2026-11-08; GBZ from the orchestrator facts).
Checked here: the PGGB rebuttal defers tree-plus-random sparsification to "implicit pangenome graphs" with the impg link (MOESM3.txt:976-982), and Yoo et al. 2025 has a Supplementary Note III subsection titled "Implicit pangenome graph (impg)" that describes impg and claims, without a measurement, that its transitive matching is "exactly equivalent" to subsetting a full graph build.

## 1. Formal definition

### 1.1 Sequences, positions and alignments

Let S = {s_1, ..., s_n} be the input sequences, s_i over {A, C, G, T, N} with length L_i; impg treats names as opaque strings (src/seqidx.rs:22-35).
Let Q = {(i, p, o) : 0 <= p < L_i, o in {+, -}} be the oriented positions, the same set as the input Q of seqwish, which contains every sequence and its reverse complement (seqwish paper, PMC9805579, Definition 2.1 passage).
An alignment is a = (i, [q_s, q_e), j, [t_s, t_e), sigma, c), with query i, target j, strand sigma in {+, -} and a CIGAR c over the ops `=`, `X`, `I`, `D`, `M`; any other op panics at query time (src/impg.rs:81-89).
Let col(a) be the set of aligned columns (t, q) of `=`, `X` and `M` ops, and col_=(a) the subset of `=` columns.
The match relation of a is mu(a) = {((j, t, +), (i, q, sigma)) and ((j, t, -), (i, q, -sigma)) : (t, q) in col_=(a)}.
The alignment set A = {a_1, ..., a_m} gives the symmetric match relation R(A), the union of mu(a) over A.
R*(A) is the same union built from col(a), so it also links `X` and `M` columns; impg projects through R*, seqwish merges only R.

### 1.2 The implied variation graph

Let ==_A be the reflexive, symmetric and transitive closure of R(A) on Q.
The implied variation graph G(A) = (V, E, P) has one node per class of ==_A (compacted into longer nodes where no branch intervenes), one path per sequence (the walk over the classes of its positions), and the edges that consecutive path steps use.
This is the construction of seqwish: "The transitive closure of a match, m+, is a set of characters in Q that are transitively linked together by other matches", and each closure becomes one node (seqwish paper, PMC9805579, induction passage).
seqwish in practice also drops exact-match runs shorter than `-k` before induction (PMC9805579, Methods passage on `seqwish -k`), and PGGB then smooths (smoothxg), normalizes (GFAffix) and sorts, so a PGGB graph is G(A) after four further transformations.
The implicit pangenome graph of A is G(A) left uncomputed, together with an index that answers questions about G(A) from A.

### 1.3 What impg stores

For every sequence id j, impg keeps one static cache-oblivious interval tree (coitrees `BasicCOITree`) over alignment records (src/impg.rs:226, 498-508).
A record holds the other sequence id, target and query start and end as i32, a file index, one u64 whose bit 63 is the strand and bit 62 the REVERSED flag with the rest a byte offset or record id, and a byte length (src/impg.rs:164-211).
No CIGAR and no sequence is stored; the CIGAR is read from the PAF bytes, or rebuilt from tracepoints with WFA2 over the segments that overlap the query, when a query needs it (src/impg.rs:1206-1417; checked here, src/impg.rs:164-174).
By default each record with query != target is inserted twice, under the target and, with the REVERSED flag and swapped coordinates, under the query; self-alignments are inserted once (checked here, src/impg.rs:1686-1712).
So the index holds 2m - m_self records, where m_self counts records with query == target.
The file format `IMPGIDX2` is a header, the name table, one serialized tree per target and a trailing offset map, and a query deserializes only the trees it touches (src/impg.rs:1758-1954).
README.md:30-32 still says the tool "stores CIGAR strings as compact deltas", which does not match HEAD (core map G18).

### 1.4 Projection as a relation on intervals

For a record a on target j and an interval I = [x, y) on j that overlaps [t_s, t_e), the projection pi_a(I) is the query interval from the first to the last query coordinate of the `=`, `X`, `M` or `I` columns that fall in I, together with the CIGAR slice for that span (checked here, src/impg.rs:2791-2929).
On the reverse strand the returned interval has first > last (src/impg.rs:2808-2813).
A pure insertion or pure deletion projects to nothing (src/impg.rs:2902-2928).
For a REVERSED record the CIGAR is inverted (I and D swapped, order reversed for the reverse strand) before projection, which gives pi of the inverse alignment (src/impg.rs:142-162, 1268-1275).
pi_a(I) is an interval that contains every query base matched by `=` columns to a base of I, plus the query insertions and mismatches between them, so it over-approximates the image of I under mu(a).
The one-hop neighbourhood is N(j, I) = {(i, pi_a(I clipped to a)) : a in the tree of j, a overlaps I} (src/impg.rs:1956, 2460-2540).
The projection relation of the index is the set of pairs (I, K) with (i, K) in N(j, I).
Status: NOW for the projection function (9 unit tests on project_target_range_through_alignment, src/impg.rs:3012-3187) and for one-hop CLI queries on synthetic PAF (11 of the 13 tests in tests/test_transitive_integrity.rs build a PAF index and query it, per the verifier).

### 1.5 Depth-bounded closure

The closure has four parameters: depth d (`-m`, default 2, 0 means unbounded), minimum hop length l (`--min-transitive-len`, effective default 101, src/main.rs:4253-4255), snapping distance delta (`--min-distance-between-ranges`, default 10) and per-hop filters phi (`--min-result-identity`, `--subset-sequence-list`, and masks from `partition`).
The breadth-first version (default, src/impg.rs:2379-2628) runs as follows.
Each sequence y has a visited set V_y of disjoint intervals; the query interval I is inserted into V_j without snapping and becomes frontier F_0 if its length is at least l.
At depth k, every frontier interval (x, J) is clipped against each overlapping record and projected; every projection (y, K) that passes phi is written to the output.
If y != x, the parts of K not yet in V_y, after snapping onto visited neighbours closer than delta, are added to V_y, and each part of length at least l joins F_{k+1}; projections with y == x are written but never expanded (checked here, src/impg.rs:2574-2589).
F_{k+1} is sorted and merged per sequence, and the loop stops when the frontier is empty or k reaches d (src/impg.rs:2444, 2597-2621).
Frontier intervals are stored as (start, end) with start <= end (checked here, SortedRanges::insert_inner at src/impg.rs:282-286), so orientation is not carried from hop to hop.
The BED writer reports '-' when first > last for the hop that produced the row (checked here, src/main.rs:12074-12078), so a row reached through two reverse-strand alignments is reported '-' although it is '+' relative to the query; this is derived from code and not run, and no test covers a multi-hop reverse path (tests/test_transitive_integrity.rs:298-347 tests one reverse hop).
Write C_d(j, I) for the bases covered by the output, and C_inf(j, I) for the case d = 0, l <= 1, delta = 0, no filters.
Status: NOW for BFS on synthetic inputs (test_transitive_coordinate_accuracy, test_transitive_depth_limit, test_min_distance_between_ranges_snaps_instead_of_discarding, test_requested_range_coordinates_stay_exact); CODE for DFS, which merges the whole stack after each pop so `-m` is not a strict bound (core map G10); the per-file `MultiImpg` closure has different semantics (its "BFS" is not FIFO and it skips self-hits, src/multi_impg.rs:813-952) and no test.

### 1.6 How the closure relates to G(A)

Proposition 1 (closedness).
With a bidirectional index (the default), d = 0, l <= 1, delta = 0 and no filters or masks, C_inf(j, I) is closed under R* restricted to alignments between different sequences: if b is in C_inf and (b, c) is in that relation, then c is in C_inf.
With `--unidirectional` the closure follows alignments from target to query only, and the proposition does not hold.
Reason: every base of C_inf lies in exactly one visited part, every visited part enters a frontier because l drops nothing, every frontier interval is queried because d is unbounded, and a query projects every record that overlaps it in both directions because of bidirectional insertion.
Consequence: the homologs of I in G(A), meaning all bases in the ==_A classes of the bases of I, are contained in C_inf(j, I) when no class needs a same-sequence alignment to connect.
The containment is strict in general, because projection hulls add query insertions and mismatches, which are then expanded in turn.
Same-sequence alignments break closedness, because self-hits are written but not expanded (src/impg.rs:2575), so a duplicate copy on the same contig contributes its own homologs only if they also align to another visited interval.
Status: CODE (derived from code; no test checks closedness on a non-trivial alignment set).

Proposition 2 (restriction).
Let C be any set of positions closed under R(A), and let A|C be the alignments clipped to the columns whose target base lies in C.
Then the classes of ==_{A|C} on C equal the classes of ==_A restricted to C, so G(A|C) is the subgraph of G(A) induced by the classes that meet C, with each path cut to its intervals in C.
Reason: any chain of matches between two bases of C stays inside C because C is closed, so restricting A to C removes no chain that connects two bases of C.
Condition: the seqwish `-k` filter must be at most 1, because the boundary of C cuts a match run at the same column on both sides, and a cut run shorter than k is dropped from G(A|C) while the whole run is kept in G(A).
Smoothing, GFAffix and sorting act after induction, so the proposition says nothing about PGGB output after smoothxg.
With d = 0, l = 0, delta = 0, `--no-merge` and `-o paf`, the BFS output already contains A|C for C = C_inf, because every alignment that overlaps a base of C is projected from the frontier interval that holds that base and written with its CIGAR slice (src/impg.rs:2544-2569; PAF rows carry `cg:Z`, src/main.rs:12286-12290).
The code does not use this: output_results_gfa keeps only the merged query intervals (checked here, src/main.rs:12326-12333) and dispatch_gfa_engine re-aligns them with the selected engine (src/lib.rs:926-951, 1112-1131).
Status: the proposition is derived here and is EXP; the pieces it needs (closure, PAF output with CIGAR, `impg graph --paf-file --no-filter --gfa-engine seqwish`) are CODE, and PAF output has no test (core map, verifier).
Yoo et al. 2025 wrote that impg's matching "is transitive and exactly equivalent to what would be obtained from subset operations on a full graph build" (checked here, Supplementary Information pdftotext copy, line 669); Propositions 1 and 2 give the conditions under which a version of that sentence holds, and neither that section nor the impg repository contains a measurement of it.

### 1.7 The second homology source: syng

The syng backend replaces A by a syncmer GBWT built from the sequences alone (`impg syng`, src/syng.rs:2578-2772).
Its alphabet is the set K of canonical closed syncmers with s-mer length 8 and total length 63, stored as `SyncmerParams { k = 8, w = 55, seed = 7 }` (src/syng.rs:1495-1522).
impg builds the hasher with window w = 55 s-mers (a 62 bp window) and stores a 63 bp syncmer (checked here, src/syng.rs:2360-2363), while upstream syng.c builds it with w + 1 and the comment "need the +1 here, awkwardly" (checked here, vendor/syng/syng.c:416).
Each sequence becomes one forward and one reverse-complement GBWT path of signed node ids with bp offsets (src/syng.rs:2684-2736).
The syng match relation R_syng links two positions when they start occurrences of the same node.
A query walks the query path over I through sampled checkpoints (src/syng.rs:3980-4044), drops the top 0.0005 fraction of nodes by GBWT count from seeding, matches exact 5-syncmer walk seeds (src/syng.rs:5131-5436), locates occurrences through `.spos` (src/syng.rs:4473-4557), chains anchors per target and strand with the sweepga scaffold filter at an adaptive minimum of 1 to 20 anchors (src/syng_transitive.rs:111-345, 866-918), and by default refines only the two chain ends with BiWFA, which needs the sequence files (src/syng_transitive.rs:426-797; `--syng-raw` skips it).
So pi_syng(I) is the hull of a collinear chain of shared 63-mers, with no interior CIGAR (src/syng_transitive.rs:14-21).
The transitive syng query is a BFS with a shared visited-node set and depth max(1, m), so `-m 0` means depth 1, not unbounded (src/main.rs:6828-6832; src/syng_transitive.rs:1379-1576).
Status: NOW for build, one-hop query and map (32 integration tests and 102 unit tests in src/syng.rs per the syng map and verifier); CODE for multi-hop, which no test runs at depth 2 or more; WIP for strand completeness, because a 20 kb sequence and its reverse complement share 34 of 715 nodes and `query` never reports the reverse copy (notes/log.md:7-11, checked here; open item at notes/tasks.md:4).
Whether upstream syng shares the asymmetry is unknown: the owner's note points at vendor/syng/syncmerset.c:59, which sets only the stored length w + k, and I did not run upstream syng.

### 1.8 One interface, two sources

The `ImpgIndex` trait (src/impg_index.rs:17-121) is implemented by `Impg`, `MultiImpg` and `SyngImpgWrapper` (src/lib.rs:235-249), so `partition` and other callers run on either source.
SyngImpgWrapper binds masks, max_depth, min_transitive_len, min_distance_between_ranges, min_output_length, identity and the subset filter to `_` (checked here, src/lib.rs:515-607), so its transitive calls are one syng query and partition applies masks afterwards (src/commands/partition.rs:447-452).
The homology parameters of section 1.5 therefore change results on the alignment source and do nothing on the syng source, without a warning.

### 1.9 Definition in one paragraph

An implicit pangenome graph over sequences S is a homology source H (a set A of pairwise alignments with base-level CIGARs or tracepoints, or a syncmer GBWT), an index that returns, for any interval on any sequence, the records of H that overlap it, a projection operator that maps the interval through each record, and a depth-bounded closure of that operator; the variation graph G(A) that seqwish would induce from A is never built, and by Proposition 2 any part of G(A) over a closed interval set can be induced on demand from the records clipped to that set.

## 2. Properties and whether the code realizes them

| Property | Status | Evidence | Caveat |
|---|---|---|---|
| Index size linear in the number of alignment records (2 entries per non-self record, coordinates plus a pointer) | NOW | src/impg.rs:164-211, 1686-1712; the 465-haplotype vs GRCh38 index is 814,414,241 bytes for a 6,342,372,371-byte PAF.gz and 17,833,266 tree entries (data/hprcv2/pafs; notes/IMPG_MEMORY_PROFILING_REPORT.md:45-66 at 7bd50a8); 45.67 bytes per entry by my division | The alignment set itself grows with the number of pairs: HPRC r2 all-vs-all PAF.gz is 309,962,462,020 bytes against 6,342,372,371 bytes for the star, 48.87 times by my division (orchestrator facts) |
| Alignments compressible with tracepoints | NOW for sizes, CODE for queries | Checked here: 466 TPA files total 25,070,431,026 bytes and 466 all-vs-1 PAF.gz files total 318,372,159,094 bytes, 12.70 times by my division; the GRCh38 pair on disk is 560,062,985 vs 6,532,446,867 bytes, 11.66 times | No test reads `.1aln` or `.tpa` (core map G1); FastgaNoDiff and Variable records plausibly panic at src/impg.rs:832; failed tracepoint hits are dropped with a debug log only (src/impg.rs:1230-1460); the local TPA index has magic `IMPGIDX3`, which HEAD rejects (src/impg.rs:1897-1911); I did not check that TPA and PAF files hold the same records |
| Lazy access (only touched target trees are loaded) | NOW | 2 tree loads for a chr1 query at `-t 1` and `-t 16`; 5 kb chr1 query 0.51 s best of 5 at 327.8 MB; MHC at `-m 0` 0.27 s and 88,500 kB (notes/IMPG_MEMORY_PROFILING_REPORT.md:109-123, 208, at 7bd50a8) | The unit of laziness is a whole chromosome tree (308 MB of the 328.1 MB peak for 5 kb is printed with a tilde at :18); a whole chr1 query ran past 10 minutes and was killed (:212); the tree cache is unbounded and the memory fixes are unmerged (core map G8) |
| Lazy materialization of graphs | NOW for local graphs from re-alignment, IDEA for restriction of G(A) | C4, 465 paths, 232,738 bp: 13:38 wall, 64.3 GB (docs/crush-vs-pggb-comparison.md:9-11, 64; includes the whole syng index load, 2026-05-26); tests at 64 bp (tests/test_graph_output_crush.rs:37-124) | Local engines re-align the extracted intervals (src/main.rs:12326-12339), so a local graph is G(A') for new alignments A', not part of G(A) |
| Any sequence can be the coordinate system | NOW | Bidirectional insertion (src/impg.rs:1686-1712); test_bidirectional_symmetry (tests/test_transitive_integrity.rs:227-290) | `--unidirectional` is untested and the index does not record which mode built it (core map F2); explicit graphs also allow any path as reference (odgi position, vg deconstruct), so the gain is no build, not the choice of frame |
| Transitive closure on demand, bounded by depth | NOW (BFS, toy), CODE (DFS, MultiImpg, syng multi-hop) | Section 1.5 | Closed only under the Proposition 1 settings; defaults truncate |
| Incremental growth by adding alignments | CODE | `--index-mode per-file`, automatic at 100 or more files, builds missing `.impg` files only (src/main.rs:11265-11345); MultiImpg federates headers (src/multi_impg.rs:135-216) | src/multi_impg.rs has 0 tests; the cache is invalidated and the unified header rebuilt whenever the list changes (src/multi_impg.rs:140-216, 1000-1010); `impg align` has no new-vs-existing pair mode (verifier) |
| Multi-resolution, from syncmer to interval to base | NOW for base (CIGAR projection unit tests) and syncmer (syng raw tests); CODE for interval (`--approximate`) | src/impg.rs:3012-3187; src/syng.rs:7953-8729; src/impg.rs:1419-1637 | `--approximate` has no test and no measurement, and its "10-100x" speedup is presented as achieved with no timing (notes/FAST_MODE_IMPLEMENTATION.md:788); bedpe, paf and maf outputs have no alignment-backend test |
| Homology defined at query time (identity, hop length, depth, cohort) | NOW for depth, CODE for the rest | test_transitive_depth_limit; `--min-result-identity` and CLI `--subset-sequence-list` untested (core map G4) | The subset filter works at haplotype or sample level and always keeps the query sequence (src/subset_filter.rs:23-58, 116-135; src/impg.rs:2490-2497); PAF and tracepoint paths apply the identity filter to different spans (src/impg.rs:1277-1281 vs 1386-1390) |
| Mixed homology sources | CODE within the alignment source, IDEA across sources | PAF, 1ALN and TPA files combine in one index (src/alignment_record.rs:67-79; main.rs:11646-11693) | No test for 1ALN or TPA; one query uses one source, so alignments and syncmers never meet in one closure |
| Two homology sources under one interface | CODE | Section 1.8 | Parameters silently ignored on syng |
| Partition into disjoint work units that together cover every base | NOW on syng, CODE on alignments | yeast235 syng run: 19,421 partitions, 383,849 member intervals, 9,901 source paths, 3,336,976,856 bp, zero uncovered bases, zero bases owned twice, 10,544 s wall, commit 295bca9 (docs/syng-gmem-bwt/observation-registry-repair.md:147-151; campaign-record-2026-10-diploid-arc.md:922) | Partitions are disjoint, not homology-closed: the first window to reach a base owns it and later closures stop at masks (src/commands/partition.rs:1309-1377; src/impg.rs:2396-2440); 11 commits touched partition.rs or lib.rs after 295bca9 (verifier); the laced graph is held whole in memory (src/lib.rs:1276-1319) |
| Per-hop provenance (CIGAR slice and identity for each projected interval) | CODE | PAF rows carry `cg:Z`, `gi:f`, `bi:f`, `an:Z`; bedpe carries `gi:f` and `bi:f` only (src/main.rs:12176-12180, 12286-12290) | No test of PAF or bedpe output; with `-d` > 0 rows are merged |
| Sequences stay compressed (AGC) | NOW | tests/test_agc_integration.rs:6-186; 0.4 ms per random 900 B or 6 KB fetch on CHM13 chr1 (commit f259c47) | No length guard for archives appended with agc older than 3.2.2 (src/agc_index.rs:383-407); the code comment puts one decompressor slot at 3.70 GB on the 3.30 GB panel, 8 slots by default (src/agc_index.rs:61, 87-100) |

## 3. Ranked opportunities

### 3.1 Scoring rule

Each opportunity gets three scores from 1 to 3, and the rank follows their product.
Novelty: 3 when no explicit-graph workflow gives the result without first building the whole graph or when the question is open in the literature, 2 when explicit tools give it after a build, 1 when it is generic tooling.
Evidence: 3 when the mechanism is NOW, 2 when all pieces are CODE, 1 when a piece is WIP or IDEA.
Feasibility: 3 when the experiment runs on the local workstation (16 CPUs, 57 GB RAM, 40 GB free disk) with data on disk or downloads under 5 GB, 2 when it needs the cluster "gemini" (size unknown) or downloads of tens of GB, 1 when it also needs a code change that is not yet written or the 309,962,462,020-byte all-vs-all PAF.
Ties break on evidence, then feasibility, then the order in which the paper's argument needs them, which I state where it applies.

| Rank | Opportunity | Status | N | E | F | Product |
|---|---|---|---|---|---|---|
| 1 | Population-scale regional homology retrieval with no graph build | NOW | 2 | 3 | 3 | 18 |
| 2 | Exact lazy materialization by restriction (Proposition 2) | CODE | 3 | 2 | 3 | 18 |
| 3 | Sparse alignment networks with transitive recall | CODE | 3 | 2 | 3 | 18 |
| 4 | Incremental growth by per-file indexes | CODE | 3 | 2 | 3 | 18 |
| 5 | Disjoint homology-defined work units, then per-partition graphs and lace | NOW | 2 | 3 | 2 | 12 |
| 6 | Locus graphs on demand | NOW | 2 | 3 | 2 | 12 |
| 7 | Queryable compressed alignment storage (TPA) | CODE | 2 | 2 | 3 | 12 |
| 8 | Base-level transitive liftover with per-hop provenance | CODE | 2 | 2 | 3 | 12 |
| 9 | Homology parameters and cohorts chosen per query | CODE | 2 | 2 | 3 | 12 |
| 10 | Locus boundary refinement for locus genotyping | CODE | 2 | 2 | 3 | 12 |
| 11 | Alignment-free homology source under the same interface | WIP | 3 | 2 | 2 | 12 |
| 12 | Region-level similarity and MDS tracks | CODE | 1 | 2 | 3 | 6 |
| 13 | A stable global node space from syncmer ids | WIP | 3 | 2 | 1 | 6 |
| 14 | Mixed homology sources in one closure | IDEA | 3 | 1 | 2 | 6 |

Ranks 2 to 4 tie on every score; I put the restriction result first because the definition of the concept rests on it, then sparsification because the PGGB review left it open, then incremental growth.

### 3.2 Details

#### 1. Population-scale regional homology retrieval with no graph build (NOW)

What it enables: `impg query -a <alignments> -r <seq:start-end> -x -d <bp>` returns, for every haplotype, the base-level intervals homologous to a region given on any assembly, from an index that took no graph induction.
impg evidence: on the 465-haplotype vs GRCh38 index, a 5 kb chr1 query took 0.51 s best of 5 at 327.8 MB and the MHC at unbounded depth took 0.27 s at 88,500 kB (notes/IMPG_MEMORY_PROFILING_REPORT.md:123, 208, at 7bd50a8); Shredtools measured impg v0.4.0 on 92 HPRC r1 chr19 haplotypes at 4.01 s and 1.66 GB per query with all pairs and 0.21 s and 12 MB with its sparse set, against 0.484 s and 79 MB for Shredtools (Shredtools paper.txt:309-312).
Explicit-graph cost: PGGB took 18.46 h and 137.72 GB at 48 threads for one 90-haplotype human chromosome 6 (PGGB Table 1), and then `odgi extract` took 46.87 s and 7.23 GB, or `vg chunk` 1838.51 s and 60.37 GB, at 16 threads on 64 haplotypes of HPRC chr6 (ODGI tables, phase-1 digest); the released HPRC r2 whole-genome PGGB GBZ is 33,768,296,600 bytes before any query (orchestrator facts); Minigraph-Cactus reports 5 h for the HPRC r1 pangenomes and 19 h for the progressive Cactus alignments and calls both rough (related-work, PMC10638906).
Experiment: on the local star index (data/hprcv2/pafs, IMPGIDX2, 814,414,241 bytes) and AGC, query 1,000 random 5 kb GRCh38 regions plus MHC, C4, LPA, SMN1 and AMY1A at `-m 2`, and extract the same regions from the HPRC r2 PGGB graph with gbz-base on the released `.gbz.db` or `vg chunk` on the GBZ on gemini; report per region the haplotypes and bp recovered by each tool, the base-level agreement of interval boundaries, wall time, peak RSS, and the up-front build or download cost of each representation; keep chr20 regions as a holdout that no parameter choice sees.

#### 2. Exact lazy materialization by restriction (CODE pieces, EXP)

What it enables: any part of the PGGB-style seqwish graph G(A) is induced from the stored alignments clipped to a closed interval set, so the whole-genome graph never has to exist and the local graph is provably the same as the corresponding subgraph of the global one (Proposition 2).
impg evidence: the closure and PAF output with `cg:Z` exist (src/impg.rs:2379-2628; src/main.rs:12286-12290), and `impg graph` accepts `--paf-file`, `--no-filter`, `--min-match-len` and `--gfa-engine seqwish` (checked here, `impg graph --help`); today's engines discard the CIGARs and re-align (src/main.rs:12326-12339).
Explicit-graph cost: one global induction over all of A before any extraction; seqwish took 46,268 s, 347.4983 GB memory and 604.4261 GB disk for 38 human haplotypes of 114.627 Gbp (seqwish Table 1, PMC9805579), and PGGB 18.46 h and 137.72 GB for one 90-haplotype chromosome 6 including smoothing (PGGB Table 1).
Experiment: tune on tests/test_data/yeast.chrV.fa.gz (7 sequences, 4,029,392 bp) and hold out a 20-haplotype C4 region extracted from the local AGC; align all-vs-all with `impg align --format paf`, build the global seqwish graph from the full PAF, and for 100 random 10 kb loci compute C with `impg query -x -m 0 --min-transitive-len 0 --min-distance-between-ranges 0 --no-merge -o paf`, build seqwish on that PAF, and compare for every base of C the set of bases that share its node in the global and in the restricted graph; the prediction is 0 differing bases with `-k` at most 1 and a positive count at `-k 23` and at the CLI defaults (`-m 2`, 101, 10), and the same comparison for the current `-o gfa:seqwish` re-alignment path measures how far today's local graphs are from G(A); whether the embedded seqwish engine can skip GFAffix and sorting is unknown (I found no flag), so the comparison must apply the same normalization to both sides or use an external seqwish.

#### 3. Sparse alignment networks with transitive recall (CODE, EXP)

What it enables: a pangenome needs far fewer than n(n-1)/2 alignments if transitive closure recovers the missing pairs, and the recall of each sparse design becomes a measured property instead of a build-time guess.
impg evidence: `impg align --sparsify` offers `random:<f>`, `giant:<p>`, `tree:<near>:<far>:<rand>` and `wfmash:<f>` with default `none` (sweepga knn_graph.rs:32-156, partition map); `giant:<p>` is a k-nearest-neighbour graph, not an Erdős-Rényi graph, and gives k = 2 for n = 7, 235, 1000 and 10000 at p = 0.99 (partition map section 6.3, my arithmetic reproduced by the verifier); with FastGA and one input FASTA the pair set is ignored (partition map G2); only a parse test covers sparsification (src/commands/align.rs:878-914).
Explicit-graph cost: PGGB applies Erdős-Rényi sparsification inside one build (scerevisiae142 10.11 h and 80.25 GB sparsified against 20.46 h and 119.68 GB, PGGB Table 1), and its reviewer asked in round 2 why not a spanning tree, which the authors deferred to impg (MOESM3.txt:387-389, 976-982); seqwish must close the whole alignment set at once.
Experiment: the HPRC r2 release already gives per-target all-vs-1 files (466 PAF.gz, median 655,074,392 bytes; 466 TPA, median 51,404,490 bytes; checked here), so hub designs need no new alignment; build indexes for 1 hub (GRCh38, on disk), 2 hubs (plus CHM13, 5,590,178,237 bytes PAF.gz) and 10 hubs, plus random and tree subsets made by filtering haplotype pairs in those files, and score 1,000 regions from 10 non-hub query haplotypes against the direct alignments in each query haplotype's own all-vs-1 file (HG00097 hap1 is 637,253,141 bytes); report recall of haplotypes and bp at `-m 1` to 4, boundary deltas, closure size per depth, and bytes of alignment used; tune on chr6, hold out chr20 and a separate set of query haplotypes; repeat on yeast with `impg align --wfmash` on per-genome FASTA files so that the pair set is honoured.

#### 4. Incremental growth by per-file indexes (CODE, EXP)

What it enables: adding a genome means adding the file of its alignments and indexing that file alone; with bidirectional insertion one file per new genome (all others aligned to it) is enough, which is the layout HPRC r2 already ships (466 per-target files, checked here).
impg evidence: per-file mode builds only missing indexes and federates them (src/main.rs:11265-11345; src/multi_impg.rs:135-216); MultiImpg has 0 tests and its transitive query differs from the single-index BFS (src/multi_impg.rs:813-952).
Explicit-graph cost: PGGB rebuilds (18.46 h for one 90-haplotype chr6, PGGB Table 1; 7 days for 1000 chr19 haplotypes, nf-core/pangenome, PMC11568064); whether Minigraph-Cactus can add genomes without a rebuild I don't know (not in the phase-1 sources); SVPG reports faster graph augmentation only in words, "nearly tenfold" (pggb map C.1).
Experiment: on gemini, index 400 of the 466 per-target files in per-file mode, add the other 66, and time the update against a single-index rebuild over all 466; on 1,000 regions check that per-file and single-index results are identical (this first measures the MultiImpg semantic gap) and that results with 400 files are a subset of results with 466 (closure monotonicity, which visited-set subtraction and the length filter could break); keep 100 regions as a holdout; the 466 TPA files (25,070,431,026 bytes) fit the local 40 GB disk only if their indexes fit the rest, and for the GRCh38 TPA the index was 757,392,357 bytes for a 560,062,985-byte TPA, 1.35 times by my division, so the local run is at risk.

#### 5. Disjoint homology-defined work units, then per-partition graphs and lace (NOW for the cover, CODE for graphs at scale)

What it enables: `impg partition` turns the whole pangenome into independent units without a graph, so per-unit graph builds can run as separate cluster jobs and be laced back by coordinates.
impg evidence: the yeast235 syng audit above (zero uncovered, zero owned twice, 10,544 s, commit 295bca9); the laced graph is tested on 3 x 30 kb (tests/test_graph_partitioned.rs:30-65); the pipeline holds every partition GFA in memory and runs GFAffix and sort on the whole laced graph, and README.md:551-553 claims that partitioned mode caps peak memory with no measurement (verifier).
Explicit-graph cost: PGGB induces and smooths a whole chromosome in one process (18.46 h, 137.72 GB for 90-haplotype chr6); nf-core/pangenome proposed exactly this split-and-lace with IMPG and gfalace (PMC11568064 Discussion); HPRC r2 ships a per-partition PGGB set, and whether impg built it is unknown (orchestrator facts).
Experiment: on gemini, a 50-haplotype HPRC chr20 set from the AGC, aligned with `impg align`; run `impg partition -o gfa --gfa-engine pggb:<W>` and a whole-chromosome PGGB run; report wall, peak RSS per job and in total, path-spelling identity for every path, dropped bp, node and edge counts, panacus growth, and the fraction of bases whose homologs fall in another partition (computed from one-hop queries of each partition against the others), which measures how far partitions are from homology-closed; hold out chr19.

#### 6. Locus graphs on demand (NOW)

What it enables: one GFA per locus from the index plus sequences, with path names that carry source coordinates.
impg evidence: C4, 465 paths, 13:38 wall, 64.3 GB, 13,288 segments (docs/crush-vs-pggb-comparison.md:9-11, 64; run 2026-05-26 at older defaults, including the whole syng index load); POA scoring defaults changed on 2026-11-08 (commit 333c21d).
Explicit-graph cost: the whole-graph build of opportunity 1, then extraction.
Experiment: 20 loci from the local star index and AGC with `-o gfa:pggb`, against subgraphs of the released HPRC r2 PGGB graph extracted on gemini; report path-spelling identity, nodes, segment bp, POVU flubbles, `gfa2vcf` calls against the released PGGB VCF of the same loci, and cost per locus with the index load timed apart; hold out 5 loci; note that with the star index the reference only chooses which intervals enter, and the local graph is re-aligned all-vs-all among them.

#### 7. Queryable compressed alignment storage (CODE)

What it enables: the implicit pangenome ships as compressed alignments plus a compressed sequence archive, smaller than the explicit graph file, and stays queryable at base level.
impg evidence: HPRC r2 TPA 25,070,431,026 bytes plus AGC 3,295,070,733 bytes is 28,365,501,759 bytes, against 33,768,296,600 bytes for the PGGB GBZ (my sums; S3 listing checked here; GBZ from the orchestrator), with the caveat that the TPA index size is unknown and that the files hold all pairs twice, once per target file, so a bidirectional index of half the files may suffice (derived, record identity unchecked); TPA queries have no test (core map G1).
Explicit-graph cost: the GBZ plus its build; GBZ queries need the GBZ or its `.gbz.db` (related-work, HPRC README).
Experiment: locally, reindex the GRCh38 TPA (560,062,985 bytes) at HEAD and query 1,000 regions at `-m 0`, 1 and 2 in exact mode against the GRCh38 PAF.gz (6,532,446,867 bytes) of the same release; exact mode must give identical sorted BED and PAF, and `--approximate` must report its boundary error and wall time against exact mode; also count records per file with `impg stats` to test record identity; hold out chr20.

#### 8. Base-level transitive liftover with per-hop provenance (CODE)

What it enables: interval liftover between any two assemblies, through intermediate genomes when no direct alignment exists, with the CIGAR slice and identity of each hop.
impg evidence: PAF output fields (src/main.rs:12286-12290), untested; the BED strand is per hop (section 1.5).
Explicit-graph cost: UCSC liftOver needs one chain file per ordered pair (Kent et al. 2003), halLiftover needs a Cactus HAL (Hickey et al. 2013), and odgi position needs the graph.
Experiment: lift 10,000 random 1 kb intervals from GRCh38 to CHM13 and from HG002 hap1 to hap2 through the GRCh38 star (2 hops), against the direct alignments in the CHM13 and HG002 all-vs-1 files and against the public UCSC GRCh38-to-CHM13 chain; report the exact-boundary rate at 0, 1, 10 and 100 bp, strand agreement, and recall; add a three-sequence synthetic fixture with two reverse-strand hops to test strand composition.

#### 9. Homology parameters and cohorts chosen per query (CODE)

What it enables: identity threshold, depth, hop length and the haplotype cohort change per query in seconds, where an explicit graph bakes them into construction.
impg evidence: flags at src/main.rs:4226-4351; depth tested, the rest untested.
Explicit-graph cost: one rebuild per setting, for example PGGB `-p` identity at 18.46 h per 90-haplotype chr6 build.
Experiment: on 20 loci, sweep `--min-result-identity` 0.90, 0.95, 0.99, `-m` 1 to 4 and a one-population subset list; report output change and seconds per run, and compare the subset local graph with an extraction of the full PGGB graph restricted to the same paths (nodes, flubbles), which shows what excluded haplotypes leave behind in an explicit graph.

#### 10. Locus boundary refinement for locus genotyping (CODE, used in a published method)

What it enables: `impg refine` widens a locus until the most haplotypes span both ends, from alignments only, before any graph is built.
impg evidence: COSIGT uses `impg refine` and `impg query` and describes "an implicit pangenomics approach using impg" (Bolognini et al. 2026, Genome Biology 27:286; cosigt.txt:45-49); refine has 1 unit test and no CLI test (partition map G5); the early stop exists only in sample and haplotype modes (verifier).
Explicit-graph cost: build the graph, then per-path coverage at each candidate boundary (odgi extract and odgi paths) per window.
Experiment: on 50 structurally variable loci (C4, LPA, KIR, HLA, AMY1A), count haplotypes spanning both ends before and after refine, the bp added, runtime, and broken paths in local graphs of raw and refined loci.

#### 11. Alignment-free homology source under the same interface (WIP)

What it enables: homology queries and partitions over a pangenome indexed from sequence alone, with no pairwise alignment for the index.
impg evidence: HPRCv2 syng index with a 5.1 GiB `.1khash` and an 8.9 GiB `.1gbwt` (both stated as "about" in docs/syng-gmem-bwt/benchmark.md:118-119), 272,213,874 nodes, 35.5 GiB resident and 178 s load (biobank-scale-datasheet.md:353-355); no build time for that index is recorded (syng map G6); the default query runs BiWFA boundary refinement (evidence-inventory verifier); the only syng versus PAF comparison is one 2 kb yeast region at d48afc8 with 209 shared paths and 124 of 209 starts within 5 bp (notes/SYNG_VS_PAF_VALIDATION.md:36-49); the reverse-complement miss is open and its fix would renumber every index (notes/log.md:7-11).
Explicit-graph cost: every explicit builder aligns or maps first (PGGB wfmash, Minigraph-Cactus minigraph and Cactus); Durbin's syng paper reports a 5.8 GB GBWT of 92 human genomes built single-threaded in 52 minutes (PMID 42878135 abstract, related-work).
Experiment: after the reverse-complement decision, build syng indexes for yeast (local) and the 50-haplotype chr20 set, record build wall and RSS, and run tests/validation/battery_syng_vs_paf.sh over 1,000 regions with results split by strand; report recall and boundary deltas against the alignment source; hold out one chromosome.

#### 12. Region-level similarity and MDS tracks (CODE)

What it enables: per-window pairwise similarity and MDS coordinates along a chromosome from homologous intervals, without a graph.
impg evidence: `impg similarity` POA or MinHash modes, 0 tests, and a Jaccard on truncated bottom-k sketches that is not the Mash union estimator (partition map G4, G15).
Explicit-graph cost: build the graph and run `odgi similarity` per extracted region.
Experiment: on HPRC chr6 windows of 1 kb, 10 kb, 100 kb and 1 Mb, compare POA and `--fast` identities with pairwise alignment identity and with `odgi similarity` on PGGB extracts; report correlation, absolute error and runtime.

#### 13. A stable global node space from syncmer ids (WIP)

What it enables: independently built local graphs and read packs share node ids without remapping.
impg evidence: raw range GFA with masking disabled keeps global syncmer ids, shown by spell equality on 109 walks (campaign-record-2026-10-diploid-arc.md:922); the default `gfa:syng` masks, clones and re-sorts, and `gfa:syng-local` and regional `-o gbwt` re-intern ids (syng verifier); the reverse-complement fix would change every id.
Explicit-graph cost: node ids belong to one build; separately built PGGB local graphs have unrelated ids.
Experiment: after the dictionary fix, build raw local graphs of adjacent overlapping windows and check that shared syncmer segments carry identical ids and sequences, and score one sample pack against both; the expected count of mismatches is 0.

#### 14. Mixed homology sources in one closure (IDEA)

What it enables: one closure that uses wfmash alignments where they exist, FastGA elsewhere, syncmer anchors in regions without alignments, and possibly multi-MUM waypoints, which the Shredtools authors suggest integrating into impg (Shredtools paper.txt:528-532).
impg evidence: PAF, 1ALN and TPA mix in one index (CODE, untested); alignments and syng never meet in one query.
Explicit-graph cost: one aligner per build; a change of homology source means a rebuild.
Experiment: on C4 with 20 haplotypes, compare closures and restricted graphs from wfmash only, FastGA only and the union, and report bases gained and lost per haplotype.

## 4. Limits of the implicit model

L1. Homology is whatever the aligner and filter reported.
Missing alignments are missing homology, and spurious ones are spurious homology that the closure then propagates.
The defaults filter with sweepga many:many, scaffold jump 50 kb and scaffold mass 10 kb (src/main.rs:2014-2028), FastGA is the default aligner, and wfmash gets a hidden 90% identity default (src/main.rs:9540-9544, 10498-10503), so reported homology depends on settings that the user does not see in `--help`.
PGR-TK names the same risk for its own fetch step, "may introduce bias due to missing or incorrect alignments" (related-work, PMC10406601).

L2. The alignment design decides what can be reached.
In a star to GRCh38, two non-reference haplotypes connect only through bases aligned to GRCh38, so sequence that both carry and GRCh38 lacks is never reached from either (derived from the definitions in section 1).
That is the reference bias that PGGB argued against, and it applies to the 465-haplotype star index on disk.
All-vs-all removes it at 309,962,462,020 bytes of PAF.gz against 6,342,372,371 bytes for the star (48.87 times by my division).
Sparse designs give connectivity only as far as the design guarantees it, and `giant:<p>` is a k-nearest-neighbour rule with k = 2 at p = 0.99 for n from 7 to 10000, not the Erdős-Rényi rule its name suggests; the Erdős-Rényi code in sweepga is not compiled (verifier).

L3. Transitive error accumulation.
Each hop clips to the frontier interval and projects a hull that includes insertions and mismatches, so boundary error and over-reach compound with depth (section 1.4).
One wrong alignment to a paralog brings that paralog's homologs in at the next hop; the yeast235 syng partition has a 574-member, 118-contig repeat partition (campaign-record-2026-10-diploid-arc.md:922), and a human chr20 infer run produced partitions anchored on CHM13 chr14, outside the queried region (notes/bug-infer-mosaic-path-span.md:21).
The defaults hide this by truncation (`-m 2`, 101 bp, 10 bp snapping), which also breaks Proposition 1.
The identity filter acts per hop and is never composed along a path, and the BED strand is per hop (section 1.5).
No measurement in the repository relates error or closure size to depth.

L4. No global node identity.
The implicit model has positions and alignments, not nodes, so every local graph numbers its own nodes, lace renumbers them (src/commands/lace.rs:915-932), and genotype evidence keyed to node ids needs translation tables (render bundle, src/render_bundle.rs:39-46).
Partitioned VCF is called on the whole laced graph, not per partition (verifier), and per-partition VCFs are laced without position sorting or BGZF (verifier).
syng gives node ids, but only the raw unmasked view keeps them (opportunity 13).

L5. Reverse complements in syng.
A 20 kb sequence and its reverse complement share 34 of 715 nodes and `query` never reports the reverse copy (notes/log.md:7-11).
impg's hasher window is w = 55 s-mers while upstream syng.c uses w + 1 (src/syng.rs:2363; vendor/syng/syng.c:416), and `.spos` checkpoints exist only for forward paths, so reverse-path occurrences are walked and dropped (src/syng.rs:2684-2720, 4473-4557).
The read matcher works around it by trying both orientations of each read (src/syng.rs:2123-2165).
A fix changes the dictionary and requires rebuilding every index, including the HPRCv2 index behind the C4 and genotyping receipts.

L6. Projection closure is not the graph.
The closure works on intervals and over-approximates the base-level classes of G(A) (Proposition 1), there is no smoothing or normalization in the implicit object, and local graphs are re-aligned from the extracted intervals, so two neighbouring local graphs need not agree at their seam.
Self-alignments are reported but not expanded, so intra-contig duplications propagate one hop only.

L7. Scale limits in the code.
Coordinates are i32, so a sequence longer than 2,147,483,647 bp wraps without an error, and one CIGAR op holds at most 536,870,911 bp (src/impg.rs:91, 108, 164-174).
A narrow query loads a whole chromosome tree, and a whole chr1 query did not finish in 10 minutes (notes/IMPG_MEMORY_PROFILING_REPORT.md:212).
The index does not store its alignment file list or build direction, so a combined index can be paired with files in another order (core map G5, plausible, not run).

L8. Silent loss on the tracepoint path.
Tracepoint hits that cannot be fetched or projected are dropped with a debug log only (src/impg.rs:1230-1460), and two TPA record types plausibly panic (src/impg.rs:832).

L9. Parameters that do nothing on syng.
The syng wrapper ignores masks, depth, length, identity and subset (section 1.8), `--syng-min-chain-fraction` is ignored unless `--syng-min-chain-anchors` is above 0 (src/main.rs:6566-6573), and multi-hop syng has no test.

## 5. History: two facts checked and how the paper should position the concept

### 5.1 PGGB peer review file (MOESM3)

Checked here in /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase1/dl_pggb/MOESM3.txt.
Reviewer 1 asked in round 2 why random sparsification and not "a spanning tree algorithm or other algorithm that can provide stronger guarantees of the edges that are kept" (MOESM3.txt:387-389).
The authors answered that a tree would bias analyses of incomplete lineage sorting, that random sampling needs much more alignment than a spanning tree for strong connectivity guarantees, and that they "reserve this study for future work, possibly focused on implicit pangenome graphs: https://github.com/pangenome/impg" (MOESM3.txt:976-982).
The answer sits between the second decision letter of 15 Apr 2024 (MOESM3.txt:244) and the acceptance in principle of 22 May 2024 (MOESM3.txt:408), so it was written in that window; PGGB was published on 2024-10-21.
The published Supplementary H says only that "neighbor joining trees over sequence similarity metrics in conjunction with randomly sampled alignments" may improve sparsification and does not name impg (MOESM1.txt:1185-1188).
The phase-1 report is correct; its line range 973-982 covers the repeated question and the answer.

### 5.2 Yoo et al. 2025, Nature 641:401-418

Checked here in the main text (PMC12058530 BioC copy in phase1/ft) and in the Supplementary Information PDF (21,063,540 bytes, CC BY 4.0, downloaded from static-content.springer.com to /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase2/yoo/dl/MOESM1.pdf, text at /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase2/yoo/MOESM1.txt).
Dates on the article page: received 2024-07-31, accepted 2025-02-19, published online 2025-04-09, issue 2025-05.
The main text says the authors "applied pangenome graph builder to construct all-to-all pairwise alignments for all 12 nonhuman primate (NHP) haplotypes (of 6 species) along with 3 T2T human haplotypes", then "used these pairwise alignment data to construct an implicit graph (Supplementary Note III, 'Implicit pangenome graph') of all six species" to compute phastCons conservation.
Supplementary Note III ("Genome alignment and sequence divergence", contributing authors include Andrea Guarracino, Bryce Kille and Erik Garrison) has a subsection "Implicit pangenome graph (impg)" (MOESM1.txt:648) that argues that alignments imply a graph, describes impg as an implicit pangenome graph built on base-level alignments between all pairs of haplotypes, and lists graph subsets, pseudo-MAF, divergence and conservation as its products (MOESM1.txt:649-678).
It states that the matching "is transitive and exactly equivalent to what would be obtained from subset operations on a full graph build" (MOESM1.txt:669-670), with no measurement in that subsection.
It describes impg as using coitrees "(implicit interval trees)" and converting CIGAR strings "to a compact delta encoding" (MOESM1.txt:686-688), which matches the 2024 README (commit 26bb7b6) and not HEAD, where records hold file offsets.
The 8p23.1 extraction ran `impg -p primates16.20231205.paf.gz -t 64 -r grch38#1#chr8:5748405-13676927 -x` on the all-vs-all set (MOESM1.txt:717), while the MHC extraction ran `impg -p .../chm13#1.aln.paf -q chm13#1#chr6:28385000-33300000` without `-x` on alignments to CHM13 only (MOESM1.txt:739-740); both regions were then built into local graphs with PGGB and drawn with odgi (MOESM1.txt:725-751).
The impg version is not stated (I searched the supplement text for "impg" and "version"; the only version string near it is `wfmash-v0.12.5` in a path).
Supplementary Fig. III.9 calls the alignment "16-way" (all T2T apes, CHM13, GRCh38 and HG002), while the main text counts 12 plus 3 haplotypes, so the supplement adds GRCh38 (MOESM1.txt:758-760).
The phase-1 related-work report is correct on the main-text phrase, the 12 plus 3 haplotypes and the code link `https://github.com/T2T-apes/ape_pangenome`; the evidence inventory's statement that the PMC XML has no "impg" string holds for the main text only, because the supplement names impg on 14 lines of my text copy.

### 5.3 Timeline from the sources

2023: seqwish formalizes alignments as match sets, the variation graph as the transitive closure of matches, and the alignment set as an "implicit interval tree"; its Discussion expects giant components to allow sparsified alignment (Garrison and Guarracino 2023, Bioinformatics 39:btac743, PMC9805579).
2024-02-09: first impg commit (54221f3, Erik Garrison); 2024-02-27: the README is titled "impg: implicit pangenome graph" and already describes transitive closure with `-x` (commit 26bb7b6, checked here with `git show`).
2024-04-15 to 2024-05-22: the PGGB rebuttal names implicit pangenome graphs and impg as the home of tree-plus-random sparsification (section 5.1).
2024-07-31 received, 2025-04-09 published: Yoo et al. give the first peer-reviewed description of impg and of an implicit pangenome graph, in Supplementary Note III (section 5.2); the related-work search found no earlier use of the phrase (PubMed, Europe PMC full text and a Crossref query, related-work section 4.2).
2024 (Bioinformatics 40:btae609): nf-core/pangenome names "The IMplicit Pangenome Graph (IMPG)" as the way to cut whole-genome alignments into pieces, build a graph per piece and lace them with gfalace (PMC11568064 Discussion).
2025 and 2026: external uses of impg v0.2.0 and v0.2.1 for region extraction (Varki et al. 2025 Genome Research; Sorin et al. 2025 and 2026 Genet Sel Evol).
2026-09-08: COSIGT (Genome Biology 27:286) calls its workflow "an implicit pangenomics approach using impg, which treats whole-genome alignments generated by minimap2 as a queryable implicit graph" (cosigt.txt:45).
2026: HPRC release 2 ships "IMPG (implicit pangenome), which represents the pangenome as a set of assembly-vs-assembly alignments that can be projected and queried on the fly", with 466 TPA files (hpp_readme.md:151, 183).
2026-07-08: Shredtools benchmarks impg v0.4.0 and describes it as a general framework over different notions of homology (Shredtools paper.txt:284-312, 528-532).

### 5.4 Positioning recommendations

1. Present seqwish's match-closure model as the formal parent and define the implicit pangenome graph as G(A) left uncomputed (section 1.2), so that the paper's novelty is query-time evaluation of the closure and on-demand induction, not the observation that alignments imply a graph, which seqwish already made.
2. Cite the PGGB rebuttal and Yoo et al. 2025 as the first public naming and the first peer-reviewed application by the same group, and state that they used a 2024 version of impg with a different internal representation and CLI (`-p`, `-q`), so the HEAD paper describes a later design.
3. Do not repeat the "exactly equivalent" sentence of Yoo et al. 2025; state Propositions 1 and 2 with their conditions and report opportunity 2 as the test, including how far the defaults and the current re-alignment path are from equality.
4. Keep "implicit pangenome graph" for the object and attribute "implicit pangenomics" to COSIGT as the name of the workflow built on it.
5. Credit HAL and halLiftover (Hickey et al. 2013) and chain liftover (Kent et al. 2003) as earlier ways to query a multi-genome alignment from any genome, and state the difference with numbers: impg needs only pairwise alignments, no multiple alignment or guide tree, and computes multi-hop closures and local graphs on request.
6. Place Shredtools (multi-MUM waypoints), PGR-TK (SHIMMER fetch) and syng (syncmer GBWT) as other homology sources for the same kind of query, and present the two-source interface of section 1.8 as the general form, with its current leaks.
7. Say plainly that "implicit" refers to the graph; the 2024 README and Yoo et al. 2025 call coitrees "implicit interval trees", but coitrees are cache-oblivious interval trees, while the "implicit interval tree" of Li and Rong (bedtk), cited as reference 15 in the Yoo supplement, is a different structure.
8. If the paper uses the computer-science sense of an implicit graph (a graph given by a rule that lists the neighbours of a vertex on demand), it needs a citation that I did not find or verify.

## 6. Resource notes for the experiments

On disk at /home/guarracino/git/impg/data/hprcv2: the 465-haplotype vs GRCh38 PAF.gz (6,342,372,371 bytes) with `.gzi` and an `IMPGIDX2` index (814,414,241 bytes), the GRCh38 all-vs-1 PAF.gz (6,532,446,867 bytes, the same file as the S3 GRCh38 all-vs-1 entry by size), the GRCh38 TPA (560,062,985 bytes) whose `.impg` has magic `IMPGIDX3` and must be rebuilt, and the HPRC r2 AGC (3,295,070,733 bytes).
On S3 (checked here): 466 TPA files, 25,070,431,026 bytes in total, from 33,955,770 to 560,062,985 bytes each with median 51,404,490; 466 all-vs-1 PAF.gz files, 318,372,159,094 bytes in total, from 422,479,077 to 6,532,446,867 bytes each with median 655,074,392.
The 309,962,462,020-byte all-vs-all PAF.gz does not fit the local 40 GB disk; the TPA set fits only without its indexes.
The HPRCv2 syng index and every C4, genotyping and projection receipt live on another machine (/home/erikg), so syng experiments at human scale start with an index build whose time is unknown.
The release binary at target/release/impg was rebuilt after the HEAD commit (mtime 2026-11-08 21:15:35 -0700 per the verifier), and a worktree on branch fix/spanning-candidate-copies exists, so every experiment should record `impg --version`, the commit and the binary hash.
The S3 listings I used are at /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase2/s3mine/tpas.1.xml and /tmp/claude-1000/-home-guarracino-git-impg-paper/ed3cfa77-35b3-454f-91de-3d0a63c6ad53/scratchpad/phase2/s3mine/pafs_all-vs-1.1.xml; the directory phase2/s3 holds files of another agent that I did not touch.

## 7. Sources read

Phase-1 inputs: FACTS_CHECKED_BY_ORCHESTRATOR.md, VERIFY_CORRECTIONS.md, core-index-projection.md, partition-regional.md, graph-construction.md, syng-alignment-free.md, evidence-inventory.md (all), related-work.md (lines 1-200), pggb-nature-methods.md (all), phase1_research_digest.txt (lines 1-80), genotyping-infer.md and genome-inference.md (summaries and opportunity headings).
Primary texts: dl_pggb/MOESM3.txt (lines 1-30, 240-410, 915-990), dl_pggb/MOESM1.txt (lines 1175-1192), ft/PMC12058530.bioc.json (passages matching implicit, impg, PGGB), the Yoo et al. 2025 Supplementary Information (lines 600-790 of my text copy), ft/PMC9805579.bioc.json (definition and induction passages), ft/PMC11568064.txt (Discussion), ft/cosigt.txt (line 45), web/hpp_readme.md (lines 149-191).
impg code at 0987752: src/impg.rs (160-212, 243-300, 1680-1740, 2379-2628, 2791-2935), src/main.rs (4253-4265, 12055-12100, 12311-12345), src/lib.rs (235-250, 515-607, 926-952), src/impg_index.rs (17-121), src/syng.rs (2358-2365), vendor/syng/syncmerset.c (55-62), vendor/syng/syng.c (410-418), tests/test_transitive_integrity.rs (test list, 156-226, 298-348), notes/log.md and notes/tasks.md (whole files, mtimes 21:05 and 21:37 -0700), README.md (1-40), `git log` and `git show 26bb7b6:README.md`, and `--help` of graph, query and align.
Shredtools line numbers refer to /home/guarracino/git/impg-paper/references/biorxiv-2026-07-03-736354/paper.txt as cited by the phase-1 reports; I did not reopen it.
ODGI benchmark numbers come from the phase-1 digest, which cites references/odgi-paper/manuscript/table_extract.tex and table_build.tex in the paper repository.
Not read: the full related-work.md beyond line 200, the full genotyping and genome-inference maps, odgi-shredtools.md and citation_table.md (I used the digest and related-work for their facts).

## To decide

Whether the paper states Propositions 1 and 2 as its formal core, which commits it to running opportunity 2 before submission.
Whether to fix the self-hit expansion and the BED strand composition in impg before any closure experiment, since both change results (sections 1.5 and 1.6).
Whether experiments use the released HPRC r2 per-target files (no new alignment, PAF on gemini or TPA locally) or new alignments made with `impg align`.

## Changed

Nothing in either repository; I wrote this report, downloaded the Yoo et al. 2025 supplement to phase2/yoo, and saved two S3 listings to phase2/s3mine.

## Found

The local graph engines re-align extracted intervals instead of using the stored alignments (src/main.rs:12326-12339), self-hits are never expanded (src/impg.rs:2575), and the BED strand is not composed across hops (src/impg.rs:282-286 with src/main.rs:12074-12078), all derived from code and not run.
The HPRC r2 TPA set is 25,070,431,026 bytes in 466 files, 12.70 times smaller than the 466 all-vs-1 PAF.gz files, and TPA plus AGC is smaller than the PGGB GBZ (28,365,501,759 against 33,768,296,600 bytes, my sum).
The Yoo et al. 2025 supplement names impg in a subsection titled "Implicit pangenome graph (impg)" and claims exact equivalence with full-graph subsetting without a measurement.
