"""Baseline measurement for the export-correctness corpus (paper S9.3).

Question: do the checks a library plausibly already has catch these defects?

Five candidate gates are measured per record. Each record carries an explicit
`trigger` -- the exact construction that produces the defective output -- because
a measurement without a recorded trigger is not reproducible (see BASELINE.md).

  B1  own-parser conformance          the writing library's own parser re-reads the output
  B2  independent-parser conformance  a parser from another implementation re-reads it
  B3  term-level fidelity             parse the output, compare against the intended graph,
                                      literal lexical forms included (value equality is not enough)
  B4  binding-level check             do prefix/namespace bindings match the intended ones (C3/C8)
  B5  source-vs-output fidelity       compare the output against the source document, so that
                                      damage done by the library's own object model is visible

Verdict per gate: caught / missed / n/a (with reason).
Headline: how many records are missed by every applicable gate.

Run with the managed venv interpreter, from the directory that has node_modules.
"""

import csv
import os
import subprocess
import tempfile

import rdflib
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

NODE = os.environ.get("NODE_BIN", "node")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
JSPROBE = os.path.join(OUT_DIR, "jsprobe.js")

FMT_TO_JS = {"turtle": "turtle", "ttl": "turtle", "nt": "ntriples", "ntriples": "ntriples",
             "nquads": "nquads", "nq": "nquads", "trig": "trig"}

GATE_KEYS = ("B1_own_parser", "B2_independent_parser", "B3_term_fidelity",
             "B4_binding_level", "B5_source_vs_output")


# --------------------------------------------------------------------------- helpers

def js_parse(fmt, path):
    jsfmt = FMT_TO_JS.get(fmt.lower())
    if jsfmt is None:
        return False, None, "no second implementation available locally for this format"
    try:
        p = subprocess.run([NODE, JSPROBE, "parse", jsfmt, path], capture_output=True, text=True)
    except FileNotFoundError:
        raise RuntimeError("node is not runnable; set NODE_BIN or put node on PATH") from None
    out = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()
    # jsprobe.js exits 0 when the file parses, 1 when it does not, and 2 when the probe
    # itself cannot run (n3 not installed). Only 0 and 1 are verdicts about the output;
    # any other exit code is an environment failure and must not be read as "caught".
    if p.returncode not in (0, 1):
        raise RuntimeError("jsprobe could not run (exit %d): %s"
                           % (p.returncode, (out[0][:110] if out else "")))
    return True, p.returncode == 1, (out[0][:110] if out else "")


def js_emit(record):
    p = subprocess.run([NODE, JSPROBE, "emit", record], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[:200])
    return p.stdout


def rdflib_parse(text, fmt):
    g = Graph()
    try:
        g.parse(data=text, format=fmt, publicID="http://example.org/")
        return True, g, ""
    except Exception as e:                                            # noqa: BLE001
        return False, Graph(), f"{type(e).__name__}: {str(e).splitlines()[0]}"[:110]


def lex_forms(g):
    return sorted((str(t), str(t.datatype) if t.datatype else None, t.language)
                  for t in g.objects() if isinstance(t, Literal))


def bindings(g):
    try:
        return {p: str(n) for p, n in g.namespaces()}
    except Exception:                                                # noqa: BLE001
        return {}


def lexical_forms_in_text(text):
    """Literal lexical forms in a serialisation, with the format's own escaping decoded.

    Minimal by design: it decodes the escapes that Turtle/N-Triples use for literals so that
    a difference in escaping style is not mistaken for a difference in the literal. It does not
    apply datatype canonicalisation, which is exactly why it can see drift that the in-memory
    graph cannot.
    """
    import re

    def unescape(s):
        for a, b in (("\\n", "\n"), ("\\t", "\t"), ("\\r", "\r"), ('\\"', '"')):
            s = s.replace(a, b)
        return s.replace("\\\\", "\\")

    triple = re.compile(r'"""(.*?)"""', re.S)
    single = re.compile(r'"((?:[^"\\]|\\.)*)"')
    forms = [unescape(m) for m in triple.findall(text)]
    rest = triple.sub("", text)
    forms += [unescape(m) for m in single.findall(rest)]
    return sorted(forms)


# --------------------------------------------------------------------------- measurement

def measure(rec, out_text, intended, source_text):
    row = dict(rec)
    row["raw_output"] = out_text.replace("\n", "\\n")[:110]

    with tempfile.NamedTemporaryFile("w", suffix=".dat", delete=False, encoding="utf-8") as fh:
        fh.write(out_text)
        path = fh.name
    try:
        js_applicable, js_caught, js_detail = js_parse(rec["declared_format"], path)
        py_ok, g_out, py_detail = rdflib_parse(out_text, rec["declared_format"])

        def verdict(caught):
            return "caught" if caught else "missed"

        if rec["language"] == "Python":
            # B1 = the writing library's own parser (rdflib); B2 = the independent one (n3.js)
            row["B1_own_parser"] = verdict(not py_ok)
            row["B1_detail"] = py_detail or "output accepted by its own parser"
            row["B2_independent_parser"] = (verdict(js_caught) if js_applicable else "n/a")
            row["B2_detail"] = js_detail
        else:
            # B1 = the writing library's own parser (n3.js); B2 = the independent one (rdflib)
            row["B1_own_parser"] = (verdict(js_caught) if js_applicable else "n/a")
            row["B1_detail"] = js_detail
            row["B2_independent_parser"] = verdict(not py_ok)
            row["B2_detail"] = py_detail or "output accepted by an independent parser"

        ok = py_ok
        if not ok:
            for k, why in (("B3_term_fidelity", "output is rejected, so the conformance gates cover it"),
                           ("B4_binding_level", "same reason")):
                row[k] = "n/a"
                row[k + "_detail"] = why
        else:
            same_shape = g_out.isomorphic(intended)
            if not same_shape:
                row["B3_term_fidelity"] = "caught"
                row["B3_detail"] = "output graph is not isomorphic to the intended graph"
            elif lex_forms(intended) != lex_forms(g_out):
                row["B3_term_fidelity"] = "caught"
                row["B3_detail"] = "literal lexical form drifted"
            else:
                row["B3_term_fidelity"] = "missed"
                row["B3_detail"] = "no term-level difference against the in-memory graph"
            bi, bo = bindings(intended), bindings(g_out)
            if bi and bo and bi != bo:
                row["B4_binding_level"] = "caught"
                d = {k: (bi.get(k), bo.get(k)) for k in set(bi) | set(bo) if bi.get(k) != bo.get(k)}
                row["B4_detail"] = f"binding difference {d}"[:110]
            else:
                row["B4_binding_level"] = "missed"
                row["B4_detail"] = "binding set matches" if (bi and bo) else "format carries no bindings"

        # B5 -- independent of any in-process model
        if source_text is None:
            row["B5_source_vs_output"] = "n/a"
            row["B5_detail"] = "no source document for this record"
        else:
            if lexical_forms_in_text(source_text) != lexical_forms_in_text(out_text):
                row["B5_source_vs_output"] = "caught"
                row["B5_detail"] = (f"source {lexical_forms_in_text(source_text)} "
                                    f"vs output {lexical_forms_in_text(out_text)}")[:110]
            else:
                row["B5_source_vs_output"] = "missed"
                row["B5_detail"] = "lexical forms in the output match the source"

        applicable = [row[k] for k in GATE_KEYS if row[k] != "n/a"]
        row["caught_by_any"] = "yes" if "caught" in applicable else "NO"
    finally:
        os.unlink(path)
    row.pop("B4_binding_level_detail", None)
    return row


# --------------------------------------------------------------------------- records

def rec_rdflib_1395():
    """C1. The defective output was captured under rdflib 6.0.0 (fixed from 6.3.2)."""
    out = ('@prefix dbo: <http://dbpedia.org/ontology/> .\n'
           '@prefix dbr: <http://dbpedia.org/resource/> .\n\n'
           'dbr:This_(journal) a dbo:Work .\n')
    g = Graph()
    try:
        g.parse(data=out, format="turtle")
    except Exception:                                                # noqa: BLE001
        pass
    intended = Graph()
    intended.add((URIRef("http://dbpedia.org/resource/This_(journal)"),
                  RDF.type, URIRef("http://dbpedia.org/ontology/Work")))
    return out, "turtle", intended, None


def rec_rdflib_3443():
    """C1 (flagged). Legal output that round-trips; the issue is the escaping style."""
    source = '@prefix ex: <http://example.org/> .\nex:s ex:p "line1\\nline2" .\n'
    g = Graph()
    g.add((URIRef("http://example.org/s"), URIRef("http://example.org/p"),
           Literal("line1\nline2")))
    return g.serialize(format="turtle"), "turtle", g, source


def rec_rdflib_3426():
    """C4. Lexical drift: the source says Z, the export says +00:00.

    Mechanism located by this measurement: rbflib normalises the lexical form when the
    source is read, so the drift has already happened before the write point, and the
    in-memory graph cannot be used as the reference.
    """
    source = ('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n'
              '<http://example.org/s> <http://example.org/p> "2024-01-01T00:00:00Z"^^xsd:dateTime .\n')
    g = Graph()
    g.parse(data=source, format="turtle")
    return g.serialize(format="nt"), "nt", g, source


JS_RECORDS = [
    dict(library="N3.js", language="JavaScript", issue="659", cls="C2",
         js_record="n3-659", declared_format="nt",
         trigger="Writer(N-Triples); addQuad whose object IRI contains a space and '<'",
         triples=[(URIRef("http://example.org/s"), URIRef("http://example.org/p"),
                   URIRef("http://example.org/a b<c>"))]),
    dict(library="N3.js", language="JavaScript", issue="165", cls="C5",
         js_record="n3-165", declared_format="nt",
         trigger="Writer(N-Triples) asked to write a quad that has a named graph, so the "
                 "output carries four terms",
         triples=[(URIRef("http://example.org/s"), URIRef("http://example.org/p"), Literal("v"))]),
]


def main():
    print("rdflib:", rdflib.__version__)
    rows = []

    python_records = [
        (dict(library="RDFLib", language="Python", issue="1395", cls="C1",
              trigger="Graph with a bound prefix; IRI whose local name contains parentheses; "
                      "output captured under rdflib 6.0.0",
              declared_format="turtle"), rec_rdflib_1395),
        (dict(library="RDFLib", language="Python", issue="3443", cls="C1",
              trigger="Graph with a literal containing a newline; serialise as Turtle",
              declared_format="turtle"), rec_rdflib_3443),
        (dict(library="RDFLib", language="Python", issue="3426", cls="C4",
              trigger="Parse a source document whose dateTime literal ends in 'Z'; serialise as N-Triples",
              declared_format="nt"), rec_rdflib_3426),
    ]
    for rec, fn in python_records:
        out_text, fmt, intended, source = fn()
        rec["declared_format"] = fmt
        rows.append(measure(rec, out_text, intended, source))

    for rec in JS_RECORDS:
        rec = dict(rec)
        triples = rec.pop("triples")
        jsrec = rec.pop("js_record")
        out_text = js_emit(jsrec)
        intended = Graph()
        for t in triples:
            intended.add(t)
        rows.append(measure(rec, out_text, intended, None))

    cols = ["library", "language", "issue", "cls", "declared_format",
            "B1_own_parser", "B2_independent_parser", "B3_term_fidelity",
            "B4_binding_level", "B5_source_vs_output", "caught_by_any",
            "B1_detail", "B2_detail", "B3_detail", "B4_detail", "B5_detail",
            "trigger", "raw_output"]
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "baseline_gates.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

    hdr = f"{'library':8} {'issue':5} {'cls':4} {'B1':7} {'B2':7} {'B3':7} {'B4':7} {'B5':7} any"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['library']:8} {r['issue']:5} {r['cls']:4} "
              f"{r['B1_own_parser']:7} {r['B2_independent_parser']:7} {r['B3_term_fidelity']:7} "
              f"{r['B4_binding_level']:7} {r['B5_source_vs_output']:7} {r['caught_by_any']}")
    n = len(rows)
    miss = [r for r in rows if r["caught_by_any"] == "NO"]
    print()
    print(f"records measured: {n}")
    print(f"caught by at least one candidate gate: {n - len(miss)}")
    print(f"MISSED BY ALL APPLICABLE GATES: {len(miss)}")
    for r in miss:
        print(f"   - {r['library']} #{r['issue']} [{r['cls']}] {r['raw_output']}")
    print("\nwrote", out_path)

    no_repro = [
        dict(library="RDFLib", issue="3105", cls="C3",
             corpus_says="'ex:' rewritten as 'ns1:'",
             trigger_tried="bind a prefix, add a triple in that namespace, serialise as Turtle",
             observed="output keeps the bound prefix ('ex:s ex:p \"v\" .'); no rewriting",
             tested="rdflib 7.6.0 and 6.0.0"),
        dict(library="RDFLib", issue="3373", cls="C8",
             corpus_says="extra namespace injected (JSON-LD)",
             trigger_tried="bind two prefixes, add one triple, serialise as JSON-LD",
             observed="output carries no @context and no injected namespace",
             tested="rdflib 7.6.0"),
        dict(library="RDFLib", issue="3279", cls="C9",
             corpus_says="XMLLiteral serialisation unfriendly",
             trigger_tried="XMLLiteral object, serialise as RDF/XML, re-parse",
             observed="output is legal RDF/XML; re-parsing recovers the same term with the "
                      "same datatype; no defective output observed",
             tested="rdflib 7.6.0"),
        dict(library="N3.js", issue="660", cls="C6",
             corpus_says="blank node split into two",
             trigger_tried="blank node used in subject and object position, Writer(Turtle)",
             observed="the node appears as _:b0 in both positions and re-parses to the same graph",
             tested="n3 2.7.2"),
        dict(library="N3.js", issue="578", cls="C1",
             corpus_says="chunk-boundary parse failure across a language tag",
             trigger_tried="not attempted",
             observed="the report describes a parser-side failure, not a writer-side one, so it "
                      "is outside the scope of a writer baseline",
             tested="-"),
    ]
    nr_cols = ["library", "issue", "cls", "corpus_says", "trigger_tried", "observed", "tested"]
    nr_path = os.path.join(OUT_DIR, "re_test_not_reproduced.csv")
    with open(nr_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=nr_cols)
        w.writeheader()
        for r in no_repro:
            w.writerow(r)
    print("wrote", nr_path, f"({len(no_repro)} records)")


if __name__ == "__main__":
    main()
