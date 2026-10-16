# STATE

## Decisions

Approved product inputs remain in [Requirements](../docs/product/requirements.md) and [Scope](../docs/product/scope.md). [AGENTS.md](../AGENTS.md) owns working rules, authorization, and unresolved technical choices. Consult those sources before recording new project-level decisions; do not reproduce product definitions here.

### AD-001

- **Decision**: Use one FastAPI application with SQLite on local storage of the dedicated Ubuntu Server 26.04.1 LTS host, retaining Python 3.11+ and private Tailscale access.
- **Reason**: The user selected this architecture for the personal collection after comparing it with a separately operated PostgreSQL service.
- **Trade-off**: Accept serialized SQLite writes and local-storage coupling to avoid operating a separate database service. Database contention must be handled without weakening uniqueness, persistence, or safe operation repetition.
- **Scope**: Server features and their shared persistence/operation contracts; details are proposed in the [1A Design](features/persistent-task-creation-editing/design.md).
- **Date**: 2026-09-13.
- **Status**: active; the Python baseline named here is superseded by [AD-003](#ad-003).

### AD-002

- **Decision**: Adopt the shared server contracts of the approved 1A Design: versioned HTTP JSON request/response over `/v1`, client-supplied operation identity with an immutable result ledger written in the same SQLite transaction as its mutation, aware-UTC instants with integer microsecond storage and a persisted IANA product-zone key, explicit `BEGIN IMMEDIATE` transactions with verified PRAGMAs, native virtual environment plus systemd plus Tailscale Serve for private access, JSON-line structured logging, and pytest, HTTPX, Ruff, mypy, build, and pip-tools as the server quality stack.
- **Reason**: The user approved the detailed 1A Design on 2026-09-13. These contracts are reused by delivery 1B, deadline emphasis, productivity analysis, and the desktop client, so they belong in the project decision log rather than one feature document.
- **Trade-off**: Request/response with an operation ledger keeps the desktop responsible for repetition and refresh, and indefinite result retention trades storage for the guarantee that a late repeated attempt never becomes a new operation.
- **Scope**: Server features and their shared persistence, operation, time, logging, and quality contracts. Exact dependency versions, deployment values, and client technology remain outside this entry.
- **Date**: 2026-09-13.
- **Status**: active; dependency locking with pip-tools is superseded by AD-004.

### AD-003

- **Decision**: Require Python 3.13 or later for the Task Analyzer Server, replacing the earlier 3.11 minimum.
- **Reason**: The user raised the baseline on 2026-09-13 while approving the task plan, so the server targets a current interpreter instead of the oldest one that satisfies the original requirement.
- **Trade-off**: A newer minimum narrows the set of acceptable host interpreters and must match what the selected Ubuntu Server 26.04.1 LTS target actually provides; the dependency task verifies that interpreter before locking versions.
- **Scope**: Server runtime, packaging metadata, dependency resolution, and the REQ-003/PCE-44 criteria. It supersedes only the Python baseline of [AD-001](#ad-001); every other part of that decision stays active.
- **Date**: 2026-09-13.
- **Status**: active.

### AD-004

- **Decision**: Use lightweight SDD inspired by TLC and uv-managed dependencies/environments. Remove mandatory TLC automation, test-count quotas and blanket verbose docstrings.
- **Reason**: The user approved simplification after the first delivery exposed disproportionate content and context-loading cost for a personal learning/portfolio project.
- **Trade-off**: Keep behavior-based specifications, tests and review, while replacing generated process artifacts with concise guidance and Git history. The bundled TLC remains optional study material.
- **Scope**: Repository workflow and dependency management; supersedes pip-tools in AD-002, preserving its server contracts and other tools.
- **Date**: 2026-09-14.
- **Status**: active.

### AD-005

- **Decision**: Deliver the Bootcamp III Phase 2 batch interface in `src/task_analyzer.py`, governed by [its contract](../specs/task_analyzer_spec.md) and [context rules](../CONTEXT_RULES.md). Reuse the approved time rules. Course-only explicit priority grouping and numeric empty averages stay in the batch interface, without changing server persistence or desktop presentation contracts.
- **Reason**: The user authorized executing the Phase 2 gap assessment, commits and pushes on 2026-10-16, and identified `.specs/` as the Phase 1 source. Its existing feature contracts remain authoritative; the course's additional function boundary is documented explicitly.
- **Trade-off**: A batch interface satisfies the academic exercise without introducing priority management into the product or claiming a metrics API exists.
- **Scope**: Phase 2 implementation, harness, packaging and submission preparation. Merge, deployment and real-database operations remain outside authorization.
- **Date**: 2026-10-16.
- **Status**: active.

## Handoff

- **Work**: Phase 2 batch analysis implemented. Delivery 1B is merged in GitHub PR #1. The original server contracts and 487 regression cases are preserved.
- **Branch**: `feat/bootcamp-phase-two` from current `origin/main`; local `main` has not been moved.
- **Next step**: Human review of [PR #4](https://github.com/BudaBecker/sdd-task-analyzer/pull/4), actual screenshots, video recording/YouTube URL and final academic submission. Use the [submission guide](../docs/phase-two/submission.md); the PDF remains a draft until the missing evidence is supplied.
- **Result**: 518 tests passed (including 30 batch cases and the new installed-wheel batch check), plus Ruff, strict mypy, dependency compatibility and source/wheel builds. Two third-party deprecation warnings remain. The public repository was renamed to `sdd-task-analyzer`; no schema change or server endpoint was added.
- **Authorization**: Implementation, local commits and pushes are authorized for Phase 2. Merge, deployment and real-database operations are not.
- **External checks**: Actual Ubuntu interpreter/lock and Tailscale access remain pending; a passing local suite does not claim target-host or private-access verification.

## Open questions

No unresolved TLC integration decisions remain. [AGENTS.md](../AGENTS.md#open-questions) owns future MVP technical decisions; the product documents retain their own questions. Reconcile this handoff against Git before resuming work.
