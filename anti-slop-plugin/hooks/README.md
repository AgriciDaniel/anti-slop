# hooks/hooks.json

This directory holds the plugin-level hooks file. Claude Code accepts only two
top-level keys in a plugin `hooks.json`: `description` and `hooks`. Any other
key is reported at startup as `hooks.json: unknown key "..." ignored`, so the
explanatory notes that used to live under a `comment` key are kept here
instead.

## What this is

Claude Code reads `hooks.json` from the plugin root, so installing or removing
the plugin installs or removes this hook. It never writes to
`~/.claude/settings.json` and never edits any global or project settings file.
Removing the plugin removes the behaviour completely.

Note the limit of that statement: it describes where the hook is registered,
not where it runs. Nothing gates it on a skill, so it fires in every session
where the plugin is enabled. See `SECURITY.md` at the repository root.

## Scope

The linter runs only when both conditions hold:

- The written file is prose: `.md`, `.markdown`, `.mdx`, `.txt` or `.rst`.
  Code and config are skipped, because a spaced double hyphen is correct in a
  shell command or a test fixture. CI still gates long dashes in `.py`,
  `.json` and `.yml`.
- The written file resolves, after symlinks, to a path inside the project the
  session was started in (`CLAUDE_PROJECT_DIR`, falling back to the hook
  input's `cwd`). A session started in this repository that edits a file in
  another directory does not restyle that file.

Every other write exits 0 without running the linter.

## Exit codes

Exit code 2 is the only blocking code. On 2, the hook's stderr is fed back to
the model as the reason and the model gets a chance to correct itself.

Exit code 1 does nothing useful here: it is treated as a non-blocking error,
the output goes to the transcript rather than back to the model, and execution
continues, so a linter failure surfaced as 1 is silently ignored.

Exit code 0 is success and the stdout is not shown to the model.

The wrapper therefore translates `lint_voice.py`'s own exit 1 (findings) into
exit 2, and writes the findings to stderr. `lint_voice.py`'s exit 2 (usage
error) also becomes 2, which is correct: a misconfigured gate should be loud,
not silent.

## What it does not do

`lint_voice.py` enforces house style: no U+2014, no U+2013, no spaced double
hyphen, plus banned tokens from a voice file. A hit is a style violation and
nothing else. It is not a slop verdict, not a quality score, and never evidence
about who or what wrote the text. See `references/false-positives.md` and
`references/markers-tier2.md`.

This hook deliberately does not run `scan_residue.py` or
`scan_placeholders.py`: those are Layer 0 scanners whose findings belong in a
review report, and the `slop-rewrite` skill carries its own scoped hook for
them.

## Failure behaviour

Exit 2 arrives after the write has happened. `PostToolUse` cannot undo a
write; it reports the violation so the model corrects the file.

Silent no-op when the written file is out of scope (see Scope), when the
linter script is absent (the sibling brain repo is not
checked out), when the tool input carried no `file_path`, or when the written
path no longer exists. A missing gate must not block unrelated work, and a
blocked write on a missing dependency would be impossible for the model to
fix.

## Environment

`${CLAUDE_PLUGIN_ROOT}` is exported to hook commands as `CLAUDE_PLUGIN_ROOT`
and resolves to this plugin's root directory. The linter lives in the sibling
brain repo, one level up, so the path is
`$CLAUDE_PLUGIN_ROOT/../anti-slop-brain/scripts/lint_voice.py`.
