#!/usr/bin/env python3
# Pair graph of the HPRC r2 TPA release
# usage: python3 -I pairs.py <nm_article dir>
import os, re, sys, statistics as st
from collections import Counter

base = sys.argv[1]
hdr = {}
for line in open(os.path.join(base, "tpa_headers_shared.tsv")):
    f = line.rstrip("\n").split("\t")
    try:
        hdr[f[0].replace(".merged.edit-distance.128.tpa", "")] = int(f[3])
    except (IndexError, ValueError) as e:
        print("skip header line:", line.strip()[:80], e, file=sys.stderr)

def own_hap(k):
    # target haplotype from file name
    if k.startswith("GCA_"): return b"GRCh38#0"
    if k.startswith("chm13"): return b"CHM13#0"
    if k.startswith("hg002"): return b"HG002#1" if ".pat" in k else b"HG002#2"
    s, h = k.split("_")[:2]
    return (s + "#" + ("1" if h in ("hap1", "pat") else "2")).encode()

d = os.path.join(base, "strtab")
edges, miss, short = set(), 0, 0
for fn in sorted(os.listdir(d)):
    k = fn[:-4]
    b = open(os.path.join(d, fn), "rb").read()
    names = re.findall(rb"[A-Za-z0-9_.\-]+#[0-9]+#[\x21-\x7e]+", b)
    if len(names) < hdr[k]: short += 1
    names = names[:hdr[k]]
    haps = {b"#".join(n.split(b"#")[:2]) for n in names}
    t = own_hap(k)
    if t not in haps: miss += 1
    edges |= {(t, q) for q in haps if q != t}
print("files", len(os.listdir(d)), "string tables shorter than header", short, "target missing", miss, file=sys.stderr)
refs = (b"GRCh38", b"CHM13")
und = {tuple(sorted(e)) for e in edges}
recip = sum(1 for (t, q) in edges if (q, t) in edges)
print("ordered pairs", len(edges), "of", 466 * 465, "= %.4f%%" % (100 * len(edges) / (466 * 465)))
print("ordered pairs present in both files", recip)
print("unordered pairs", len(und), "of", 466 * 465 // 2, "= %.4f%%" % (100 * len(und) / (466 * 465 / 2)))
asm = [k for k in os.listdir(d) if not k.startswith(("GCA_", "chm13"))]
print("assembly files listing GRCh38#0", sum(1 for (t, q) in edges if q == b"GRCh38#0" and not t.startswith(refs)),
      "listing CHM13#0", sum(1 for (t, q) in edges if q == b"CHM13#0" and not t.startswith(refs)), "of", len(asm))
nr = {e for e in und if not any(x.startswith(refs) for x in e)}
print("non-reference unordered pairs", len(nr), "of", 464 * 463 // 2, "= %.4f%%" % (100 * len(nr) / (464 * 463 / 2)))
adj = {}
for a, c in nr:
    adj.setdefault(a, set()).add(c); adj.setdefault(c, set()).add(a)
deg = sorted(len(v) for v in adj.values())
print("non-reference degree min", deg[0], "median", st.median(deg), "max", deg[-1], "nodes", len(deg))
r1, r2 = [], []
for s, h1 in adj.items():
    h2 = set().union(*(adj[x] for x in h1)) | h1
    h2.discard(s)
    r1.append(len(h1)); r2.append(len(h2))
print("non-reference haplotypes reached of 463 without references: 1 hop min", min(r1), "median", st.median(r1),
      "; 2 hops min", min(r2), "median", st.median(r2))
