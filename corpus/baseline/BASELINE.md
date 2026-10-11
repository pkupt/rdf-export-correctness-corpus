# Baseline measurement — method, numbers, and what it changed

Date: 2026-10-10. Companion to `run_baseline.py`, `jsprobe.js`, `baseline_gates.csv`,
`re_test_not_reproduced.csv`.

## The question

Paper §9.3 asks the question a reviewer will ask first: **do the checks these libraries
plausibly already have catch these defects?** The prior draft answered it with a plan. This
run answers it with numbers, on the subset of the corpus that can be brought into a defective
state with the toolchains available locally.

## Definition of a gate

Five candidate gates, each of them something a project could plausibly already have in place:

| Gate | Question it asks | How it is implemented here |
|---|---|---|
| **B1** own-parser conformance | does the writing library's own parser accept the output? | re-parse the output with the same library that wrote it |
| **B2** independent-parser conformance | does a parser from another implementation accept it? | re-parse with a different implementation (n3.js 2.7.2 for Python output, rdflib 7.6.0 for JavaScript output) |
| **B3** term-level fidelity | does the output mean what the in-memory graph meant? | parse the output, compare against the intended graph including literal lexical forms |
| **B4** binding-level check | do prefix/namespace bindings match the intended ones? | compare the namespace manager of the two graphs (relevant to C3/C8) |
| **B5** source-vs-output fidelity | does the output say what the *source document* said? | compare the literal lexical forms of the output against those of the source, decoding the format's own escaping |

`B5` exists because of a result in the table below: comparing against the in-memory graph
cannot see damage that the library's own object model has already done.

Verdicts: `caught` / `missed` / `n/a`. "Missed by all applicable gates" is the headline.

## What was measured

Five records could be brought into a defective state locally. Each carries a recorded
**trigger** — the exact construction that produces the defective output — because a
measurement whose trigger is not recorded is not reproducible.

| Library | Issue | Class | B1 own | B2 independent | B3 fidelity | B4 binding | B5 source |
|---|---|---|---|---|---|---|---|
| RDFLib | 1395 | C1 | caught | caught | n/a | n/a | n/a |
| RDFLib | 3443 | C1 | missed | missed | missed | missed | missed |
| RDFLib | 3426 | C4 | missed | missed | missed | missed | **caught** |
| N3.js | 659 | C2 | caught | caught | n/a | n/a | n/a |
| N3.js | 165 | C5 | caught | caught | n/a | n/a | n/a |

- **records measured: 5**
- **caught by at least one candidate gate: 4**
- **missed by every applicable gate: 1** — RDFLib #3443, which is the record already flagged
  as an escaping-style feature request (§4.4 of the paper). That it is invisible is not a
  surprise; it is the expected consequence of it not being a defect.

Tool versions: rdflib 7.6.0 (the output for #1395 was captured under 6.0.0 and is rejected by
the parser of both versions), n3.js 2.7.2, Node 22.22.2.

## Three things the run changed

### 1. The second engine buys nothing on this sample

B1 and B2 return the same verdict on all five records. The independent implementation caught
nothing that the writing library's own parser did not already catch. The corpus supports the
weaker claim in §6.2 — that a round-trip check using the library's own parser would have
caught some of these defects — and does **not** support the stronger claim that an
independent engine is needed to find them. That is worth saying, because "cross-check with a
second engine" is the assumed doctrine in this area.

Caveat: five records is five records. B2 was exercised only on Turtle and N-Triples, and the
independent parser does add reach for formats where the writing library's parser is absent or
lenient. The claim made in the paper is scoped to this sample.

### 2. The quiet tier is invisible from inside the object model

B3 and B4 caught **nothing**. That is not an implementation accident. RDFLib #3426 rewrites a
`Z` timezone designator into `+00:00`, and the measurement located the mechanism: the rewrite
happens when the *source is read*, not when the output is written. By the time any in-process
gate can compare graphs, the in-memory graph already holds `+00:00`, so it agrees with the
output and the drift is undetectable by construction.

Only B5 — comparing the output against the **source document** — sees it. Consequence for the
paper: the check design needs three layers, not two, and the third one must compare against
the artefact that came in, not against the object that is in memory at the time of writing.

### 3. Our own corpus has a reproducibility gap

Four records were re-tested and did **not** reproduce under the construction reconstructed
for them (`re_test_not_reproduced.csv`): RDFLib #3105, #3373, #3279 and N3.js #660. A fifth
row records N3.js #578 as `not attempted`: it is parse-side and was withdrawn from the
corpus in this revision, so it is not counted among the four. The prior pass recorded a `runtime_repro`
verdict but not the construction behind it, so this is a **discrepancy to reconcile, not a
verdict against those records** — a different trigger may produce the described symptom.

The fix is a protocol change, and it is the same fix the external review was asking for:
`trigger` becomes a required column of the corpus. A record whose trigger is not written down
cannot be re-checked by a reader, which is the whole point of publishing the corpus.

## Cross-version check: the JavaScript records on the current release

The measurement above pins `n3@2.7.2` (released 2026-09-01), which was current when the corpus
was assembled. The package has moved since: `latest` is `n3@2.13.12` (2026-10-10), with #660's
fix listed between the two at 2.10.2. To check that the measured JavaScript verdicts are not an
artefact of the old pin, the four emit constructions were re-run against 2.13.12 on 2026-10-12,
and the defective outputs were re-parsed under the parser of both versions.

| Construction | Output on 2.7.2 | Output on 2.13.12 | Own parser, both versions |
|---|---|---|---|
| `n3-659` (C2, IRI with a space and `<`) | IRI written through unescaped | **identical** | rejects (exit 1) |
| `n3-165` (C5, N-Triples asked, quad written) | four terms emitted | **identical** | rejects (exit 1) |
| `n3-660` (C6, blank node in two positions) | node kept whole, re-parses | identical | accepts |
| `n3-659b` (C2, Turtle, IRI with a space) | IRI written through unescaped | **identical** | rejects (exit 1) |

Two things follow. First, the B1/B2 verdicts for #659 and #165 are not a property of the pinned
version: the current release writes the same defective output and its own parser still rejects
it, so a project on `latest` is in the same position as one on 2.7.2, and the closure of #165
without a fix has not since been overtaken by a fix. Second, the C6 construction for #660
reproduces on neither version — consistent with the re-test row above and with the tracker's
record that #660 is resolved in 2.10.2, so it stays a discrepancy to reconcile rather than a
finding.

The pin stays at `2.7.2` so that the published numbers remain the ones that were measured; the
2.13.12 check is recorded here rather than folded into the pin.

## Reproducing this

```
cd corpus
pip install -r requirements.txt && npm install   # rdflib==7.6.0, n3@2.7.2
python baseline/run_baseline.py                  # writes baseline_gates.csv and re_test_not_reproduced.csv
```

The Python interpreter must have rdflib 7.6.0, and `node` must be on `PATH` with `n3@2.7.2`
installed. `run_baseline.py` locates `jsprobe.js` next to itself, so it can be run from any
directory; the probe resolves `n3` from the nearest `node_modules`, which `npm install`
creates in `corpus/`. If the probe itself cannot run, it exits 2 and the measurement stops
with an error rather than recording the record as caught.

## What is still not measured

- The 10 records whose toolchains are absent locally (JVM, Cargo, .NET SDK), and jsonld.js #206,
  which predates the runnable line.
- The libraries' own **test suites** — the gates above are parsers and comparators, not the
  tests the projects actually ship. "Would their CI have caught it?" remains unanswered.
- The reference shape validator (SHACL) as a gate; no record in this subset has a shape to
  validate against, so it would report `n/a` throughout.
