# Screening protocol — KG export-correctness corpus

Version 2026-10-12. Applies to `corpus_cross_library.csv`, `corpus_semantica_case.csv`, `excluded_candidates.csv`, `withdrawn_records.csv`.

This protocol is written so that a second person can reproduce the selection, not just the counts. It is intended for publication alongside the corpus.

## 1. Unit of analysis

The unit is a **defect record**, anchored to a public issue or PR in a public tracker. A record is admitted only if it documents that a serialiser/exporter wrote output that is one of:

- **not well-formed** for the format it declared, or
- well-formed but **semantically mis-labelled** (wrong namespace, wrong datatype, wrong format actually emitted), or
- **lossy on round-trip** (re-parse does not recover the input graph), or
- accompanied by an **export-time failure that passed silently**.

A defect whose effect is confined to the read side is out of scope. What section 1 asks is whether the **written output** is wrong, not where in the pipeline the wrongness entered: a defect whose mechanism sits on the read side but whose effect shows in the written output — a value rewritten as the source is read, so that the export disagrees with its input — is in scope, and RDFLib #3426 is admitted on that reading. A defect visible only in what the reader accepts or rejects leaves the written output correct and is out of scope, which is why the four withdrawn records of section 7 do not qualify. The formats in scope are the RDF and JSON-LD serialisation syntaxes and the SPARQL result-set formats (TSV, CSV): both are written by an exporter at the same boundary, so a record about a result-set writer is admitted on the same terms as one about a graph serialiser (RDF4J #747 and #6084 are the two in this corpus). Data formats such as GraphML, Parquet or Arrow are outside that boundary and out of scope for the main table.

## 2. Library pool and selection criteria

A library enters the pool if all of the following hold: it is a general-purpose RDF or JSON-LD processor; it has had merged activity within the last three years; and it is a distinct implementation rather than a wrapper. Language coverage is deliberately spread so that a claim about a class of defect does not rest on one ecosystem's idioms.

Pool (7): RDFLib (Python), N3.js (JavaScript), jsonld.js (JavaScript), Apache Jena (Java), RDF4J (Java), Oxigraph (Rust), dotNetRDF (C#).

Semantica is **excluded from the cross-library statistics** and reported separately as a case study, because the author maintains it. Mixing it in would let a third of the main table be self-reported.

## 3. Search protocol

For each pool library, the issue tracker is searched with the fixed keyword set:

`serialize`, `serializer`, `serialization`, `serialisation`, `escaping`, `namespace`, `prefix`, `turtle`, `n-triples`, `n-quads`, `json-ld`, `round-trip`, `writer`, `export`

Both spellings of `serialis-/serializ-ation` are listed because trackers match literally and do not normalise them: a search of the largest library in the pool returns 36 hits for `serialisation` against 194 for `serialization` (measured 2026-10-10), so screening with a single spelling would have under-counted the other systematically. The set is deliberately weighted toward format words, which means some classes are reached only indirectly: C2 (IRI), C6 (blank nodes) and C8 (JSON-LD context) are carried in by `turtle`, `writer` or `json-ld` rather than by a word specific to the class, so their recall is correspondingly uneven.

Hits are then read in full and passed through section 1 and section 4 by hand. Keyword hits are candidates, never samples; nothing enters the corpus on a title alone.

## 4. Inclusion and exclusion

Include when section 1 holds. Exclude when any of the following holds:

- the output is valid for the declared format and semantically identical, and the complaint is about verbosity or compaction quality;
- the report is a feature request rather than a defect;
- the maintainers have re-classified it as a non-defect, on the ground that the output is correct;
- the defect is only about memory safety or the security of the processing path rather than the correctness of the written output;
- no concrete defective output is shown.

A maintainer statement decides a record only when it is a statement about the output. A closure that says where the fix belongs — that the caller should validate its terms, that the case is handled by another component, that the terms should be validated before they reach the writer — keeps the record and is recorded in `fix_evidence`; it is not a re-classification as a non-defect. The two N3.js records closed on those grounds in October 2026 are therefore kept out of the headline rather than excluded (section 7). A maintainer who reads a record as a specification question without asserting that the output is correct is a third case: the record also stays in the corpus, and is likewise kept out of the headline (RDF4J 5521).

Where a maintainer closes a report without a fix and without asserting that the output is correct, the record stays in the corpus but is kept out of the headline; where a record's admission is itself under review it is carried with a separate flag. The front-line counts are computed three ways, not twice: the full corpus, the corpus with the maintainer-closed records removed, and the corpus with both the maintainer-closed and the flagged records removed.

## 5. Recording schema

One row per defect: `library`, `language`, `issue`, `url`, `year`, `class`, `one_line`, `state`, `fix_evidence`, `runtime_repro`, `trigger`, `notes`.

`class` uses the ten-class taxonomy of the paper (C1 literal escaping and token boundaries, C2 IRI/IRIREF, C3 namespace/prefix, C4 round-trip, C5 format mislabelling, C6 blank nodes, C7 control characters/Unicode, C8 JSON-LD context/@vocab, C9 RDF/XML escaping, C10 export-validation). C10 is a property of the write path rather than a term-level class, and is recorded for records where an export-time failure passed silently, whatever the underlying class would have been.

`runtime_repro` records what was actually executed, and on which version. A fix commit, or a maintainer statement, counts as `fix_evidence` but is not a substitute for `runtime_repro`.

`trigger` is **required for every record whose `runtime_repro` claims a reproduction**: the minimum code, input and version needed for someone else to see the defect. It was added on 2026-10-10 after a baseline measurement found that four records (166, 660, 3373, 3279) carried a `reproduced` verdict with no recorded construction; §8 of this file records the re-test that followed. A verdict a reader cannot re-run is not evidence.

A record that was executed on a version where the defect no longer triggers is still an execution, and is recorded as `executed on <tool> <version>: no longer triggers`. This is deliberately distinct from the `fix_evidence` column: `runtime_repro` records what we ran, `fix_evidence` records whether and how the defect was resolved, and an earlier revision of this schema conflated the two by writing `fixed` in both columns, which made the executed-and-already-fixed records indistinguishable from records that had never been run, and broke the count in the paper's §4.3.

`state` is the issue state returned by the GitHub API at the time of the query (open or closed), as queried on 2026-10-11. Whether the defect still reproduces in the latest release is recorded separately, in `fix_evidence` and `runtime_repro`: a row may be `closed` and still carry `still live` evidence, and those are two different facts.

## 6. Decision log — the eight excluded candidates

| Library | Issue | What it is | Caught by |
|---|---|---|---|
| Oxigraph | 993 | did not use the default prefix, output valid but verbose | §4 verbosity |
| Oxigraph | 1121 | parse/serialise not 1:1 for SPDX RDF/XML | §4 maintainer statement (Tpt: output is valid RDF/XML of the same graph) |
| Oxigraph | 1345 | serialiser picks a shorter matching prefix; `myProperties:name` emitted as `myOntology:props\/name` | §4 verbosity/compaction: the two prefixes are nested, so the output resolves to the same IRI and the `\/` is a legal local-name escape |
| Oxigraph | 1543 | no JSON-LD compaction / remote context | §4 feature request |
| dotNetRDF | 10 | compressed writer did not compress collections/base URIs | §4 verbosity, semantics preserved |
| dotNetRDF | 34 | avoid `WriteRaw()` on XML writers | §4 no concrete defective output (hardening) |
| jsonld.js | 584 | prototype pollution via `@id: "__proto__"` | §4 security of the processing path, not of the written output; kept as a side finding |
| RDFLib | 948 | prefixed names do not allow escaping | §4 maintainer re-classification (aucampia: output is valid Turtle, only PName shortening is missing) |

Three of these are not defects of the written output at all (Oxigraph 1121, RDFLib 948, Oxigraph 1345) and are excluded on that rule; Oxigraph 1121 and RDFLib 948 had been carried as samples in an earlier draft and were withdrawn after reading the maintainer threads. Recording the withdrawal matters: the same judgement, applied to the paper's own earlier list, is what a reviewer will apply.

## 7. Known biases and limits

- **Screening is keyword-seeded.** A library whose defects happen to be described without the keyword set will be under-counted. Both spellings of `serialis-/serializ-ation` are in the set, but the set is format-weighted, so C2, C6 and C8 are reached mainly through format words and their recall is uneven. The counts are a floor, not a census.
- **Fix status is uneven.** Older records are mostly closed; the newest are open. Cross-library "still live" rates would compare discovery speed, not defect density.
- **Runtime reproduction is uneven.** Python and JavaScript records were executed locally; Java, Rust and C# records were not, because no JVM, Cargo or .NET SDK was available. Records from those three are labelled `not run`.
- **Class distribution is skewed after the de-bias cut.** With Semantica removed, C4 (round-trip) and C10 (export-validation) are thin, and C10 has no third-party representative at all at this revision. Any claim about those two classes is correspondingly weaker, and the paper should say so rather than let the histogram imply uniform coverage.
- **Three maintainer-closed specimens.** RDF4J 5521 is labelled `wontfix/specification`, a reading of the specification rather than an assertion that nothing was lost; N3.js 659 and 165 were closed in October 2026 with the written output left as it was, on the ground that the validation belongs elsewhere, and no closure claims the recorded output is correct. N3.js 659 is further narrowed to its IRI half: the same issue also lists control characters, and that half was closed with a statement that the output is valid and round-trips, which under section 4 takes the half out of scope (paper §4.4). Headline counts should be reported alongside the count that excludes these three.
- **Four records were withdrawn in this revision.** N3.js 578 (a StreamParser failure across a chunk boundary), Apache Jena 2766 (a `turtle` validation warning raised while parsing a legal IRI), and Apache Jena 3281 and 3931 (both ask the parsers to reject surrogate escape sequences) are all read-side defects, and this protocol admits only defects in the written output. They are released in `withdrawn_records.csv` rather than deleted, so that the withdrawal is auditable and the criterion can be seen applied to a record we had ourselves admitted.
- **One record was excluded on reading in this revision.** Oxigraph 1345 joins RDFLib 948 and Oxigraph 1121 in `excluded_candidates.csv`: the output is valid for its declared format and resolves to the same graph, so the complaint is about compaction (section 4, first bullet). It is excluded rather than carried as a maintainer closure because no maintainer claim about the behaviour was involved, only about the writing of the prefix.
- **One record is admitted with a flag.** RDFLib 3443 was judged a feature request rather than a defect in the prior reproduction report. It is carried with an explicit flag in the `notes` column rather than silently dropped, and its membership is under review. If it were removed, the corpus would be 23 records with a headline of 20. The paper states this in §4.4 instead of leaving it to a reader to notice.

## 8. Re-test log (2026-10-10)

Five records were brought into a defective state and measured against five candidate detection gates; the definitions, the per-record verdicts and the tool versions are in `baseline/BASELINE.md`. Two things came out of the exercise that belong in the protocol rather than in the paper.

**Reproduction triggers are now mandatory.** Four further records were re-tested and did not reproduce under the construction reconstructed for them: N3.js 660, RDFLib 3105, RDFLib 3373, RDFLib 3279. Their `notes` column now carries `trigger not recorded; did not reproduce on re-test 2026-10-10`. This is **not a verdict against those records** — the earlier pass may have used a different construction, and it did not record one, which is precisely the defect. They stay in the corpus with the flag; the fix is the `trigger` column above, and re-establishing their triggers is open work. These four are not the same four as the records whose `reproduced` verdict was recorded with no construction at all (166, 660, 3373, 3279): the two sets overlap in three records and differ in 3105 (executed, no longer triggers) and 166 (verdict carried from the earlier pass). The two are therefore named separately rather than together.

**One record's mechanism is not what its label suggests.** RDFLib 3426 is recorded as round-trip drift. The re-test located the drift: it happens when the source is read, not when the output is written, so the graph in memory already holds the drifted lexical form. The record stays in C4 because the observable effect is a round-trip that does not recover the input, but the mechanism is a read-side normalisation and the paper says so in §9.3.

## 9. Provenance

Prior corpus (19 cross-library records): earlier internal corpus notes (verified 2026-09-02, not released). These records are **inherited, not re-screened**: the 2026-09-02 pass is the screening event for them, and its runtime runs are recorded in the `runtime_repro` column. One caveat attaches to the inheritance. The prior pass was run under an earlier version of section 1, before the read-side/effect wording above was settled and before the specification-question case of section 4 was separated from the exclusion rule, so its labels were formed against a slightly looser criterion than this document states. Every inherited record was re-read against the current criterion in the 2026-10-11 revision, which is what withdrew four records and moved one to the excluded list; the labels the remaining records carry are those of that re-reading, not of the 2026-09-02 pass. A second person re-running this protocol from scratch would reproduce the method for the new records and would have to re-perform the earlier pass for the other 19.
New records: ten were admitted at screening on 2026-10-10 from the candidate table of the same earlier pass; nine remain in the corpus, Oxigraph 1345 having moved to the excluded list in the 2026-10-11 revision.
Baseline measurement: `baseline/` in the same directory (`BASELINE.md`, `run_baseline.py`, `jsprobe.js`, `baseline_gates.csv`, `re_test_not_reproduced.csv`).
