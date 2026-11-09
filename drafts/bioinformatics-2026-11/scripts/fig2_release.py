#!/usr/bin/env python3
"""Fig. 2: the HPRC release 2 TPA files as an alignment network.

Inputs, relative to the draft folder (the parent of scripts/):
  data/s3_tpas.xml      anonymous S3 listing of
                        s3://human-pangenomics/pangenomes/freeze/release2/impg/tpas/
  data/strtab/*.bin.gz  first bytes of each TPA file, cut after its string table
  data/partners.tsv     earlier census (stem, records, strings, names, haplotypes),
                        used only as a cross-check
Output: fig/fig2_release.pdf, and every plotted number on stdout.

  python3 -I scripts/fig2_release.py              # draw the figure
  python3 -I scripts/fig2_release.py --prep DIR   # cut DIR/<stem>.bin into data/strtab
"""
import gzip, os, re, struct, sys
import statistics as st
import xml.etree.ElementTree as ET
from collections import Counter

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, FIG = os.path.join(ROOT, "data"), os.path.join(ROOT, "fig")
SUFFIX = ".merged.edit-distance.128.tpa"
REFS = ("GRCh38#", "CHM13#")
PANSN = re.compile(r"^([^#]+#[0-9]+)#\S+$")
TPT = ["Standard", "Mixed", "Variable", "Fastga", "FastgaNoDiff"]
METRIC = ["edit-distance", "diagonal-distance"]
DIST = {0: ("edit", 0), 1: ("gap-affine", 3), 2: ("gap-affine-2p", 5)}
BLUE, ORANGE, INK, MUTED = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e"


def die(msg):
    sys.exit(f"ERROR: {msg}")


def varint(b, i):
    v = s = 0
    while True:
        c = b[i]
        i += 1
        v |= (c & 0x7F) << s
        s += 7
        if c < 0x80:
            return v, i


def parse_tpa_prefix(b, stem):
    # layout from tpa crate src/format.rs
    if b[:4] != b"TPA\0":
        die(f"{stem}: bad magic {b[:4]!r}")
    if b[4] != 1:
        die(f"{stem}: TPA version {b[4]}, only version 1 is parsed")
    try:
        nrec, i = varint(b, 5)
        nstr, i = varint(b, i)
        tpt, met = b[i + 2], b[i + 3]
        maxc, i = varint(b, i + 4)
        if b[i] not in DIST:
            die(f"{stem}: unknown distance code {b[i]}")
        dname, npar = DIST[b[i]]
        pars = struct.unpack_from(f"<{npar}i", b, i + 1)
        i += 1 + 4 * npar
        if b[i] not in (0, 1):
            die(f"{stem}: bad all-records flag {b[i]}")
        i += 1
        names = []
        for _ in range(nstr):
            n, i = varint(b, i)
            if i + n > len(b):
                raise IndexError(f"name {len(names) + 1} of {nstr} ends past the prefix")
            names.append(b[i:i + n].decode())
            _, i = varint(b, i + n)
    except (IndexError, struct.error, UnicodeDecodeError) as e:
        die(f"{stem}: truncated or corrupt header or string table: {e}")
    return dict(nrec=nrec, nstr=nstr, tpt=TPT[tpt] if tpt < len(TPT) else tpt,
                met=METRIC[met] if met < len(METRIC) else met, maxc=maxc,
                dist=(dname,) + pars, names=names, end=i)


def prep_prefixes(raw):
    # keep bytes up to string table end
    out = os.path.join(DATA, "strtab")
    os.makedirs(out, exist_ok=True)
    fns = sorted(f for f in os.listdir(raw) if f.endswith(".bin"))
    print(f"prep: {len(fns)} prefixes from {raw} into {out}")
    for fn in fns:
        b = open(os.path.join(raw, fn), "rb").read()
        t = parse_tpa_prefix(b, fn)
        with open(os.path.join(out, fn + ".gz"), "wb") as fh, \
                gzip.GzipFile(fileobj=fh, mode="wb", mtime=0) as gz:
            gz.write(b[:t["end"]])
        print(f"prep\t{fn}\tprefix {len(b)}\tkept {t['end']}\tstrings {t['nstr']}")


def read_s3_sizes(path):
    ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    root = ET.parse(path).getroot()
    if root.findtext("s3:IsTruncated", namespaces=ns) != "false":
        die(f"{path}: listing is truncated")
    sizes = {}
    for c in root.findall("s3:Contents", ns):
        key = c.findtext("s3:Key", namespaces=ns)
        if not key.endswith(SUFFIX):
            die(f"{path}: unexpected key {key}")
        sizes[os.path.basename(key)[:-len(SUFFIX)]] = int(c.findtext("s3:Size", namespaces=ns))
    kc = root.findtext("s3:KeyCount", namespaces=ns)
    if kc is not None and int(kc) != len(sizes):
        die(f"{path}: KeyCount {kc} but {len(sizes)} keys parsed")
    print(f"input {path}: {len(sizes)} keys, KeyCount {kc}")
    return sizes


def own_haplotype(stem):
    # target haplotype from the file name
    if stem.startswith("GCA_"):
        return "GRCh38#0"
    if stem.startswith("chm13"):
        return "CHM13#0"
    if stem.startswith("hg002"):
        return "HG002#1" if ".pat" in stem else "HG002#2"
    s, h = stem.split("_")[:2]
    if h not in ("hap1", "hap2", "pat", "mat"):
        die(f"{stem}: cannot name the target haplotype")
    return s + "#" + ("1" if h in ("hap1", "pat") else "2")


def spread(v):
    # partner_summary.txt indices, then median
    v, m = sorted(v), len(v)
    return (f"min {v[0]} p10 {v[int(0.1 * (m - 1))]} p50 {v[(m - 1) // 2]} "
            f"p90 {v[int(0.9 * (m - 1))]} max {v[-1]} mean {sum(v) / m:.4f} median {st.median(v)}")


def load_release():
    sizes = read_s3_sizes(os.path.join(DATA, "s3_tpas.xml"))
    d = os.path.join(DATA, "strtab")
    stems = sorted(f[:-len(".bin.gz")] for f in os.listdir(d) if f.endswith(".bin.gz"))
    print(f"input {d}: {len(stems)} string-table prefixes")
    if set(stems) != set(sizes):
        die(f"stems differ: only S3 {sorted(set(sizes) - set(stems))[:5]}, "
            f"only strtab {sorted(set(stems) - set(sizes))[:5]}")
    rel = {}
    for stem in stems:
        b = gzip.open(os.path.join(d, stem + ".bin.gz"), "rb").read()
        t = parse_tpa_prefix(b, stem)
        if t["end"] != len(b):
            die(f"{stem}: {len(b) - t['end']} bytes after the string table")
        haps = set()
        for n in t["names"]:
            m = PANSN.match(n)
            if not m:
                die(f"{stem}: name is not PanSN: {n!r}")
            haps.add(m.group(1))
        own = own_haplotype(stem)
        if own not in haps:
            die(f"{stem}: target haplotype {own} is not in its string table")
        rel[stem] = dict(t, haps=haps, own=own, partners=haps - {own}, bytes=sizes[stem])
    owns = Counter(r["own"] for r in rel.values())
    if len(owns) != len(rel):
        die(f"target haplotype shared by files: {[h for h, c in owns.items() if c > 1]}")
    return rel


def check_census(rel):
    # compare with the earlier partners.tsv census
    path = os.path.join(DATA, "partners.tsv")
    rows = [l.rstrip("\n").split("\t") for l in open(path)]
    print(f"input {path}: {len(rows)} rows")
    if {r[0] for r in rows} != set(rel):
        die("partners.tsv stems differ from the string-table stems")
    diff = []
    for stem, nrec, nstr, got, nh in rows:
        r = rel[stem]
        if (int(nrec), int(nstr)) != (r["nrec"], r["nstr"]):
            die(f"{stem}: partners.tsv records/strings {nrec}/{nstr} vs header {r['nrec']}/{r['nstr']}")
        if int(got) != r["nstr"] or int(nh) != len(r["haps"]):
            diff.append(f"{stem} names {got} vs {r['nstr']}, haplotypes {nh} vs {len(r['haps'])}")
    print(f"partners.tsv rows that differ from the parsed string tables: {len(diff)}")
    for x in diff:
        print("  " + x)


def describe_release(rel):
    print("files", len(rel), "bytes", sum(r["bytes"] for r in rel.values()),
          "records", sum(r["nrec"] for r in rel.values()),
          "strings", sum(r["nstr"] for r in rel.values()))
    enc = Counter((r["tpt"], r["met"], r["maxc"], r["dist"]) for r in rel.values())
    print("encoding (tracepoint type, metric, max complexity, distance):", dict(enc))
    grp = Counter("hprc_r2" if "_hprc_r2_" in s else "genbank" if s.endswith("genbank")
                  else "hg002" if s.startswith("hg002") else "reference" for s in rel)
    smp = {s.split("_")[0] for s in rel if "_hprc_r2_" in s}
    print("composition", dict(grp), "hprc_r2 samples", len(smp))
    for s, r in rel.items():
        if r["own"].startswith(REFS):
            print(f"reference {r['own']}: bytes {r['bytes']} records {r['nrec']} partners {len(r['partners'])}")


def network_numbers(rel):
    n = len(rel)
    edges = {(r["own"], q) for r in rel.values() for q in r["partners"]}
    print("ordered pairs", len(edges), "of", n * (n - 1), "= %.4f%%" % (100 * len(edges) / (n * (n - 1))))
    asm = [r for r in rel.values() if not r["own"].startswith(REFS)]
    print("assembly files", len(asm), "partners", spread([len(r["partners"]) for r in asm]))
    print("assembly files, non-reference partners only",
          spread([sum(not q.startswith(REFS) for q in r["partners"]) for r in asm]))
    k = len(asm)
    tot = sum(len(r["partners"]) for r in asm)
    print("nonref pairs", tot, "of", k * (n - 1), "= %.4f%%" % (100 * tot / (k * (n - 1))))
    recip = sum((q, t) in edges for t, q in edges)
    und = {tuple(sorted(e)) for e in edges}
    print("ordered pairs present in both files", recip, "unordered", recip // 2)
    print("unordered pairs", len(und), "of", n * (n - 1) // 2, "= %.4f%%" % (200 * len(und) / (n * (n - 1))))
    for ref in ("GRCh38#0", "CHM13#0"):
        print(f"assembly files listing {ref}", sum(ref in r["partners"] for r in asm), "of", k)
    nr = {e for e in und if not any(x.startswith(REFS) for x in e)}
    print("non-reference unordered pairs", len(nr), "of", k * (k - 1) // 2,
          "= %.4f%%" % (200 * len(nr) / (k * (k - 1))))
    adj = {}
    for a, c in nr:
        adj.setdefault(a, set()).add(c)
        adj.setdefault(c, set()).add(a)
    if len(adj) != k:
        die(f"non-reference network has {len(adj)} nodes, expected {k}")
    r1, r2 = [], []
    for s, h1 in adj.items():
        h2 = set().union(h1, *(adj[x] for x in h1)) - {s}
        r1.append(len(h1))
        r2.append(len(h2))
    print(f"non-reference reach of {k - 1}: 1 hop", spread(r1))
    print(f"non-reference reach of {k - 1}: 2 hops", spread(r2))
    return asm, r1, r2


def draw_figure(rel, asm, r1, r2):
    plt.rcParams.update({"font.size": 7, "pdf.fonttype": 42, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.edgecolor": MUTED})
    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.4), constrained_layout=True)
    # a: partners per assembly file
    p = [len(r["partners"]) for r in asm]
    h = Counter(p)
    print("panel a histogram (partners: files)", dict(sorted(h.items())))
    ax[0].bar(sorted(h), [h[x] for x in sorted(h)], width=0.8, color=BLUE)
    ax[0].axvline(st.median(p), color=INK, lw=0.8, ls="--")
    ax[0].text(st.median(p) + 1, max(h.values()), f"median {st.median(p):g}", va="top", color=INK)
    ax[0].set(xlabel="Partner haplotypes per assembly file", ylabel="TPA files", xlim=(0, None))
    # b: bytes against records, log axes
    for refs, col, lab in ((False, BLUE, "assembly"), (True, ORANGE, "reference")):
        rr = [r for r in rel.values() if r["own"].startswith(REFS) == refs]
        ax[1].scatter([r["nrec"] for r in rr], [r["bytes"] / 1e6 for r in rr], s=8, color=col,
                      edgecolors="white", linewidths=0.3, label=f"{lab} ({len(rr)})")
    for r in rel.values():
        if r["own"].startswith(REFS):
            ax[1].annotate(r["own"].split("#")[0], (r["nrec"], r["bytes"] / 1e6),
                           xytext=(-4, 0), textcoords="offset points", ha="right", va="center")
    bpr = [r["bytes"] / r["nrec"] for r in rel.values()]
    print("panel b bytes per record", spread([round(x, 2) for x in bpr]))
    print("panel b assembly bytes", spread([r["bytes"] for r in asm]))
    print("panel b assembly records", spread([r["nrec"] for r in asm]))
    ax[1].set(xscale="log", yscale="log", xlabel="Alignment records per file (millions)",
              ylabel="File size (MB)")
    for axis, ticks in ((ax[1].xaxis, (0.5e6, 1e6, 2e6, 5e6, 1e7)), (ax[1].yaxis, (30, 50, 100, 200, 500))):
        axis.set_minor_locator(matplotlib.ticker.NullLocator())
        axis.set_ticks(ticks, [f"{t / 1e6:g}" if t >= 1e5 else f"{t:g}" for t in ticks])
    ax[1].legend(frameon=False, loc="lower right")
    # c: reach without the references
    for y, v, lab in ((1, r1, "1 hop"), (0, r2, "2 hops")):
        jit = [y + 0.25 * ((i * 0.6180339887) % 1 - 0.5) for i in range(len(v))]
        ax[2].scatter(v, jit, s=4, color=BLUE, alpha=0.5, linewidths=0)
        txt = (f"{lab}: all {len(v)} reach {v[0]}" if min(v) == max(v)
               else f"{lab}: {min(v)} to {max(v)}, median {st.median(v):g}")
        ax[2].text(5, y + 0.2, txt, ha="left", va="bottom", color=INK)
    h1 = Counter(r1)
    print("panel c 1-hop histogram (reach: haplotypes)", dict(sorted(h1.items())))
    print("panel c 2-hop histogram (reach: haplotypes)", dict(sorted(Counter(r2).items())))
    k = len(asm) - 1
    ax[2].axvline(k, color=MUTED, lw=0.8, ls=":")
    ax[2].set(xlim=(0, k + 15), ylim=(-0.5, 1.7), yticks=[0, 1], yticklabels=["2 hops", "1 hop"],
              xlabel=f"Haplotypes reached (of {k})")
    for a, letter in zip(ax, "abc"):
        a.set_title(letter, loc="left", fontweight="bold")
    os.makedirs(FIG, exist_ok=True)
    out = os.path.join(FIG, "fig2_release.pdf")
    fig.savefig(out)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--prep":
        prep_prefixes(sys.argv[2])
        return
    if len(sys.argv) != 1:
        die(__doc__)
    rel = load_release()
    check_census(rel)
    describe_release(rel)
    asm, r1, r2 = network_numbers(rel)
    draw_figure(rel, asm, r1, r2)


if __name__ == "__main__":
    main()
