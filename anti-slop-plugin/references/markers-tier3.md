<!--
Adapted from "Wikipedia:Signs of AI writing" and WikiProject AI Cleanup,
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing , retrieved
2026-07-27, by Wikipedia contributors. Licensed CC BY-SA 4.0,
https://creativecommons.org/licenses/by-sa/4.0/ . Changes: reorganised into
evidence tiers, false-positive classes added, routed to structural procedures,
and figures replaced with the sources recorded in this project's ledger.
This file and adaptations of it remain under CC BY-SA 4.0.
-->

# Tier 3 markers: folk wisdom

Load this when you are tempted to flag a single word, a punctuation habit, or a
heuristic you picked up somewhere and cannot cite.

**Nothing in this file is actionable.** Tier 3 items are recorded so that they
can be argued with, not so that they can be used. A tier 3 item never selects a
span, never contributes to a cluster count, never appears in a finding, and
never appears in a severity table. Its entire function is to give you somewhere
to put a hunch other than the report.

Why record them at all: an unwritten heuristic is not a discarded heuristic. It
is a heuristic that operates without review. Writing them down is what makes it
possible to notice when one of them is wrong, and to notice when one of them
graduates because somebody finally measured it.

---

## The tier 3 test

Before you act on any pattern, ask three questions.

1. **Who measured it, on what corpus, and where can I read that?** If the
   answer is "everyone knows" or "I have seen it a lot", it is tier 3.
2. **What is its false-positive class?** If you cannot name a legitimate
   document that would trip it, you have not thought about it hard enough to
   use it.
3. **Would it survive being shown to the author?** A finding you would not
   defend to the person who wrote the text is not a finding.

---

## Individual words in isolation

The single most common tier 3 error is treating one cohort word as evidence.

`markers-tier1.md` documents excess vocabulary as a **density** phenomenon
measured across more than 15 million abstracts. One instance of "delve" is not
a small amount of that evidence. It is none of it. The Wikipedia guide states
the threshold directly: one or two of these words appearing in an edit may be
coincidental, while text introducing many of them, many times, is the pattern
worth investigating.

Three specific traps.

**Synonym generalization.** The guide's own discipline rule is that this
section is to be taken as literally as possible: a word being overused by AI
does not imply its synonyms are also overused. "Delve" is on the list.
"Explore", "examine" and "investigate" are not. Extending the list by intuition
is how it fills with taste.

**Cohort rot.** The list is dated. The guide gives three cohorts: 2023 to
mid-2024 (additionally, boasts, bolstered, crucial, delve, emphasizing,
enduring, garner, intricate, interplay, key, landscape, meticulous, pivotal,
underscore, tapestry, testament, valuable, vibrant), mid-2024 to mid-2025
(align with, bolstered, crucial, emphasizing, enhance, enduring, fostering,
highlighting, pivotal, showcasing, underscore, vibrant), and mid-2025 onward
(emphasizing, enhance, highlighting, showcasing, plus the notability
vocabulary). Flagging a retired cohort word in a 2026 document is flagging the
past.

**Convergence.** Yakura et al., arXiv 2409.01754, measured delve up 48 percent,
realm up 35 percent and adept up 51 percent in spontaneous human speech within
18 months of ChatGPT's release. The words are entering ordinary usage. A word
list is a depreciating asset.

---

## Heuristics recorded here, and why each is not usable

These come from working practice and from prior art. Several are plausible.
None carries a corpus measurement in this project's ledger, which is exactly
what keeps them here.

**Uncited stylistic patterns inherited from prior art.** blader/humanizer
(MIT, v2.9.1 at 2026-07-22) contributes eight patterns with no cited
corroboration: persuasive authority tropes ("the real question is", "at its
core", "what really matters"), signposting and announcements ("let's dive in",
"here's what you need to know"), fragmented headers (a heading followed by a
one-line restatement of the heading), diff-anchored writing, manufactured
punchlines and staccato drama, aphorism formulas ("X is the Y of Z"),
conversational rhetorical openers ("Honestly?", "Look,", "Here's the thing"),
and predicate-position hyphenation ("the report is high-quality"). These are
plausible descriptions of how current chat models write for blog and technical
audiences. They match nothing in the corpus literature this project holds. The
Wikipedia guide's own maintainer gate is the right standard and none of them
meet it: only add a word to the vocabulary box if its overuse is corroborated
by at least one reliable, non-pop-science external source.

One of these has a partial exception. Diff-anchored writing is not usable as a
*marker*, but the underlying defect is real and decidable on the code surface:
a comment that narrates a change stops being true at the next commit. That is
handled in `code-markers.md` as a load-bearing test target, not as a marker.

**Emoji as formatting.** Recorded in the Wikipedia guide as historically
observed, mostly on talk pages and in edit summaries, and noted as more rare
now. Falls to tier 3 because it is a house style question in most projects, not
a defect.

**Title case in headings.** A Wikipedia manual-of-style preference. AP style,
Chicago headline style and most product documentation use title case
deliberately. Never a defect outside a project whose style guide says so.

**Curly quotation marks.** The guide lists innocent causes: Chicago Manual of
Style, Word smart quotes, macOS and iOS defaults, LanguageTool, and citation
tools. It also records a discriminator that cuts the other way, which is
precisely why this is unusable: Gemini and Claude models typically do not use
curly quotes. A marker that is absent from several major model families is not
a marker.

**Skipping heading levels and thematic breaks before headings.** Recorded in
the guide as observed formatting habits. Also produced by every Markdown editor
and every documentation generator in existence.

**Passive voice.** Correct and preferred in scientific writing where the agent
is genuinely irrelevant, in incident reports, and in legal drafting. There is
no measurement here and there is a large legitimate-genre class.

**Small unnecessary tables.** Recorded in the guide. Also a normal preference.

**Elegant variation and synonym cycling.** Recorded in the guide with two
caveats that gut it as a marker: it does not apply across separately generated
edits, and non-native English speakers are frequently taught to avoid repeating
words. Italian schools are the example the guide names.

**English-variety mismatch.** The guide records that several models default to
American English, so an Indian author writing about an Indian institution in
American English is a noted pattern. The guide immediately caveats it:
second-language speakers mix varieties, code switching is normal, and only
dramatic and not easily explainable shifts count. It sits at tier 3 in this
plugin because acting on it means reasoning about the author's nationality,
which is exactly the reasoning class that `false-positives.md` shows produces
measured demographic harm.

---

## Historical indicators

Recorded for archaeology only. These identify old model output. They are not
usable on current text, and finding one in a 2023 document tells you about
2023.

- Didactic disclaimers, November 2022 to 2024: "it's important to note",
  "it's crucial to remember", "worth noting", "may vary".
- Section summaries: "In summary", "In conclusion", "Overall", and standalone
  "Conclusion" sections.
- Prompt refusals left in text: "as an AI language model", "as a large language
  model", "I cannot offer medical advice, but I can".
- Abrupt cut-offs from token limits. Caveat from the guide: also caused by bad
  copy-paste and by copyright violations.
- Outdated access-date parameters, such as a December 2025 article whose
  citations all read 12 December 2024.

Note the boundary between this list and Layer 0. A *stale* access date is tier
3 folk wisdom. A *placeholder* access date such as `2025-XX-XX` is a
deterministic defect that `scan_placeholders.py` decides. The difference is
that one is a guess about provenance and the other is unambiguously broken.

---

## Below tier 3: the ineffective indicators

Wikipedia's guide maintains a separate list of signals that are not merely weak
but actively misleading, under the heading "Ineffective indicators". These sit
below tier 3: tier 3 items are unmeasured, while these are things the guide
positively advises against treating as evidence. They are reproduced here so
that a tier 3 hunch cannot quietly promote one of them.

- **Perfect grammar.**
- **A mix of casual and formal registers**, or language that is both clinical
  and emotional. The guide's listed explanations: a technical-field writer,
  youth, playfulness, neurodivergence, or simply several editors on one page.
- **"Bland" or "robotic" prose.** The guide notes that model output has
  specific traits and skews positive and verbose by default, so "flat" is not
  the signature.
- **"Fancy", "academic" or "formal" prose.** The guide is explicit that the
  vocabulary findings concern *specific words* and that the correlation does
  not extend to formal-sounding prose in general.
- **Transition words in isolation.**
- **Curly quotation marks alone.**
- **Em dashes alone.**
- **Unsourced content.** Hundreds of thousands of Wikipedia articles are tagged
  for citations, most of them predating LLMs, and modern models cite often.
- **Correct or complex formatting.**
- **Bizarre wikitext**, which the guide traces to browser extensions and known
  editor bugs.
- **Secondhand text**: a watched phrase appearing inside a quotation, a title,
  a proper name, or an example where the phrase is being discussed rather than
  used. Never flag the mention.

The opening of that section is the part worth memorising: false accusations of
AI use drive away new contributors and foster an atmosphere of suspicion, and
before claiming AI was used you should consider whether the Dunning-Kruger
effect or confirmation bias is clouding your judgement.

**The cluster rule.** The guide's operative standard, and this plugin's: look
for clusters of signs, not isolated ones. A single sign means nothing. Signs of
different kinds, co-occurring densely in one span, are what carry information.
This plugin implements that as a hard reporting threshold, stated in
`markers-tier1.md`: three independent signals plus a structural artifact for a
LOW finding, and no isolated signal is reportable at any severity.

The full list, with the evidence on who gets wrongly flagged and why the
threshold is set where it is, is in `false-positives.md`. Read that before any
style-evidenced finding.

---

## Graduation

An item leaves this file when someone measures it. The requirements, matching
this project's source ledger rules:

- A named source with a URL, a date, and a stated method.
- A corpus with a stated size.
- A stated false-positive class.
- A retrieval date and a refresh date, because marker evidence rots.

Until then it stays here, and it stays out of the report.

---

## The rule

If a pattern is in this file, and the text in front of you exhibits it, the
correct output is a line in the report's "Not flagged, and why" section. That
is the whole permitted use.

Marker taxonomy, the ineffective-indicators framing, and the historical
indicator list are adapted from Wikipedia:Signs of AI writing
(https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), retrieved
2026-07-27, under CC BY-SA 4.0. The full ineffective-indicators list and its
cluster rule are in `false-positives.md`, which you must read before any
style-evidenced finding.
