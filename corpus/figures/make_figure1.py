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

LIBS = ["RDFLib", "RDF4J", "N3.js", "Oxigraph", "dotNetRDF"]
LANG = {"RDFLib": "Python", "RDF4J": "Java", "N3.js": "JavaScript",
        "Oxigraph": "Rust", "dotNetRDF": "C#", "jsonld.js": "JavaScript"}
CLASSES = ["C%d" % i for i in range(1, 11)]
# Short column headings. The full criteria are in section 5 of the paper. Each
# heading is kept to at most two lines of ten characters, which is what the
# column width below can hold without two headings colliding.
CLASS_HEAD = {
    "C1": ["literal", "escaping"], "C2": ["IRI", "IRIREF"],
    "C3": ["namespace", "prefix"], "C4": ["round-trip", "fidelity"],
    "C5": ["format", "mislabelled"], "C6": ["blank nodes"],
    "C7": ["control", "chars"], "C8": ["JSON-LD", "context"],
    "C9": ["RDF/XML", "escaping"], "C10": ["export", "validation"],
}

mat = defaultdict(int)
for r in rows:
    mat[(r["library"], r["class"])] += 1

FILL = {0: "#f2f4f7", 1: "#bcd6f0", 2: "#7fb0e0", 3: "#4a86c8"}
TEXT = {0: "#9aa4b0", 1: "#12283f", 2: "#0d1f30", 3: "#ffffff"}

# Layout. The block below the matrix (rule, totals, legend) is positioned so
# that nothing runs off the bottom or the right edge of the canvas.
LAB_W, CW, CH, PADX, PADY = 118, 54, 34, 14, 8
TITLE_Y, SUB1_Y, SUB2_Y = 26, 44, 59
HDR_ID_Y, HDR_L1_Y = 86, 97
TOP = 118                      # top edge of the first data row
ROW_H = CH + 12


def cell_count(lib, cls):
    return mat.get((lib, cls), 0)


width = PADX + LAB_W + CW * len(CLASSES) + PADX
rows_bottom = TOP + len(LIBS) * ROW_H
rule_y = rows_bottom + 4
totals_y = rule_y + 20
legend_y = rule_y + 44
note_y = legend_y + 30
height = note_y + PADY + 8

p = []
p.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Helvetica, Arial, sans-serif">' % (width, height, width, height))
p.append('<rect width="100%" height="100%" fill="#ffffff"/>')
n_total = sum(mat.values())
p.append('<text x="%d" y="%d" font-size="15" font-weight="bold" fill="#111">Fig. 1 — the %d cross-library records as a library-by-class matrix</text>' % (PADX, TITLE_Y, n_total))
p.append('<text x="%d" y="%d" font-size="11.5" fill="#556">Cell shading is the number of records; darker means more. Generated from corpus_cross_library.csv.</text>' % (PADX, SUB1_Y))
p.append('<text x="%d" y="%d" font-size="11.5" fill="#556">The blank cells show where the corpus is thin, not where the class is absent in the wild (see paper §6.6).</text>' % (PADX, SUB2_Y))

# column headers
x0 = PADX + LAB_W
for j, c in enumerate(CLASSES):
    cx = x0 + j * CW + CW / 2.0
    p.append('<text x="%.1f" y="%d" font-size="12.5" font-weight="bold" fill="#222" text-anchor="middle">%s</text>' % (cx, HDR_ID_Y, c))
    for k, seg in enumerate(CLASS_HEAD[c]):
        p.append('<text x="%.1f" y="%d" font-size="8.4" fill="#667" text-anchor="middle">%s</text>' % (cx, HDR_L1_Y + k * 10, seg))

# class totals
totals = {c: sum(cell_count(l, c) for l in LIBS) for c in CLASSES}

for i, lib in enumerate(LIBS):
    y = TOP + i * ROW_H
    p.append('<text x="%d" y="%d" font-size="12.5" fill="#111">%s</text>' % (PADX, y + 21, lib))
    p.append('<text x="%d" y="%d" font-size="9.5" fill="#778">%s</text>' % (PADX, y + 32, LANG[lib]))
    for j, c in enumerate(CLASSES):
        cx = x0 + j * CW
        n = cell_count(lib, c)
        p.append('<rect x="%.1f" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="#d7dde5"/>' % (cx + 3, y + 4, CW - 6, CH, FILL[n]))
        if n:
            p.append('<text x="%.1f" y="%d" font-size="13" font-weight="bold" fill="%s" text-anchor="middle">%d</text>' % (cx + CW / 2.0, y + 4 + CH / 2.0 + 4.5, TEXT[n], n))

# totals row
p.append('<text x="%d" y="%d" font-size="11.5" font-weight="bold" fill="#222">all libraries</text>' % (PADX, totals_y))
for j, c in enumerate(CLASSES):
    cx = x0 + j * CW + CW / 2.0
    p.append('<text x="%.1f" y="%d" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">%d</text>' % (cx, totals_y, totals[c]))
p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#cfd6de"/>' % (PADX, rule_y, width - PADX, rule_y))

# legend
p.append('<text x="%d" y="%d" font-size="10" fill="#556">records:</text>' % (PADX, legend_y + 12))
for k, n in enumerate([0, 1, 2, 3]):
    lx = PADX + 58 + k * 44
    p.append('<rect x="%d" y="%d" width="18" height="15" rx="3" fill="%s" stroke="#d7dde5"/>' % (lx, legend_y, FILL[n]))
    p.append('<text x="%d" y="%d" font-size="10" fill="#556">%d</text>' % (lx + 24, legend_y + 12, n))
p.append('<text x="%d" y="%d" font-size="9.5" fill="#556">C10 has no third-party record; C4 has one (RDFLib #3426); the Semantica case carries the only two C10 records (paper §6.6).</text>' % (PADX, note_y))
p.append('</svg>')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(p))

print("wrote", OUT)
print("canvas %dx%d" % (width, height))
print("matrix:")
for lib in LIBS:
    print("  %-12s" % lib, [cell_count(lib, c) for c in CLASSES])
print("  totals      ", [totals[c] for c in CLASSES], "sum =", sum(totals.values()))
