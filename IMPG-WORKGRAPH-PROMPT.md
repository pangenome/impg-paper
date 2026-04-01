# IMPG Paper Workgraph: Autopoietic Task Graph Generator

This document serves as a complete specification for recreating the task graph needed to produce the IMPG (Implicit Pangenome Graphs) paper from scratch. When processed by a workgraph coordinator, it should generate all necessary tasks with proper dependencies to complete the manuscript.

## Project Context

**Project**: IMPG paper for Bioinformatics (Oxford University Press)
**Repository**: Academic manuscript targeting peer-reviewed publication
**Core Innovation**: Treating pairwise alignments as queryable pangenome representations without upfront graph construction

### What is IMPG?

IMPG (Implicit Pangenome Graphs) is a computational framework that enables pangenome-scale analysis directly from pairwise alignments, avoiding expensive upfront graph construction. Key capabilities:

1. **Transitive coordinate projection**: Multi-hop liftover across populations from pairwise alignments
2. **Alignment-based partitioning**: Decompose pangenomes along connectivity boundaries  
3. **On-demand graph materialization**: Build graphs only for regions of interest, in real-time

The tool operates on the principle that pairwise alignments inherently encode a variation graph structure, making explicit graph construction optional for most analyses.

### Publication Target

- **Venue**: Bioinformatics (Oxford University Press)
- **Format**: Methods paper with experimental validation
- **Style**: Follow ODGI and "Unbiased pangenome graphs" papers as structural models
- **Scope**: Conceptual contribution + practical tool demonstration

## Repository Structure

```
/home/erik/impg-paper/
├── main.tex                          # Main LaTeX document
├── sections/                         # Modular manuscript sections
│   ├── 01.introduction.tex
│   ├── 02.methods-overview.tex
│   ├── 03.results.tex
│   ├── 04.discussion.tex
│   ├── 05.acknowledgments.tex
│   ├── 06.figures.tex
│   ├── 07.methods-detail.tex
│   └── 08.supplementary.tex
├── fig/                              # Publication figures (PDF format)
├── experiments/                      # Self-contained experiment directories
│   ├── yeast-chrV/                   # Chromosome V experiments
│   ├── yeast-full/                   # Full genome experiments
│   ├── scaling/                      # Performance scaling curves
│   └── batch-test/                   # Batch processing validation
├── impg/                             # Git submodule: impg tool source
├── reference-tracepoints/            # Reference paper (Bioinformatics template)
├── research/                         # Analysis documents
├── bibliography.bib                  # Main bibliography
└── CLAUDE.md                         # Project instructions for agents
```

### Critical Files and Constraints

**impg Binary**: Always use local build at `/home/erik/impg-paper/impg/target/release/impg`
- Git submodule containing the actual tool
- Upstream-first development policy: all changes must be implementation-quality
- Rebuild after any source modifications: `cd /home/erik/impg-paper/impg && cargo build --release`

**Test Datasets**:
- Main dataset: Yeast 235 genomes (AGC format) - available from https://garrisonlab.s3.amazonaws.com/index.html?prefix=yeast/
- Quick test subset: S. cerevisiae chrV - available from https://garrisonlab.s3.amazonaws.com/index.html?prefix=yeast/

**Agent File Restrictions**:
- Manuscript agents: ONLY modify assigned section file in `sections/`
- Experiment agents: ONLY work within designated `experiments/<name>/` directory
- NO agent modifies `main.tex` without explicit task assignment

## Task Graph Architecture

### Phase 1: Foundation (Parallel Setup Tasks)

**Core Setup**:
```bash
wg add "set-up-experiment" -d "
Create experiment infrastructure:
- mkdir -p experiments/{yeast-chrV,yeast-full,scaling}
- Add 'experiments/' to .gitignore
- Decompress test data to appropriate experiment directories
- Extract sample lists from AGC archive for planning
- Verify impg binary builds and runs

Test data verification:
- Download yeast235.agc from https://garrisonlab.s3.amazonaws.com/index.html?prefix=yeast/ → ragc inspect, log sample count
- Download cerevisiae chrV data from S3 → decompress to experiments/yeast-chrV/
- Download full cerevisiae genome from S3 → decompress to experiments/yeast-full/

DO NOT run impg commands yet — just prepare data landscape.
"
```

**Research Foundation**:
```bash
wg add "research-reference-papers" -d "
Find and analyze structural models for IMPG paper:
1. 'Unbiased pangenome graphs' (Garrison et al., Bioinformatics)
2. ODGI paper (graph toolkit, Bioinformatics-style)

Analyze for IMPG paper guidance:
- Section organization and flow
- Methods presentation style (mathematical formalism level)
- Experiment structure and benchmarking approach  
- Figure design patterns
- Writing tone and conceptual vs. practical balance
- Length and scope conventions

Study impg README/documentation for complete subcommand coverage.
Output: research/reference-paper-analysis.md
"
```

**Repository Survey**:
```bash
wg add "survey-repo-structure" -d "
Comprehensive analysis of current manuscript state:
- Read all sections/ files for content assessment
- Identify gaps, placeholders, incomplete sections  
- Analyze current argument structure and flow
- Note existing experimental references and figure placeholders
- Document current bibliography state
- Assess alignment with Bioinformatics format requirements

Output: Current manuscript assessment with specific improvement recommendations.
"
```

### Phase 2: Experimental Validation (After Setup)

**Core Experiments** (parallel after set-up-experiment):

```bash
wg add "experiment-transitive-reach" --after set-up-experiment -d "
Demonstrate transitive coordinate projection capability.
Work in: experiments/yeast-chrV/

Design:
1. Select test coordinate range on S. cerevisiae chrV  
2. Use impg to project coordinates transitively across all 7 yeast strains
3. Compare direct vs. transitive coverage expansion
4. Measure projection accuracy and completeness
5. Time projection operations (should be sub-second)

Key metrics: coverage expansion factor, projection time, accuracy validation.
Validates core 'liftover at population scale' capability.
"

wg add "experiment-on-demand" --after set-up-experiment -d "
Demonstrate on-demand graph materialization capability.
Work in: experiments/yeast-chrV/

Design:
1. Select regions of varying size (1kb, 5kb, 10kb)
2. Use impg to materialize graphs for each region
3. Compare graph construction engines (seqwish, POA, recursive)
4. Measure time and memory for each materialization
5. Generate GFA output and validate structure
6. Use odgi for graph visualization/statistics

Validates 'query before you build' paradigm — show sub-second region → graph.
"

wg add "experiment-partitioning-demonstration" --after set-up-experiment -d "
Demonstrate alignment-based pangenome partitioning.
Work in: experiments/yeast-full/

Design:
1. Use impg to partition full yeast pangenome along connectivity
2. Analyze partition size distribution
3. Show how partitioning follows biological structure (chromosomes, repeat regions)
4. Compare partition boundaries to known genomic features
5. Demonstrate partition-based parallel processing

Validates decomposition capability for scalable analysis.
"

wg add "experiment-yeast-full" --after set-up-experiment -d "
Full-scale validation on complete yeast dataset.
Work in: experiments/yeast-full/

Design:
1. Run complete IMPG workflow on all 7 yeast genomes
2. Benchmark memory usage and runtime
3. Compare to traditional graph construction approaches
4. Validate large-scale coordinate projection accuracy
5. Test batch processing capabilities

Validates production-scale applicability.
"
```

**Scaling Analysis**:
```bash
wg add "experiment-scaling-curve" --after experiment-yeast-full -d "
Generate performance scaling curves for paper.
Work in: experiments/scaling/

Design:
1. Test IMPG performance across varying genome counts (2, 5, 10, 25, 50+ genomes)
2. Measure time and memory scaling for key operations:
   - Coordinate projection
   - Graph materialization  
   - Partitioning computation
3. Compare against baseline approaches where applicable
4. Generate scaling curve data for publication figures

Critical for demonstrating computational advantages.
"
```

### Phase 3: Figure Generation (After Experiments)

```bash
wg add "generate-paper-figures" --after experiment-transitive-reach,experiment-on-demand,experiment-partitioning-demonstration,experiment-yeast-full,experiment-scaling-curve -d "
Generate publication-quality figures from experimental results.
Work in: fig/

Create figures:
1. Conceptual overview (alignment space → implicit graph)
2. Scaling curves (genomes vs. time/memory)
3. Transitive reach demonstration (coverage expansion)
4. Partitioning results (size distribution, biological boundaries)  
5. On-demand materialization (region → graph workflow)

Requirements:
- PDF format for LaTeX inclusion
- Publication quality (proper fonts, labels, legends)
- Save generation scripts alongside figures
- Document all figure filenames and descriptions

Feeds into: update-figures-section and all manuscript rewriting.
"
```

### Phase 4: Manuscript Writing (After Research and Figures)

**Section Rewrites** (parallel after research-reference-papers AND generate-paper-figures):

```bash
wg add "rewrite-introduction-section" --after research-reference-papers,generate-paper-figures -d "
Rewrite sections/01.introduction.tex for Bioinformatics format.
ONLY modify sections/01.introduction.tex.

Guidelines:
- Open with pangenome graph construction cost problem
- Position alignments as existing pangenome representation 
- Lead with key results early (laptop-scale, sub-second queries)
- Frame projection/partitioning/materialization as unified capability
- Match tone of ODGI/unbiased pangenome papers
- Mathematical clarity where appropriate
- Tight, concise Bioinformatics style

Use research/reference-paper-analysis.md for structural guidance.
"

wg add "rewrite-methods-section" --after research-reference-papers,generate-paper-figures -d "
Rewrite sections/02.methods-overview.tex for Bioinformatics format.
ONLY modify sections/02.methods-overview.tex.

Cover:
- Alignment space formalization 
- Transitive projection algorithm
- Partitioning methodology
- On-demand materialization approach
- Implementation details (impg subcommands)

Balance conceptual explanation with algorithmic precision.
Reference generated figures appropriately.
"

wg add "rewrite-results-section" --after research-reference-papers,generate-paper-figures -d "
Rewrite sections/03.results.tex with experimental validation.
ONLY modify sections/03.results.tex.

Present:
- Transitive projection results and validation
- Scaling curve analysis
- Partitioning performance and biological relevance
- On-demand materialization benchmarks
- Comparison to existing tools where applicable

Reference all generated figures. Include concrete performance numbers.
"

wg add "rewrite-discussion-section" --after research-reference-papers,generate-paper-figures -d "
Rewrite sections/04.discussion.tex with broader implications.
ONLY modify sections/04.discussion.tex.

Address:
- Significance for pangenomics field
- Relationship to existing graph construction pipelines
- Scalability implications for population-scale analysis
- Limitations and future directions
- Integration with current workflows (PGGB, etc.)

Position IMPG as complementary infrastructure, not replacement.
"
```

**Figure Section Update**:
```bash
wg add "update-figures-section" --after generate-paper-figures -d "
Update sections/06.figures.tex with generated figures.
ONLY modify sections/06.figures.tex.

Tasks:
- Include all generated PDF figures from fig/
- Write descriptive captions for each figure  
- Ensure proper LaTeX figure formatting
- Cross-reference figures appropriately in text
- Order figures logically (concept → results → analysis)

Must match figures created in generate-paper-figures task.
"
```

### Phase 5: Integration and Finalization

```bash
wg add "integrate-manuscript-cross" --after rewrite-introduction-section,rewrite-methods-section,rewrite-results-section,rewrite-discussion-section,update-figures-section -d "
Integration pass over complete rewritten manuscript.

Tasks:
1. Read ALL section files and main.tex
2. Check cross-references: all \\ref{} and \\cite{} resolve
3. Verify narrative flow between sections
4. Check terminology and notation consistency
5. Update bibliography.bib for new citations
6. Build PDF: pdflatex main && bibtex main && pdflatex main && pdflatex main
7. Fix any build errors
8. Document remaining issues and next steps

First complete build of rewritten paper. Commit integrated manuscript.
"
```

## Validation Workflows

Each major task should include embedded validation criteria:

**Experiment Tasks**:
- Validate data integrity before processing
- Time all operations for performance reporting
- Generate reproducible output files
- Log all results with `wg artifact` and `wg log`

**Writing Tasks**:
- Verify section builds in LaTeX context
- Check all references resolve
- Validate figure citations match generated files
- Ensure Bioinformatics format compliance

**Integration Tasks**:
- Full document compilation without errors
- All placeholders filled with actual results
- Cross-references validated across sections

## Dependencies and Parallelization

**Parallel Blocks**:

1. **Setup Phase**: set-up-experiment, research-reference-papers, survey-repo-structure
2. **Experiments**: All experiment-* tasks (after set-up-experiment)  
3. **Writing**: All rewrite-* tasks (after research-reference-papers AND generate-paper-figures)

**Sequential Dependencies**:

- generate-paper-figures ← ALL experiments complete
- integrate-manuscript-cross ← ALL writing tasks complete
- experiment-scaling-curve ← experiment-yeast-full (needs baseline for comparison)

**Critical Path**: set-up-experiment → experiments → generate-paper-figures → writing → integration

## Implementation Conventions

**Experiment Directory Structure**:
```
experiments/<experiment-name>/
├── README.md              # Experiment description and methodology
├── run.sh                 # Execution script
├── data/                  # Input data (decompressed, prepared)
├── results/               # Output files
└── analysis/              # Analysis scripts and figures
```

**File Naming**:
- Experiment outputs: `results/<metric>_<condition>.txt`
- Figures: `fig/<type>_<subject>.pdf` 
- Analysis: `analysis/<experiment>_analysis.py/R`

**Git Management**:
- Commit experiment scripts and documentation
- Use `wg artifact` for large intermediate data
- experiments/ in .gitignore for size management
- Commit final figures to fig/

**Documentation**:
- Log all major results with `wg log`
- Preserve analysis rationale in experiment READMEs
- Reference data paths absolutely for reproducibility

## Quality Gates

**Before Moving to Next Phase**:

1. **Setup → Experiments**: All test data accessible, impg builds successfully
2. **Experiments → Figures**: All experiments completed with recorded results
3. **Figures → Writing**: All figure PDFs generated and saved to fig/
4. **Writing → Integration**: All sections rewritten and individually validated

**Final Validation**:
- Complete manuscript builds without errors
- All figures referenced and display correctly  
- Bibliography complete and properly formatted
- Experimental claims backed by recorded data
- Ready for submission to Bioinformatics

## Recovery Patterns

**If Task Fails**:
- Check dependencies: are prerequisite outputs available?
- Validate environment: does impg binary work?  
- Check data paths: are test datasets accessible?
- Resource constraints: sufficient memory/storage for large experiments?

**If Integration Fails**:
- Incremental build: test individual sections first
- Cross-reference audit: missing citations or figures
- Format validation: LaTeX compliance for Bioinformatics template

---

**Usage**: Provide this document to a fresh workgraph coordinator to recreate the complete IMPG paper task graph. Each section contains sufficient detail for generating concrete `wg add` commands with proper dependencies and validation criteria.

The resulting task graph will produce a publication-ready manuscript for Bioinformatics, with complete experimental validation and publication-quality figures.
