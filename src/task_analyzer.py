"""Read-only batch analysis for the Bootcamp III Phase 2 contract."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import TypedDict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from task_analyzer_server.clock import deadline_cutoff

_MICROSECOND = timedelta(microseconds=1)
_MICROSECONDS_PER_HOUR = 3_600_000_000
_MAX_DEADLINE = date(9999, 12, 30)


class TaskValidationError(ValueError):
    """An analysis input violates the batch contract; no result is produced."""


@dataclass(frozen=True, slots=True)
class Task:
    """An analysis record, independent of persistent task identity and text."""

    created_at: datetime
    completed_at: datetime | None = None
    deadline: date | None = None
    priority: bool = False
    deleted: bool = False


class TaskAnalysis(TypedDict):
    total_tarefas: int
    total_concluidas: int
    total_pendentes: int
    tempo_medio_conclusao_horas: float
    tempo_medio_conclusao_horas_por_prioridade: dict[str, float]
    taxa_atraso_percentual: float


def analyze_tasks(
    tasks: Iterable[Task], *, product_time_zone: str
) -> TaskAnalysis:
    """Analyze a batch using explicit product time and UTC elapsed durations.

    Pending and deleted tasks never enter completion means or the overdue rate.
    Empty means/rates return 0.0 for the academic interface, before formatting.
    """
    zone = _product_zone(product_time_zone)
    try:
        records = iter(tasks)
    except TypeError as error:
        raise TaskValidationError(
            "tasks must be an iterable of Task records"
        ) from error
    total = completed = eligible = late = 0
    duration_us = {False: 0, True: 0}
    completed_by_priority = {False: 0, True: 0}

    for index, task in enumerate(records):
        created_at, completed_at = _validated_instants(task, index)
        if task.deleted:
            continue
        total += 1
        if completed_at is None:
            continue
        completed += 1
        completed_by_priority[task.priority] += 1
        duration_us[task.priority] += (
            completed_at - created_at
        ) // _MICROSECOND
        if task.deadline is not None:
            try:
                cutoff = deadline_cutoff(task.deadline, zone)
            except (ValueError, OverflowError) as error:
                raise TaskValidationError(
                    f"tasks[{index}].deadline has no representable cutoff"
                ) from error
            eligible += 1
            late += completed_at >= cutoff

    return {
        "total_tarefas": total,
        "total_concluidas": completed,
        "total_pendentes": total - completed,
        "tempo_medio_conclusao_horas": _mean_hours(
            sum(duration_us.values()), completed
        ),
        "tempo_medio_conclusao_horas_por_prioridade": {
            "priority": _mean_hours(
                duration_us[True], completed_by_priority[True]
            ),
            "non_priority": _mean_hours(
                duration_us[False], completed_by_priority[False]
            ),
        },
        "taxa_atraso_percentual": late * 100 / eligible if eligible else 0.0,
    }


def _product_zone(key: str) -> ZoneInfo:
    if not isinstance(key, str):
        raise TaskValidationError("product_time_zone must be an IANA zone key")
    try:
        return ZoneInfo(key)
    except (ZoneInfoNotFoundError, ValueError, OSError) as error:
        raise TaskValidationError(
            "product_time_zone must be a valid IANA zone key"
        ) from error


def _validated_instants(
    task: Task, index: int
) -> tuple[datetime, datetime | None]:
    if not isinstance(task, Task):
        raise TaskValidationError(f"tasks[{index}] must be a Task record")
    if type(task.priority) is not bool or type(task.deleted) is not bool:
        raise TaskValidationError(
            f"tasks[{index}].priority and deleted must be booleans"
        )
    if task.deadline is not None and (
        type(task.deadline) is not date or task.deadline > _MAX_DEADLINE
    ):
        raise TaskValidationError(
            f"tasks[{index}].deadline must be a calendar date within the range"
        )
    created_at = _utc_instant(task.created_at, index, "created_at")
    completed_at = (
        None
        if task.completed_at is None
        else _utc_instant(task.completed_at, index, "completed_at")
    )
    if completed_at is not None and completed_at < created_at:
        raise TaskValidationError(
            f"tasks[{index}].completed_at must not precede created_at"
        )
    return created_at, completed_at


def _utc_instant(value: datetime, index: int, field: str) -> datetime:
    if (
        not isinstance(value, datetime)
        or value.tzinfo is None
        or value.utcoffset() is None
    ):
        raise TaskValidationError(
            f"tasks[{index}].{field} must be an aware datetime"
        )
    try:
        return value.astimezone(UTC)
    except (ValueError, OverflowError) as error:
        raise TaskValidationError(
            f"tasks[{index}].{field} has no representable UTC instant"
        ) from error


def _mean_hours(duration_us: int, count: int) -> float:
    return duration_us / (count * _MICROSECONDS_PER_HOUR) if count else 0.0
