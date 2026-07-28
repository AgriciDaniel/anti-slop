<!--
Adapted from "Wikipedia:Signs of AI writing" and WikiProject AI Cleanup,
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing , retrieved
2026-07-27, by Wikipedia contributors. Licensed CC BY-SA 4.0,
https://creativecommons.org/licenses/by-sa/4.0/ . Changes: reorganised into
evidence tiers, false-positive classes added, routed to structural procedures,
and figures replaced with the sources recorded in this project's ledger.
This file and adaptations of it remain under CC BY-SA 4.0.
-->

# Tier 2 markers: measured, but high false positive

Load this before writing any finding that rests on em-dash density, burstiness,
or uniformity of sentence length.

**Tier 2 never fails a build, never fails a review, and never appears in a
report on its own.** Not at LOW, not with a hedge, not as an "observation". A
tier 2 hit does exactly one thing: it selects a span for a Layer 1 structural
test. If the structural test comes back clean, the hit is dropped and nothing
is written down.

The difference between tier 1 and tier 2 is not whether the pattern was
measured. All three markers here have been measured. The difference is the
**unit the measurement applies to**. Tier 1 markers were measured on spans and
documents. Tier 2 markers were measured on populations, and a population-level
shift tells you nothing decidable about the document in front of you. That is
not this file's editorial opinion. It is the stated conclusion of the strongest
study in the area, quoted verbatim below.

---

## T2-1. Em-dash density

**What it is.** Frequency of U+2014 (and, in some framings, U+2013) per unit of
text, above some baseline.

**Citation.** Czuma, "Em-ergence of the em-dash", arXiv 2606.29540, 2026-06-28.
**Pre-registered on OSF as HFT8C**, which is the single reason this measurement
is trustworthy where the vendor claims are not. Corpus: **69,632 medRxiv
preprints**.

Findings:

- Em-dash prevalence in Discussion sections rose from **4.23 percent
  pre-ChatGPT to 11.58 percent post**, a rise of 7.35 percentage points, 95
  percent CI 6.94 to 7.77, odds ratio 2.96.
- Trajectory: roughly 4 percent through 2023, **8.0 percent in 2024**, **20.3
  percent in 2025**.
- A placebo split within the pre-LLM era showed no change, plus 0.13 percentage
  points. This is what separates a real discontinuity from a drifting baseline,
  and it is why the pre-registration matters.

The author's own conclusion, adopted here verbatim and treated as binding:

> **"The em-dash is a population-level indicator, not a per-paper detector of
> LLM use."**

Limitations recorded honestly: this is a preprint. Pre-registration raises
confidence substantially relative to unregistered claims, but it does not make
it peer reviewed.

**Example of the marker.** A 900-word document containing eleven em dashes,
most of them spaced.

**False-positive class.** Large, and it runs in several directions at once.

- **The measurement is a rate over a corpus.** An 11.58 percent post-period
  prevalence means that in the post period, 11.58 percent of Discussion
  sections contained the feature. It does not mean a document containing the
  feature is 11.58 percent anything. Reading a population rate as a per-document
  probability is the specific error the paper's conclusion forbids.
- **The marker can run backwards.** Freeburg, "The Last Fingerprint", arXiv
  2603.27006, 2026-03-27, measured base Llama 3.1 8B at 0.49 em dashes per
  1,000 words and its instruction-tuned counterpart at **0.00**. Fine-tuning
  can eliminate the marker as easily as amplify it, which makes em-dash rate a
  signature of a training procedure rather than a universal tell. That preprint
  is single-author, unaffiliated and not peer reviewed, tier CONTESTED, and
  must carry that flag whenever it is cited next to peer-reviewed work.
- **Typography.** The em dash is standard punctuation with centuries of use.
  Chicago style, most trade publishing, and a great many good writers use it
  heavily. En dashes are worse still as a marker: numeric and date ranges, page
  ranges, score lines and open-compound modifiers all require them, and nothing
  in the Wikipedia guide supports treating an en dash as a sign at all.
- **Tooling.** Word, macOS, Google Docs and many CMSes autocorrect double
  hyphens into em dashes without the author noticing.
- **Surface.** The Wikipedia guide records that the sign is much more common on
  discussion pages than in article prose, that the AI form is usually
  *spaced* (contrary to typographic convention), and that GPT-5.1 already
  suppresses the habit. So the marker is surface-dependent, form-dependent, and
  already decaying.

**Routes to.** Nothing, by itself. If em-dash density is elevated *and* a tier
1 marker fired in the same span, run the tier 1 marker's structural test. The
em dash contributes to cluster count only after that test produces an artifact.

**A note on the house rule.** This plugin's `lint_voice.py` rejects U+2014 and
U+2013 outright. That is a **house style rule**, not a slop verdict and not an
application of this marker. It exists because the operator asked for it. Never
report a `lint_voice.py` hit as evidence about a text's origin, and never let
the existence of the house rule inflate what this marker is allowed to
support.

---

## T2-2. Burstiness

**What it is.** Variance in per-sentence or per-window perplexity. Human prose
is generally described as more "bursty": long stretches of predictable text
punctuated by genuinely surprising sentences. Low burstiness, a flat variance
profile, is the marker.

**Citation.** Burstiness is a real, published feature used by perplexity-based
detectors. **This project holds no source that measures a burstiness threshold
on a corpus in a form fit to quote, so no threshold is stated here.** If you
want a number, there isn't one in this plugin, and inventing one is prohibited.

What the project does hold is evidence about how the detectors built on this
feature behave:

- Russell, Karpinska and Iyyer, ACL 2025, arXiv 2501.15654: a majority vote of
  five expert human annotators misclassified **1 of 300** articles, beating
  commercial and open-source detectors even under paraphrase evasion. The
  statistical features lose to attentive readers.
- OpenAI withdrew its own classifier on 2023-07-20, citing its low rate of
  accuracy: 26 percent true positive at a 9 percent false positive rate.

**False-positive class.** Enormous, and largely structural.

- **Genre flattens variance by design.** Reference documentation, API specs,
  legal drafting, standards text, changelogs and technical manuals are supposed
  to be uniformly predictable. Low burstiness there is competence.
- **Editing flattens variance.** A heavily copyedited human document loses
  burstiness. So does translated text. So does text written to a style guide.
- **Short documents have no measurable variance.** Below a few hundred words
  the statistic is noise.
- **The feature is directly implicated in demographic bias.** Detectors built
  on perplexity and burstiness are the ones measured to over-flag
  English-language-learner writing. See `false-positives.md`.

**Routes to.** Deletion and stranger, on the specific spans, never on the
document. If a section is uniformly flat *and* individual sentences in it fail
deletion or stranger, you report the deletion and stranger findings. The
variance statistic is never the finding and is never quoted in the report.

---

## T2-3. Uniform sentence length

**What it is.** Standard deviation of sentence length near zero across a
passage, or a run of sentences all landing in the same narrow band.

**Citation.** Same position as T2-2. **This project holds no corpus measurement
of a sentence-length uniformity threshold, so no threshold is stated.** The
related published evidence is directional rather than diagnostic: van Nuenen,
"Voice Under Revision", arXiv 2604.22142, 2026-04-24, found that under LLM
revision, function words, contractions and first-person pronouns fall while
vocabulary diversity and word length rise, **even under explicit preserve-voice
prompts**, and that rewritten texts converge in feature space. Tier: CONTESTED,
preprint verified at abstract level. That says revision moves texts toward each
other. It does not give you a cutoff.

**False-positive class.** Everything in T2-2, plus two specific to this
statistic: the measurement is extremely sensitive to how you split sentences
(abbreviations, decimals, citations and code all break naive splitters), and
some capable human writers genuinely write in a narrow band by preference.

Note also the complication that this marker's naive interpretation runs into.
Miletic and Falk, arXiv 2605.19936, 2026-05-19, across more than 37,000 ACL
Anthology papers, found that LLM-modified text has **lower lexical diversity**
and yet expert readers rated it **more understandable and more exciting**.
Tier: CONTESTED. Uniformity is not automatically a quality defect, which is
another reason it cannot carry a finding on its own.

**Routes to.** Same as T2-2. The finding, if there is one, is the structural
one.

---

## Why Pangram's numbers are not used

Pangram's supporting-evidence page (https://www.pangram.com/supporting-evidence,
retrieved 2026-07-27) is the most widely circulated source of em-dash and
tricolon rate claims. It is recorded in this project's source ledger at tier
**FOLKLORE**, confidence **low**, and it is **not used as a measured figure
anywhere in this plugin**. The reasons, stated so the decision can be argued
with rather than merely obeyed:

1. **It is undated.** There is no publication date and no revision history, so
   there is no way to know which model cohort any figure describes. Given how
   fast the em-dash marker is documented to move (T2-1: roughly 4 percent in
   2023 to 20.3 percent in 2025), an undated rate is unusable.
2. **It is uncited.** No paper, no preprint, no dataset, no link to anything a
   reader could check.
3. **It states no sample size and no corpus description.** There is no way to
   compute an interval, and no way to know what population the baseline
   describes.
4. **It contradicts itself on the same page.** The page states a human em-dash
   baseline of **5 per 10,000 words** in its by-model section and **2 per
   10,000** in its summary table. Two different human baselines, same page, no
   reconciliation. A source that disagrees with itself about its own control
   condition cannot be used for either figure.
5. **The one independent measurement available disagrees with both.**
   Freeburg, arXiv 2603.27006, measured a human baseline of 3.23 per 1,000
   words, which is **32.3 per 10,000**, roughly six to sixteen times higher
   than Pangram's two figures. Freeburg is itself weak evidence (single-author,
   unaffiliated, not peer reviewed, tier CONTESTED), which is the point: the
   only thing checking the vendor number is a preprint the ledger also
   distrusts, and they disagree by an order of magnitude.
6. **The vendor sells a detector.** A larger measured gap between human and
   model punctuation rates is a selling point for the product. That conflict is
   not proof of anything, and it is not ignorable either. The project's own
   downgrade rule covers it: a vendor study with no methodology or sample size
   is capped at low confidence and CONTESTED tier, and a marketing page with no
   date and no citation is FOLKLORE and is never quoted as a measured figure.

Czuma (T2-1) is used instead: pre-registered, corpus stated, interval reported,
placebo split run, and a conclusion that limits its own application.

**What this means in practice.** If a document you are reviewing cites
Pangram's em-dash or tricolon figures, that is an attribution finding, and the
artifact is this section: the page is undated, uncited, gives no sample size,
and states two contradictory human baselines. Report the defect in the cited
document. Do not report a competing number in its place unless the document's
claim needs one, and then cite Czuma with its stated limitation.

---

## The rule this whole file exists to enforce

A tier 2 marker cannot fail anything and cannot be reported alone. When you
find yourself wanting to write "the em-dash density here is notable", stop:
either you have a structural artifact, in which case report that and leave the
punctuation out of it, or you do not, in which case there is no finding.

Tier 2 hits belong in the "Not flagged, and why" section of the report. That
section is the only visible evidence that the discipline in this file was
applied.
