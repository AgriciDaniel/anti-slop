---
type: "meta"
title: "Tag Taxonomy"
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
  - "[[index|Index]]"
  - "[[overview|Overview]]"
  - "[[Evidence Tiers]]"
  - "[[Evidence Quality Ladder]]"
  - "[[The Firewall]]"
  - "[[Provenance Trace Policy]]"
  - "[[Knowledge Base Surface]]"
source_urls: []
---

# Tag Taxonomy

The controlled vocabulary. Three axes, lowercase, hierarchical. Every note
carries exactly one tag from each, and each tag mirrors a frontmatter field so
the two can never drift apart unnoticed.

## Axis 1, domain

One value for the whole brain: `#domain/anti-slop`. It exists so notes stay
identifiable if this vault is ever merged into a larger one.

## Axis 2, type

Mirrors the `type:` frontmatter field.

| Tag | Used for | Counts toward substance scoring |
| --- | --- | --- |
| `#type/concept` | The phenomenon, its causes, and its counterarguments | Yes |
| `#type/marker` | A signal, with its tier and false-positive class | Yes |
| `#type/procedure` | A structural test that emits an artifact | Yes |
| `#type/surface` | An artifact type where slop appears | Yes |
| `#type/meta` | Conventions and operating policy | No |
| `#type/source` | The dated research pack | No |
| `#type/question` | An open or resolved question | No |
| `#type/index`, `#type/overview`, `#type/hot`, `#type/log` | The memory spine | No |

The four scored types are the ones passed to `scripts/score_substance.py`. A
type outside that list is excluded from the density, duplication and citation
floors, which is why meta and spine notes are not held to them.

## Axis 3, confidence

Mirrors the `confidence:` frontmatter field, and a note inherits the weakest
confidence of the sources it depends on.

| Tag | Means |
| --- | --- |
| `#confidence/evidence-based` | Peer reviewed or pre-registered, figures verified |
| `#confidence/practitioner` | Credible first-hand or institutional account |
| `#confidence/contested` | Preprint, vendor study, or a disputed identifier |
| `#confidence/folklore` | Recorded so it can be argued with, never asserted |

Promoting a note above its sources is the most common way a knowledge base
starts asserting things it cannot support. See [[Evidence Quality Ladder]].

## Graph colouring

`.obsidian/graph.json` colour groups key on `#domain/` and `#type/` queries
rather than folder paths, so the graph stays correct if a note moves folder.
