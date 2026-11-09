# Experiment plan for the impg Bioinformatics draft

Written 2026-11-09 (session clock) from supporting/plan.md sections 2 and 7 to 13, with every command and flag checked against the code and the tool help in this step.
Code is /home/guarracino/git/impg at HEAD 0987752 (`git describe` v0.5.0-656-g0987752, `impg 0.5.0`). I read it and ran only `--help` and `--version`.
The live binary (mtime 2026-11-08 22:10:17 -0700) prints help for index, query, refine, align, partition, stats and graph that is byte-identical to phase2/plan_help_*.txt (`cmp`, 2026-11-09).
External flags come from the local help of seqwish v0.7.11-35-gaab5bee, vg v1.76.1 (`vg chunk --help`), bedtools v2.31.1 (`bedtools random -h`) and odgi v0.9.4-82-g34c461ff, saved in the scratchpad at phase3/exthelp/. No wfmash help is saved there, and no command below calls wfmash directly.
Shredtools, Mumemto, liftOver, paf2chain, halLiftover, gbz-base and panacus are not installed (`command -v`, 2026-11-09), so their commands are not written.
The command blocks below are copied by script from Supplementary Table S1 (sections/08b.supplement-experiments.tex), which is the canonical copy.
Paths without a leading slash are relative to /home/guarracino/git/impg unless they start with phase1/, phase2/ or phase3/ (the session scratchpad) or with sections/, supporting/ or data/ (the draft folder). The exception is data/hprcv2, which is /home/guarracino/git/impg/data/hprcv2.
Status labels follow plan.md: NOW, CODE, EXP, WIP.

## 0. Corrections to plan.md found by checking commands

| # | plan.md text | What the code or tool does | Fix used here | Evidence |
| --- | --- | --- | --- | --- |
| 1 | E1, E2, E3b build bedtools genome files from `impg stats --list-sequences` with awk filters | `print_list_sequences` prints a header line `Sequence<TAB>Length` first. The E2 filter `$1 !~ /^(GRCh38|CHM13)#/` keeps that line, so `bedtools random` reads a non-numeric length | `NR>1` in every awk filter | src/main.rs:13267-13277 |
| 2 | `while read c b e n` over `bedtools random` output | bedtools random writes 6 columns (name, score, strand), so `n` receives 3 fields and the output names break | `while read -r c b e n rest` | `bedtools random -l 10 -n 2 -seed 1` with bedtools v2.31.1 prints rows such as `c1 528 538 1 10 -`. `bedtools random -h` does not list the output columns |
| 3 | E2 and E8 `vg chunk -p "$c:$b-$e"` with BED coordinates | `vg chunk -p` takes a 0-based inclusive range | `-p "$c:$b-$((e-1))"` | `vg chunk --help` (v1.76.1): "0-based inclusive" |
| 4 | E6 uses tests/test_data/yeast.chrV.fa.gz directly for `--sequence-files` and `seqwish -s` | The file is plain gzip ("gzip compressed data, was yeast.chrV.fa"), not BGZF, and has no `.fai`, `-o gfa` needs random access | Decompress to yeast.chrV.fa and run `samtools faidx` first | `file`, `ls tests/test_data/` |
| 5 | E4 and E5 `subset_pairs.py --jobs jobs_auto` | `impg align --format joblist -o DIR` writes DIR/align_jobs.txt, `--format paf -o DIR` writes DIR/alignments.paf | `--jobs jobs_auto/align_jobs.txt` | src/commands/align.rs:521, 737 |
| 6 | E5 reads the `auto` pair count from the log to test Shredtools' "17%, the default auto setting" | Selection groups FASTA records by PanSN haplotype and applies the rule to haplotypes (10 or fewer: all pairs, 50 or fewer: `giant:0.99`, above 50: `tree:5:2:0.05`). It expands each selected haplotype pair to record pairs and adds every within-haplotype record pair. If every haplotype has exactly one record, sweepga skips the grouping and applies the rule to records (sweepga 4713ce0 src/knn_graph.rs:644, 673). The log line "Selected N pairs out of M total" counts record pairs, so its percentage is not the haplotype-pair fraction. The wfmash joblist has one line per selected haplotype pair plus one self line per haplotype that has at least 2 records | Count haplotype pairs as joblist lines whose two haplotypes differ. Report the logged record count beside it | src/commands/align.rs:147-179, 253-322, 715-730, sweepga 4713ce0 src/knn_graph.rs:514-532, 589-618, 636-677 |
| 7 | E4 and E5 "all pairs" PAF | sweepga adds within-haplotype record pairs whenever PanSN grouping applies and a haplotype has 2 or more records, and `collect_file_pairs` then keeps (f, f), so every PAF from `impg align`, sparsified or not, holds within-haplotype alignments between contigs | `subset_pairs.py` keeps within-haplotype records in every subset, as `impg align` does, so only between-haplotype pairs vary | sweepga 4713ce0 src/knn_graph.rs:606-614, src/commands/align.rs:377-395, 440 |
| 8 | E2 downloads TPA files into a folder and indexes them | The tpa crate rebuilds a missing `.tpa.idx` next to each TPA file | TPA folder must be writable. Add the sidecars to the disk estimate (40,256,530 bytes for the GRCh38 file on disk) | tpa f21b012 src/lib.rs:1148, `ls -la data/hprcv2` |
| 9 | E6 C4 holdout queries the extracted FASTA | `-r` splits on the last `:`, `-o fasta` names sequences `NAME:START-END`, so a bare name with `:` is parsed as a range | Pass an explicit range, e.g. `-r 'GRCh38#0#chr6:31891045-32123783:0-232738'` | src/commands/partition.rs:1783-1795, src/main.rs:7446-7466 |
| 10 | E1 TPA arm runs with `-v 2` to log dropped hits | Dropped hits are `debug!` lines, one per hit, written to the same stderr as `/usr/bin/time -v` | Use the counted warning of C2 at `-v 1` | src/impg.rs:1230-1236, 1247-1254 |
| 11 | E1b queries the unidirectional index without `--unidirectional` | The index header does not record the build direction | Pass `--unidirectional` at query time as well (C4 adds the check) | supporting/plan.md C4, impg query --help |
| 12 | E2 and E5 name "Shredtools v0.1.0" | The preprint prints no Shredtools version. It gives github.com/vikshiv/shredtools and Mumemto v1.4.0 | Pin a Shredtools commit at install | references/biorxiv-2026-07-03-736354/paper.txt:637-643 |
| 13 | E2 latency runs at `-t 1` with `IMPG_AGC_DECOMPRESSOR_SLOTS` set | Slots are capped by the thread count, so `-t 1` gives 1 slot | Record the effective slot count per run | src/agc_index.rs:61-82 |
| 14 | E5 "the gene BED on CHM13 chr19 from the same annotation" | The CAT folder holds 178 GFF3 files plus one transfer manifest, 89 named `*.chm13.gff3.gz` and 89 `*.hg38.gff3.gz` (CHM13 plus 88 haplotypes of 44 samples per run). The CHM13 run is 8,452,176,760 bytes | Query genes from CHM13.chm13.gff3.gz. Truth from the other 88 `*.chm13.gff3.gz` files | `aws s3 ls --no-sign-request --recursive` of the CAT folder, 2026-11-09 |
| 15 | Fig. 3d thread sweep "1 to 48" while E2 runs threads 1, 4, 16 | Inconsistent | E2 batch arm runs 1, 4, 16 and 48 | supporting/plan.md section 6 Fig. 3 and E2 |
| 16 | U1 "HPRC r2 MC GBZ file name and size not checked" | Listed on 2026-11-09 | See U1 | `aws s3 ls --no-sign-request` of release2/minigraph-cactus/v2.1/ |
| 17 | E9 parameters copied from the syng-backed yeast235 run | That run also used `--no-rehome-singletons`, `--syng-min-chain-anchors 5` and `--syng-min-chain-fraction 0.5`. The plan keeps default rehoming | Keep default rehoming and say so. The syng flags do not apply to alignments | VERIFY_CORRECTIONS.md:72 |
| 18 | E2 compute: "33,877,515,253 bytes for GBZ v3 and bumbl" | 6,398,170,680 + 27,478,774,573 = 33,876,945,253 | Corrected sum | python3 arithmetic, 2026-11-09 |

Checked and confirmed without change.
- `-i` forces single mode (src/main.rs:11277-11291).
- `--approximate` refuses any input that is not `.1aln` or `.tpa` (src/main.rs:7393-7408), and it warns when `-x` runs without `--min-transitive-len` (src/main.rs:10581-10595).
- `--min-transitive-len` has an effective default of 101 and compares with `>=`, so 0 and 1 both keep every hop (src/main.rs:4253-4255, src/impg.rs:2585).
- The subset list removes sequences before they join the next frontier, so it removes them as bridges too, and it always keeps the query target (src/impg.rs:2496-2505).
- Self-hits are written and not expanded (src/impg.rs:2574-2589).
- `impg partition` has no `-x`, and its `-d` is required (impg partition --help).
- `impg refine` writes an 8-column table to stdout (src/main.rs:7964-7981).
- The local PAF.gz files are BGZF (gzip header with the `BC` extra field).

## 1. Common setup

### 1.1 Variables

The shared variables are the first lines of the Table S1 block.

```bash
# bash. IMPG is the tagged build: record sha256sum $IMPG and $IMPG --version
IMPG=/path/to/impg-TAG/target/release/impg
D=/home/guarracino/git/impg/data/hprcv2
P38=$D/GCA_000001405.15_GRCh38_no_alt_analysis_set.PanSN.merged.paf.gz
T38=$D/GCA_000001405.15_GRCh38_no_alt_analysis_set.PanSN.merged.edit-distance.128.tpa
AGC=$D/HPRC_r2_assemblies_0.6.1.agc
X=/home/guarracino/git/impg-paper/experiments            # workstation scratch
S=/scratch/aguarracino/impg-paper                        # cluster scratch
R2=s3://human-pangenomics/pangenomes/freeze/release2
T='/usr/bin/time -v'
export IMPG_AGC_DECOMPRESSOR_SLOTS=2       # workstation: slots x 3.70 GB must fit free RAM
```

### 1.2 Rules for every run

- One tagged impg build, never the target/release binary that other work rebuilds. Record `sha256sum $IMPG`, `$IMPG --version`, the commit, the host, the threads and the `/usr/bin/time -v` output next to each result (C1, D6).
- The build copies wfmash with its WFA2 shared libraries, and FastGA, FAtoGDB, GIXmake, GIXrm, ALNtoPAF, PAFtoALN and ONEview next to impg (build.rs:20-31, VERIFY_CORRECTIONS.md:107). Cargo also builds the gfaffix binary (Cargo.toml:9-11). Hash them all.
- Single-index mode for every benchmark: always pass `-i` (src/main.rs:11277-11291), and pass the same list file to index and query (C4).
- Fixed seeds for every region and pair set: E1 1, E2 2, E3a 3, E3b 4, E4 5, E5 6, E6 loci 7, E6 C4 haplotypes 8, E7 9, E8 10, pair subsets 1.
- `bedtools random -n 1200`: first 1,000 lines tune, last 200 are held out, sort after the split.
- Held-out sets (the 200-region sets, ScRAP 142, the C4 holdout) never choose `-d`, `-m`, `--min-transitive-len`, `--min-distance-between-ranges` or subset fractions. Report tuning and holdout side by side. The E2 and E3a command blocks below query only tuning regions (`head -n 1000`, `g38.1k.bed`), so each needs a run on its held-out lines. The E3b block queries all of q10.bed in one run, so its scoring must split off the last 20 regions per Q_i.
- Workstation scratch in /home/guarracino/git/impg-paper/experiments/<name>/ (folder does not exist yet, 42,256,977,920 bytes free on `/` on 2026-11-09), never `/tmp`. Cluster scratch /scratch/aguarracino/impg-paper/<name>/.
- `IMPG_AGC_DECOMPRESSOR_SLOTS` so that slots x 3.70 GB fits free RAM (code comment at src/agc_index.rs:87-100), 2 slots on the workstation (17,134,936,064 bytes available on 2026-11-09, 15,510,704,128 on 2026-11-08). Slots never exceed `-t` (src/agc_index.rs:67-82).
- Only flags printed by `<tool> --help` are used. Scripts run under bash (process substitution, `$T` word splitting).
- Warm cache by default. Cold cache only where the cluster lets jobs drop the page cache (Q6).
- 5 replicates per query measurement, 3 per workstation build. Cluster build replicates are an author decision (Note S5).
- Pass targets are fixed by the authors before any run (D2). The values below marked "proposed" come from plan.md section 2.

### 1.3 Harness (code fix C14)

None of these scripts exists yet. Each needs verbose diagnostics, a non-zero exit on any parse failure and a toy-data test with a known answer before use.

| Script | Purpose | Toy test |
| --- | --- | --- |
| `bp_metrics.py` | modes `identity` (sorted-row identity of two BEDPE files), `delta` (boundary shifts), `recall` (bp recall, precision, exact-boundary rates against a truth BEDPE), `genes` (containment, flank excess, wrong locus, copies against CAT), `jaccard` (per region and haplotype bp Jaccard by stratum) | hand-written BEDPE pairs with known overlaps |
| `subset_pairs.py` | modes `random` (exact fraction of between-haplotype pairs, fixed seed), `joblist` (keep haplotype pairs listed in align_jobs.txt), `star` (keep pairs with the hub). Keeps within-haplotype records in every mode, as `impg align` does | 4-haplotype PAF with every pair |
| `compare_classes.py` | for every base of closure C, the node class in the global and the local GFA. Counts bases whose class set differs | 3 sequences where the answer is known, one with a cut match run shorter than k |
| `exact_once_audit.py` | per base of every FASTA record, the number of partitions that own it. Uncovered and multiply owned bp. Partitions spanning more than one S288C chromosome | 2 sequences and 3 hand-made partitions |
| `chunk_paths_to_bed.py` | path intervals of each vg chunk GFA as BED | toy GFA with 2 paths |
| `locus_depth.py` | records per haplotype and maximum per-base record depth inside a locus (generalizes phase2/judge/c4_depth.py) | 3 overlapping records |
| `split_by_haplotype.py` | one bgzipped, faidx-indexed FASTA per PanSN haplotype | 2 haplotypes x 2 contigs |
| `cat_to_bed.py` (new) | CAT GFF3 genes to BED on graph path names through a seqid map | 2 genes, 1 renamed contig |
| `pick_pairs.py` (new, extends data/pairs.py) | reciprocal pairs for E1b and non-reciprocal Q_i, P_i pairs for E3b from the TPA string tables | the pairs_out.txt counts (2,966 ordered pairs in both files) |

## 2. Order of work and gates

1. Code gate on the workstation: C1 to C8 and C14. Then E1 and E1b.
2. If E1 fails, stop and take D1.
3. Workstation, in parallel with cluster setup: E6, E7, E3a.
4. Send Q1 to Q6 before cluster work and name the node (D5).
5. Cluster: E2, then E3b, E8 and E10 on the E2 index.
6. Cluster and workstation: E5 (needs Shredtools, CAT), then E4 (tuning on E5 alignments, holdout ScRAP 142), then E9.
7. Compare F1 to F5 with the targets fixed in step 1. If all pass, run U1 to U3 and take D14. Otherwise write the Bioinformatics paper from Tier 1.
8. Preprint when E2 and E3 have numbers, if the authors choose (D11).

## 3. Tier 1 experiments

### E1. Tracepoint projection against PAF projection (workstation, gate for every TPA number)

- Question. Does exact TPA projection return the same rows as PAF projection of the same alignments, how many tracepoint hits does it drop, and what does `--approximate` change?
- Data. GRCh38 star on disk: TPA 560,062,985 bytes, PAF.gz 6,532,446,867 bytes (BGZF), both 8,916,633 records. AGC 3,295,070,733 bytes, 1,000 random 10 kb GRCh38 regions plus 200 held out (seed 1). E1b: two assembly TPA files that list each other (one of the 1,483 reciprocal unordered pairs, picked with `pick_pairs.py`), median 51,382,206 bytes each over the 464 assembly files (51,401,828 bytes is the median over all 466 files, including GRCh38 and CHM13), from `s3://human-pangenomics/pangenomes/freeze/release2/impg/tpas/`.
- Compared. impg PAF exact, impg TPA exact, impg TPA `--approximate`, at `-m` 1, 2 and 0, E1b bidirectional against `--unidirectional`.
- Metrics. Identical sorted BEDPE rows (%), rows in one output only, largest start and end shift (bp), dropped tracepoint hits (after C2), index bytes, wall time, peak RSS. For approximate mode, the shift distribution and per-query time, E1b index entries against 2 x records and merged BED identity.
- Pass target (proposed, F1). 100% identical sorted rows at `-m 1` on the tuning and held-out sets, and 0 dropped hits, `-m 2` and `-m 0` reported. E1b: to fix (D2).
- Commands.

```bash
# E1. TPA projection against PAF projection (workstation)
mkdir -p $X/e1 && cd $X/e1
$T $IMPG index -a $P38 -i paf.impg -f -t 16 2> paf.index.time
$T $IMPG index -a $T38 -i tpa.impg -f -t 16 2> tpa.index.time
$IMPG stats -a $P38 -i paf.impg --list-sequences > g38.seqs.tsv
awk -F'\t' 'NR>1 && $1 ~ /^GRCh38#0#chr[0-9XY]+$/ {print $1"\t"$2}' g38.seqs.tsv > g38.genome
bedtools random -l 10000 -n 1200 -seed 1 -g g38.genome > r1200.bed
head -n 1000 r1200.bed | sort -k1,1 -k2,2n > tune.bed
tail -n 200 r1200.bed | sort -k1,1 -k2,2n > hold.bed
for b in tune hold; do for m in 1 2 0; do
  $T $IMPG query -a $P38 -i paf.impg -b $b.bed --no-merge -x -m $m -o bedpe \
    -O paf.$b.m$m -t 16 2> paf.$b.m$m.time
  $T $IMPG query -a $T38 -i tpa.impg -b $b.bed --no-merge -x -m $m --sequence-files $AGC \
    -o bedpe -O tpa.$b.m$m -t 16 2> tpa.$b.m$m.time
  $T $IMPG query -a $T38 -i tpa.impg -b $b.bed --no-merge -x -m $m --approximate \
    -o bedpe -O apx.$b.m$m -t 16 2> apx.$b.m$m.time
  python3 -I bp_metrics.py --mode identity paf.$b.m$m.bedpe tpa.$b.m$m.bedpe > id.$b.m$m.tsv
  python3 -I bp_metrics.py --mode delta tpa.$b.m$m.bedpe apx.$b.m$m.bedpe > apx.$b.m$m.tsv
done; done
# E1b. A.tpa and B.tpa list each other (picked with pick_pairs.py)
# ab.bed: bedtools random -l 10000 -n 100 -seed 1 on the sequences of A
$IMPG index -a A.tpa B.tpa -i ab.bi.impg -f -t 16
$IMPG index -a A.tpa B.tpa -i ab.uni.impg -f --unidirectional -t 16
$IMPG query -a A.tpa B.tpa -i ab.bi.impg -b ab.bed -d 0 -x -m 2 --sequence-files $AGC \
  -o bed -O ab.bi -t 16
$IMPG query -a A.tpa B.tpa -i ab.uni.impg --unidirectional -b ab.bed -d 0 -x -m 2 \
  --sequence-files $AGC -o bed -O ab.uni -t 16
```

- Compute and disk. Workstation, 0 bytes to download for E1, 2 TPA files for E1b. Two indexes (older indexes on disk are 757,392,357 bytes for `.impgv3` and 810,892,155 bytes for the IMPGIDX3 `.impg` that HEAD rejects). Wall time unknown.
- Blockers. C1 (tag), C2 (fixtures, dropped-hit counter), C4 (file list binding), C5 (not hit here, the index is written first), `--min-result-identity` stays unset (C2).
- Feeds. Supplementary Fig. S2, Results 5.1 (sections/05.results.tex, `sec:res-tpa`), F1.

### E2. Index and query the whole release (cluster)

- Question. Can impg index all 389,234,668 released alignments on one node in single mode, and what does a regional query cost against the released graph and the released Shredtools index?
- Data. `s3://human-pangenomics/pangenomes/freeze/release2/impg/tpas/` (466 files, 25,070,431,026 bytes, all Standard tracepoints, edit distance, max complexity 128). AGC 3,295,070,733 bytes copied from the workstation. GBZ v3 `.../release2/pggb/gfas/whole-genome/20250930_hprc25272.p98-k311.tmp.fix.v3.gbz` (6,398,170,680 bytes). Shredtools `s3://genome-idx/mumemto/hprc/hprcv2_merged.bumbl` (27,424,443,909 bytes) and `.bumbl.bi` (54,330,664 bytes), regions: 1,200 per size class (1 kb, 10 kb, 100 kb, 1 Mb) on non-reference haplotypes and 1,200 GRCh38 10 kb regions (seed 2, last 200 held out). One whole-chromosome query (CHM13#0#chr1).
- Compared. impg exact and `--approximate`, vg v1.76.1 `chunk` on GBZ v3, Shredtools extract (commit to pin) on hprcv2_merged.bumbl, gbz-base on the `.gbz.db` (61,240,860,672 bytes) only as U10.
- Metrics. Build wall time, CPU time, peak RSS, index bytes. Per query median and p95 wall time and peak RSS, 5 replicates for impg (the vg loop below runs each region once and needs the same 5 replicates), warm cache. Batch throughput with `-b` at 1, 4, 16, 48 threads and identity of the outputs, whole-chromosome wall time and RSS, dropped-hit count. Where each competitor wins (Shredtools: remote HTTP access, index build cost when alignment is counted, vg: a graph output).
- Pass target (proposed, F2). All 466 files index in single mode on one node. The whole-chromosome query finishes. Median per-query wall time for 10 kb regions at `-x -m 2`, `-t 1`, exact, is at most the Shredtools median on the same 1,000 regions, both numbers printed. The commands must run impg, vg and Shredtools on one BED. As written, the impg per-region loop reads nr.10000.bed, and the vg loop and the Shredtools placeholder read g38.10000.bed. Batch outputs identical across threads (to fix, D2).
- Commands.

```bash
# E2. Index and query the whole release (cluster)
mkdir -p $S/e2/tpas $S/e2/q $S/e2/vg && cd $S/e2
aws s3 cp --no-sign-request --recursive $R2/impg/tpas/ tpas/
ls $PWD/tpas/*.tpa | sort > tpa466.list && sha256sum tpas/*.tpa > tpa466.sha256
$T $IMPG index --alignment-list tpa466.list -i r2.impg -t 32 2> r2.index.time
$IMPG stats --alignment-list tpa466.list -i r2.impg > r2.stats
$IMPG stats --alignment-list tpa466.list -i r2.impg --list-sequences > r2.seqs.tsv
awk -F'\t' 'NR>1 && $1 !~ /^(GRCh38|CHM13)#/ {print $1"\t"$2}' r2.seqs.tsv > nonref.genome
awk -F'\t' 'NR>1 && $1 ~ /^GRCh38#0#chr[0-9XY]+$/ {print $1"\t"$2}' r2.seqs.tsv > g38.genome
for L in 1000 10000 100000 1000000; do
  bedtools random -l $L -n 1200 -seed 2 -g nonref.genome > nr.$L.bed; done
bedtools random -l 10000 -n 1200 -seed 2 -g g38.genome > g38.10000.bed
for L in 1000 10000 100000 1000000; do for m in 1 2; do for rep in 1 2 3 4 5; do
  while read -r c b e n rest; do
    $T $IMPG query --alignment-list tpa466.list -i r2.impg -r "$c:$b-$e" -d 0 -x -m $m \
      --sequence-files $AGC -o bedpe -O q/ex.$L.$m.$rep.$n -t 1 2> q/ex.$L.$m.$rep.$n.time
    $T $IMPG query --alignment-list tpa466.list -i r2.impg -r "$c:$b-$e" -d 0 -x -m $m \
      --approximate -o bedpe -O q/ap.$L.$m.$rep.$n -t 1 2> q/ap.$L.$m.$rep.$n.time
  done < <(head -n 1000 nr.$L.bed)
done; done; done
head -n 1000 nr.10000.bed > nr.10000.tune.bed
for t in 1 4 16 48; do
  $T $IMPG query --alignment-list tpa466.list -i r2.impg -b nr.10000.tune.bed -d 0 -x -m 2 \
    --sequence-files $AGC -o bedpe -O batch.t$t -t $t 2> batch.t$t.time; done
$T $IMPG query --alignment-list tpa466.list -i r2.impg -r 'CHM13#0#chr1' -d 0 -o bed \
  -O chr1 -t 16 2> chr1.time
GBZ=20250930_hprc25272.p98-k311.tmp.fix.v3.gbz
aws s3 cp --no-sign-request $R2/pggb/gfas/whole-genome/$GBZ .
while read -r c b e n rest; do                     # vg chunk -p is 0-based inclusive
  $T vg chunk -x $GBZ -p "$c:$b-$((e-1))" -c 0 -O gfa -t 1 > vg/$n.gfa 2> vg/$n.time
done < <(head -n 1000 g38.10000.bed)
aws s3 cp --no-sign-request s3://genome-idx/mumemto/hprc/hprcv2_merged.bumbl .
aws s3 cp --no-sign-request s3://genome-idx/mumemto/hprc/hprcv2_merged.bumbl.bi .
# Shredtools extract on hprcv2_merged.bumbl with g38.10000.bed: not written (not installed)
```

- Compute and disk. A node with more than 59,163,669,536 bytes of RAM (build floor from field sizes, CODE inference: 389,234,668 x 56 + 778,469,336 x 48 bytes). Scratch for TPA, AGC and index of 61,427,685,951 to 63,916,842,350 bytes (three index estimates, judge-feasibility.md section 3) plus the `.tpa.idx` sidecars, plus 33,876,945,253 bytes for GBZ v3 and the Shredtools index (plan.md prints 33,877,515,253, an addition error). Downloads 25,070,431,026 + 6,398,170,680 + 27,478,774,573 bytes, 4 x 2 x 5 x 1,000 x 2 = 80,000 per-region impg processes, each paying index header load (launch overhead) in its wall time. Wall time unknown.
- Blockers. C1 to C6, C9, C14, D5 and Q6 (node). Whether vg v1.76.1 reads the v3 GBZ (help names "graph or XG index", the README says v3 needs a release of vg after an unnamed version). GBZ path names (PanSN form assumed). Shredtools and Mumemto install. Whether `--approximate` needs `--sequence-files` (check with the E1 fixtures).
- Feeds. Fig. 3, Results 5.2, abstract slots [H] [G] [T], F2.

### E3. Reach and reference dependence (E3a workstation, E3b cluster)

- Question. How much of what a query reaches depends on GRCh38 and CHM13, measured in bases, and how well does transitive projection recover a held-out direct alignment?
- Data. E3a: GRCh38 star PAF.gz on disk, the CHM13 per-target PAF.gz `.../release2/impg/pafs/all-vs-1/chm13v2.0_maskedY_rCRS.fa.PanSN.merged.paf.gz` (5,590,178,237 bytes), 1,200 random 1 kb GRCh38 regions (seed 3, 200 held out), a public GRCh38-to-CHM13 chain file (choice and provenance to record). E3b: the E2 index, 10 non-reference query haplotypes Q_i (seed 4), each with one partner P_i whose records only Q_i's file stores (non-reciprocal, 25,221 - 2,966 = 22,255 ordered pairs are stored in one file only, data/pairs_out.txt), Q_i per-target PAF.gz (10 files, 6,540,662,155 bytes at the median size of 654,066,215.5 bytes over the 464 assembly files), 100 random 10 kb regions per Q_i (last 20 held out).
- Compared. E3a: direct GRCh38-to-CHM13 projection, projection through haplotypes at `-m` 2 and 3 with the direct records removed, and the chain. E3b: direct projection Q_i to P_i on the full index against transitive projection on the held-out index, each with and without the two references as bridges.
- Metrics. bp recall and bp precision per region and target haplotype, exact-boundary rate at 0, 1, 10 and 100 bp. Haplotypes and bp reached per depth. Strand agreement after D3 only.
- Pass target (proposed, F3). E3b median per-region bp recall at `-m 2` without bridges is at least 0.95 times the recall with bridges, both printed. E3a: to fix (D2). Control: E3b at `-m 1` on the held-out index has no direct Q_i to P_i alignment.
- Commands.

```bash
# E3a. GRCh38 to CHM13 through haplotypes (workstation)
mkdir -p $X/e3a && cd $X/e3a
aws s3 cp --no-sign-request \
  $R2/impg/pafs/all-vs-1/chm13v2.0_maskedY_rCRS.fa.PanSN.merged.paf.gz chm13.paf.gz
pigz -dc $P38 | awk -F'\t' '$1 !~ /^CHM13#/' | bgzip -@ 8 > g38.noCHM13.paf.gz
pigz -dc chm13.paf.gz | awk -F'\t' '$1 !~ /^GRCh38#/' | bgzip -@ 8 > chm13.noGRCh38.paf.gz
$IMPG index -a $P38 chm13.paf.gz -i full.impg -f -t 16
$IMPG index -a g38.noCHM13.paf.gz chm13.noGRCh38.paf.gz -i held.impg -f -t 16
bedtools random -l 1000 -n 1200 -seed 3 -g ../e1/g38.genome > g38.1k.raw.bed
head -n 1000 g38.1k.raw.bed | sort -k1,1 -k2,2n > g38.1k.bed      # last 200: holdout
$IMPG query -a $P38 chm13.paf.gz -i full.impg -b g38.1k.bed -d 0 -o bedpe -O direct -t 16
for m in 2 3; do
  $IMPG query -a g38.noCHM13.paf.gz chm13.noGRCh38.paf.gz -i held.impg -b g38.1k.bed -d 0 \
    -x -m $m -o bedpe -O held.m$m -t 16; done
# chain arm: liftOver of g38.1k.bed with the public chain: not written (not installed)

# E3b. Held-out partners on the release (cluster, after E2)
mkdir -p $S/e3b && cd $S/e3b       # q10.txt: 10 SAMPLE#HAP (seed 4), Qi.paf.gz and Pi per pair
awk -F'\t' 'NR>1 && $1 !~ /^(GRCh38|CHM13)#/ {print $1}' ../e2/r2.seqs.tsv > nonref_contigs.txt
while read -r q; do
  awk -F'\t' -v q="$q#" 'NR>1 && index($1,q)==1 {print $1"\t"$2}' ../e2/r2.seqs.tsv > $q.genome
  bedtools random -l 10000 -n 100 -seed 4 -g $q.genome          # last 20 per Q_i: holdout
done < q10.txt > q10.bed
# per Q_i: drop the partner's records from the per-target PAF of Q_i
pigz -dc Qi.paf.gz | awk -F'\t' -v p="$Pi#" 'index($1,p)!=1' | bgzip -@ 8 > Qi.held.paf.gz
grep -v -F -f q10_tpa_stems.txt ../e2/tpa466.list > held.list
ls $PWD/*.held.paf.gz >> held.list                     # 456 TPA + 10 filtered PAF
$T $IMPG index --alignment-list held.list -i held.impg -f -t 32 2> held.index.time
$IMPG query --alignment-list ../e2/tpa466.list -i ../e2/r2.impg -b q10.bed -d 0 \
  --sequence-files $AGC -o bedpe -O truth.direct -t 16
for m in 1 2 3 4 0; do
  $IMPG query --alignment-list held.list -i held.impg -b q10.bed -d 0 -x -m $m \
    --sequence-files $AGC -o bedpe -O held.refs.m$m -t 16
  $IMPG query --alignment-list held.list -i held.impg -b q10.bed -d 0 -x -m $m \
    --subset-sequence-list nonref_contigs.txt --sequence-files $AGC \
    -o bedpe -O held.norefs.m$m -t 16
done
```

- Compute and disk. E3a: 5,590,178,237 bytes to download, filtered copies of at most 6,532,446,867 and 5,590,178,237 bytes, two indexes. E3b: 6,540,662,155 bytes to download at the assembly-file median size, one more single-index build at the E2 RAM floor. Wall time unknown.
- Blockers. C2 must add a mixed PAF and TPA index test (the held-out index mixes 456 TPA and 10 PAF files), C7 and D3 before strand is scored. The subset list matches PanSN at haplotype or sample level and keeps the query target (VERIFY_CORRECTIONS.md:18), so it lists every non-reference contig, `-m 0` on the release may not finish, then reported with its limit. liftOver install and chain provenance, `pick_pairs.py`.
- Feeds. Fig. 2d, Fig. 4c, Results 5.3, F3.

### E4. Sparse alignment sets and transitive error (tuning chr19 from E5, holdout ScRAP 142)

- Question. As the fraction of aligned pairs falls, how much homology does transitive projection recover against direct all-pairs projection, by depth?
- Data. Tuning: the all-pairs chr19 alignments of E5 (90 haplotypes, 4,005 haplotype pairs). Holdout: ScRAP 142 S. cerevisiae assemblies (O'Donnell et al. 2023, Nat Genet 55:1390-1399, 10.1038/s41588-023-01459-y, accessions, download path and size not checked), one bgzipped, faidx-indexed FASTA per strain with PanSN names, 10,011 strain pairs, 1,000 random 10 kb regions on non-hub strains (seed 5).
- Compared. impg on subsets (random 0.06, random 0.17, the `--sparsify auto` haplotype pairs, a star to one strain fixed in advance, D8) against direct projection on the all-pairs index.
- Metrics. Haplotype pairs aligned, alignment CPU time, bp recall, bp precision, exact-boundary rate at 0, 10 and 100 bp, haplotypes reached, per `-m` 1, 2, 3, 4 and 0. Record pairs and haplotype pairs selected by `auto`. Tuning and holdout side by side.
- Pass target. None proposed in plan.md. To fix or to report only (D2).
- Commands.

```bash
# E4. Sparse alignment sets (chr19 pairs from E5 for tuning, ScRAP 142 holdout here)
mkdir -p $X/e4 && cd $X/e4        # scrap142/*.fa.gz: one bgzipped, faidx-indexed FASTA per strain
$IMPG align --sequence-files scrap142/*.fa.gz --wfmash --format joblist --sparsify auto \
  -o jobs_auto                                    # writes jobs_auto/align_jobs.txt
$T $IMPG align --sequence-files scrap142/*.fa.gz --wfmash --format paf --sparsify none \
  -o y_all -t 16 2> y_all.align.time              # writes y_all/alignments.paf
for f in 0.06 0.17; do python3 -I subset_pairs.py --paf y_all/alignments.paf --mode random \
  --fraction $f --seed 1 > r$f.paf; done
python3 -I subset_pairs.py --paf y_all/alignments.paf --mode joblist \
  --jobs jobs_auto/align_jobs.txt > auto.paf
python3 -I subset_pairs.py --paf y_all/alignments.paf --mode star --hub "$HUB" > star.paf
cp y_all/alignments.paf all.paf
for s in all r0.06 r0.17 auto star; do bgzip -f -@ 8 $s.paf
  $IMPG index -a $s.paf.gz -i $s.impg -f -t 16; done
cat scrap142/*.fa.gz.fai | awk -F'\t' -v h="$HUB#" 'index($1,h)!=1 {print $1"\t"$2}' > y.genome
bedtools random -l 10000 -n 1000 -seed 5 -g y.genome | sort -k1,1 -k2,2n > y_r1000.bed
$IMPG query -a all.paf.gz -i all.impg -b y_r1000.bed -d 0 -o bedpe -O truth.direct -t 16
for s in r0.06 r0.17 auto star; do for m in 1 2 3 4 0; do
  $IMPG query -a $s.paf.gz -i $s.impg -b y_r1000.bed -d 0 -x -m $m -o bedpe -O $s.m$m -t 16
done; done
```

- Compute and disk. Index and query on the workstation. The all-pairs wfmash run over 10,011 strain pairs has unknown wall time and may move to the cluster. ScRAP size unknown (the PGGB scerevisiae142 input is 1,702,093,905 bp, PGGB Table 1, and whether it is the same set is unknown).
- Blockers. ScRAP accessions. Hub strain (D8), `random:<f>` keeps pairs by a `DefaultHasher` threshold, so the harness draws pairs (sweepga knn_graph.rs:371-392), per-genome FASTA files, because FastGA on one FASTA ignores the pair set (src/commands/align.rs:485-500). The logged `auto` percentage counts record pairs (correction 6), C14.
- Feeds. Fig. 4a, Results 5.4.

### E5. Gene-level accuracy and Shredtools on the same input (cluster)

- Question. On HPRC year-1 chr19, how often does each tool return the annotated copy of a gene per haplotype, with what flank, and at what alignment, index and query cost?
- Data. Paths of `s3://human-pangenomics/pangenomes/freeze/freeze1/pggb/chroms/chr19.hprc-v1.0-pggb.gfa.gz` (345,202,999 bytes, dated 2021-12-02, built with `-n 90`). Truth, the 88 haplotype files `*.chm13.gff3.gz` of `s3://human-pangenomics/submissions/FC7E9302-5A35-4A4F-9D4A-B3E957118E36--Y1_CAT_ANNOTATION_GENCODE38/` (89 files with CHM13, 8,452,176,760 bytes, the folder holds 178 GFF3 files of 16,907,655,933 bytes with the hg38 run, plus one 42,795-byte transfer manifest). Query genes from CHM13.chm13.gff3.gz on chr19, 1,000 random 10 kb regions (seed 6) for latency. The set is named as ours, because Shredtools' 92-haplotype list is not in the preprint (paper.txt:283-312).
- Compared. impg (tag) on all pairs, random 0.17, random 0.06, the `auto` haplotype pairs and a CHM13 star. Shredtools (commit to pin) with Mumemto v1.4.0 on the same per-haplotype FASTA files. Optional U9 (impg v0.4.0).
- Metrics. Per stage (alignment, index, query) wall time, CPU time and peak RSS at 1, 8, 16 and 48 threads. The commands below measure index cost at 1, 8, 16 and 48 threads, alignment at 48 threads, gene queries at 16 threads and per-region latency at 1 thread with one run per region. Add `-t` and replicate loops to the align and query commands to measure alignment and query cost at all 4 thread counts and 5 latency replicates (section 1.2). Bytes of PAF and index. Per gene and haplotype containment of the CAT interval, flank excess bp, wrong-locus rate, copies returned, per-query median and p95. Haplotype pairs that `auto` selects at this n, against Shredtools' "17%, the default auto setting" (paper.txt:311-312).
- Pass target (proposed, F4). impg gene-copy containment at least the Shredtools containment on the same genes and haplotypes, and the impg wrong-locus rate at most the Shredtools rate.
- Commands.

```bash
# E5. Gene-level accuracy and Shredtools on HPRC year-1 chr19 (cluster)
mkdir -p $S/e5/hap $S/e5/lat $S/e5/cat && cd $S/e5
aws s3 cp --no-sign-request \
  s3://human-pangenomics/pangenomes/freeze/freeze1/pggb/chroms/chr19.hprc-v1.0-pggb.gfa.gz .
CATB=s3://human-pangenomics/submissions
CATD=FC7E9302-5A35-4A4F-9D4A-B3E957118E36--Y1_CAT_ANNOTATION_GENCODE38
aws s3 cp --no-sign-request --recursive --exclude '*' --include '*.chm13.gff3.gz' \
  $CATB/$CATD/ cat/                                      # 89 files, 8,452,176,760 bytes
zcat chr19.hprc-v1.0-pggb.gfa.gz > chr19.gfa
odgi build -g chr19.gfa -o chr19.og -t 48
odgi paths -i chr19.og -f > chr19.paths.fa
python3 -I split_by_haplotype.py chr19.paths.fa hap/     # bgzip + samtools faidx per haplotype
$IMPG align --sequence-files hap/*.fa.gz --wfmash --format joblist --sparsify auto -o jobs_auto
$T $IMPG align --sequence-files hap/*.fa.gz --wfmash --format paf --sparsify none \
  -o aln_all -t 48 2> align.all.time
cp aln_all/alignments.paf all.paf
python3 -I cat_to_bed.py --gff cat/CHM13.chm13.gff3.gz --chrom chr19 --names seqmap.tsv \
  > cat_genes_chm13_chr19.bed                       # CAT seqid to PanSN path name join
for f in 0.17 0.06; do python3 -I subset_pairs.py --paf all.paf --mode random --fraction $f \
  --seed 1 > r$f.paf; done
python3 -I subset_pairs.py --paf all.paf --mode joblist --jobs jobs_auto/align_jobs.txt > auto.paf
python3 -I subset_pairs.py --paf all.paf --mode star --hub 'CHM13#' > star.paf
for s in all r0.17 r0.06 auto star; do bgzip -f -@ 16 $s.paf
  for t in 1 8 16 48; do
    $T $IMPG index -a $s.paf.gz -i $s.t$t.impg -f -t $t 2> $s.index.t$t.time; done
  [ -s chr19.genome ] || $IMPG stats -a $s.paf.gz -i $s.t48.impg --list-sequences \
    | awk -F'\t' 'NR>1 {print $1"\t"$2}' > chr19.genome
  [ -s rand1000.bed ] || bedtools random -l 10000 -n 1000 -seed 6 -g chr19.genome > rand1000.bed
  $IMPG query -a $s.paf.gz -i $s.t48.impg -b cat_genes_chm13_chr19.bed -d 0 -x -m 2 \
    -o bedpe -O genes.$s -t 16
  while read -r c b e n rest; do
    $T $IMPG query -a $s.paf.gz -i $s.t48.impg -r "$c:$b-$e" -d 0 -x -m 2 -o bed \
      -O lat/$s.$n -t 1 2> lat/$s.$n.time
  done < rand1000.bed
done
python3 -I bp_metrics.py --mode genes --truth cat/ --calls genes.all.bedpe   # each subset
# Shredtools and Mumemto on hap/*.fa.gz: not written (not installed)
```

- Compute and disk. Cluster at 48 threads (Shredtools' setting, paper.txt:346-349), 4,005 haplotype pairs (90 x 89 / 2) with unknown wall time. Downloads 345,202,999 + 8,452,176,760 bytes.
- Blockers. CAT seqids must be joined to the graph path names (not checked). The overlap of the 88 CAT haplotypes with the 90 graph paths (88 + GRCh38 + CHM13 expected, not checked). Shredtools and Mumemto install, Q5, C14, `cat_to_bed.py`.
- Feeds. Fig. 4b, Results 5.5, F4.

### E6. Local graphs and restriction (workstation)

- Question. Does seqwish on the alignments clipped to a closed interval set give the node classes of the global seqwish graph on that set (Proposition 2), and how far are the CLI closure defaults and the `-o gfa` path from it?
- Data. Tuning: tests/test_data/yeast.chrV.fa.gz (7 sequences, 4,029,392 bp, plain gzip), 100 random 10 kb loci (seed 7). Holdout: the C4 region GRCh38#0#chr6:31891045-32123783 (232,738 bp) in 20 haplotypes (seed 8) extracted from the AGC through the E1 PAF index.
- Compared. Restricted against global seqwish graph at `-k 0`. The same at `-k 23`. The closure at CLI defaults (`-m 2`, 101 bp, 10 bp), `impg query -o gfa --gfa-engine seqwish`.
- Metrics. Closure bases whose node class differs (count and fraction), per locus and in total.
- Pass target (proposed, F5). 0 differing bases at `-k 0` on the 100 tuning loci and on the C4 holdout.
- Commands.

```bash
# E6. Local graphs and restriction (workstation)
mkdir -p $X/e6 && cd $X/e6
zcat /home/guarracino/git/impg/tests/test_data/yeast.chrV.fa.gz > yeast.chrV.fa  # gzip, not bgzip
samtools faidx yeast.chrV.fa && Y=$PWD/yeast.chrV.fa
$IMPG align --sequence-files $Y --wfmash --format paf --sparsify none -o aln -t 16
seqwish -p aln/alignments.paf -s $Y -g global.k0.gfa -k 0 -t 16
seqwish -p aln/alignments.paf -s $Y -g global.k23.gfa -k 23 -t 16
bgzip -c aln/alignments.paf > aln.paf.gz && $IMPG index -a aln.paf.gz -i aln.impg -f -t 16
while read -r c b e n rest; do                     # loci100.bed: bedtools random -l 10000 -n 100 -seed 7 -g yeast.chrV.fa.fai
  $IMPG query -a aln.paf.gz -i aln.impg -r "$c:$b-$e" -x -m 0 --min-transitive-len 0 \
    --min-distance-between-ranges 0 --no-merge -o paf -O C.$n -t 16
  seqwish -p C.$n.paf -s $Y -g R.$n.k0.gfa -k 0 -t 16
  seqwish -p C.$n.paf -s $Y -g R.$n.k23.gfa -k 23 -t 16
  $IMPG query -a aln.paf.gz -i aln.impg -r "$c:$b-$e" -x --no-merge -o paf -O D.$n -t 16
  seqwish -p D.$n.paf -s $Y -g RD.$n.k0.gfa -k 0 -t 16
  $IMPG query -a aln.paf.gz -i aln.impg -r "$c:$b-$e" -x -m 0 --min-transitive-len 0 \
    --min-distance-between-ranges 0 -d 0 -o gfa --gfa-engine seqwish --sequence-files $Y \
    -O T.$n -t 16
  for a in "k0 R.$n.k0" "k23 R.$n.k23" "k0 RD.$n.k0" "k0 T.$n"; do set -- $a
    python3 -I compare_classes.py --global global.$1.gfa --local $2.gfa --closure C.$n.paf \
      > cmp.$2.tsv; done                        # denominator: the bases of closure C
done < loci100.bed
# C4 holdout: 20 haplotypes (seed 8) from the E1 star index; then the same steps on c4_20.fa
$IMPG query -a $P38 -i ../e1/paf.impg -r 'GRCh38#0#chr6:31891045-32123783' -d 0 \
  --subset-sequence-list c4_20_contigs.txt --sequence-files $AGC -o fasta -O c4_20 -t 16
# c4_20.fa names carry ':start-end', so -r on them needs an explicit range, e.g.
# -r 'GRCh38#0#chr6:31891045-32123783:0-232738'
```

- Compute and disk. Workstation, 0 bytes to download for tuning. The C4 holdout reads 20 sequences from the AGC. Wall time unknown.
- Blockers. `-o paf` has no alignment-backend test (VERIFY_CORRECTIONS.md:15-16), so check the reverse-strand CIGAR slice of PAF rows on a fixture first, `compare_classes.py` on a 3-sequence toy. The `-o gfa` arm re-aligns and normalizes, so it measures distance, not equality (src/main.rs:12326-12340), self-alignments break closedness (Proposition 1), so count bases on contigs with self-hits apart, C14.
- Feeds. Fig. 5a, Results 5.6, Note S1, F5.

### E7. Copy representation in the released alignments (workstation, gate for any copy statement)

- Question. Do the released alignments store gene copies as separate records, per haplotype, at multi-copy loci?
- Data. GRCh38 PAF.gz on disk, CHM13 PAF.gz from E3a, 3 assembly per-target PAF.gz files (seed 9, 1,962,198,646.5 bytes at the median size of the 464 assembly files). Loci C4 (done on GRCh38: 895 records from 465 haplotypes, 401 with depth 1, phase2/judge/c4_depth_out.txt), AMY1, SMN1/SMN2, LPA, CYP2D6 from GENCODE records written to loci.<target>.bed in each target's coordinates.
- Compared. None (audit).
- Metrics. Records per haplotype. Maximum per-base record depth per haplotype. Fraction of haplotypes with depth at least 2. Query contigs per haplotype. Record query span.
- Pass target. None. The authors decide which depth makes a copy statement allowed (D3 with C7).
- Commands.

```bash
# E7. Copy representation in the released alignments (workstation)
mkdir -p $X/e7 && cd $X/e7          # a1..a3.paf.gz: 3 assembly per-target PAF.gz files, seed 9
for f in $P38 ../e3a/chm13.paf.gz a1.paf.gz a2.paf.gz a3.paf.gz; do
  k=$(basename $f .paf.gz)
  while read -r c b e n rest; do
    pigz -dc -p 4 "$f" | cut -f1-12 \
      | awk -F'\t' -v c="$c" -v b="$b" -v e="$e" '$6==c && $8<e && $9>b' > $k.$n.tsv
    python3 -I locus_depth.py --start $b --end $e $k.$n.tsv >> depth.tsv
  done < loci.$k.bed                                # locus coordinates in each target
done
```

- Compute and disk. Workstation. The C4 extraction on the GRCh38 file took 221 s (judge-reviewer.md section 1). Downloads 1,962,198,646.5 bytes at the assembly-file median size plus the CHM13 file of E3a.
- Blockers. Locus coordinates on the 3 assembly targets (from a projection in E3a or E2), `locus_depth.py`.
- Feeds. Supplementary Fig. S5, Discussion, the gate for U4.

### E8. Consistency with the released PGGB graph (cluster, supplement)

- Question. Per region and haplotype, how much do impg intervals and the paths of the PGGB graph built from the same alignments overlap?
- Data. E2 index. GBZ v3, 1,000 random 10 kb regions on GRCh38 and 1,000 on non-reference haplotypes (seed 10). Segmental duplication and satellite strata (annotation source to choose).
- Compared. impg `-x -m 2` against `vg chunk` path intervals.
- Metrics. Per region and haplotype bp Jaccard, haplotypes found by one method only, boundary shifts, per stratum.
- Pass target. Jaccard target fixed before the run (D2), 100% is not expected, because `-k 311` drops exact matches shorter than 311 bp (hpp_readme.md:155).
- Commands.

```bash
# E8. Consistency with the released PGGB graph (cluster, after E2)
cd $S/e2 && mkdir -p cons        # cons.bed: 1,000 GRCh38 + 1,000 non-reference 10 kb, seed 10
$IMPG query --alignment-list tpa466.list -i r2.impg -b cons.bed -d 0 -x -m 2 \
  --sequence-files $AGC -o bed -O cons.impg -t 16
while read -r c b e n rest; do
  vg chunk -x $GBZ -p "$c:$b-$((e-1))" -c 0 -O gfa -t 1 > cons/$n.gfa
done < cons.bed
python3 -I chunk_paths_to_bed.py cons/ > cons.vg.bed
python3 -I bp_metrics.py --mode jaccard cons.impg.bed cons.vg.bed --strata strata.bed
```

- Compute and disk. Cluster after E2. No alignment or graph download beyond E2, plus the segmental duplication and satellite annotation for strata.bed (source and size unknown).
- Blockers. E2. Whether vg reads the v3 GBZ. Whether `vg chunk -p` accepts non-reference haplotype paths in a GBZ (unknown, not run), `chunk_paths_to_bed.py` on a toy graph.
- Feeds. Supplementary Fig. S3, Results 5.2 (labelled consistency).

### E9. Alignment-backed partition audit on ScRAP 142 (workstation)

- Question. Does `impg partition` on the alignment backend cover every base exactly once, and how many partitions join material from different chromosomes?
- Data. The E4 all-pairs ScRAP PAF and index, `-w 10000 -d 1000 --selection-mode haplotype`, default rehoming, fixed in advance.
- Compared. None (audit). The syng-backed yeast235 run (19,421 partitions, 3,336,976,856 bp, 0 uncovered, 0 owned twice, commit 295bca9, VERIFY_CORRECTIONS.md:72-73) is context for this file only and stays out of the Results, because syng is WIP.
- Metrics. Partitions counted from the BED files (the logged count can exceed them after rehoming, src/commands/partition.rs:142-156, 676-678, 746-748), member intervals, uncovered bp, bp owned more than once, partitions spanning more than one S288C chromosome, wall time, peak RSS.
- Pass target (plan.md E9). 0 uncovered bp and 0 bp owned more than once.
- Commands.

```bash
# E9. Alignment-backed partition audit on ScRAP 142 (workstation, after E4)
cd $X/e4
$T $IMPG partition -a all.paf.gz -i all.impg -w 10000 -d 1000 --selection-mode haplotype \
  -o bed --output-folder part -t 16 2> part.time
python3 -I exact_once_audit.py --bed-dir part --fai scrap142/*.fa.gz.fai > part.audit.tsv
```

- Compute and disk. Workstation after E4. Wall time unknown. The per-window clone of the mask map grows with the masked ranges (src/impg.rs:2182, 2399-2401), measured here at yeast scale only.
- Blockers. E4. Port of the audit in docs/syng-gmem-bwt/observation-registry-repair.md to alignments, C11 (`-w 0` never advances. The partition test passes a nonexistent `--reference-fai`).
- Feeds. Supplementary Fig. S4, Results 5.8.

### E10. Locus refinement against Shredtools zoom (cluster)

- Question. At TERT and IGKV6-21, how many haplotypes span both ends after `impg refine`, with what extension, compared with Shredtools enhance and zoom?
- Data. E2 index, IGKV6-21 at CHM13 chr2:89168754-89169041 as printed in paper.txt:445 (BED start 89168753 if the print is 1-based, to check against the CHM13 annotation). TERT from the CHM13 v2.0 annotation (Shredtools gives no coordinates, paper.txt:463-470). The 15 T2T genomes of the Shredtools example where present in the 466 files (list from Q5), and all 466.
- Compared. impg refine against Shredtools enhance and zoom on hprcv2_merged.bumbl.
- Metrics. Haplotypes spanning both ends before and after (refine columns original.support and new.support), extension bp per side, genomes dropped by zoom, wall time.
- Pass target. None. Report both tools, with Shredtools' printed numbers (328,599 bp and 74,147 bp bounds, then 0 bp on 13 of 15 genomes at IGKV6-21, 25 to 35 kbp, then exact bounds on 476 genomes at TERT, paper.txt:445-470) as theirs.
- Commands.

```bash
# E10. Locus refinement against Shredtools zoom (cluster, after E2)
cd $S/e2       # tert_igk.bed: IGKV6-21 CHM13#0#chr2 89168753 89169041, TERT from the annotation
$T $IMPG refine --alignment-list tpa466.list -i r2.impg -b tert_igk.bed -d 10k -x -m 2 \
  --pansn-mode haplotype --span-bp 1000 --max-extension 0.5 --extension-step 1000 \
  --support-output refine.support.bed --sequence-files $AGC -t 16 > refine.tsv 2> refine.time
$T $IMPG refine --alignment-list tpa466.list -i r2.impg -b tert_igk.bed -d 10k -x -m 2 \
  --pansn-mode haplotype --span-bp 1000 --max-extension 0.5 --extension-step 1000 \
  --subset-sequence-list t2t15.txt --support-output refine15.support.bed \
  --sequence-files $AGC -t 16 > refine15.tsv 2> refine15.time
# Shredtools enhance and zoom on hprcv2_merged.bumbl: not written (not installed)
```

- Compute and disk. Cluster after E2. Wall time unknown.
- Blockers. E2. Shredtools install, C11 (refine CLI test), non-transitive refine ignores `--approximate` (src/commands/refine.rs:213, 527-535), so approximate mode is not used. The T2T list (Q5).
- Feeds. Fig. 5b, Results 5.7.

## 4. Tier 2 experiments (upgrade to the Nature Methods Brief, or optional)

### U1. Minigraph-Cactus regional comparator

- Question. What does the HPRC r2 Minigraph-Cactus graph return for the E2 and E5 regions, at what cost? PGGB reviewer 1 required MC comparisons (judge-reviewer.md section 3.2).
- Data. `s3://human-pangenomics/pangenomes/freeze/release2/minigraph-cactus/v2.1/hprc-v2.1-mc-grch38/hprc-v2.1-mc-grch38.gbz` (5,492,627,216 bytes) and `.full.gbz` (34,234,954,016 bytes), CHM13-based `hprc-v2.1-mc-chm13.gbz` (6,160,361,544 bytes), `aws s3 ls`, 2026-11-09.
- Compared. vg v1.76.1 `chunk` on the MC GBZ against impg and the PGGB GBZ (E2).
- Metrics. As E2 (wall time, RSS) and as E8 (bp Jaccard of path intervals).
- Pass target. None proposed.
- Commands. `vg chunk -x hprc-v2.1-mc-grch38.gbz -p "$c:$b-$((e-1))" -c 0 -O gfa -t 1 > mc/$n.gfa` over the E2 GRCh38 10 kb set (flags as in E2).
- Compute and disk. Cluster, 5,492,627,216 bytes (clipped) or 34,234,954,016 bytes (full) to download.
- Blockers. MC path naming in the GBZ. Clipped graphs drop sequence, so the full graph is the fair comparator for coverage (to decide).
- Feeds. Fig. 3b, Fig. 4b.

### U2. Liftover arms

- Question. Does chain liftover, direct and chained through one intermediate genome, recover the same intervals as impg on the E5 alignments?
- Data. E5 all-pairs PAF. Chains from paf2chain. A HAL file if one exists for these haplotypes (unknown).
- Compared. UCSC liftOver direct and chained, halLiftover, and impg at `-m 1` and `-m 2`.
- Metrics. As E5 (containment, flank excess, wrong locus).
- Pass target. None proposed.
- Commands. Not written: liftOver, paf2chain and halLiftover are not installed and their flags are unchecked.
- Compute and disk. Cluster, small.
- Blockers. Installs. HAL availability.
- Feeds. Fig. 4b.

### U3. Simulation with a logged coordinate map

- Question. How accurate is transitive projection against a truth that no aligner produced, by event class, strand and hop count 1 to 4?
- Data. Tens of 10 Mbp genomes simulated from a CHM13 chr20 slice with SNVs, indels, inversions, tandem and dispersed duplications.
- Compared. impg on all pairs and sparse subsets.
- Metrics. bp recall, precision, exact boundaries, strand agreement, per event class and hop count.
- Pass target. None proposed.
- Commands. Not written: the simulator does not exist (judge-feasibility.md section 4.1).
- Compute and disk. Workstation.
- Blockers. Simulator, D3 (strand).
- Feeds. A new Fig. 4 panel.

### U4. AMY1 copies per haplotype

- Question. Do impg intervals at AMY1 match published copy numbers on shared assemblies?
- Data. Bolognini et al. 2024 (10.1038/s41586-024-07911-1) copy calls. HPRC r2 haplotypes in common (overlap unknown).
- Compared. impg intervals against the published counts. Read depth on 1000 Genomes CRAMs only for an Article.
- Metrics. Copies per haplotype, agreement.
- Pass target. None proposed.
- Commands. `impg query --alignment-list tpa466.list -i r2.impg -b amy1.bed -d 0 -x -m 2 --sequence-files $AGC -o bedpe -O amy1 -t 16` (flags as in E2).
- Compute and disk. Cluster after E2.
- Blockers. Gated on E7 and C7 (self-hits). Sample overlap. No read-depth method chosen.
- Feeds. Article Fig. 6 only.

### U5. Incremental growth with per-file indexes

- Question. Does adding files to a per-file index leave old answers byte-identical to a single-index rebuild?
- Data. E2 TPA files split into a first set and an added set.
- Compared. `--index-mode per-file` with added files against a single index of all files.
- Metrics. Byte identity of sorted outputs. Time to add files.
- Pass target. Byte identity (to fix).
- Commands. `impg index --alignment-list first.list --index-mode per-file -t 32`, then the same with all.list, then `impg query --alignment-list all.list --index-mode per-file -b r.bed -d 0 -x -m 2 --sequence-files $AGC -o bedpe -O pf` against the single-index output (flags in impg index and query --help).
- Compute and disk. Cluster.
- Blockers. MultiImpg FIFO BFS, self-hits, eviction and a single-vs-per-file equality test (C6 second part, src/multi_impg.rs:757-952).
- Feeds. Supplement.

### U6. Whole HPRC r2 partition on alignments

- Question. Does alignment-backed partition run at release scale, and how does it compare with the 7,424 released partition graphs if Q1 is yes?
- Data. E2 index. The released partition list (7,424 files, phase2/s3/part_sizes.tsv).
- Compared. impg partition against the released partitions.
- Metrics. As E9.
- Pass target. As E9.
- Commands. `impg partition --alignment-list tpa466.list -i r2.impg -w 10000 -d 1000 --selection-mode haplotype -o bed --output-folder part --sequence-files $AGC -t 32` (flags in impg partition --help).
- Compute and disk. Cluster. The mask-map clone cost is unmeasured (src/impg.rs:2182, 2399-2401).
- Blockers. E9 first, Q1.
- Feeds. Supplement.

### U7. Homology across acrocentric short arms

- Question. Which haplotypes share sequence across the short arms of chr13, 14, 15, 21 and 22 when the query starts on a non-reference haplotype and no reference bridges?
- Data. E2 index, short-arm completeness in HPRC r2 unknown.
- Compared. With and without references.
- Metrics. Haplotypes and chromosomes reached, bp.
- Pass target. None proposed.
- Commands. `impg query --alignment-list tpa466.list -i r2.impg -b parms.bed -d 0 -x -m 2 --subset-sequence-list nonref_contigs.txt --sequence-files $AGC -o bedpe -O parms -t 16` (flags as in E3b).
- Compute and disk. Cluster after E2.
- Blockers. Completeness of the short arms. Guarracino et al. 2023 as context.
- Feeds. Article only.

### U8. Local pggb-engine graphs against the released partition graphs

- Question. At 5 loci, how do impg `-o gfa` pggb-engine graphs compare with the released partition graphs (path spelling, segment bp, cost)?
- Data. E2 index. The released `partitionN.final.gfa.zst` files covering the loci.
- Compared. impg local graph against the released partition graph.
- Metrics. Path spelling identity, segment bp, wall time, RSS.
- Pass target. Path spelling identity (to fix).
- Commands. `impg query --alignment-list tpa466.list -i r2.impg -r "$locus" -d 0 -x -m 2 -o gfa --gfa-engine pggb --sequence-files $AGC -O u8.$n -t 16` (flags in impg query --help).
- Compute and disk. Cluster.
- Blockers. D9 (POA smoothing default: 87 against 2,224 spurious bp on yeast, .claude/runs/poa-score/pggb_yeast.out:1-2).
- Feeds. Supplement.

### U9. E5 at impg v0.4.0

- Question. How much of the gap to Shredtools' printed numbers comes from the impg version?
- Data. E5 inputs.
- Compared. impg v0.4.0 (tag dated 2026-01-16, Shredtools reference [6], paper.txt:838-839) against the paper's tag.
- Metrics. As E5 cost.
- Pass target. None.
- Commands. Build v0.4.0 in a separate checkout, then the E5 index and latency commands with that binary (its flags to check with its own `--help`).
- Compute and disk. Cluster.
- Blockers. v0.4.0 build.
- Feeds. Table S4.

### U10. gbz-base on the released `.gbz.db`

- Question. What does the released graph's own random-access path cost per region?
- Data. `.../20250930_hprc25272.p98-k311.tmp.fix.gbz.db` (61,240,860,672 bytes).
- Compared. As E2.
- Metrics. As E2.
- Pass target. None.
- Commands. Not written: gbz-base is not installed.
- Compute and disk. Cluster, 61,240,860,672 bytes.
- Blockers. Install.
- Feeds. Fig. 3b.

### U11. A. thaliana 69 accessions

- Question. Do the E4 and E5 results hold on Shredtools' second set?
- Data. 69 accessions (Lian et al. 2024). No released alignments. Accessions not checked.
- Compared. As E5.
- Metrics. As E5 cost and E4 recall.
- Pass target. None.
- Commands. `impg align --sequence-files ath/*.fa.gz --wfmash --format paf --sparsify none -o ath_all -t 48`, then the E4 steps (flags in impg align --help).
- Compute and disk. Cluster, 2,346 accession pairs (69 x 68 / 2).
- Blockers. Accessions and FASTA download.
- Feeds. Supplement.

## 5. Code fixes before benchmarking

| ID | Fix | Why it blocks | Evidence |
| --- | --- | --- | --- |
| C1 | Cut one tag, archive it with a Zenodo version DOI, build the container from the tag, point the paper-repo submodule at the tag, record the binary sha256 in every run, stop rebuilding the benchmark binary | HEAD is 656 commits past v0.5.0. The Dockerfile clones the default branch. The binary mtime moved at least 5 times on 2026-11-08. The paper repo records f773342 while its checkout is 7bd50a8 | `git describe`, Dockerfile:38, judge-reviewer.md section 1, plan.md section 4 |
| C2 | Standard TPA and 1ALN fixtures with exact-vs-PAF identity tests on both strands and on a mixed PAF and TPA index. Count and warn on dropped tracepoint hits. Return an error for FastgaNoDiff and Variable records instead of an index panic. One identity-filter span for PAF and tracepoints, or keep `--min-result-identity` out | The release is TPA and no test touches tracepoint projection | no `.tpa` or `.1aln` in tests/*.rs, src/impg.rs:1230-1236, 1247-1254, 1330-1338, 1436-1442, 1453-1460, src/tpa_parser.rs:202-224, src/impg.rs:832, src/impg.rs:1277-1281 vs 1386-1390 |
| C3 | Merge a bounded tree cache and the coitrees clone fix | c03ea0e, cfa20d5, c6e85dd and e2d093a are not in HEAD, Cargo.lock pins stock coitrees 0.4.0. The only record of a killed whole-chr1 query is an untracked note | VERIFY_CORRECTIONS.md:48, notes/IMPG_MEMORY_PROFILING_REPORT.md:212 (untracked, not citable) |
| C4 | Store the ordered file list (paths, sizes) and the build direction in the index header and refuse a mismatch. Skip the IMPGIDX3 magic at the next format bump | `get_combined_index_filename` hashes the sorted names while impg numbers files in the order given, so a reordered list reads CIGARs from the wrong file without error. An IMPGIDX3 file sits in user data | src/main.rs:11778-11798 vs src/impg.rs:1657-1663, src/impg.rs:1897-1898 |
| C5 | Keep in-memory trees non-evictable in `impg stats` | `print_stats` evicts each tree and reloads it through `File::open` of the index path, which is empty on a fresh in-memory index | src/main.rs:13298-13304, src/impg.rs:1827-1832 |
| C6 | Benchmark only in single mode with `-i`. A node above the RAM floor or a lower-memory build. MultiImpg FIFO BFS, self-hits, eviction and an equality test only for U5 | 466 files select the untested per-file path under `auto`. The single build needs at least 59,163,669,536 bytes | src/main.rs:11277-11291, src/multi_impg.rs:757-780, 813-821, 876-882, 933-952, judge-feasibility.md section 1.1 |
| C7 | Decide and test closure semantics: compose strand across hops or document per-hop strand with a two-reverse-hop fixture. Expand self-hits or document that they are not expanded | Strand agreement in E3a and any duplicated-locus count depend on it | src/impg.rs:282-286, 2574-2589, src/main.rs:12072-12079 |
| C8 | Measure the 1,483 reciprocal pairs: index entries against 2 x records, BEDPE and PAF duplicate rows, merged BED identity with `--unidirectional` | Duplicate entries inflate the index and unmerged rows | data/pairs_out.txt, E1b |
| C9 | Fail when an AGC fetch returns a length other than end minus start | Archives appended with agc older than 3.2.2 return wrong ranges silently. The local agc is 3.2.1 | src/agc_index.rs:383-407, notes/bug-agc-appended-sample-range.md |
| C10 | Enforce `--min-transitive-len` in approximate transitive mode. Pass `--approximate` through non-transitive refine or reject it there | The flag only warns. Refine ignores it | src/main.rs:10581-10595, src/commands/refine.rs:213, 527-535 |
| C11 | Tests for bedpe and paf output on the alignment backend, a refine CLI test, a fixed `test_partition_window_separation`, and `-w 0` rejected | Every command and format in the paper needs a test, `-w 0` never advances | VERIFY_CORRECTIONS.md:8, 15-16, 92, tests/test_transitive_integrity.rs:595-643 |
| C12 | README and help: `--min-identity` (README.md:137), refine examples without `-d` (README.md:214-226), "compact deltas" (README.md:30-33), `--approximate` ".1aln only" (README.md:142), `--syng-min-chain-fraction` default (README.md:434), `giant` described as k-nearest (README.md:586, 595). State that `--sparsify` selects haplotype pairs for PanSN names (record pairs otherwise), always keeps within-haplotype pairs, and logs a record-pair percentage (correction 6). Mark experimental subcommands in `impg --help`. Remove campaign language from `impg infer --help` | Reviewers run the README and `--help` | VERIFY_CORRECTIONS.md:92, 297, src/main.rs:5217-5227, sweepga 4713ce0 src/knn_graph.rs:589-677 |
| C13 | Error on sequences longer than 2,147,483,647 bp and on PAF without `cg:Z` at index time | Silent wrap and a query-time panic | src/impg.rs:80-109, 164-174, 610-615 |
| C14 | Benchmark harness in impg-paper/experiments/ (section 1.3), each script with verbose diagnostics and a toy-data test | The PGGB evaluation bug surfaced only in review round 2 | phase1_research_digest.txt PGGB LESSONS, MOESM3.txt:934-945 |
| C15 | Optional: build local graphs from the projected PAF records instead of re-aligning (the restriction path) | Needed only if `-o gfa` itself must equal the restriction | src/main.rs:12326-12340, D4 |

## 6. Decisions only the authors can make

- D1. If E1 fails, fix the TPA path or move every run to the 318,372,159,094-byte per-target PAF set on the cluster.
- D2. The targets for F1 to F5 (proposed values in E1, E2, E3, E5, E6 above), the E3a, E4 and E8 targets, fixed before any run.
- D3. Compose strand across hops or document per-hop strand. Expand self-hits or document their non-expansion (C7).
- D4. Whether to implement the restriction path (C15) so that `-o gfa` itself induces from clipped alignments.
- D5. Which cluster node runs E2, E3b, E5, E8 and E10, or whether to fund a lower-memory build if no node exceeds 59,163,669,536 bytes.
- D6. The tag name, who owns C1 to C14, and how to keep the benchmark binary frozen while other work rebuilds target/release.
- D7. Bioinformatics first or the editor's Brief-first order.
- D8. ScRAP 142 (published) or yeast235 (local, 1,039,122,903 bytes, publication unknown) as the yeast set, and the star hub strain.
- D9. The POA smoothing default (87 against 2,224 spurious bp on yeast) before any pggb-engine graph appears (U8).
- D10. Whether `impg infer` is labelled experimental or product surface in `--help`.
- D11. Preprint timing, given that the Shredtools sentence is public since 2026-07-08.
- D12. Add remote HTTP access before submission or state it as a limit.
- D13. Who sends Q1 to Q5.
- D14. If F1 to F5 pass, approach Nature Methods with an abstract-only enquiry sent when E2 has numbers and before this manuscript is final, or with a full Brief Communication, because the journal says enquiries are not for written manuscripts (venue-assessment.md section 8.1). The same decision covers suggested and excluded reviewers.
- New in this file, under D2: the number of cluster build replicates (1 or 3) for E2 and E5, and the public GRCh38-to-CHM13 chain file for E3a.

## 7. Questions for outside parties

| ID | To | Question |
| --- | --- | --- |
| Q1 | HPRC builders | Did `impg partition` and `impg lace` build the 7,424 released partition graphs (`partitionN.final.gfa.zst`, a `laced` VCF)? |
| Q2 | HPRC builders | Which pair-selection rule and wfmash settings produced the release network (11.2583% of ordered non-reference pairs)? |
| Q3 | HPRC builders | What did the r2 PGGB build cost, split by alignment, induction and smoothing (CPU hours, peak RAM)? |
| Q4 | HPRC builders | Who produced the IMPG product, so that the paper can disclose it? |
| Q5 | Shredtools authors | The 92-haplotype chr19 list, the impg command lines, the meaning of "17%, the default auto setting", the 15 T2T genomes of the IGKV6-21 example and the TERT coordinates |
| Q6 | Cluster administrators | Which gemini node has more than 59,163,669,536 bytes of RAM and 63,916,842,350 bytes of scratch, and can jobs drop the page cache? |

## 8. Unknowns and where I looked

- Cluster CPU, RAM, disk and page-cache policy: no phase measured them (plan.md section 14).
- Whether vg v1.76.1 reads the released v3 GBZ and accepts non-reference haplotype paths in `-p`: `vg chunk --help` names "graph or XG index" and path ranges only. Not run.
- ScRAP 142 accessions, download path and size: not checked in any phase.
- The overlap between the 88 CAT haplotypes and the 90 chr19 graph paths, and the CAT seqid join: file names listed on 2026-11-09, contents not read.
- Shredtools commands, flags and version: not installed. The preprint prints none (paper.txt p.4-5, p.12-14).
- Whether `-m 0` on the whole release finishes: not run.
- Whether `--approximate` on TPA needs `--sequence-files`: help does not say. Not run.
- Wall time of every experiment: no basis found.
