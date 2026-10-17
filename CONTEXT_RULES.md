# AI context rules

## Authority and boundaries

Follow [AGENTS.md](AGENTS.md) for repository workflow, database safeguards and
authorization. For the Bootcamp III Phase 2 function, read
[the batch contract](specs/task_analyzer_spec.md) before changing code or tests.
The user identified `.specs/` as the Phase 1 source; retain its approved REQ/PCE/TLD
scenarios. Do not invent an earlier academic submission or claim the new batch
signature was already present there.

## Implementation rules

- Use Python 3.13+, typed functions and the existing uv environment and lock.
- Implement `analyze_tasks` and `TaskValidationError` at the required path.
- Keep the analysis deterministic and read-only. Never access a real database,
  credentials, network or the host clock from the batch function.
- Use explicit aware instants and the supplied product zone; reuse the existing
  deadline resolver instead of approximating dates or daylight-saving boundaries.
- Validate chronology and input shape with specific exceptions. Guard every
  denominator and preserve full precision until presentation.
- Keep priority grouping and numeric empty results within the academic boundary.
  Do not add priority fields to persistent tasks or change the server API.
- Preserve approved examples and failures. Do not weaken tests to obtain a pass.
- Describe actual prompts, outputs, corrections and verification. A passing test
  run is evidence for the tested behavior, not proof of all possible behavior.

## Evidence and publication

The user authorized commits and pushes for this delivery on 2026-10-16. Open a
documented PR for review. The user subsequently authorized merging the delivery
and deleting incorporated branches on the same date; PR #4 is merged and its
branch was removed. This does not establish a human GitHub review. Deployment
and real-database operations still require separate authorization.
Do not fabricate screenshots, human approval, video URLs or submission status.
Export `requirements.txt` from `uv.lock`; it is not a second dependency source.

## Open questions

The final video URL and academic submission metadata remain user inputs. See
the batch contract for delivery-specific questions.
