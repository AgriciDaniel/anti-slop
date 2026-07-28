---
type: "surface"
title: "Dependency Surface"
domain: "detection and repair of AI slop in prose, code, documentation, and agent output, grounded in corpus evidence rather than authorship detection"
status: "active"
created: "2026-07-27"
updated: "2026-07-27"
tags:
  - "#domain/anti-slop"
  - "#type/surface"
  - "#confidence/practitioner"
confidence: "practitioner"
related:
  - "[[Package Hallucination Evidence|Package Hallucination and Slopsquatting]]"
  - "[[Code Surface]]"
  - "[[The Load Bearing Test|The Load-Bearing Test]]"
  - "[[The Firewall]]"
  - "[[Evidence Tiers]]"
  - "[[The Firewall|Severity and Confidence]]"
  - "[[Marker Cohort Rot]]"
  - "[[The Generation Verification Asymmetry|Generation-Verification Asymmetry]]"
  - "[[Commit and Review Surface]]"
source_urls:
  - "https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf"
  - "https://arxiv.org/abs/2605.17062"
  - "https://arxiv.org/abs/2606.28438"
---

# Dependency Surface

This surface is a security gate, not a style review. Everything else in this
vault routes markers to structural tests and refuses to hard-fail. Here the
check is decidable, the scan costs milliseconds, and the failure is remote code
execution on a developer machine, so the gate is allowed to hard-fail and does.

## Gate definition

`scan_packages.py` blocks a change when any import, requirement line, lockfile
entry, or install command in the diff names a package that does not resolve in
its registry. There is no severity ladder and no confidence axis on this gate.
A name resolves or it does not. This is the one place in the brain where
[[The Firewall|Severity and Confidence]] collapses to a single boolean, and the reason is
that the check consults an authority rather than a judgement.

The gate covers, at minimum: PyPI, npm, crates.io, RubyGems, Packagist,
Maven Central, Go module proxy, and NuGet. It also covers install instructions
inside prose and README blocks, because a fabricated `pip install` line in
documentation is executed by a human just as readily as one in a script.

## Threat model

Slopsquatting is the attack in which a third party registers a package name that
language models are known to hallucinate, then waits for a developer or an agent
to install it. It is a supply-chain attack whose targeting information is
produced for free by the models themselves, and it differs from classic
typosquatting in one important way: the attacker does not need to guess what a
human will mistype, because the model publishes the guess repeatedly and
identically.

Repetition is what makes it economic. `spracklen-package-hallucination`, published
at USENIX Security 2025, found that 43 percent of hallucinations recurred across
all ten reruns of the same prompt and 58 percent recurred more than once. A name
that only ever appears once is not worth registering. A name that appears in
four out of ten reruns is a reliable channel.

## Rate history

| Cohort | Hallucination rate | Scale | Source |
| --- | --- | --- | --- |
| 2024 models, all | 19.7 percent of recommended packages did not exist | 16 models, 576,000 samples | `spracklen-package-hallucination` |
| 2024 commercial | 5.2 percent | same study | `spracklen-package-hallucination` |
| 2024 open-source | 21.7 percent | same study | `spracklen-package-hallucination` |
| 2026 frontier | 4.62 percent to 6.10 percent | corroborated across 199,845 responses | `churilov-package-hallucination-2026` |
| Claude Haiku 4.5 | 4.62 percent | same study | `churilov-package-hallucination-2026` |
| GPT-5.4-mini | 6.10 percent | same study | `churilov-package-hallucination-2026` |

Two numbers carry the whole argument. The 2024 study observed **205,474 unique
hallucinated package names**, which is the size of the attack surface. The 2026
study found **53 hallucinated package names still registerable at time of
measurement**, which is the size of the surface that survived two years of
improvement. The rate compressed by roughly an order of magnitude and the spread
between model families collapsed, which is real progress. The registerable
count did not reach zero, which is the only number the gate cares about.

The 2026 figure is a preprint verified at abstract level, so it is tier
CONTESTED under [[Evidence Tiers]] and its confidence is capped at medium. The
2024 figure is peer-reviewed at a top-tier security venue and is tier
EVIDENCE-BASED. Do not quote the 19.7 percent figure as current; quote it as the
2024 cohort measurement it is, and pair it with the 2026 range. This pairing is
the standing rule under [[Marker Cohort Rot]].

## Verification procedure

1. **Extract every dependency name from the diff.** Parse import statements,
   requirement and manifest files, lockfiles, Dockerfile install lines, CI
   workflow install steps, and fenced install commands in Markdown.
2. **Resolve each name against its registry index.** Registry index lookup, not
   a web search and not a model recall. A model asserting that a package exists
   is the failure mode this gate was built to catch.
3. **Fail the build on any unresolved name.** Emit the name, the file, the line,
   and the registry consulted. Do not attempt a correction automatically.
4. **For every name that does resolve, check three secondary signals.** First
   publication date newer than the code that imports it. Total downloads
   implausibly low for a package the change treats as a standard tool.
   Maintainer account created within days of first publication. Any one of these
   escalates to human review rather than blocking.
5. **Diff the resolved set against the project's existing lockfile.** A new
   transitive dependency introduced by an agent-authored change is reviewed as a
   dependency decision, not as a formatting change.
6. **Record the result as an artifact.** The scan output is attached to the
   review, so a later reader can see which registry was consulted and when.
7. **Re-run after every repair.** A fix that changes an import must re-enter at
   step 1. Model self-review does not substitute for the re-run; see
   `song-rubber-stamp-regime` and [[The Firewall]].

## Marker routing and false positives on this surface

| Signal | Tier | Action | False-positive class specific to dependencies |
| --- | --- | --- | --- |
| Unresolvable package name | Layer 0 | hard fail | private or internal registry not configured in the scanner |
| Package resolves but is days old | Layer 1 | human review | genuinely new library that the author chose deliberately |
| Plausible-sounding name near a real one | Layer 1 | [[The Load Bearing Test|The Load-Bearing Test]] on the import | legitimate forks and scoped rewrites, such as a `-ng` or `2` suffix |
| Import present but unused | Layer 1 | delete and rebuild | re-export modules and plugin registration side effects |
| Version pin that does not exist | Layer 0 | hard fail | yanked release that the lockfile still references |
| Install command inside prose | Layer 0 | hard fail | documentation deliberately showing a wrong command as a counterexample |

The private-registry row is the one that will actually bite. A scanner
configured only against public indexes will fail every internal package in a
monorepo, and a team that learns to ignore the gate has lost the gate. Configure
the internal index before enabling the check, and treat a wave of failures on
internal names as a scanner misconfiguration rather than as findings.

## Why the gate stays as rates fall

The asymmetry is the argument. A registry lookup costs milliseconds and can be
cached. A successful slopsquat costs whatever the attacker's payload does with
developer credentials, and the blast radius includes anything the build machine
can reach. A control whose cost is bounded and whose avoided loss is unbounded
does not get removed because the incidence dropped, any more than seatbelts get
removed because crash rates fell.

There is a second reason that is specific to this brain. The dependency gate is
the clearest worked example of the principle in [[The Generation Verification Asymmetry|Generation-Verification Asymmetry]]:
generating a plausible package name is free, and verifying it is nearly free
too, which is exactly the shape of problem where a deterministic check beats
every form of judgement. Most of this vault deals with the opposite shape, where
verification is expensive and the model's confidence is worth nothing. This note
is the easy case, and the easy case should be automated first.

## Related

- [[Code Surface]]
- [[Documentation Surface]]
- [[Agent Output Surface]]
- [[Package Hallucination Evidence|Package Hallucination and Slopsquatting]]
- [[The Attribution Test|Fabricated Citations]]
- [[Provenance Trace Policy]]
- [[Note Conventions]]
- [[index|Index]]
