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

### AD-006

- **Decision**: Retain `.specs/` and `docs/product/requirements.md` as the authoritative Phase 1 sources; the required Google Docs URL is a submission link only. Keep the approved batch signature, English input fields and Portuguese output keys, with explicit terminology mapping and Phase 2 Given/When/Then examples. The academic-only exception includes explicit boolean priority/group means, numeric `0.0` for empty averages/rates, explicit zone and validated deleted records; REQ-023's deadline-window average is excluded. Python remains 3.13+, satisfying the brief's 3.11+ floor. Non-iterable collections and zone-construction `OSError` raise `TaskValidationError`, while errors consuming an iterable propagate. Windows trailing-space zone acceptance remains a known shared limitation. The user reviews and merges PR #4 into `main`, retains the branch, and supplies the required Docs/video links; the final PDF follows the merge and uses `main` links.
- **Reason**: The Phase 2 review records DEC-01 through DEC-05 and DEC-09 to make contract provenance, the academic exception, validation boundaries and final submission sequence explicit.
- **Trade-off**: Keep the product requirements and server unchanged while documenting the academic boundary and requiring the public default branch to contain the delivery before submission.
- **Scope**: Phase 2 review corrections and submission preparation; no agent merge, deployment or real-database operations. Server zone validation belongs to a separate `fix/` follow-up.
- **Date**: 2026-10-16.
- **Status**: active.

### AD-007

- **Decision**: Merge the Phase 2 delivery, delete incorporated local/remote branches and synchronize on `main`, using `main` links in active guidance and the draft report. Keep the commit and PR history. Merge authorization is not evidence of a human GitHub review.
- **Reason**: On 2026-10-16 the user explicitly requested the assistant to merge all work, delete merged branches and update local/remote state. This supersedes AD-006's user-only merge sequence and branch-retention instruction.
- **Trade-off**: A single shared branch simplifies navigation; retained PR/commit history supplies the delivery provenance after branch cleanup.
- **Scope**: Repository integration, cleanup and documentation synchronization. Deployment and real-database operations remain outside authorization.
- **Date**: 2026-10-16.
- **Status**: active.

## Handoff

- **Work**: Phase 2 batch analysis and independent-review corrections implemented: exact rate arithmetic, specific errors for non-iterable collections/zone OSError, stronger duration evidence and corrected submission/governance documentation. The original server contracts and 487 regression cases are preserved.
- **Branch**: `main` is the shared branch. [PR #4](https://github.com/BudaBecker/sdd-task-analyzer/pull/4) merged as `58d09ed`; incorporated feature branches were deleted under the user's later instruction. Post-merge documentation uses a short-lived `docs/` branch and the same merge/cleanup procedure.
- **Next step**: The user supplies their own GitHub review/comment evidence, required Phase 1 Docs/YouTube URLs, actual screenshots and academic identification before the final PDF/submission. The code and required tree are on `main`; active links target it. The independent review and merge authorization do not count as a recorded human review. Use the [submission guide](../docs/phase-two/submission.md).
- **Result**: 523 tests passed (35 harness cases, 487 server cases and the installed-wheel batch check), plus Ruff, strict mypy, dependency compatibility and source/wheel builds. Mutation checks detect day loss, mean rounding and second truncation. Two third-party deprecation warnings remain. The PDF is still a draft; no schema change or server endpoint was added.
- **README**: Clarified fresh checkout, executable batch example, first-time database creation versus daily API startup/restart, API docs and focused/full test commands. Verified the batch example and API startup/restart using only a disposable temporary database; all 523 tests and README quality checks passed again.
- **Authorization**: Implementation, commits, pushes, merging the delivery and deleting incorporated branches are authorized. Deployment and real-database operations are not.
- **External checks**: Actual Ubuntu interpreter/lock and Tailscale access remain pending; a passing local suite does not claim target-host or private-access verification.
- **Follow-up**: In a separate `fix/` branch, handle zone-construction `OSError` in the server's `_confirm_known_zone`; it is unchanged here. Windows trailing-space zone acceptance remains a known limitation shared by batch and server.

## Open questions

No unresolved TLC integration decisions remain. [AGENTS.md](../AGENTS.md#open-questions) owns future MVP technical decisions; the product documents retain their own questions. Reconcile this handoff against Git before resuming work.
