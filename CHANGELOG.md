# Changelog

Revision history of the manuscript in [`paper.md`](paper.md). Up to v1.13 the
history was carried inside the manuscript, as a note on the title block; from
v1.14 it lives here, so that the released manuscript reads as a finished paper
and not as a working draft with its edit log attached.

## v1.15 - 2026-10-12

Pre-submission corrections to the released manuscript. No count moves, and the
corpus, the four tables and Figure 1 are untouched.

- Appendix B no longer carries the arXiv endorsement-policy URL; it was a
  submission-preparation note, not a source for the paper's content.
- The Ethics paragraph in §10 states that the corpus carries two
  security-relevant records, not one (N3.js #659 and #166).
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
