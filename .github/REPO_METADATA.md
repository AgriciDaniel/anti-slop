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

Not set. GitHub will fall back to a generated card. If you add one, 1280x640
PNG under Settings, Social preview.
