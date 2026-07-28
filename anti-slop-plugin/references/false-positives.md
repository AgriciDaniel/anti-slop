<!--
Adapted from "Wikipedia:Signs of AI writing" and WikiProject AI Cleanup,
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing , retrieved
2026-07-27, by Wikipedia contributors. Licensed CC BY-SA 4.0,
https://creativecommons.org/licenses/by-sa/4.0/ . Changes: reorganised into
evidence tiers, false-positive classes added, routed to structural procedures,
and figures replaced with the sources recorded in this project's ledger.
This file and adaptations of it remain under CC BY-SA 4.0.
-->

# False positives, and the ethics

Read this before writing any finding whose evidence is style rather than
substance. Always read it before reviewing writing by a non-native English
speaker.

This is not a politeness file. It is the file that says who gets hurt when this
plugin is used carelessly, and it leads with the measurement rather than the
sentiment.

---

## 1. Who gets wrongly flagged, measured

**Stowe, Afanaseva, Raimundo, Sun and Patil (Pindrop), "Identifying Bias in
Machine-generated Text Detection", ACL 2026, peer reviewed, arXiv 2512.09292.**

Method: **16 detection models** run over student essays labelled for gender,
race and ethnicity, English-language-learner status, and socioeconomic status.

Findings:

- **English-language-learner essays were more likely to be flagged** as
  machine-generated.
- **Non-White ELL students were disproportionately flagged relative to White
  ELL peers.** The bias is not explained by second-language status alone. It
  compounds.
- **Human annotators, on the same essays, showed no significant demographic
  bias.**

Read the third finding carefully, because it is the one that determines what
this plugin is allowed to do. The bias is not a property of the task. It is a
property of the automated approach to the task. Humans reading the same essays
did not produce it. So a tool that automates the judgement does not inherit a
human failure mode, it manufactures a new one.

This supersedes the 2023 finding the field usually quotes, and it is the
current peer-reviewed citation for detector demographic bias.

**Liang et al., "GPT detectors are biased against non-native English writers",
Patterns 4(7):100779, 2023-07-10.** DOI 10.1016/j.patter.2023.100779

Seven detectors misclassified **61.3 percent** of TOEFL essays as
AI-generated, with **19.8 percent** unanimously flagged by all seven.

**The caveat travels with the number, every time: n equals 91 essays, seven
detectors, and the essays predate 2020.** Quoting 61.3 percent without the
sample size is exactly the overgeneralization defect this plugin flags in other
people's documents. It is a striking result on a small sample. Stowe et al. is
the larger, newer, peer-reviewed replacement; Liang et al. is the origin of the
concern and is cited for that.

**What follows from this, operationally.**

1. Firewall rule 1 is not a courtesy. **Never emit an authorship verdict.** The
   probability that a false accusation lands on a second-language writer is not
   uniform, and it is not small.
2. A LOW finding needs a **higher** bar than a HIGH one, not a lower one. HIGH
   findings rest on decidable facts, so they are cheap to check and cheap to
   correct. LOW findings rest on style, and style is where the measured harm
   lives.
3. When the author is a non-native English writer, style-evidenced findings are
   suppressed unless a structural test produced an artifact. No exceptions, and
   not "reported with lower confidence".
4. Never suggest that a text be run through a detector, never report a detector
   score, and never repeat one you are given as if it decided something. OpenAI
   withdrew its own classifier on 2023-07-20 citing its low rate of accuracy:
   26 percent true positive at a 9 percent false positive rate.

---

## 2. The ineffective indicators

Wikipedia's guide maintains a list of signals that should not be treated as
evidence. Reproduced here, adapted from Wikipedia:Signs of AI writing
(https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), retrieved
2026-07-27, under CC BY-SA 4.0.

The section opens with the harm, and the framing is worth keeping: false
accusations of AI use drive away new contributors and foster an atmosphere of
suspicion, and before claiming AI was used you should consider whether the
Dunning-Kruger effect or confirmation bias is clouding your judgement.

**Do not flag any of these.**

- **Perfect grammar.** Careful writers exist. Copy editors exist. Grammar
  checkers have existed for decades.
- **A combination of casual and formal registers**, or prose that is both
  clinical and emotional. The guide's own listed explanations: a technical-field
  writer, youth, playfulness, neurodivergence, or simply several editors
  working on one page.
- **"Bland" or "robotic" prose.** The guide notes that model output has
  specific traits and skews positive and verbose by default. Flat and dry is
  not the signature.
- **"Fancy", "academic" or "formal" vocabulary.** The guide is explicit: the
  vocabulary findings concern *specific words*, and the correlation does not
  extend to formal, academic, or elaborate-sounding prose in general.
  Generalizing the word list to "sounds educated" is precisely the step that
  produces the bias in section 1.
- **Common transition words in isolation.** However, moreover, furthermore,
  additionally. Density across a document may contribute to a cluster. One
  transition is nothing.
- **Curly quotation marks alone.** Innocent causes the guide names: the Chicago
  Manual of Style, Word smart quotes, macOS and iOS defaults, LanguageTool, and
  citation tools. It also records that Gemini and Claude models typically do
  not use them, so the marker is absent from major model families.
- **Em dashes alone.** See `markers-tier2.md` for the full treatment. Short
  version: the strongest study in the area concludes the em dash is a
  population-level indicator and not a per-paper detector, the marker is
  produced and eliminated by fine-tuning choices, and every word processor
  turns double hyphens into em dashes automatically.
- **Unsourced content.** Hundreds of thousands of Wikipedia articles carry
  citation-needed tags, most of them predating LLMs. The correlation now runs
  the other way: modern models cite frequently.
- **Correct, complex or consistent formatting.** Produced by editors, linters,
  templates and formatters.
- **Secondhand text.** A watched word or phrase appearing inside a quotation, a
  title, a proper name, a code sample, or an example where the phrase is being
  **discussed rather than used**. This file itself is full of watched phrases.
  So is every document about AI writing. Never flag the mention, and never
  rewrite a watched phrase inside quoted source text. This is why
  `lint_voice.py` leaves markdown blockquotes alone by default, and why turning
  that off requires the explicit `--include-quotes` flag.

---

## 3. The cluster rule

The guide's operative standard: look for **clusters** of tells, not isolated
ones. A single sign means nothing. Signs of different kinds co-occurring
densely in one span are what carry information.

This plugin implements that as a hard reporting threshold.

| Independent signals in one span | What you may report |
|---|---|
| 0 | Nothing. |
| 1 | Nothing, at any severity, with any hedge. It goes in "Not flagged, and why". |
| 2 | The structural finding on its own artifact, if a structural test produced one. The markers are not mentioned. |
| 3 or more, plus a structural artifact | A LOW finding, which must state how many independent signals it rests on. |

"Independent" is doing work in that table. Three tier 1 markers that are all
manifestations of the same sentence are one signal. Puffery vocabulary inside a
puffery construction inside a puffery paragraph is one thing seen three times.

A tier 2 marker contributes to a cluster count only after some tier 1 marker in
the same span has produced a structural artifact. A tier 3 marker never
contributes to a cluster count at all.

---

## 4. Signals of human writing, which must be preserved

The guide records, from over 25 years of observed article text, syntax patterns
that are **more** common in human-written articles. This list matters because
the naive de-slop instinct deletes every item on it.

- Simple copula phrases: "there is a", "it has a".
- Plain words over stiff synonyms: wrote rather than authored, moved rather
  than relocated, used rather than utilized, tried rather than attempted, died
  rather than passed away.
- Superlative and definitive statements: "one of the best", "is the only", "was
  the first".
- **Hedging qualifiers and intensifiers: very, perhaps, tends to.**
- **Isolated wordy constructions: as a result of, in order to, all of the, a
  part of, the fact that.**

The last two items are a direct contradiction of the most common
de-slop advice, and this plugin resolves it in the guide's favour.
**Mechanically stripping filler and hedging makes text read more generated, not
less.** Only cut a hedge when a finding says the hedged claim is vacuous, and
then cut the claim rather than the hedge.

Two more preservation rules worth stating:

- **Specific, unusual, hard-to-fabricate detail is a human signal.** The
  documented mechanism runs the other way: models regress toward the most
  statistically likely phrasing that fits the widest range of cases, so
  specifics get rounded off. A rewrite that removes a specific is moving the
  text in the wrong direction.
- **Text predating 2022-11-30 cannot involve a chatbot.** The guide states this
  plainly, and it is the one genuinely decidable authorship fact in the whole
  field. It is also not a licence to reason about anything after that date.

---

## 5. Genre and register, which are not defects

A pattern is a defect only against the conventions of the document actually in
front of you. Check the genre before the sentence.

| Genre | Do not flag |
|---|---|
| Marketing copy, grant applications, award citations, museum labels, obituaries | Puffery, significance claims, promotional register. Asserting importance is the document's job. |
| Reference documentation, API specs, standards text, legal drafting | Uniform sentence length, low burstiness, repetition of exact terms, passive voice, formulaic section structure. |
| Scientific and medical writing | Hedging, passive voice where the agent is irrelevant, formal vocabulary, structured abstracts. |
| Changelogs, release notes, migration guides, ADRs | Diff-anchored writing. Narrating change is the point. |
| Tutorials, teaching repositories, example code | Redundant comments, step narration, obvious explanations. |
| Translated text | Elegant variation, unusual collocations, flattened rhythm, mixed English varieties. |
| Templated PR bodies, compliance attestations | Canned assurance language required by the repository. |
| Fiction | Nearly everything in this plugin. Invented detail is the job. |

---

## 6. Scanner false positives

Layer 0 is allowed to hard-fail, which makes its false positives more expensive
than anywhere else. Known classes, per scanner:

- **`scan_residue.py`**: a document *about* residue markers, which quotes them.
  Test fixtures containing residue on purpose. Legitimate lenticular brackets
  in Japanese and Chinese text. In markdown, fenced code and inline code spans
  are skipped by default for exactly this reason; `--include-code` turns that
  protection off, so use it deliberately.
- **`scan_placeholders.py`**: template files, scaffolding, form letters and
  boilerplate where the placeholder is the deliverable. Infobox comments such
  as "Add spouse if reliably sourced" predate LLMs and are normal.
- **`scan_refs.py`**: paywalled and library-proxied links legitimately fail an
  anonymous fetch. Rate limits and authentication walls are not fabrication.
  Bots and copy-paste truncate URLs, so a malformed URL is a formatting defect.
  An access date in the past is normal; an access date in a placeholder format
  such as `2025-XX-XX` is not. Resolution requires `--online`; the offline
  default checks shape and checksums only, and an offline run is not a clean
  bill of health.
- **`scan_packages.py`**: private registries, monorepo-local packages, git and
  path dependencies, scoped names the lookup does not resolve, optional imports
  guarded by try/except. Existence checks require `--online`. Use
  `--allowlist` for known-good internal names rather than silencing the
  scanner.
- **`lint_voice.py`**: this one is a **house style rule**, not a slop signal.
  Its hits are style violations and are never evidence about a text's origin.
  It leaves markdown blockquotes alone by default because quoted source text is
  not yours to restyle.

When a scanner fires on a legitimate case, record it as a scanner false
positive in the report and leave the artifact alone. Never edit code or prose
to make a scanner quiet.

---

## 7. Why the markers rot, and what that obliges

Every marker in this plugin is a description of a moving target.

- **Cohorts shift.** The Wikipedia guide gives three dated vocabulary cohorts.
  Words characteristic of 2023 output are largely absent from 2026 output.
- **Human usage is converging on model usage.** Yakura et al., arXiv
  2409.01754, measured delve up 48 percent, realm up 35 percent and adept up 51
  percent in spontaneous human speech within 18 months of ChatGPT's release,
  across more than 740,000 hours of audio, with a preregistered follow-up at n
  equals 496. The baseline is moving under the measurement.
- **Training choices create and destroy markers.** Freeburg, arXiv 2603.27006,
  measured base Llama 3.1 8B at 0.49 em dashes per 1,000 words and its
  instruction-tuned counterpart at 0.00. Tier CONTESTED, single-author
  unaffiliated preprint.
- **Models are instructed away from tells.** The guide records that some newer
  models are instructed to avoid boldface overuse, and that GPT-5.1 suppresses
  em dashes.
- **Writers adjust.** The guide notes that people change their behaviour to
  avoid accusations, or become defensive about tropes they never used.

The obligation this creates: every marker entry carries its retrieval date and
its citation so that a reader can tell how old the claim is. When you cannot
tell how current a marker is, weight it lower. When a marker's cohort is
retired, say so rather than flagging it.

---

## 8. The bright line

This plugin **does not detect AI authorship** and **cannot be used to accuse
anyone**.

It reports defects: fabricated citations, packages that do not exist, APIs that
do not exist, tests that assert nothing, padding that survives deletion,
claims that survive inversion as vacuous, attributions that do not resolve.
Every one of those is a defect regardless of who or what produced it, and every
one of them is fixable by the author without any admission about process.

That is the whole design. A defect report is actionable and falsifiable. An
authorship claim is neither, and the measurement in section 1 shows who pays
for it.

If you are asked to produce an authorship verdict, decline and say what this
plugin does instead. If you are asked to estimate a percentage, there is no
such number here. If you are handed a detector score, do not repeat it as
though it decided something.

The one honest thing that can be said about human judgement here comes from
Russell, Karpinska and Iyyer, ACL 2025, arXiv 2501.15654: a majority vote of
five expert annotators misclassified **1 of 300** articles, outperforming
commercial and open-source detectors even under paraphrase evasion. Careful
human readers are the best instrument available, and that is an argument for
reading the text, not for automating a verdict about its origin.
