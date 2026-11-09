import sys, re
# count PanSN haplotypes in a TPA string table prefix
for path in sys.argv[1:]:
    b = open(path, "rb").read()
    names = re.findall(rb"[A-Za-z0-9_.\-]+#[0-9]+#[\x21-\x7e]+", b)
    haps = sorted({b"#".join(n.split(b"#")[:2]).decode() for n in names})
    print(f"{path}\tnames {len(names)}\thaps {len(haps)}\tfirst {haps[:3]}", file=sys.stdout)
