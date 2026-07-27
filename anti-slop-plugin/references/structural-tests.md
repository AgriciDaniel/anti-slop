# The five structural tests

Load this when you are about to run a structural test and need the artifact
format, or when a finding arrives without an artifact and you need to know what
was supposed to be there.

Every test here is mechanical. Each one produces a named artifact: a concrete
thing you can hand to someone who does not trust you. A test you did not
actually run produces no artifact and therefore no finding. There is no
"probably padding" and no "reads as generic".

This is the whole design constraint. LLM-as-judge agreement with human slop
labels is near zero (kappa 0.01 for GPT-5, -0.01 for DeepSeek-V3, 0.03 for
o3-mini; Shaib, Chakrabarty, Garcia-Olano and Wallace, arXiv 2509.19163, rev.
2026-01-24). Span-level extraction by the same judges runs at precision 0.14
and recall 0.11. So the model is never asked whether something looks like slop.
It is asked to perform an operation and report what happened.

**The examples below are constructed for illustration.** Where a real source is
named, it is real and cited. Where a fact about a river, an institute or a
person appears, it is invented scaffolding for the example and is not a claim
about the world.

---

## 1. Deletion

**Procedure.** Cut the span. Read what remains. Name what was lost.

**Artifact.** The cut span, plus the named loss. If the loss is "nothing", the
span was padding and you have a MEDIUM finding.

**Worked case, defect found.**

Original:

> The Statistical Institute of Catalonia was officially established in 1989,
> marking a pivotal moment in the evolution of regional statistics in Spain.
> This initiative was part of a broader movement across Spain to decentralize
> administrative functions and enhance regional governance.

Cut span:

> marking a pivotal moment in the evolution of regional statistics in Spain

Artifact:

> Lost: nothing. No prior moment is named, no later moment is named, and no
> evolution is described anywhere in the paragraph or the section, so nothing
> is being ranked against anything. The founding date and the decentralization
> context both survive the cut intact.

Finding: MEDIUM, confidence high. Padding.

**Worked case, no defect.**

Original:

> The institute was established in 1989, three years after census
> administration was devolved to the autonomous communities.

Cut span:

> three years after census administration was devolved to the autonomous
> communities

Artifact:

> Lost: the ordering that places the founding after devolution, and the only
> statement in the paragraph that explains why a regional statistics body
> existed to be founded.

No finding. The clause is load-bearing. Record it in "Not flagged, and why".

**Failure mode.** Cutting a span and then paraphrasing the rest so that the
loss disappears. Cut and read. Do not repair while testing.

---

## 2. Inversion

**Procedure.** Negate the claim. Write the negation out in full as a sentence
someone might publish. Ask whether anyone would assert it.

**Artifact.** The negation, written out. If nobody would ever assert it, the
original carries no information and you have a MEDIUM finding.

**Worked case, defect found.**

Original claim:

> The river plays a crucial role in the regional ecosystem.

Negation, written out:

> The river plays no role in the regional ecosystem.

Artifact:

> Nobody would assert the negation about a river in its own watershed. Every
> river plays some role in the ecosystem it runs through, so the original
> sentence excludes no possible state of the world and therefore states
> nothing.

Finding: MEDIUM, confidence high. Vacuous claim. Repair is to state the
specific role the source describes, or to cut.

**Worked case, no defect.**

Original claim:

> The river supplies the irrigation canals of the Hetao district.

Negation, written out:

> The river does not supply the irrigation canals of the Hetao district.

Artifact:

> Someone could assert the negation, and both versions are checkable against a
> source. The original therefore carries information.

No finding.

**Failure mode.** Negating a word instead of the claim. "Crucial" inverted to
"not very crucial" is a hedge, not a negation. Negate the proposition: does the
thing happen at all.

**Second failure mode.** Applying this to definitions and stipulations. "A
catchment area is the geographic area served by a facility" inverts to
something nobody would assert, but it is a definition, not an empty claim.
Definitions are exempt. Claims about significance, influence, contribution and
role are the target.

---

## 3. Stranger

**Procedure.** Ask whether someone who never read the source could have written
this sentence, given only the topic and the shape of the document.

**Artifact.** The specific fact that only someone who did the work would know.
If you cannot name one from the source, the span is generic and you have a
finding.

**Worked case, defect found.**

Original:

> Her views have been cited in local, regional and national media outlets, and
> she maintains an active social media presence.

Artifact:

> A stranger could write this sentence about any commentator in any field
> without reading anything. Searching the source material for a fact that
> would survive this test returns one: the source names a single outlet and a
> single topic, and says nothing about social media.

Finding: MEDIUM, confidence high. Genericity. Repair is to name the outlet and
the topic, and to cut the social media clause because the source does not
support it.

**Worked case, no defect.**

Original:

> Her 1994 dissent is the only opinion in the series to cite the 1911 statute
> directly.

Artifact:

> A stranger could not produce "1994", "the only", or "the 1911 statute". Each
> requires having read the series.

No finding.

**Failure mode.** Confusing "generic" with "simple". "The gallery is in
Portland" is simple and specific. "The gallery serves as a vibrant hub for the
regional arts community" is elaborate and generic. Plainness is not the defect.

**Second failure mode.** Applying this to a lead sentence or an abstract, whose
job is to be summary. Test the body.

---

## 4. Attribution

**Procedure.** For every appeal to unnamed authority, resolve it to a named
source, then check that the source supports that specific claim.

Triggers: "studies show", "research suggests", "experts say", "observers have
noted", "it is widely regarded", "industry reports", "critics argue",
"scholars", "several sources", "some have argued".

**Artifact.** The resolved source, with what it actually says, and a statement
of whether it supports the claim. Or the explicit statement that it does not
resolve. There is no third outcome.

**Worked case, resolves and supports, with a scope correction.**

Original claim:

> Studies show that AI detectors are biased against non-native English
> speakers.

Artifact:

> Resolves to Stowe, Afanaseva, Raimundo, Sun and Patil (Pindrop), ACL 2026,
> arXiv 2512.09292: 16 detection models run on student essays labelled for
> gender, race, English-language-learner status and socioeconomic status.
> English-language-learner essays were more likely to be flagged, non-White
> ELL students were disproportionately flagged versus White ELL peers, and
> human annotators showed no significant demographic bias. The source supports
> the claim. The plural "studies" overstates it: this is one peer-reviewed
> paper on student essays.

Finding: LOW, confidence high. Overgeneralization of source count. Repair is to
name the paper and its scope.

**Worked case, resolves and contradicts.**

Original claim:

> Research shows the em dash is a reliable indicator of LLM use in an
> individual document.

Artifact:

> Resolves to Czuma, "Em-ergence of the em-dash", arXiv 2606.29540,
> 2026-06-28, pre-registered as OSF HFT8C on 69,632 medRxiv preprints. The
> paper's own stated conclusion is: "The em-dash is a population-level
> indicator, not a per-paper detector of LLM use." The source is real, it is
> the right source, and it contradicts the claim it is attached to.

Finding: HIGH, confidence high. Misattribution.

**Worked case, does not resolve.**

Original claim:

> Industry reports indicate the market is consolidating rapidly.

Artifact:

> No report is named in the document. A search of the document's own
> bibliography returns nothing on market structure. The claim does not
> resolve.

Finding: HIGH if the claim is load-bearing for the reader, MEDIUM if it is
decorative. Confidence high either way, because non-resolution is decidable.

**The defect that hides here.** Retrieval-augmented systems attach superficial
analysis to a real, named source that does not say anything close to the claim
(Wikipedia's superficial-analyses section, citing Reinhart et al., PNAS 122(8),
2025). Existence of the source is not support. Always open it.

**Counting rule.** Also test the claimed number of sources. One or two sources
described as "several", a single named person rendered as "scholars", or a
short list implied to be non-exhaustive are all attribution defects even when
every cited source is real.

---

## 5. Load-bearing (code)

**Procedure.** Delete the comment, wrapper, handler, abstraction or
assertion-free test. Then determine what broke.

**Artifact.** What broke, named. Or "nothing broke", with the evidence for it.

**Worked case, assertion-free test.**

Original:

```python
def test_user_creation():
    user = create_user("alice")
    assert user is not None
```

Artifact:

> Replaced the body of `create_user` with `return object()`. The test still
> passes. It asserts that the function returns something, not that a user was
> created, that the name was stored, or that the row reached the database.
> Deleting the test loses no coverage.

Finding: HIGH, confidence high. A test that names a behavior and does not test
it is a false statement about the state of the codebase. The mutation is the
artifact: state exactly what you changed and that the test still passed.

**Worked case, handler that is load-bearing.**

Original:

```python
def get_user(user_id):
    try:
        return session.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        return None
```

Artifact:

> Deleted the handler. The single caller is `if get_user(uid) is None:
> abort(404)`. Without the handler, `NoResultFound` propagates and the request
> returns 500 instead of 404. Something broke.

No load-bearing finding. A separate, smaller finding may still apply if the
handler catches bare `Exception` rather than the specific error.

**Worked case, comment.**

Original:

```python
# Increment the counter
counter += 1
```

Artifact:

> Deleted the comment. Lost: nothing. The statement is its own documentation.

Finding: LOW, confidence high, and only worth reporting as part of a cluster.

Contrast:

```python
# The API returns 200 with an empty body when rate limited, so a status check
# alone is not enough here.
if resp.status_code == 200 and resp.json():
```

Artifact:

> Deleted the comment. Lost: the only statement of why the second condition
> exists. The next reader would reasonably simplify the condition and
> reintroduce the bug.

No finding.

**Worked case, wrapper.**

Artifact format:

> Deleted `retry_fetch_user`. Its only caller is `handlers.py:88`, which passed
> its arguments through unchanged to `fetch_user`. Rewired that call site
> directly. Nothing broke and no retry behavior was lost, because the wrapper
> contained no retry logic.

**Failure modes.**

- Flagging defensive code without knowing what it defends against. Run the
  test. Find the callers.
- Flagging an abstraction with one implementation when the user can name the
  planned second one. Ask before flagging.
- "I would have written this differently" is not an artifact.

---

## Reporting rules that apply to all five

- Every finding carries a verbatim quote of the span, the test name, and the
  artifact. Three fields, none optional.
- Severity is impact: HIGH for a fabricated fact, citation or API; MEDIUM for
  padding or filler that changes nothing if cut; LOW for a stylistic tell
  corroborated by a cluster and by at least one structural test.
- Confidence is certainty, on its own axis: high, medium, low.
- Never merge the two axes into one score.
- Markers select spans for testing. A marker is never itself a finding.
- If a test comes back clean, drop the marker hit. Do not downgrade it to LOW
  to keep the finding alive.
