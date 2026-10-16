# Bootcamp III Phase 2 submission

## Delivery boundary

The course requires a public repository, `analyze_tasks`, `TaskValidationError`,
the pytest harness, a documented PR, a five-minute YouTube video and a PDF with
links and evidence. GitHub Actions and Docker belong to Phase 3.

Use [the batch specification](../../specs/task_analyzer_spec.md) and
[context rules](../../CONTEXT_RULES.md). The user identified `.specs/` as the
Phase 1 source; the Phase 2 contract explicitly documents the additional batch
boundary rather than claiming those files already contained this signature.
Priority grouping is a course-only input. Server metrics, priority management,
desktop features, deployment and real databases are outside this change.

## Reproducible verification

Public repository: <https://github.com/BudaBecker/sdd-task-analyzer>.
Phase 2 branch: `feat/bootcamp-phase-two`.
Documented PR: <https://github.com/BudaBecker/sdd-task-analyzer/pull/4> (open;
human review pending). The repository was renamed to match the brief; the local
checkout directory remains `task-analyzer`.

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
Local verification passed on 2026-10-16: **518 tests** (30 harness cases,
487 existing server cases and one new installed-wheel analysis smoke test),
Ruff formatting/lint, strict mypy, dependency compatibility and both build formats.
Two third-party deprecation warnings remain.
See [verification.txt](verification.txt) for recorded results. Capture the actual
terminal during the harness run; text transcripts are not terminal screenshots.

## AI prompts and critical review

The implementation followed this session's instructions, summarized here rather
than presented as a verbatim conversation transcript:

1. Compare the intermediate challenge PDF with the repository's current state.
2. Execute the Phase 2 work, making the necessary commits and pushes.
3. Use `.specs/` as the Phase 1 specification source, as clarified by the user.

The context rules constrained the work to typed Python, uv, the approved
chronology/deadline semantics and disposable test data. The contract makes the
course's additional priority input and empty-result semantics explicit, avoiding
an unapproved priority field in the server database. The implementation reuses
the existing cutoff resolver and tests UTC elapsed time across DST transitions.
The tests preserve the approved 2-hour/4-hour mean and overdue eligibility rules.

During verification, the first lint run found an overlong harness docstring;
it was shortened and checks rerun. Packaging was extended and checked from an
installed wheel so passing source-tree imports could not hide a missing module.
These are concrete checks and corrections, not proof that hallucinations cannot
occur. Human review of the code and this reconciliation remains necessary.

## Five-minute recording outline

Record horizontally with audio and a visible camera. Use YouTube Unlisted or
Public visibility; do not publish a Short.

| Time | Show and explain |
| --- | --- |
| 00:00-00:40 | Introduce Task Analyzer, Phase 2 and the repository URL. |
| 00:40-01:25 | Show the GitHub tree, context rules, `.specs/` sources and batch contract. Explain the course-only priority boundary. |
| 01:25-02:20 | Open `src/task_analyzer.py`; show typed input, the custom exception, UTC duration, cutoff reuse and guarded denominators. |
| 02:20-03:30 | Run the harness in the terminal. Show both named scenarios and the passing summary; explain counts, group means and the cutoff equality case. |
| 03:30-04:20 | Show branches, atomic commits and the Phase 2 PR's changes and verification. Do not claim an unperformed human review. |
| 04:20-05:00 | Explain human validation against context rules, remaining limitations and links in the submission PDF. |

## Submission completion checklist

- [x] Verify the public repository and Phase 2 PR links above.
- [ ] Review the new batch contract and code against the academic expectations.
- [ ] Capture the actual terminal with a 100%-passing harness summary.
- [ ] Include GitHub tree and PR screenshots; retain their actual provenance.
- [ ] Record/upload the required video and insert its verified YouTube URL.
- [ ] Include the Phase 1 Google Docs URL if the course rubric requires it.
- [ ] Add student/course identification if required by the platform.
- [ ] Rebuild/review the submission PDF and submit it to salaonline.

## Open questions

The [PDF draft](../../output/pdf/phase-two-report-draft.pdf) is a preparation
artifact, not a completed submission: screenshots, the video URL, human review
and salaonline submission remain pending. The rubric also mentions a Google Docs
link; the user identified local `.specs/` as the source, so confirm whether its
published GitHub link is accepted or a separate Docs URL is required.
