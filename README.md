# RDF export-correctness corpus

A cross-library corpus of **silent export defects**: cases where an RDF or JSON-LD
serialiser reports success and writes output that a conforming parser rejects, that is
well-formed but mislabelled, or that loses information on round-trip.

This repository holds the corpus and the artefacts for the manuscript in
[`paper.md`](paper.md):

> **Silent corruption at the export boundary — A cross-library corpus and a ten-class typology of RDF export defects**

## Contents

| Path | What it is |
|---|---|
| [`paper.md`](paper.md) | The manuscript. |
| [`references.bib`](references.bib) | The bibliography of the manuscript in BibTeX: one entry for every work cited in §2, mirroring the References section of `paper.md`. |
| [`corpus/`](corpus/) | The corpus, the screening protocol and the generation script. [`corpus/README.md`](corpus/README.md) describes every file in it. |
| [`corpus/corpus_cross_library.csv`](corpus/corpus_cross_library.csv) | 21 defect records across 5 third-party libraries and 5 languages (7 libraries were screened; Apache Jena carries no admitted record). |
| [`corpus/corpus_semantica_case.csv`](corpus/corpus_semantica_case.csv) | 11 first-party case-study records, kept out of every cross-library count. |
| [`corpus/excluded_candidates.csv`](corpus/excluded_candidates.csv) | 8 screened-out candidates and the reason for each. |
| [`corpus/withdrawn_records.csv`](corpus/withdrawn_records.csv) | 4 records admitted in an earlier revision and withdrawn in this one, kept for audit rather than deleted. |
| [`corpus/screening_protocol.md`](corpus/screening_protocol.md) | Library selection, keyword protocol, inclusion criteria, decision log, known biases. |
| [`corpus/baseline/`](corpus/baseline/) | The detection baseline of the paper's §9.3: gate definitions, per-record verdicts, and the re-test of records that did not reproduce. |
| [`corpus/figures/`](corpus/figures/) | Figure 1 and the script that draws it from the CSV. |
| [`corpus/repro/`](corpus/repro/) | Minimal reproductions for the two records that were run end to end. |

## Headline counts

21 records, 5 contributing libraries (of 7 screened), 5 languages. Three records (RDF4J #5521,
N3.js #659 and #165) were closed by their maintainers without a fix, so the headline is
reported three ways: **21** with them, a headline of **18** without them, and a most
conservative reading of **17** once the flagged record (RDFLib #3443, admission unsettled) is
removed as well. See §4.4 of the manuscript.

## Regenerating the tables

The four CSVs under `corpus/` are generated, not hand-written. Edit the tables in
[`corpus/build_corpus.py`](corpus/build_corpus.py) and re-run it (standard library only):

```bash
python corpus/build_corpus.py            # regenerates the four CSVs
python corpus/figures/make_figure1.py    # regenerates Figure 1 from the CSV
```

The runtime reproductions and the detection baseline need third-party packages; the exact
commands are in [`corpus/README.md`](corpus/README.md).

## Scope and limits

19 of the 21 records were executed locally; the other 2 are labelled `not run`. Four records did
not reproduce under the construction reconstructed for them. No second annotator has been
used yet. All samples come from public issue trackers; no private or customer data is
included. These limits are stated in the manuscript as well, and are repeated here so that the
corpus is not read as more than it is.

## Licence

- The manuscript (`paper.md`) and the data (`corpus/**/*.csv`, `corpus/**/*.md`) are
  released under [CC BY 4.0](LICENSE-CC-BY-4.0.txt).
- The code (`corpus/**/*.py`, `corpus/**/*.js`) is released under the [MIT licence](LICENSE).
