# Changelog

Revision history of the manuscript in [`paper.md`](paper.md). Up to v1.13 the
history was carried inside the manuscript, as a note on the title block; from
v1.14 it lives here, so that the released manuscript reads as a finished paper
and not as a working draft with its edit log attached.

## v1.23 - 2026-10-13

Bookkeeping. An external verification of v1.22 found the data clean, the
withdrawals sound and the conclusions intact, but fifteen stale counts left
behind by the v1.20-v1.22 revisions across four files, plus two precision points.
No record was added or removed; this revision corrects the text.

- `paper.md`: libraries with an admitted record (6 → **5**; jsonld.js is at zero
  after #206); the 2026-10-13 executions named in §4.3 (five → **six**, adding
  RDF4J #1317) and "executed for the journal revision" (seven → **six** — the
  seventh was the #1395 re-run); the #3443 counterfactual in §4.4 (**20 / 17**,
  was 22 / 19); the root-cause coverage in §7 (**nine of the twenty-one**, was
  eleven of the twenty-four); the unmeasured count in §9.3 (**sixteen**, was
  nineteen); the `withdrawn_records.csv` row in §11 (**7** withdrawn, split into
  read-side and §3.4 grounds, no longer "all read-side"); §12's "23 defect
  records" (→ **21**) and its unmeasured count (→ **sixteen**); and the count of
  records left `not run` in this revision (**two**).
- `corpus/README.md`: the file row counts and the headline block (24 / 21 / 20 →
  **21 / 18 / 17**); the contributing-library sentence (**five of the seven**,
  jsonld.js also at zero); the withdrawn row (**7**, with the read-side and §3.4
  grounds separated); and the runtime split (**19** executed — 9 `reproduced`,
  5 no longer triggering, 5 still reproducing).
- `corpus/screening_protocol.md`: the #3443 counterfactual (**20 / 17**).
- §4.4's #747 paragraph is narrowed to the point the reconstruction actually
  makes — the quotation-mark escaping — and states why the later commit that
  stopped escaping quotes (#789, merged 2017-04-01) does not rescue the report's
  premise.
- dotNetRDF #70's `runtime_repro` no longer reads "no .NET SDK": #903 was executed
  on .NET 3.5.2 in the same revision, and #70 is carried with an
  admission-under-review note, so the column now points at the note. Appendix A's
  row follows.
- Toolchain. `md2tex.py` maps `…` (U+2026) to `\ldots`; it had passed through raw
  and rendered in the built PDF as a missing glyph in §4.4. `check_package.py`'s
  page-count assertion is 28, matching the built PDF — it had claimed 27 because
  the font and metadata checks are skipped when `pymupdf` is absent. With the
  library installed the full check passes: 15 faces embedded, none Type 3.
- `main.tex` and the built PDF are regenerated from this revision.

## v1.22 - 2026-10-13

Two more records withdrawn, on §3.4 exclusion grounds the author approved.

- RDF4J #4929 is withdrawn: a reconstruction on 2.5.5, 4.3.10 and 6.1.0 produced
  output isomorphic to the input, so the difference is one of compaction rather
  than correctness, which §3.4 excludes (the rule that removed Oxigraph #1345 and
  RDFLib #948).
- RDF4J #747 is withdrawn: the report carries no minimal test case and a
  reconstruction shows the escaping matching the TSV rules, so its premise is not
  established.
- Both join `withdrawn_records.csv` (now seven) and are named in §4.4. The main
  table is 21 records, the headline **18**, the most conservative reading **17**;
  §4.2 drops a C1 and a C3 record; §4.3 gives Java 5 records; §3.1, §5, §6.1,
  §6.4, §6.6, §7.3 and Appendix A are updated. Figure 1 is redrawn.
- dotNetRDF #70 is retained with an `admission under review` note (a
  specification question), and RDF4J #5521 stays `not run` — so the two records
  that remain unexecuted are #5521 and #70.

## v1.21 - 2026-10-13

The last four `not run` records are dispositioned. Three are re-read against the
issue threads and one is executed.

- RDF4J #1317 is executed (4.3.10 and 6.1.0: the `escapeUnicode` flag is honoured,
  so the defect no longer triggers; the setting's class does not exist on the 2019
  line, so no affected version was pinned). Executed count 18 → 19, `not run` 5 → 4.
- RDF4J #4929, RDF4J #747 and dotNetRDF #70 are carried with an explicit
  `admission under review` ground in `notes`: a reconstruction shows #4929's
  output is isomorphic to its input (a compaction, not a correctness, difference),
  #747's escaping conforms to the TSV rules, and #70's percent-escaping concerns a
  bare `%` that is not a well-formed IRI. Whether they stay is left to the author.
- §1.5, §4.1, §4.3, §9.2, §11, §12, the abstract and the two READMEs follow the
  new 19/4 split.

## v1.20 - 2026-10-13

One record withdrawn, and every count that depends on the corpus size restated.

- jsonld.js #206 is withdrawn: its reporter retracted the report on 2017-11-09 as a
  misreading of the N-Quads grammar, so the record's premise does not hold and it
  leaves the corpus under §3.4. It joins the withdrawn table (now five) and is named
  in §4.4. The main table is 23 records, the headline **20**, the most conservative
  reading **19**; §4.2 drops jsonld.js and C2 falls to 4; §4.3 gives JavaScript 5
  records; §7.1 no longer cites the record. Figure 1 is redrawn over the five
  contributing libraries, and the pool is five contributing libraries of seven.
- §1.2, §1.3, §1.5, §4.1, §4.2, §4.3, §4.4, §5, §6.1, §6.6, §7.1, §9.2, §9.3, §11,
  §12, the abstract, Appendix A, and the repository's `README.md`,
  `corpus/README.md`, `corpus/screening_protocol.md` and `corpus/figures/make_figure1.py`
  are updated to the new counts.

## v1.19 - 2026-10-13

Journal revision, second pass: three more records executed, the gap search
upgraded to a systematic one.

- Five records move from `not run` to `executed` (13 → 18 executed): RDF4J
  #6084 (6.1.0), RDF4J #1535 (2.5.5, fixed by 4.3.10), RDF4J #1815 (2.5.5 and
  3.0.0, fixed by 6.1.0), dotNetRDF #903 (3.5.2) and Oxigraph #1859 (0.5.9 and
  0.5.11). Three of the five pin a version boundary. Every count that quotes
  the execution split is updated across §1.5, §4.1, §4.3, §9.2, §11, §12, the
  abstract, Appendix A, and the repository's `README.md`, `corpus/README.md`
  and `corpus/screening_protocol.md`. Six records remain `not run`. Two
  `notes` cells record later reading of the issue threads: jsonld.js #206 was
  retracted by its reporter, and RDF4J #747 was closed without a test case.
- §2.7 is upgraded from a quick search to a systematic one: a fixed query set
  across arXiv, OpenAlex and Crossref (2026-10-13), with the DBLP and Semantic
  Scholar gaps stated. The gap claim is unchanged.
- The trigger-coverage row of §1.5 and the trigger passages of §3.5 and §9.3
  are brought into line with the completed `trigger` column (v1.18).

## v1.18 - 2026-10-13

Journal revision: trigger coverage completed and scope welded into citable
sentences. No count moves, and the corpus, the four tables and Figure 1 are
untouched.

- The `trigger` column is populated for all 24 records (previously 5). The 19
  new triggers are extracted from the public issue text on 2026-10-13, each
  traced to its source issue. The four records that did not reproduce on
  re-test (§9.3) carry their reconstructed construction with the failure
  recorded in `notes`.
- Six wording surgeries weld scope into sentences that could be quoted out of
  context (§6.2 ×2, §9.3 ×2, §6.1, §11): "no second implementation is needed"
  becomes "in both records, exposing the disagreement required no second
  implementation"; "buys nothing here" becomes "buys nothing on these five
  records"; "structural rather than incidental" is attributed to RDFLib
  #3426; "not being retired by time alone" gains "In this pool"; the missing
  scripts are stated as a limitation of the artefact rather than a provenance
  note. The abstract gains "The corpus supports existence claims, not
  prevalence claims" ahead of the self-reported counts.
- The journal submission line is opened: the arXiv preprint (v1.17) is the
  baseline; this revision adds the missing trigger column and the wording
  surgeries for the journal version.

## v1.17 - 2026-10-12

- §10 gains a "Use of language models" note: a language model ran the
  annotation pre-check named in §5 and was a writing aid for the prose. It is
  disclosed on the paper's own standard, because the annotation use was already
  named while the writing use was not.

## v1.16 - 2026-10-12

- §2.7 no longer states that a systematic search is "a prerequisite for
  submission". It reports the quick search that was run — arXiv, OpenAlex and
  Crossref (2026-10-12), with DBLP and Semantic Scholar not covered — and keeps
  the systematic search as future work. The gap claim itself is unchanged.

## v1.15 - 2026-10-12

Pre-submission corrections to the released manuscript. No count moves, and the
corpus, the four tables and Figure 1 are untouched.

- Appendix B no longer carries the arXiv endorsement-policy URL; it was a
  submission-preparation note, not a source for the paper's content.
- The Ethics paragraph in §10 is restated in the plural, matching the two
  security-relevant records the corpus carries (N3.js #659 and #166), instead
  of "the one security-relevant record".
- The possessive in the abstract and Appendix B is made singular, matching the
  paper's single author ("the author's").
- §9.1 and §11 give full `corpus/...` paths for the baseline, figures and
  reproduction artefacts.

## v1.14 - 2026-10-12

Preparation for the arXiv submission.

- The revision note moves out of `paper.md` into this file, and the draft-status
  line on the title block becomes a plain date.
- The abstract is replaced by the 1,911-character version prepared for the arXiv
  metadata field, so that the abstract in the PDF and the abstract in the
  submission form are the same text. The longer version is in the git history.
- Nothing else changes. No count moves, and the corpus, the four tables and
  Figure 1 are untouched.

## v1.1-v1.13

The notes below were carried in `paper.md` itself before v1.14.

Revision note: v1.1 incorporated an adversarial review; the itemised changes are kept in an internal change log outside this file and are not part of this release. v1.2 acts on the three items that review left open — the baseline has been run (§9.3), the typology is presented on two axes rather than as ten siblings (§5), and the claim-status table now sits at the end of §1. v1.3 acts on a second review pass and on an in-house blind pass over the corpus that was run on a language model, not on an independent human annotator: two records whose defect is on the read side were withdrawn (§4.4), C1, C2, C4 and C7 were tightened at the boundaries that pass found fragile (§5), one record was retagged under the tightened C2, and the public counts became **27** records with a headline of **26**.

v1.4 is a consistency pass over v1.3 after a third review and its verification: the counts in the baseline and re-test passages were reconciled with the records that remain after the withdrawals, the C1/C2 retag was propagated to Appendix A and the baseline table, the criteria stress test was disclosed as a language-model check rather than as an agreement study, and the figure, the gate count and the column lists were brought back into line with the CSV. v1.5 is a hygiene and consistency pass: local file paths are removed from every released artefact, the two distinct four-record sets in the baseline passages are named separately, the baseline table's header is corrected, and Figure 1 and the §11 artefact list are brought back into line with the corpus. v1.6 reconciles the provenance narration with the measurement log: §4.3 now states that the 2026-10-10 measurement and its re-test re-executed eight inherited records without producing new `runtime_repro` verdicts, Appendix A records that re-confirmation for RDFLib #3426, and compiled artefacts are removed from the released package. v1.7 records the public release: the corpus repository is live and its URL is now set in §11, and the draft-status line reflects that this working draft is public.

v1.8 aligns the Appendix A one-line for RDFLib #3426 with the corpus label and the class label of §6.4 (semantic drift). The Chinese reading guide and the pre-submission to-do list live outside this file so that no export of the paper carries internal notes. v1.9 adds the author byline. v1.10 adds a References section: one entry for every work cited in §2, keyed by the author or tool name used there, each checked against a primary source. v1.11 names Asghar et al. (2016) in §2.6 so that every entry in References is keyed by a name that appears in the text.

v1.12 is a consistency pass after three rounds of external review and their verification: the fourth row of the §9.1 layer table moves out of the table into the sentence that follows it; the `state` column is narrowed to the GitHub issue state (open or closed) so that liveness is carried only by `fix_evidence` and `runtime_repro`; three issue years are corrected against the tracker; three records leave the corpus — two Jena records whose reports constrain what the parser accepts rather than what the writer emits, and an Oxigraph record whose output resolves to the same IRI in a longer lexical form — while the two N3.js records their maintainers closed in October 2026 join the disputed set; the corpus counts are restated three ways (**24** / **21** / **20**) in every place that quotes them; §2.4 gains the canonicalization and JSON-LD test-suite literature; and the released package gains `references.bib` and the dependency manifests needed to re-run the baseline.

v1.13 is a consistency pass after a fourth round of review (three external passes and one in-house) and its verification. It moves no count. The §3.1 admission test and the §4.4 withdrawal ground are both restated in terms of the written output rather than the side of the pipeline, with RDFLib #3426 named as the record that turns on the difference. N3.js #659 is narrowed to the IRI half of its issue, the control-character half being a closure about the output that §3.4 excludes. The three records outside the headline are described as maintainer-closed rather than disputed, and the ground of each is separated. §9.3 gains the three-way reading of its five-record subset. §7.3 narrows the claim of guideline G3 to a blocking gate over a fixed adversarial set, and §8.3 records that independent-engine verification is not original to this paper. §5 notes that the C7 and C4 criteria are wider than their surviving representatives. Accuracy corrections land alongside: "blank cells" replaces "blank rows" in §4.2, the three missing manifests join the §11 artefact list, the two query dates are separated, #660's resolved-in-2.10.2 note joins §9.3, #165's closure is quoted verbatim together with the fate of its pull request, and §6.7 dates the second reading.
