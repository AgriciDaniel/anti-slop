---
type: "procedure"
title: "The Attribution Test"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/procedure"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[The Firewall]]"
  - "[[The Stranger Test]]"
  - "[[The Deletion Test]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Superseded Figures]]"
  - "[[Corpus Study Method]]"
  - "[[Puffery and Undue Emphasis]]"
  - "[[Knowledge Base Surface]]"
  - "[[Documentation Surface]]"
  - "[[Humanizers]]"
source_urls:
  - "https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing"
  - "https://github.com/blader/humanizer"
  - "https://arxiv.org/abs/2501.03437"
  - "https://arxiv.org/abs/2509.19163"
---

# The Attribution Test

"Studies show." "Experts say." "It is widely regarded as." "Research
increasingly suggests." Each of these promises that somewhere there is a named
source which supports the specific claim attached to it. The test is the
cashing of that promise, and it has exactly three ways to fail.

The three failures are arranged below as a ladder, ordered by how much
apparatus the claim is wearing rather than by how much damage it does. Rung 1
wears nothing. Rung 3 wears a full citation with a DOI. The damage runs the
other way for the first two rungs and then doubles back, which is the reason
the ladder is worth walking rather than collapsing into a single check.

| Rung | Failure | Apparatus worn | Who catches it | Automatable |
| --- | --- | --- | --- | --- |
| 1 | Attribution with no name | none | any attentive reader | partially, by phrase match |
| 2 | Named source that does not support the claim | a real, correct, resolvable citation | only a reader who opens the source | no |
| 3 | Citation that does not exist or resolves elsewhere | a full reference, sometimes a DOI | a resolver | yes, `scripts/scan_refs.py` |

Rung 2 is the dangerous one. It is the only rung where every visible signal is
correct, and it is the rung the current generation of retrieval-augmented
systems produces natively.

## Rung 1: attribution with no name

The claim asserts that some body of work exists, without identifying any of it.
`wikipedia-signs-of-ai-writing` documents this as vague attribution and weasel
wording, with a watch list that includes industry reports, observers have
cited, experts argue and several sources. It also documents the half that most
prior art omits: overgeneralisation of opinions, where one or two sources are
presented as a widely held view, where the existence of multiple reviewers or
scholars is implied while a single person is cited, and where a list of
examples is implied to be non-exhaustive when the sources give no indication
that other examples exist.

Worked example, from a draft internal standard:

```text
CLAIM AS WRITTEN:  "Studies show that code review catches most defects
                    before release."
ATTRIBUTION PHRASE: "studies show"
RESOLVES TO:        nothing. No study is named anywhere in the document.
QUANTIFIER CHECK:   "most" is a numeric claim wearing a word.
RUNG:               1
FINDING:            unsupported claim. severity high, confidence confirmed.
REPAIR OPTIONS:     (a) name the study and restate what it measured, or
                    (b) cut the sentence, or
                    (c) rewrite as a first-person policy statement:
                        "We require review because we have found it catches
                        defects earlier than our staging environment does."
```

Option (c) is worth noting because it is usually the honest repair and it is
almost never the one taken. Converting a fake appeal to literature into a
stated house position removes the defect without pretending to evidence.

## Rung 2: a real source that does not support the claim

Here a source is named. The name is correct. The source exists, the link
resolves, the author is real and alive, and the paper says nothing like what
the sentence claims it says.

`wikipedia-signs-of-ai-writing` records this explicitly as a property of the
current model generation rather than an occasional slip. Its superficial
analyses section notes that newer chatbots with retrieval-augmented generation
may attach evaluative statements to named sources regardless of whether those
sources say anything close, and its project guidance is blunter still: most AI
content is not unsourced, because sometimes it has real sources that are
unrelated to the topic, and the existence of real sources should not by itself
be taken as evidence about how the text was produced.

Worked example, from a literature summary:

```text
CLAIM AS WRITTEN:  "Kobak et al. found that roughly a third of recent
                    abstracts are AI-generated."
CITED SOURCE:      kobak-excess-vocabulary. Real, peer reviewed, correct
                    author, correct venue, working DOI.
OPEN THE SOURCE:   the published finding is that at least 13.5 percent of
                    2024 PubMed abstracts were processed with a model,
                    reaching 40 percent in some subcorpora, measured by a
                    detector-free excess-vocabulary method over more than
                    15 million abstracts.
SUPPORTS THE CLAIM? no, on three counts.
                    (1) "roughly a third" matches no figure in the paper.
                    (2) "AI-generated" is not "processed with an LLM";
                        the method cannot separate drafting from editing.
                    (3) the widely quoted 10 and 30 percent figures come
                        from a withdrawn 2024 preprint version.
RUNG:               2
FINDING:            misattribution. severity critical, confidence confirmed.
REPAIR:             quote the 13.5 percent floor, keep the word "processed",
                    and record the withdrawn figures under
                    [[Superseded Figures]] rather than deleting them.
```

Every mechanical check passes on that sentence. The link works, the checksum
is valid, the author exists, the title matches the DOI record. Only reading the
paper catches it. This is why the ladder cannot be replaced by a resolver, and
why `blader-humanizer`, whose no-fabrication rule is a prompt instruction with
no verification mechanism and which has no coverage of citations at all, cannot
reach this rung even in principle.

There is a second form of rung 2 which is easier to miss: the citation is
attached to a claim the source does support, but at a strength the source does
not licence. A preprint verified at abstract level becomes "researchers have
established". A single vendor survey becomes "the industry has found". The
check is the same. Open the source, read what it claims about itself, and
compare the modal verbs.

## Rung 3: the citation that does not exist

`wikipedia-signs-of-ai-writing` maintains a citations taxonomy for this rung,
and it is the part of the guide with the least ambiguity. The catalogued
defects are broken external links absent from web archives, invalid DOIs and
ISBNs that fail their checksums, DOIs that resolve to entirely unrelated
articles, book citations with no page numbers, book citations whose stated
pages do not contain the claim, broken named-reference syntax, and vendor
tracking parameters left in reference URLs. Its worked case is two fabricated
conference citations carrying real but wrong DOIs, one of them attributed to an
author who had been dead for more than thirty years.

Worked example:

```text
CLAIM AS WRITTEN:  "Latency-aware scheduling reduces tail latency by 40
                    percent (Marchetti and Okoro, 2024, doi:10.1109/0000.0000)."
RESOLVER OUTPUT:   refs.doi_zero_registrant, then refs.doi_unresolved.
ISBN/ARXIV:        not applicable.
RUNG:              3
FINDING:           fabricated citation. severity critical, confidence
                   confirmed by scanner exit code, not by reading.
REPAIR:            delete the citation and the number it was supporting.
                   The number was never independently present in the draft;
                   removing the citation alone would leave a bare 40 percent
                   with no origin, which is a rung 1 defect wearing a corpse.
```

The last line is the operational point. Repairing rung 3 by deleting the
reference and keeping the sentence demotes a critical finding into a high one
and calls it fixed. The claim goes with the citation.

`masrour-damage-humanizers` lists hallucinated citations among the documented
failure modes of tools that rewrite text toward a more natural register, which
means rung 3 defects can be introduced by the repair step as well as by the
original draft. Any pipeline that rewrites must re-run the resolver afterwards.
That is rule 4 of [[The Firewall]] applied to references.

## The procedure

1. Extract every attribution in the span. An attribution is any construction
   that transfers responsibility for a claim to someone other than the author:
   a name, a citation, a passive appeal, a quantified appeal to a group.
2. For each one, write the claim it is supporting as a standalone sentence.
   Attribution defects hide in the gap between the sentence and its citation,
   so the two must be separated before they can be compared.
3. Classify the rung. No name is rung 1. A name is rung 2 or 3.
4. For rung 3, run `python3 scripts/scan_refs.py --online` over the document
   and record the rule ids and exit code verbatim.
5. For rung 2, open the source. Read the abstract at minimum and the relevant
   section where one exists. Write down what it actually claims, in its own
   numbers, next to what the document claims it claims.
6. For rung 1, search the document and its bibliography for any named source
   at all. If none exists, the finding is complete without further work.
7. Emit the artifact: claim, attribution as written, what it resolves to, the
   rung, the finding with severity and confidence, and the repair.
8. Re-run step 4 after any repair.

## What the scanner reaches

`scripts/scan_refs.py` automates the bottom rung and only the bottom rung. It
extracts every DOI, arXiv identifier, ISBN and URL in the document and decides
what is decidable offline: DOI shape, placeholder registrants, arXiv identifier
shape and date plausibility, and ISBN-10 and ISBN-13 checksums, which are pure
arithmetic. With `--online` it resolves identifiers and compares the retrieved
title against the cited title.

That is the whole of its reach, and the boundary is worth stating plainly
because a green exit code from it is routinely misread as a clean bibliography.

| Question | Decidable by scanner |
| --- | --- |
| Is this DOI well formed | yes |
| Does this DOI resolve | yes, with `--online` |
| Does the resolved title match the cited title | yes, with `--online` |
| Does this ISBN pass its checksum | yes |
| Does the cited page contain the claim | no |
| Does the paper support the sentence | no |
| Is "studies show" backed by any study | no |
| Is the claim stated at a strength the source licences | no |

Rungs 1 and 2 are human work by construction. `shaib-measuring-slop` is the
reason they are not delegated to a model: it measured LLM-as-judge agreement
with human slop labels at kappa 0.01 for GPT-5, minus 0.01 for DeepSeek-V3 and
0.03 for o3-mini, with models flagging at 0.03 to 0.08 against a human rate of
0.34. A model asked whether a source supports a claim is being asked for
exactly the holistic judgment that measurement rules out.

## Where the test over-fires

- **Common knowledge does not need a source.** "HTTP is stateless" carries no
  attribution and needs none. Demanding one produces citation theatre.
- **First-person experience is not an attribution failure.** "We saw this twice
  last quarter" is a claim about the author, checkable by asking them. It is
  weak evidence and it is honestly labelled, which is the distinction that
  [[Evidence Quality Ladder]] exists to hold.
- **Over-repair produces over-attribution.** `wikipedia-signs-of-ai-writing`
  separately catalogues canned emphasis on sources, where every trivial fact is
  painstakingly attributed in body text. A document repaired by adding a named
  source to every sentence has traded one documented defect for another.
- **A source that fails this test is not thereby wrong.** The finding is about
  the support relation, never about the claim's truth and never about the
  document's origin. See [[The Firewall]], rule 1.

## Related

- [[The Firewall]]
- [[The Stranger Test]]
- [[The Deletion Test]]
- [[The Inversion Test]]
- [[Evidence Quality Ladder]]
- [[Superseded Figures]]
- [[Corpus Study Method]]
- [[Knowledge Base Surface]]
- [[Humanizers]]
- [[overview|Overview]]
