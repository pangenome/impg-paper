# Memory

## Rules
- The user does not want workgraph (wg) in this project (2026-11-08). Use the Workflow tool for multi-agent work.
- Never overwrite sections/*.tex: they hold uncommitted user changes. New drafts go in a new directory.
- Use /home/guarracino/git/impg for facts about impg, not the outdated ./impg submodule.

## Verified facts
- HPRC release 2 data exists in /home/guarracino/git/impg/data/hprcv2 (AGC archive HPRC_r2_assemblies_0.6.1.agc, GRCh38-anchored PAF and TPA files with .impg indexes).
- ODGI DOI is 10.1093/bioinformatics/btac308 (Shredtools prints btac213, which is an unrelated paper).
- impg HEAD builds wfmash commit 9b2a738 (through sweepga 4713ce0 and wfmash-rs 07ed9a3).
- The current draft lives in drafts/bioinformatics-2026-11/; build with ./build.sh.
