<!--
Adapted from "Wikipedia:Signs of AI writing" and WikiProject AI Cleanup,
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing , retrieved
2026-07-27, by Wikipedia contributors. Licensed CC BY-SA 4.0,
https://creativecommons.org/licenses/by-sa/4.0/ . Changes: reorganised into
evidence tiers, false-positive classes added, routed to structural procedures,
and figures replaced with the sources recorded in this project's ledger.
This file and adaptations of it remain under CC BY-SA 4.0.
-->

# Tier 1 markers: corpus-validated

Load this when you are selecting spans to test, or when a finding needs to name
which marker put the span on your list.

**A tier 1 marker is not a finding.** It is corpus-validated evidence that a
span is worth spending a structural test on. The test is what you report. If
the test comes back clean, you drop the marker hit; you do not downgrade it to
LOW to keep the finding alive. That rule is firewall rule 2 and it is not
negotiable at any tier, least of all this one, where the evidence is strongest
and the temptation to skip the test is therefore greatest.

**Tier 1 means the pattern has been measured on a corpus by someone who
published their method.** It does not mean the pattern identifies an author. No
marker in this file, at any density, licenses a statement about who or what
wrote a text. See `false-positives.md` for the measured cost of getting that
wrong.

Marker taxonomy and the words-to-watch lists below are adapted from
Wikipedia:Signs of AI writing (https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
retrieved 2026-07-27, used under CC BY-SA 4.0. The corpus figures come from the
sources named in each entry.

---

## T1-1. Excess vocabulary

**What it is.** A cohort of stylistic verbs and adjectives whose frequency in
published text rose sharply and simultaneously after late 2022, far beyond what
the pre-2023 trend predicts. The cohort is overwhelmingly stylistic rather than
topical: the excess sits in words that colour a claim, not in words that carry
one. Current watch list, per the Wikipedia guide: additionally (especially
opening a sentence), align with, boasts (meaning "has"), bolstered, crucial,
delve, emphasizing, enduring, enhance, fostering, garner, highlight (as a
verb), interplay, intricate, intricacies, key (as an adjective), landscape (as
an abstract noun), meticulous, meticulously, pivotal, robust, showcase,
tapestry (as an abstract noun), testament, underscore (as a verb), valuable,
vibrant.

**Example.**

> Additionally, a distinctive feature of Somali cuisine is the incorporation of
> camel meat. An enduring testament to Italian colonial influence is the
> widespread adoption of pasta in the local culinary landscape, showcasing how
> these dishes have integrated into the traditional diet.

Four cohort words in two sentences (additionally, enduring, testament,
landscape, showcasing). Density is the signal, not any single word.

**Citation.** Kobak et al., "Delving into LLM-assisted writing in biomedical
publications through excess vocabulary", Science Advances 11(27), 2025-07-02,
DOI 10.1126/sciadv.adt3813. Over 15
million PubMed abstracts, 2010 to 2024, using a detector-free method that
compares observed word frequencies against frequencies extrapolated from the
pre-2023 trend. Finding: **at least 13.5 percent** of 2024 abstracts show the
excess-vocabulary signature, **reaching 40 percent in some subcorpora**.

The widely quoted **10 percent and 30 percent** pair is from the withdrawn June
2024 preprint version. Do not use it. If you see those two numbers in a
document citing Kobak, that is itself an attribution finding: the citation
resolves to a paper that says something different.

**False-positive class.** The largest in this file, and it grows.

- **Register.** Biomedical and policy prose used "crucial", "robust" and "key"
  long before 2022. The cohort was selected by a change in rate, not by a
  claim that the words are bad.
- **Convergence.** Human speech is moving toward the cohort. Yakura et al.,
  arXiv 2409.01754, measured delve up 48 percent, realm up 35 percent and adept
  up 51 percent in spontaneous human speech within 18 months of ChatGPT's
  release, across more than 740,000 hours of podcast audio, with a
  preregistered follow-up at n equals 496 confirming entrenchment in active
  vocabulary. A word this list calls a marker in 2026 may be ordinary English
  by 2028.
- **Cohort rot.** The guide documents three dated cohorts, not one list. The
  2023 to mid-2024 set (delve, tapestry, testament, meticulous) is largely
  gone from current model output; the mid-2025 and later set narrows to
  emphasizing, enhance, highlighting, showcasing plus the notability
  vocabulary. A hit on a retired cohort word says less than a hit on a current
  one, and this file will age.
- **Synonyms are not implicated.** The guide's own discipline rule: a word
  being overused does not imply its synonyms are. "Delve" is on the list.
  "Explore" is not. Do not generalize the list.
- **Secondhand use.** A document discussing the marker list, quoting it, or
  naming a phrase rather than using it is not a hit.

**Routes to.** Deletion first, then stranger. Cohort words cluster around spans
that assert importance without asserting content, which is exactly what
deletion detects. If the span survives deletion, run stranger on it before you
give up: the second most common home for these words is a sentence that names
nothing a reader could not have guessed.

---

## T1-2. Puffery and undue emphasis on significance

**What it is.** Statements that inflate importance rather than state facts, and
statements that situate an arbitrary detail inside a broader trend, legacy or
debate that the source never establishes. The mechanism is documented: the
model regresses toward the most statistically likely phrasing that fits the
widest range of cases, so a specific fact ("inventor of the first
train-coupling device") is replaced by a generic superlative ("a revolutionary
titan of industry"). The subject becomes simultaneously less specific and more
exaggerated.

Words to watch, per the guide: stands as, serves as, is a testament to, is a
reminder of, a vital role, a significant role, a crucial role, a pivotal
moment, a key turning point, underscores its importance, highlights its
significance, reflects broader, symbolizing its ongoing, contributing to the,
setting the stage for, marking a shift, evolving landscape, focal point,
indelible mark, deeply rooted. Also the trend and debate variants: generated
debate, shaped emerging policy discussions, prompted broader reflection,
raising philosophical questions. Also the hedging preamble that concedes
unimportance and then asserts importance anyway: "Though it saw only limited
application, it contributes to the broader history of early aviation
engineering."

**Example.**

> The Statistical Institute of Catalonia was officially established in 1989,
> marking a pivotal moment in the evolution of regional statistics in Spain.

**Citation.** Wikipedia:Signs of AI writing, sections WP:AIPUFFERY and
WP:AILEGACY, retrieved 2026-07-27. The guide records a model-generation
calibration worth carrying: older models produce more blatantly positive text,
while newer models are more subtly positive and tend to avoid obviously
superlative statements such as "the best". The absence of loud superlatives is
therefore not evidence of anything.

**False-positive class.** Genre. Marketing copy, grant applications, museum
labels, obituaries, award citations and press releases are supposed to assert
significance; that is the document's job. Promotional register is a defect only
where the document claims to be neutral. Also: an author who genuinely
established a claim's significance earlier in the document is entitled to refer
back to it.

**Routes to.** Inversion, then deletion. "X plays a crucial role in Y" is the
canonical inversion target: write out "X plays no role in Y", ask whether
anyone would assert it, and if nobody would, the original excluded no possible
state of the world. Definitions and stipulations are exempt from inversion; see
`structural-tests.md`.

---

## T1-3. Over-attribution

**What it is.** Two related defects that both concern how sources are talked
about rather than whether they exist.

*Canned emphasis on notability and coverage.* The text works to establish that
the subject is important enough to write about, in the body prose, where a
human would use an inline citation or nothing at all. Words to watch:
independent coverage, local media outlets, regional media outlets, national
media outlets, trade publications, profiled in, written by a leading expert,
active social media presence, maintains a strong digital presence. The guide
notes this is more common in output from tools released in 2025 or later, and
that models often echo Wikipedia's own guideline vocabulary such as
"independent coverage".

*Overgeneralization of source count.* One or two sources presented as a
consensus. A single named person rendered as "scholars" or "researchers". A
short list implied to be non-exhaustive when the source gives no indication
that other cases exist. Words to watch: industry reports, observers have cited,
experts argue, some critics argue, several sources, several publications,
described in scholarship, modern researchers treat, such as (introducing a list
that is in fact exhaustive).

The RAG-era form is the dangerous one: a superficial claim attached to a real,
correctly cited, named source that does not say anything close to it. The
citation resolves. The identity matches. The support is absent.

**Example.**

> Her views have been cited in local, regional and national media outlets, and
> toy industry publications such as *The Toy Insider* and *Mojo Nation* have
> described her influence.

Two named publications are presented as a class ("toy industry publications
such as"), and the media-outlets clause names nothing at all.

**Citation.** Wikipedia:Signs of AI writing, sections WP:OVERATTRIBUTION,
WP:AIATTR and WP:AIWEASEL, retrieved 2026-07-27. The WikiProject AI Cleanup
page states the operative rule directly: as of 2026, recent models will usually
cite real sources and will likely not verify the content those sources are
being cited for, so the existence of the sources should not by itself be taken
as evidence about how the text was produced.

**False-positive class.** Notability prose is correct in a document whose
purpose is to establish notability, such as an award nomination or an editorial
justification. Vague attribution is correct where the field genuinely has a
consensus and the document has already cited the review that establishes it.
And a source-count claim is not a defect when the document's bibliography
actually contains the sources implied.

**Routes to.** Attribution, always, and it is the one tier 1 marker that can
produce a HIGH finding, because non-resolution and non-support are decidable.
Run `scan_refs.py` for the mechanical layer first. Then apply the counting
rule: count the distinct sources actually cited, then read what the sentence
claims about how many exist.

---

## T1-4. Negative parallelism

**What it is.** Definition by contrast with a negated alternative that nobody
proposed. The guide splits it into three subtypes; the third is the one most
often missed.

1. *Not just X, but also Y.* "Not only ... but ...", "It is not just ..., it's
   ..."
2. *Not X, but Y.* "It's not ..., it's ...", and the clipped tailing negation
   tacked onto a sentence end: "no guessing", "no wasted motion".
3. *X rather than Y.* The reversed form, which the guide records as
   particularly common in Grok output: "prioritizing empirical consolidation of
   power amid fragmented loyalties rather than ideological purity."

The construction can also spread across several sentences rather than sitting
inside one.

**Example.**

> It's not just about the beat riding under the vocals; it's part of the
> aggression and atmosphere. It's not merely a song, it's a statement.

**Citation.** Wikipedia:Signs of AI writing, section WP:AIPARALLEL, retrieved
2026-07-27.

**False-positive class.** The construction is legitimate and old whenever the
negated alternative is one a reader would actually hold. "The bug is not a race
condition, it is an off-by-one in the retry counter" corrects a real
expectation and carries information. Rhetoric, speeches, opinion columns and
advocacy writing use the form deliberately and well. The defect is the negated
half being a straw alternative nobody asserted.

**Routes to.** Inversion, applied to the negated half. Ask what the sentence
would lose if the "not X" clause were deleted outright. If the answer is
nothing, because no reader believed X, the construction is doing rhythm rather
than work, and you have a deletion finding on the negated clause.

---

## T1-5. Tricolons and the rule of three

**What it is.** Ideas forced into groups of three: "adjective, adjective,
adjective" or "short phrase, short phrase, and short phrase". The structure
makes a superficial analysis look comprehensive. The tell is not the presence
of three items but that the third item was chosen for cadence, so it is either
a near-synonym of the second or a category error next to the first two.

**Example.**

> The event features keynote sessions, panel discussions, and networking
> opportunities. Attendees can expect innovation, inspiration, and industry
> insights.

**Citation.** Bakhshi, "Saying More Than They Know", arXiv 2604.19768,
2026-03-27. 225 texts, roughly 600,000 tokens. Finding: LLMs produce tricolons
at **nearly twice the expert human rate**. Tier: CONTESTED. This is a preprint
verified at abstract level only, and it must be cited with that caveat
alongside peer-reviewed work.

Note what is not cited here. Pangram's claim that AI uses tricolons about four
times as often as humans is not used, for the reasons set out in
`markers-tier2.md`.

**False-positive class.** Three is a real number and lists of three are
ordinary. Legal drafting, API documentation, specifications and requirements
lists all enumerate exhaustively and often land on three. A tricolon is
reportable only when the third item fails to add a distinct thing, and you
demonstrate that by naming what the third item contributes.

**Routes to.** Deletion, applied to the third item alone. Cut it, read the
sentence, and name what was lost. "Lost: nothing, because industry insights is
what panel discussions produce" is an artifact. "The rule of three appears
twice in this paragraph" is not.

---

## T1-6. Hesitancy and hedging markers

**What it is.** Elevated density of epistemic hedges: may, might, could
potentially, it is possible that, some argue, arguably, generally, tends to,
in many cases. Measured density is the marker. Individual hedges are not.

**Example.**

> It could potentially possibly be argued that the policy might have some
> effect on outcomes.

**Citation.** Bakhshi, "Saying More Than They Know", arXiv 2604.19768,
2026-03-27. Same corpus as T1-5. Finding: LLMs produce hesitancy markers at
**roughly twice human density**. Tier: CONTESTED, preprint verified at abstract
level.

**False-positive class.** The worst in this file, because the naive repair
makes things worse in a measurable direction. Wikipedia's own list of empirical
signals of human writing, drawn from over 25 years of observed article text,
includes hedging qualifiers and intensifiers (very, perhaps, tends to) and
wordy constructions (in order to, as a result of, the fact that, all of the, a
part of). Stripping hedges mechanically converges the text toward the generated
register rather than away from it. Also: hedging is correct writing in science,
law, medicine and risk analysis, where an unhedged claim would be a false one.
Non-native English writers frequently hedge more, which puts this marker
directly in the path of the bias documented in `false-positives.md`.

**Routes to.** Inversion, applied to the hedged proposition, never to the
hedge. The question is whether the claim underneath says anything, not whether
the author sounded confident. If the unhedged claim carries information, there
is no finding and you leave the hedge alone. Only when the claim is vacuous do
you have a finding, and then the repair cuts the claim, not the hedge.

---

## Corpus-cited secondhand

One further marker sits at tier 1 strength but reaches this file through an
intermediary, so it is separated rather than mixed in.

### T1-7. Copula avoidance

**What it is.** Elaborate constructions substituted for plain "is" and "are":
serves as, stands as, marks, functions as, operates as, represents, boasts,
features, maintains, offers, refers to. Also the career forms: "ventured into
politics as a candidate" for "was a candidate", "began his career as" for
"was".

**Example.**

> Gallery 825 serves as the association's exhibition space and boasts over
> 3,000 square feet.

**Citation.** Wikipedia:Signs of AI writing, its section on avoidance of basic
copulatives, retrieved 2026-07-27, which cites Geng and Trotta (arXiv
2404.08627) for an over 10 percent decrease in the use of "is" and "are" in
academic writing in 2023.
**This is a secondhand citation chain.** The underlying paper is not in this
project's source ledger and was not independently verified here. Treat the
pattern as tier 1 and the number as unverified: quote the pattern, not the
figure.

**False-positive class.** "Serves as" and "functions as" are correct where a
thing plays a role it was not built for. "Represents" is correct in
mathematics, diplomacy and law. The guide adds a specific trap: do not confuse
this with "has" in the present perfect, as in "has been featured".

**Routes to.** Stranger. Copula avoidance rarely creates a false claim; it
creates a sentence a stranger could have written. Name the specific fact
recoverable from the sentence. If the only fact is the square footage, the
elaboration was carrying nothing.

---

## How tier 1 hits combine

A single tier 1 hit selects one span for one test. It does not raise the
severity of anything and it does not appear in the report.

Clusters matter, and the cluster rule is the same one Wikipedia states: one or
two of these appearing may be coincidence, while a text introducing many of
them, many times, is the pattern worth investigating. Operationally, in this
plugin: a LOW finding must name at least three independent signals in one span
and must still carry a structural artifact. Two signals and an artifact is a
MEDIUM finding on the artifact alone, with the marker not mentioned. One signal
is not reportable at any severity.

Read `markers-tier2.md` before adding em-dash density, burstiness or sentence
uniformity to a cluster count. Those do not carry the same weight and the file
says why.
