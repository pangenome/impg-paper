<!-- workgraph-managed -->
# Workgraph

Use workgraph for task management.

**At the start of each session, run `wg quickstart` in your terminal to orient yourself.**
Use `wg service start` to dispatch work — do not manually claim tasks.

## For All Agents (Including the Orchestrating Agent)

CRITICAL: Do NOT use built-in TaskCreate/TaskUpdate/TaskList/TaskGet tools.
These are a separate system that does NOT interact with workgraph.
Always use `wg` CLI commands for all task management.

CRITICAL: Do NOT use the built-in **Task tool** (subagents). NEVER spawn Explore, Plan,
general-purpose, or any other subagent type. The Task tool creates processes outside
workgraph, which defeats the entire system. If you need research, exploration, or planning
done — create a `wg add` task and let the coordinator dispatch it.

ALL tasks — including research, exploration, and planning — should be workgraph tasks.

### Orchestrating agent role

The orchestrating agent (the one the user interacts with directly) does ONLY:
- **Conversation** with the user
- **Inspection** via `wg show`, `wg viz`, `wg list`, `wg status`, and reading files
- **Task creation** via `wg add` with descriptions, dependencies, and context
- **Monitoring** via `wg agents`, `wg service status`, `wg watch`

It NEVER writes code, implements features, or does research itself.
Everything gets dispatched through `wg add` and `wg service start`.

## Project: IMPG Paper

This repository contains the manuscript for the IMPG (Implicit Pangenome Graphs) paper,
targeting Bioinformatics (OUP). The paper is structured into `sections/*.tex` files
that are `\input{}`'d from `main.tex`.

### impg: Complete Pangenome Graph Construction Pipeline

The impg tool is a git submodule at `./impg/` and has evolved into a **complete pangenome 
graph construction pipeline**. It embeds core pggb components (sweepga, seqwish, gfasort) 
and implements the full workflow from sequence input to finished pangenome graphs.

**ALWAYS use the local build for all experiments:**

```
/home/erik/impg-paper/impg/target/release/impg
```

Do NOT use any globally installed impg. The local version is the one the paper describes.
If you modify impg source code, rebuild before running experiments:
```bash
cd /home/erik/impg-paper/impg && cargo build --release
```

### IMPG Pipeline Architecture

The core impg pipeline follows these stages:

1. **Covering alignments** — Generate all-vs-all or sparsified alignments using embedded sweepga
2. **Sparsification** — Apply sparsification strategies (`giant:0.99`, `random`, `tree`) at the top level before partitioning
3. **Partitioning** — Use the partition lace approach to divide the pangenome into manageable windows
4. **Graph building** — Build graphs per partition using embedded pggb components (sweepga + seqwish)
5. **Evaluation** — Use panacus to measure pangenome growth and generate basic statistics

### Key Components

- **Embedded sweepga**: All-vs-all alignment generation (replaces wfmash)
- **Embedded seqwish**: Graph induction from alignments
- **Embedded gfasort**: Graph optimization and sorting
- **Sparsification engine**: Reduces O(n²) complexity while maintaining connectivity
- **Partition system**: Window-based genome division with lacing for reassembly
- **panacus integration**: For pangenome growth analysis and evaluation metrics

### Sparsification Strategies

Instead of traditional covering alignments, impg uses intelligent sparsification:
- `giant:0.99` (default): Erdős-Rényi strategy ensuring 99% probability of connected giant component
- `random:<fraction>`: Random subset of alignment pairs
- `tree:<k_near>:<k_far>:<rand>`: k-nearest + k-farthest + random pairs based on Mash distances

### impg development

We follow an **upstream-first policy** for impg changes. All fixes and improvements
to impg should be implementation-quality code suitable for pushing upstream — not hacks.

**Rules for modifying impg:**

1. **Work in the submodule**: All changes go in `./impg/src/`. Do not copy impg code elsewhere.
2. **Rebuild after changes**: `cd /home/erik/impg-paper/impg && cargo build --release`
3. **Test with small data first**: Validate changes on small inputs (e.g., cerevisiae chrV)
   before running full-scale experiments.
4. **Write clean code**: Changes will be pushed upstream to the impg repo. Write proper
   implementations with error handling, not quick workarounds.
5. **Commit in the submodule**: Changes to `./impg/` should be committed within the submodule
   so the paper repo tracks the exact version used.

### Test data

- Main dataset: Yeast 235 genomes (AGC format) - available from https://garrisonlab.s3.amazonaws.com/index.html?prefix=yeast/
- Quick test subset: S. cerevisiae chrV - available from https://garrisonlab.s3.amazonaws.com/index.html?prefix=yeast/

### Experiment conventions

- All experiments go in `experiments/<experiment-name>/` directories
- Each experiment directory is self-contained: scripts, outputs, figures
- Add `experiments/` to .gitignore if intermediate files are large
- Final figures go in `fig/` for inclusion in the paper
- Agents must NOT modify files outside their designated experiment directory or assigned section file
- Use `wg log` and `wg artifact` to record all results

### Reference papers (for style/structure)

- TracePoints paper (Bioinformatics template reference): `reference-tracepoints/`
- "Building pangenome graphs" (PGGB) — Garrison et al., Nature Methods 2024
- "Unbiased pangenome graphs" — search for this, also Bioinformatics
- ODGI paper — the graph toolkit paper, also Bioinformatics-style

### Manuscript sections

Agents working on manuscript text should ONLY modify their assigned section file:
- `sections/01.introduction.tex`
- `sections/02.methods-overview.tex`
- `sections/03.results.tex`
- `sections/04.discussion.tex`
- `sections/05.acknowledgments.tex`
- `sections/06.figures.tex`
- `sections/07.methods-detail.tex`
- `sections/08.supplementary.tex`

Do NOT modify `main.tex` unless specifically tasked with preamble/structure changes.
