# -*- coding: utf-8 -*-
"""Generate figure1: the corpus as a library-by-class matrix.

Reads corpus_cross_library.csv (the single source of the corpus) and emits
figure1_class_by_library.svg next to this script. Re-run after any change to the
CSV so the figure cannot drift from the data.
"""
import csv, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(HERE, "..", "corpus_cross_library.csv"))
OUT = os.path.join(HERE, "figure1_class_by_library.svg")

with open(CSV_PATH, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

LIBS = ["RDFLib", "RDF4J", "N3.js", "Oxigraph", "dotNetRDF", "jsonld.js"]
LANG = {"RDFLib": "Python", "RDF4J": "Java", "N3.js": "JavaScript",
        "Oxigraph": "Rust", "dotNetRDF": "C#", "jsonld.js": "JavaScript"}
CLASSES = ["C%d" % i for i in range(1, 11)]
CLASS_NAME = {
    "C1": "literal escaping / token boundary", "C2": "IRI / IRIREF", "C3": "namespace / prefix",
    "C4": "round-trip fidelity", "C5": "format mislabelling", "C6": "blank nodes",
    "C7": "control chars / Unicode", "C8": "JSON-LD context", "C9": "RDF/XML escaping",
    "C10": "export validation (property)",
}

mat = defaultdict(int)
for r in rows:
    mat[(r["library"], r["class"])] += 1

FILL = {0: "#f2f4f7", 1: "#bcd6f0", 2: "#7fb0e0", 3: "#4a86c8"}
TEXT = {0: "#9aa4b0", 1: "#12283f", 2: "#0d1f30", 3: "#ffffff"}

LAB_W, TOP, CW, CH, PADX, PADY = 118, 96, 54, 34, 14, 8


def cell_count(lib, cls):
    return mat.get((lib, cls), 0)


width = PADX + LAB_W + CW * len(CLASSES) + PADX
lib_h = 30
height = TOP + len(LIBS) * (CH + 12) + lib_h + PADY * 4 + 10

p = []
p.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Helvetica, Arial, sans-serif">' % (width, height, width, height))
p.append('<rect width="100%" height="100%" fill="#ffffff"/>')
n_total = sum(mat.values())
p.append('<text x="%d" y="34" font-size="15" font-weight="bold" fill="#111">Fig. 1 — the %d cross-library records as a library-by-class matrix</text>' % (PADX, n_total))
p.append('<text x="%d" y="55" font-size="11.5" fill="#556">Cell shading is the number of records; darker means more. Generated from corpus_cross_library.csv.</text>' % PADX)
p.append('<text x="%d" y="72" font-size="11.5" fill="#556">The blank cells show where the corpus is thin, not where the class is absent in the wild (see paper §6.6).</text>' % PADX)

# column headers
x0 = PADX + LAB_W
for j, c in enumerate(CLASSES):
    cx = x0 + j * CW + CW / 2.0
    p.append('<text x="%.1f" y="%d" font-size="12.5" font-weight="bold" fill="#222" text-anchor="middle">%s</text>' % (cx, TOP - 26, c))
    name = CLASS_NAME[c]
    parts = name.split(" / ")
    for k, seg in enumerate(parts[:2]):
        p.append('<text x="%.1f" y="%d" font-size="8.6" fill="#667" text-anchor="middle">%s</text>' % (cx, TOP - 14 + k * 10, seg))

# class totals
totals = {c: sum(cell_count(l, c) for l in LIBS) for c in CLASSES}

for i, lib in enumerate(LIBS):
    y = TOP + i * (CH + 12)
    p.append('<text x="%d" y="%d" font-size="12.5" fill="#111">%s</text>' % (PADX, y + 21, lib))
    p.append('<text x="%d" y="%d" font-size="9.5" fill="#778">%s</text>' % (PADX, y + 32, LANG[lib]))
    for j, c in enumerate(CLASSES):
        cx = x0 + j * CW
        n = cell_count(lib, c)
        p.append('<rect x="%.1f" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="#d7dde5"/>' % (cx + 3, y + 4, CW - 6, CH, FILL[n]))
        if n:
            p.append('<text x="%.1f" y="%d" font-size="13" font-weight="bold" fill="%s" text-anchor="middle">%d</text>' % (cx + CW / 2.0, y + 4 + CH / 2.0 + 4.5, TEXT[n], n))

# totals row
ty = TOP + len(LIBS) * (CH + 12) + 4
p.append('<text x="%d" y="%d" font-size="11.5" font-weight="bold" fill="#222">all libraries</text>' % (PADX, ty + 20))
for j, c in enumerate(CLASSES):
    cx = x0 + j * CW + CW / 2.0
    p.append('<text x="%.1f" y="%d" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">%d</text>' % (cx, ty + 20, totals[c]))
p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#cfd6de"/>' % (PADX, ty + 6, width - PADX, ty + 6))

# legend
ly = ty + 44
p.append('<text x="%d" y="%d" font-size="10.5" fill="#556">records:</text>' % (PADX, ly + 12))
for k, n in enumerate([0, 1, 2, 3]):
    lx = PADX + 62 + k * 46
    p.append('<rect x="%d" y="%d" width="18" height="15" rx="3" fill="%s" stroke="#d7dde5"/>' % (lx, ly, FILL[n]))
    p.append('<text x="%d" y="%d" font-size="10.5" fill="#556">%d</text>' % (lx + 24, ly + 12, n))
p.append('<text x="%d" y="%d" font-size="10.5" fill="#556">C10 has no third-party record; C4 has one (RDFLib #3426); the Semantica case carries the only two C10 records (paper §6.6).</text>' % (PADX, ly + 30))
p.append('</svg>')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(p))

print("wrote", OUT)
print("matrix:")
for lib in LIBS:
    print("  %-12s" % lib, [cell_count(lib, c) for c in CLASSES])
print("  totals      ", [totals[c] for c in CLASSES], "sum =", sum(totals.values()))
