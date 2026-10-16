"""Phase 2 scenarios and boundaries from the batch-analysis specification."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from task_analyzer import Task, TaskValidationError, analyze_tasks

ZONE = "America/Sao_Paulo"
CREATED = datetime(2026, 9, 14, 8, tzinfo=UTC)


def test_scenario_1_counts_means_priority_and_overdue_rate() -> None:
    tasks = [
        Task(CREATED, CREATED + timedelta(hours=2), date(2026, 9, 14)),
        Task(
            datetime(2026, 9, 14, 23, tzinfo=UTC),
            datetime(2026, 9, 15, 3, tzinfo=UTC),
            date(2026, 9, 14),
            priority=True,
        ),
        Task(CREATED, CREATED + timedelta(hours=3)),
        Task(CREATED, deadline=date(2026, 9, 10), priority=True),
        Task(CREATED),
    ]
    original = tasks.copy()

    result = analyze_tasks(tasks, product_time_zone=ZONE)

    assert result == {
        "total_tarefas": 5,
        "total_concluidas": 3,
        "total_pendentes": 2,
        "tempo_medio_conclusao_horas": 3.0,
        "tempo_medio_conclusao_horas_por_prioridade": {
            "priority": 4.0,
            "non_priority": 2.5,
        },
        "taxa_atraso_percentual": 50.0,
    }
    assert tasks == original
    assert (
        analyze_tasks(
            [*tasks, replace(tasks[1], deleted=True)], product_time_zone=ZONE
        )
        == result
    )


def test_scenario_2_rejects_completion_before_creation() -> None:
    invalid = Task(CREATED, CREATED - timedelta(seconds=1))
    tasks = [Task(CREATED), invalid]

    with pytest.raises(TaskValidationError, match=r"tasks\[1\].completed_at"):
        analyze_tasks(tasks, product_time_zone=ZONE)

    assert tasks == [Task(CREATED), invalid]


@pytest.mark.parametrize("pending_count", [0, 1, 3])
def test_empty_and_pending_only_batches_have_numeric_zero_averages(
    pending_count: int,
) -> None:
    result = analyze_tasks(
        (
            Task(CREATED, deadline=date(2026, 9, 1), priority=True)
            for _ in range(pending_count)
        ),
        product_time_zone=ZONE,
    )

    assert result == {
        "total_tarefas": pending_count,
        "total_concluidas": 0,
        "total_pendentes": pending_count,
        "tempo_medio_conclusao_horas": 0.0,
        "tempo_medio_conclusao_horas_por_prioridade": {
            "priority": 0.0,
            "non_priority": 0.0,
        },
        "taxa_atraso_percentual": 0.0,
    }


def test_req_022_two_and_four_hours_average_three() -> None:
    result = analyze_tasks(
        [Task(CREATED, CREATED + timedelta(hours=h)) for h in (2, 4)],
        product_time_zone=ZONE,
    )

    assert result["tempo_medio_conclusao_horas"] == 3.0
    assert result["tempo_medio_conclusao_horas_por_prioridade"] == {
        "priority": 0.0,
        "non_priority": 3.0,
    }
    assert result["taxa_atraso_percentual"] == 0.0


def test_req_024_eligible_population_and_unrounded_rate() -> None:
    cutoff = datetime(2026, 9, 15, 3, tzinfo=UTC)
    tasks = [
        Task(CREATED, cutoff, date(2026, 9, 14)),
        Task(CREATED, cutoff - timedelta(microseconds=1), date(2026, 9, 14)),
        Task(CREATED, CREATED + timedelta(hours=1), date(2026, 10, 1)),
    ]

    result = analyze_tasks(tasks, product_time_zone=ZONE)
    with_ineligible = analyze_tasks(
        [
            *tasks,
            Task(CREATED, deadline=date(2026, 9, 1)),
            Task(CREATED, cutoff),
            replace(tasks[0], deleted=True),
        ],
        product_time_zone=ZONE,
    )

    assert result["taxa_atraso_percentual"] == pytest.approx(100 / 3)
    assert result["taxa_atraso_percentual"] != 33.3
    assert (
        with_ineligible["taxa_atraso_percentual"]
        == result["taxa_atraso_percentual"]
    )


def test_req_025_reopening_and_recompletion_use_latest_completion() -> None:
    original = Task(CREATED, CREATED + timedelta(hours=2))
    reopened = replace(original, completed_at=None)
    recompleted = replace(reopened, completed_at=CREATED + timedelta(hours=4))

    pending = analyze_tasks([reopened], product_time_zone=ZONE)
    latest = analyze_tasks([recompleted], product_time_zone=ZONE)

    assert pending["total_pendentes"] == 1
    assert pending["tempo_medio_conclusao_horas"] == 0.0
    assert latest["tempo_medio_conclusao_horas"] == 4.0


def test_equal_creation_and_completion_are_valid() -> None:
    result = analyze_tasks([Task(CREATED, CREATED)], product_time_zone=ZONE)

    assert result["total_concluidas"] == 1
    assert result["tempo_medio_conclusao_horas"] == 0.0


def test_all_deleted_tasks_are_excluded() -> None:
    result = analyze_tasks(
        [Task(CREATED, CREATED, deleted=True), Task(CREATED, deleted=True)],
        product_time_zone=ZONE,
    )

    assert result == analyze_tasks([], product_time_zone=ZONE)


@pytest.mark.parametrize(
    ("zone_key", "start", "finish", "hours"),
    [
        ("America/New_York", (2026, 3, 8, 1), (2026, 3, 8, 4), 2.0),
        ("America/New_York", (2026, 11, 1, 0), (2026, 11, 1, 3), 4.0),
    ],
)
def test_duration_uses_elapsed_time_across_dst(
    zone_key: str,
    start: tuple[int, ...],
    finish: tuple[int, ...],
    hours: float,
) -> None:
    zone = ZoneInfo(zone_key)
    task = Task(datetime(*start, tzinfo=zone), datetime(*finish, tzinfo=zone))

    result = analyze_tasks([task], product_time_zone=zone_key)

    assert result["tempo_medio_conclusao_horas"] == hours


@pytest.mark.parametrize(
    ("zone", "deadline", "cutoff"),
    [
        (
            "America/Havana",
            date(2020, 10, 31),
            datetime(2020, 11, 1, 4, tzinfo=UTC),
        ),
        (
            "America/Havana",
            date(2020, 3, 7),
            datetime(2020, 3, 8, 5, tzinfo=UTC),
        ),
        (
            "Pacific/Apia",
            date(2011, 12, 29),
            datetime(2011, 12, 30, 10, tzinfo=UTC),
        ),
    ],
)
def test_pce_049_050_cutoff_discontinuities(
    zone: str, deadline: date, cutoff: datetime
) -> None:
    created = cutoff - timedelta(hours=2)
    for offset, expected_rate in [(-1, 0.0), (0, 100.0), (1, 100.0)]:
        task = Task(created, cutoff + timedelta(microseconds=offset), deadline)

        assert (
            analyze_tasks([task], product_time_zone=zone)[
                "taxa_atraso_percentual"
            ]
            == expected_rate
        )


@pytest.mark.parametrize(
    "invalid",
    [
        Task(datetime(2026, 9, 14)),
        Task(CREATED, datetime(2026, 9, 14)),
        Task(CREATED, deadline=date.max),
        Task(CREATED, deadline=CREATED),
        Task(CREATED, priority=1),
        Task(CREATED, deleted=1),
        Task(CREATED, CREATED - timedelta(seconds=1), deleted=True),
        Task(datetime.min.replace(tzinfo=timezone(timedelta(hours=1)))),
        {"created_at": CREATED},
    ],
)
def test_malformed_records_raise_specific_validation_error(
    invalid: object,
) -> None:
    with pytest.raises(TaskValidationError, match=r"tasks\[0\]"):
        analyze_tasks([invalid], product_time_zone=ZONE)


@pytest.mark.parametrize("zone", ["", "Invalid/Zone", "/etc/localtime", None])
def test_invalid_product_zone_is_rejected_even_for_empty_input(
    zone: str,
) -> None:
    with pytest.raises(TaskValidationError, match="product_time_zone"):
        analyze_tasks([], product_time_zone=zone)


@pytest.mark.parametrize("deadline", [date.min, date(9999, 12, 30)])
def test_pce_051_supported_deadline_bounds(deadline: date) -> None:
    result = analyze_tasks(
        [Task(CREATED, CREATED, deadline)], product_time_zone="UTC"
    )

    assert result["taxa_atraso_percentual"] == (
        100.0 if deadline == date.min else 0.0
    )


@pytest.mark.parametrize(
    ("durations", "hours"),
    [
        ((timedelta(hours=26, minutes=30), timedelta(minutes=20)), 161 / 12),
        ((timedelta(microseconds=1),), 1 / 3_600_000_000),
    ],
)
def test_mean_keeps_multi_day_and_sub_second_precision(
    durations: tuple[timedelta, ...], hours: float
) -> None:
    result = analyze_tasks(
        [Task(CREATED, CREATED + duration) for duration in durations],
        product_time_zone=ZONE,
    )

    assert result["tempo_medio_conclusao_horas"] == hours
