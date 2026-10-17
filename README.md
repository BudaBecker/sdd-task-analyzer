# Task Analyzer

A personal learning and portfolio project for task management and productivity analysis. The Python server owns persistence and business rules; the planned Windows client will provide the interface.

## Current project status

Delivery 1A implements task creation, pending-task editing, validation, uniqueness, fixed product time and recoverable operation results. Delivery 1B adds the remaining server-side lifecycle: completing a task, editing the observations of a completed task, reopening it and deleting a managed task. The Bootcamp III Phase 2 delivery adds a read-only batch analysis module and its test harness. The Windows client, deadline emphasis and server metrics API are not implemented.

Stack: Python 3.13+, FastAPI, SQLite and uv. Dedicated Ubuntu hosting and private Tailscale access remain planned; actual host verification has not run.

## Development setup

Prerequisites: Python 3.13+, uv and Git. The commands below use PowerShell on
Windows. For a fresh checkout:

```powershell
git clone https://github.com/BudaBecker/sdd-task-analyzer.git
cd sdd-task-analyzer
git switch feat/bootcamp-phase-two
```

Until PR #4 is merged, the Phase 2 files are on `feat/bootcamp-phase-two`.
For an existing checkout, open a terminal in its repository root. Install the
project and development tools:

```powershell
uv sync --locked
```

uv creates the ignored `.venv` and installs this package plus development tools. `pyproject.toml` declares dependencies; `uv.lock` records their resolved versions. `requirements.txt` is a generated course deliverable, not a second dependency source. Regenerate it after dependency changes with `uv export --locked --no-emit-project --format requirements-txt --output-file requirements.txt`. Routine development uses `uv run`; activation is optional.

### Without uv

For the conventional course evaluation path on Windows:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pip install --no-deps -e .
.venv\Scripts\python -m pytest tests/test_harness.py -v
```

The hashed requirements export installs dependencies only. Install the project
separately so both `task_analyzer` and `task_analyzer_server` are importable.
Keep `-e .` out of the hashed export: pip cannot verify editable project hashes.

## Phase 2 batch analysis

Read [the contract](specs/task_analyzer_spec.md) and [AI context rules](CONTEXT_RULES.md).
The module analyzes typed records without accessing a database or starting the
server. Run this complete example in PowerShell to print its results:

```powershell
@'
from datetime import UTC, datetime, timedelta
from task_analyzer import Task, analyze_tasks

created = datetime(2026, 9, 14, 8, tzinfo=UTC)
result = analyze_tasks(
    [Task(created, created + timedelta(hours=2), priority=True)],
    product_time_zone="America/Sao_Paulo",
)
assert result["tempo_medio_conclusao_horas"] == 2.0
print(result)
'@ | uv run python -
```

Run the course scenarios with `uv run python -m pytest tests/test_harness.py -v`.
Priority is an explicit batch input, with `priority` and `non_priority` result
groups. Empty averages/rates return `0.0`; this numeric interface does not change
the product dashboard's N/A rule. See the [submission guide](docs/phase-two/submission.md)
for verification evidence, the PR and the remaining video/submission steps.

## Run the server locally

The server requires an explicit existing database and never creates one at
startup. For the first local exercise only, create a new database. Skip this
step when `.local/tasks.sqlite3` already exists; initialization refuses to
overwrite it:

```powershell
New-Item -ItemType Directory -Force .local | Out-Null
uv run python -c "from pathlib import Path; from task_analyzer_server.schema import initialize_database; initialize_database(Path('.local/tasks.sqlite3').resolve())"
```

Start the API from the repository root in each new terminal session, using the
existing exercise database:

```powershell
$env:TASK_ANALYZER_DATABASE_PATH = Join-Path (Get-Location) '.local/tasks.sqlite3'
uv run python -m uvicorn task_analyzer_server.app:application_factory --factory --host 127.0.0.1 --port 8000
```

Keep that terminal open and visit `http://127.0.0.1:8000/docs`. For a newly
initialized database, configure the fixed product time zone using
`PUT /v1/configuration` with `{"product_time_zone":"America/Sao_Paulo"}`.
Configuration persists across restarts. Create tasks with `POST /v1/tasks`,
a fresh UUID in `Operation-Id` and `{"title":"Read notes"}`. To generate an ID
in another PowerShell terminal, run `[guid]::NewGuid().ToString()`. Replay the
same attempt with the same ID and body; use a new ID for a new action.

Press `Ctrl+C` to stop the API. To restart, run only the start block above;
keep the existing database. This starts the local API and interactive API docs;
the Windows desktop application is still planned.

The lifecycle commands take the same envelope and an exact JSON body: `POST /v1/tasks/{task_id}/completion` with `{}`, `PUT /v1/tasks/{task_id}/observations` with `{"observations":"..."}` or `{"observations":null}`, `POST /v1/tasks/{task_id}/reopening` with `{}`, and `DELETE /v1/tasks/{task_id}` with `{}`. A successful deletion answers with the task's final snapshot, and `GET /v1/operations/{operation_id}` still recovers any original result.

## Run tests

After `uv sync --locked`, run these commands from the repository root:

```powershell
# All tests, including server regressions and installed-wheel smoke tests
uv run python -m pytest

# Only the Phase 2 success, error and boundary scenarios
uv run python -m pytest tests/test_harness.py -v

# Only server and installed-package tests
uv run python -m pytest tests/server
```

Tests create disposable databases and do not require a running API or an
initialized local exercise database. The full suite also builds and installs
the wheel in temporary environments outside the checkout.

## Quality checks

```powershell
uv run ruff format --check src tests
uv run ruff check src tests
uv run python -m mypy --strict
uv run python -m pytest
uv pip check
uv build
```

The suite includes isolated SQLite, restart, concurrency and installed-wheel tests. It creates only disposable databases. Installed-wheel tests export runtime dependencies from `uv.lock` into a temporary requirements file and use uv outside the checkout.

## Project guide

- [Development instructions](AGENTS.md): the lightweight SDD workflow and safeguards.
- [Current handoff and shared decisions](.specs/STATE.md): where to resume.
- [Product requirements](docs/product/requirements.md), [scope](docs/product/scope.md), and [backlog](docs/product/backlog.md): behavior and boundaries.
- [1A specification](.specs/features/persistent-task-creation-editing/spec.md) and [design](.specs/features/persistent-task-creation-editing/design.md): accepted behavior and server contracts.
- [1B specification](.specs/features/task-lifecycle-deletion/spec.md) and [design](.specs/features/task-lifecycle-deletion/design.md): the task lifecycle and deletion delta.
- [Deployment](docs/architecture/deployment/server.md): the separately authorized Ubuntu/Tailscale procedure.

Server modules live in `src/task-analyzer-server/task_analyzer_server/`; server tests live in `tests/server/`. The course module is `src/task_analyzer.py`, its contract is `specs/task_analyzer_spec.md`, and its harness is `tests/test_harness.py`. Both modules ship in the same wheel. The bundled `.ai/skills/tlc-spec-driven/` is optional historical study material, not the active development workflow. Old plans and audit details remain available in Git at `8c68d6a`.

## Open questions

Target-host values, Windows client technology and later feature contracts remain open. Deadline emphasis and the server metrics API are not started. Phase 2 video recording and academic submission remain user steps.
