# Container and continuous delivery

The container is an alternative package for the existing single-worker server.
It preserves the server contract: startup requires an existing SQLite file and
does not initialize or migrate one. The image runs as an unprivileged user and
listens on port 8000; Compose publishes that port only to host loopback.

## Local container use

Build and start the server with `docker compose up --build`. By default, the
ignored `.local` directory is mounted at `/var/lib/task-analyzer`; set
`TASK_ANALYZER_STATE_DIR` to an absolute host directory to use another state
location. The database path inside the container is fixed to
`/var/lib/task-analyzer/tasks.sqlite3`.

For a brand-new local exercise, first obtain authorization to create a database
and run the initializer explicitly. It refuses to overwrite an existing file:

```sh
docker compose run --rm api python -c "from pathlib import Path; from task_analyzer_server.schema import initialize_database; initialize_database(Path('/var/lib/task-analyzer/tasks.sqlite3'))"
```

Then start the service and configure the product zone through `PUT
/v1/configuration`, as described in the README. Never use this command against
an existing or production database.

## GitHub flow

`.github/workflows/continuous-integration.yml` runs on every pull request and
branch push. It installs the locked environment, runs the documented quality
checks and tests, builds the wheel, and builds the container image.

After the same job succeeds for a push to `main`, a separate job publishes
`ghcr.io/BudaBecker/sdd-task-analyzer` with immutable commit-SHA and `latest`
tags. It uses the workflow-scoped `GITHUB_TOKEN` with `packages: write`; no
long-lived registry credential is required. This is continuous delivery to the
registry, not deployment: target-host verification, database initialization,
Tailscale configuration, and service changes remain separately authorized.

## Open questions

The target host's container runtime, registry visibility policy, and rollout
mechanism have not been selected. No target deployment is performed by this
workflow.
