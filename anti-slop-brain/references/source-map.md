# Source Map

## Raw Sources

- Drafts, diffs, commit messages, pull request descriptions, agent transcripts, and documents supplied by the operator

## Enrichment Sources

- Peer-reviewed corpus studies of LLM stylistic markers and detector reliability
- Wikipedia WikiProject AI Cleanup and the Signs of AI writing guide
- Official regulatory texts on AI content transparency and provenance standards
- Primary repository sources for prior-art skills and linters

## Import Strategy

- Copy raw source files into `.raw/sources/`.
- Record path, hash, retrieval date, owner, and source type.
- Record external research sources in `references/source-ledger.json`.
- Record implemented schemas and adapters in `references/adapter-manifest.json`.
- Create a source note under `wiki/sources/`.
- Link affected entities, workflows, and deliverables.
