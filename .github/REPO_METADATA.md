# GitHub repository metadata

Not applied automatically. Run these after creating the repository, or set the
same values in Settings.

## Description

Copy verbatim into the About field, 254 char limit:

> Find and repair substance defects in AI-assisted prose, code, docs, and agent output. Reports defects, never authorship. Structural tests over model judgement, because LLM judges agree with human slop labels at chance.

## Topics

GitHub allows up to 20. These are ordered by discoverability value.

```
ai-slop
writing-quality
claude-code
agent-skills
code-quality
citation-verification
research-integrity
static-analysis
obsidian
knowledge-base
technical-writing
editorial-tools
llm
prompt-engineering
developer-tools
```

## Commands

```bash
gh repo edit --description "Find and repair substance defects in AI-assisted prose, code, docs, and agent output. Reports defects, never authorship. Structural tests over model judgement, because LLM judges agree with human slop labels at chance."

gh repo edit --add-topic ai-slop,writing-quality,claude-code,agent-skills,code-quality
gh repo edit --add-topic citation-verification,research-integrity,static-analysis,obsidian,knowledge-base
gh repo edit --add-topic technical-writing,editorial-tools,llm,prompt-engineering,developer-tools

gh repo edit --homepage "https://github.com/AgriciDaniel/anti-slop#readme"
gh repo edit --enable-issues --enable-discussions --enable-wiki=false --enable-projects=false
```

## Applied state, verified 2026-07-29

These are set on the live repository. Verified through the API, not assumed.

| Setting | State |
|---|---|
| Visibility | public |
| Default branch | `main` |
| Topics | 15 |
| Description | set |
| Secret scanning | enabled |
| Secret scanning push protection | enabled |
| Dependabot alerts and security updates | enabled |
| Discussions | enabled |
| Wiki, Projects | disabled |
| Delete branch on merge | enabled |
| Auto-merge | enabled |
| Branch protection on `main` | requires all three CI checks; force pushes and deletions blocked |

Two things the API cannot set:

- **Social preview.** Neither the REST API nor `gh repo edit` exposes it. Upload
  `.github/social-preview.png` at Settings, Social preview. The image is already
  the README header, so the repository page is unaffected either way.
- **Extended secret scanning patterns.** `secret_scanning_non_provider_patterns`
  and `secret_scanning_validity_checks` returned disabled after an enable call.
  Toggle them under Settings, Code security if you want them.

The homepage currently points at a Skool community rather than the README. That
is a deliberate-looking marketing choice rather than a defect, so it was left
alone; change it under Settings if it was not intended.

## Settings worth enabling

| Setting | Value | Why |
|---|---|---|
| Default branch | `main` | CI triggers on `main`; a `master` default means CI never runs on push |
| Branch protection on `main` | require CI to pass | the whole point of the gates |
| Vulnerability alerts | on | free, and dependabot is already configured |
| Private vulnerability reporting | on | `SECURITY.md` and the issue template both link to it |
| Discussions | on | `SUPPORT.md` points there first |
| Wiki | off | the knowledge base is in the repo, a second wiki would fragment it |
| Projects | off | not used |
| Squash merge only | on | keeps history readable |
| Auto-delete head branches | on | housekeeping |

## Release

Tag after the first CI run goes green on `main`.

```bash
git tag -a v0.1.0 -m "First public release"
git push origin v0.1.0
gh release create v0.1.0 --title "v0.1.0" --notes-file <(sed -n '/## \[0.1.0\]/,/^\[Unreleased\]/p' CHANGELOG.md)
```

## Social preview

`.github/social-preview.png` is committed and is the same image the README uses
as its hero. It is not applied automatically: upload it under Settings, Social
preview, which is the only way GitHub accepts one. Until that upload happens
GitHub falls back to a generated card.
