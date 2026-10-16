# Phase 2 batch task analysis

## Scope and sources

Implement the Bootcamp III intermediate challenge as a read-only Python batch
function, `analyze_tasks`, and `TaskValidationError` in `src/task_analyzer.py`.
The user authorized implementation, local commits and pushes on 2026-10-16 and
identified `.specs/` and `docs/product/requirements.md` as the authoritative
Phase 1 sources. The Phase 1 Google Docs URL is a required submission link only;
its contents are not reimported or reconciled. Preserve the existing
[1A](../.specs/features/persistent-task-creation-editing/spec.md) and
[1B](../.specs/features/task-lifecycle-deletion/spec.md) contracts and identifiers.

Those specifications describe persistence and lifecycle, not the batch signature
or the challenge's numbered scenarios. This document makes that missing boundary
explicit using the approved [product time and metric rules](../docs/product/requirements.md).
The scenarios below are the Phase 2 acceptance examples; they are not presented
as a verbatim copy of an unavailable earlier academic submission.

The course requires priority-grouped averages and numeric `0.0` for empty
averages. These apply only to this batch interface. The server retains its
existing task model, fixed configured zone and API; its metrics endpoint and
desktop dashboard are not implemented by this delivery. In particular, an
explicit input priority is not automatic product prioritization, and numeric
batch results do not change the dashboard's N/A presentation rule.
The deadline-window percentage average from REQ-023 is outside this batch
interface. Python 3.13+ (AD-003) satisfies the brief's Python 3.11+ minimum.

### Brief terminology

| Brief | Batch contract |
| --- | --- |
| `data_criacao` | `Task.created_at` |
| `data_conclusao` | `Task.completed_at` (`None` means pending) |
| `data_conclusao < data_criacao` | Scenario 2 raises `TaskValidationError`. |
| "por prioridade" | `Task.priority: bool`; `priority`/`non_priority` groups in `tempo_medio_conclusao_horas_por_prioridade`. |
| Acceptance scenarios in Dado-Quando-Então | Scenarios 1 and 2 use Given/When/Then. |

## Input and output contract

`analyze_tasks(tasks: Iterable[Task], *, product_time_zone: str) -> TaskAnalysis`
accepts typed, immutable `Task` records:

| Field | Type and meaning |
| --- | --- |
| `created_at` | Required aware `datetime`: original creation instant. |
| `completed_at` | Aware `datetime` or `None` (default): latest completion; absence means pending. |
| `deadline` | Calendar `date` or `None` (default); inclusive range `0001-01-01` through `9999-12-30`. A datetime is not a calendar date input. |
| `priority` | Strict `bool`, default `False`; externally supplied grouping flag. |
| `deleted` | Strict `bool`, default `False`; excluded from every metric. |

The caller passes the collection's retained IANA zone explicitly. There is no
host-zone default, clock lookup, database lookup, string/date coercion or input
mutation. Task identity, titles and observations are irrelevant to this input.
All records, including deleted records, are validated. Invalid record types,
timestamps, calendar deadlines, flags or zones raise `TaskValidationError`.
Completion before creation is rejected; equal timestamps are valid.
A non-iterable collection, such as `None` or `5`, raises `TaskValidationError`.
Only failure to obtain an iterator is translated; errors raised while consuming
the caller's iterable propagate unchanged. `OSError` while constructing the
product zone is translated to `TaskValidationError`, including directory keys
that raise `PermissionError` on Windows.

The result is a dictionary with these exact keys (Portuguese names are the
external identifiers required by the challenge; code and documentation are English):

| Key | Value |
| --- | --- |
| `total_tarefas` | Non-deleted pending plus completed count. |
| `total_concluidas` | Non-deleted tasks with a completion instant. |
| `total_pendentes` | Non-deleted tasks without a completion instant. |
| `tempo_medio_conclusao_horas` | Mean elapsed UTC hours across completed tasks; `0.0` when empty. |
| `tempo_medio_conclusao_horas_por_prioridade` | Dictionary with `priority` and `non_priority` means, each `0.0` when its completed group is empty. |
| `taxa_atraso_percentual` | Late completed tasks with deadlines / all completed tasks with deadlines * 100; `0.0` when empty. |

Use the existing deadline resolver: midnight after the deadline in the product
zone, first occurrence when ambiguous and first valid instant when nonexistent
(including the skipped Apia date). Completion exactly at the cutoff is late.
Pending tasks and completed tasks without deadlines never enter the overdue-rate
denominator. Preserve full precision; display rounding belongs to presentation.
Compute elapsed duration on the UTC timeline, including across DST changes.

## Acceptance scenarios

### Scenario 1: successful analysis

Given `America/Sao_Paulo` and these five non-deleted tasks:

| Task | Created (UTC) | Completed (UTC) | Deadline | Priority |
| --- | --- | --- | --- | --- |
| A | 2026-09-14 08:00 | 2026-09-14 10:00 | 2026-09-14 | false |
| B | 2026-09-14 23:00 | 2026-09-15 03:00 | 2026-09-14 | true |
| C | 2026-09-14 08:00 | 2026-09-14 11:00 | absent | false |
| D | 2026-09-14 08:00 | absent | 2026-09-10 | true |
| E | 2026-09-14 08:00 | absent | absent | false |

When analyzed, then counts are total **5**, completed **3**, pending **2**;
mean completion is **3.0 hours**, priority **4.0**, non-priority **2.5**;
overdue rate is **50.0%** (B is late at the cutoff; C and D are ineligible).
Adding a deleted task changes none of these results. This retains REQ-021's
2-pending/3-completed example and REQ-024's eligibility/cutoff rules.

### Scenario 2: invalid completion chronology

Given a task created at `2026-09-14T10:00:00Z` and completed one second earlier,
when analyzed, then raise `TaskValidationError` identifying the record index and
completion field, with no partial result or input mutation.

### Boundaries and regressions

- Empty input and pending-only input return zero counts as applicable and `0.0`
  for every average/rate, including empty priority groups.
- Preserve REQ-022's 2-hour/4-hour -> 3-hour mean and REQ-024's one late among
  three eligible completed tasks -> unrounded `100 / 3` percent.
- A zero-duration completion is valid. Pending overdue tasks do not alter the rate.
- Reopening is represented by absent completion; recompletion uses original
  creation and latest completion, as required by REQ-025 and TLD-16/TLD-23.
- Preserve PCE-49/PCE-50's ambiguous/nonexistent midnight and skipped-date rules.
- Reject naive instants, invalid zones, malformed records and invalid date bounds.
- Preserve multi-day and sub-second duration precision without rounding means.

## Steps and verification

- [x] Implement the module and package it alongside the existing server.
- [x] Translate both scenarios and meaningful boundaries into `tests/test_harness.py`.
- [x] Run the harness, the server regression suite, README checks and an
  installed-wheel analysis smoke test outside the checkout.
- [x] Publish commits and a documented PR; prepare verification notes and a video script.

## Open questions

- Windows may accept a zone key with trailing spaces; this known limitation is
  shared with the server. The server's zone-validation follow-up is separate.
- Before final submission, the user reviews PR #4 in GitHub and merges it into
  `main`, retaining the feature branch. Generate the final PDF after the merge,
  using `main` links and the required Phase 1 Google Docs URL.
- The user must record the required five-minute video with visible camera/audio
  and provide its YouTube URL before final submission.
