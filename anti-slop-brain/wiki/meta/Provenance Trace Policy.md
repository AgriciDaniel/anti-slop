---
type: "meta"
title: "Provenance Trace Policy"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-28"
updated: "2026-07-28"
tags:
  - "#domain/anti-slop"
  - "#type/meta"
  - "#confidence/evidence-based"
confidence: "evidence-based"
related:
  - "[[Note Conventions]]"
  - "[[Tag Taxonomy]]"
  - "[[The Attribution Test]]"
  - "[[Evidence Quality Ladder]]"
  - "[[Superseded Figures]]"
  - "[[research-pack-2026-07-27|Research Pack 2026-07-27]]"
  - "[[What This Brain Does Not Claim]]"
  - "[[index|Index]]"
source_urls: []
---

# Provenance Trace Policy

Every claim in a deliverable must be traceable backwards to a dated source
without leaving this repository. The chain is: source, claim, note, decision,
deliverable. A break anywhere invalidates everything downstream of it.

## The chain

| Link | Lives in | Carries |
| --- | --- | --- |
| Source | `references/source-ledger.json` | URL, retrieved, refresh_due, tier, limitations |
| Claim | the ledger `claims` array | one sentence, quotable |
| Note | `wiki/**` | the id in body text, the URL in `source_urls` |
| Decision | `wiki/questions/` or the log | what was concluded and on what basis |
| Deliverable | adapter output | the finding, its artifact, and its evidence span |

## Rules

1. A numeric claim in a note cites a ledger id in the body text and carries the
   matching URL in `source_urls`. Neither alone is sufficient.
2. A note never asserts more confidence than its weakest cited source.
3. A figure that cannot be traced to a ledger id does not appear in a
   deliverable. It may appear in prose, explicitly marked as unquotable, which
   is what happened to the MSR 2026 figures while their identifier was wrong.
4. A superseded figure is recorded with its correction attached, never
   overwritten. See [[Superseded Figures]].
5. A source that could not be read is recorded as unread rather than omitted.
   An unreadable source is a known unknown; a missing one is invisible.

## What this policy does not guarantee

It guarantees that a claim traces to a source. It does **not** guarantee that
the source says what the claim says. Those are different properties, and
conflating them is exactly the failure [[The Attribution Test]] describes at
rung two.

That distinction is not theoretical here. On 2026-07-28 an adversarial pass
found five ledger entries whose titles matched no real paper, in a vault that
had asserted the opposite. The identifiers traced correctly; the titles were
invented. Provenance held and verification had not been done.

The honest statement of coverage is in [[What This Brain Does Not Claim]].

## Operating contract

This policy is an operating contract, not advice. A deliverable that violates
it is defective regardless of how well it reads.

1. Advisory and read-only. This brain proposes corrections; it does not apply
   them to a user's source material without approval.
2. Every claim traces to a ledger id, or it does not ship.
3. Every note carries a confidence tag drawn from the four-value vocabulary in
   [[Tag Taxonomy]], and that confidence tag may never exceed the weakest
   source the note depends on.
4. A correction is appended with its date and its cause. Silent overwriting
   breaks the trace and is prohibited.
5. No credentials, tokens, private user content, or local absolute paths enter
   any artifact.

## Verification cadence

| Check | When |
| --- | --- |
| Identifier resolves | On ingest, and at every refresh |
| Title matches the real paper | On ingest, and at every refresh |
| Quoted figure appears in the source | Spot-checked, not exhaustive |
| Full paper read | Rare, and stated when it has happened |
