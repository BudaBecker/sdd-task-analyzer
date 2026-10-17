# Bootcamp III Phase 2 submission

## Delivery boundary

The course requires a public repository, `analyze_tasks`, `TaskValidationError`,
the pytest harness, a documented PR, a five-minute YouTube video and a PDF with
links and evidence. GitHub Actions and Docker belong to Phase 3.

Use [the batch specification](../../specs/task_analyzer_spec.md) and
[context rules](../../CONTEXT_RULES.md). The authoritative Phase 1 sources are
`.specs/` and `docs/product/requirements.md`; the required Phase 1 Google Docs
URL is included as a submission link only, without reimporting its contents.
The Phase 2 contract explicitly documents the additional batch
boundary rather than claiming those files already contained this signature.
Priority grouping is a course-only input. Server metrics, priority management,
desktop features, deployment and real databases are outside this change.
The spec maps the brief's `data_criacao` and `data_conclusao` to `Task.created_at`
and `Task.completed_at`, including Scenario 2's `TaskValidationError`. Its
Given/When/Then examples derive from approved REQ/PCE/TLD rules. Python 3.13+
satisfies the brief's Python 3.11+ floor. REQ-023's deadline-window average is
outside the batch interface.

## Reproducible verification

Public repository: <https://github.com/BudaBecker/sdd-task-analyzer>.
Phase 2 branch: `feat/bootcamp-phase-two`.
Documented PR: <https://github.com/BudaBecker/sdd-task-analyzer/pull/4> (open;
human review pending). The repository was renamed to match the brief; the local
checkout directory remains `task-analyzer`.
The default branch is still `main`, which does not contain this delivery until
the user merges PR #4. Complete human review and merge before submission, then
generate the final PDF with the repository root, `tree/main` and PR #4 links.
Keep `feat/bootcamp-phase-two` after the merge.

From the repository root:

```powershell
uv sync --locked
uv run python -m pytest tests/test_harness.py -v
uv run ruff format --check src tests
uv run ruff check src tests
uv run python -m mypy --strict
uv run python -m pytest
uv pip check
uv build
```

The full suite includes an installed-wheel batch-analysis check in a fresh
temporary environment outside the checkout. No test uses a real database.
Local verification passed on 2026-10-16: **523 tests** (35 harness cases,
487 existing server cases and one new installed-wheel analysis smoke test),
Ruff formatting/lint, strict mypy, dependency compatibility and both build formats.
Two third-party deprecation warnings remain.
The README's "Without uv" route was also verified in a fresh disposable venv:
hashed requirements, separate editable project install and 35 passing harness cases.
See [verification.txt](verification.txt) for recorded results. Capture the actual
terminal during the harness run; text transcripts are not terminal screenshots.

## AI prompts and critical review

The implementation followed this session's instructions, summarized here rather
than presented as a verbatim conversation transcript:

1. Compare the intermediate challenge PDF with the repository's current state.
2. Execute the Phase 2 work, making the necessary commits and pushes.
3. Use `.specs/` as the Phase 1 specification source, as clarified by the user.

AI drafted the batch specification and `CONTEXT_RULES.md` in the same initial
session, from the brief and `.specs/`. They were committed in `9bae22c` before
the code in `1c9daa1`; the initial user prompts did not separately supply those
new files as context. Their creation order alone does not prove that they
prevented hallucinations.

An independent review checked the code against those documents and found an
avoidable rate-precision loss ("preserve full precision"), an invalid zone
escaping as `PermissionError` ("specific exceptions"), and a harness that did
not reject a duration implementation using `.seconds`, which discards days.

The correction session explicitly read `CONTEXT_RULES.md` and the batch
specification before editing code. It changed the rate to `late * 100 / eligible`,
made the REQ-024 rate assertion exact, translated zone-construction `OSError`
and non-iterable inputs into `TaskValidationError`, and added multi-day and
sub-second duration cases. Only obtaining the iterator is wrapped; consumption
errors continue to propagate. Mutation checks in disposable copies confirmed
that discarding days, rounding means and truncating seconds are now detected.

This independent review does not count as the user's human review of the PR.
Human review remains pending. Tests support executed cases; they do not prove
all AI output is correct or that hallucinations are impossible.

## Five-minute recording outline

Record horizontally with audio and a visible camera. Use YouTube Unlisted or
Public visibility; do not publish a Short.

| Time | Show and explain |
| --- | --- |
| 00:00-00:40 | Introduce Task Analyzer, Phase 2 and the repository URL. |
| 00:40-01:25 | Show the GitHub tree, context rules, `.specs/` sources and batch contract. Explain the course-only priority boundary. |
| 01:25-02:20 | Open `src/task_analyzer.py`; show typed input, the custom exception, UTC duration, cutoff reuse and guarded denominators. |
| 02:20-03:30 | Run the harness in the terminal. Show both named scenarios and the passing summary; explain counts, group means and the cutoff equality case. |
| 03:30-04:20 | Show branches, commits and PR #4. The user records their own review/comment and merges into `main`, preferably during recording, retaining the branch. Verify the required tree on `main`. |
| 04:20-05:00 | Explain human validation against context rules, remaining limitations and links in the submission PDF. |

## Submission completion checklist

- [x] Verify the public repository and Phase 2 PR links above.
- [ ] Review the new batch contract and code against the academic expectations.
- [ ] The user records a human review or their own comment in PR #4 on GitHub.
- [ ] The user merges PR #4 into `main`, retaining `feat/bootcamp-phase-two`.
- [ ] Verify `main` contains `README.md`, `CONTEXT_RULES.md`, `.gitignore`,
  `requirements.txt`, `specs/`, `tests/test_harness.py` and `src/task_analyzer.py`.
- [ ] Capture the actual terminal with a 100%-passing harness summary.
- [ ] Include screenshots of the `main` tree and PR #4; retain their provenance.
- [ ] Record/upload the required video and insert its verified YouTube URL.
- [ ] Include the required Phase 1 Google Docs URL (rubric, page 6); not supplied.
- [ ] Add student/course identification if required by the platform.
- [ ] After merge, generate the final PDF with the repository root, `tree/main`,
  PR #4 and required Docs/video links; review it and submit to salaonline.

## Open questions

The [PDF draft](../../output/pdf/phase-two-report-draft.pdf) is a preparation
artifact, not a completed submission. The user must supply the required Docs and
video URLs, real screenshots, human review, merge and academic identification,
then submit the final PDF to salaonline. Windows trailing-space zone acceptance
remains a known shared limitation; server zone validation is a separate fix.
