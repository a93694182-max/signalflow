from unittest.mock import MagicMock, patch

import pytest

from app.services import scheduler_service


def test_scheduled_engine_closes_db_on_success():
    db = MagicMock()

    with (
        patch.object(scheduler_service, "SessionLocal", return_value=db),
        patch.object(
            scheduler_service,
            "run_signal_engine",
            return_value={
                "filtered_count": 5,
                "flow_count": 2,
            },
        ) as mock_engine,
    ):
        scheduler_service.scheduled_signal_engine()

    mock_engine.assert_called_once_with(db)
    db.close.assert_called_once()


def test_scheduled_engine_closes_db_on_failure():
    db = MagicMock()

    with (
        patch.object(scheduler_service, "SessionLocal", return_value=db),
        patch.object(
            scheduler_service,
            "run_signal_engine",
            side_effect=RuntimeError("Engine failed"),
        ),
    ):
        with pytest.raises(RuntimeError, match="Engine failed"):
            scheduler_service.scheduled_signal_engine()

    db.close.assert_called_once()


def test_start_scheduler_registers_interval_job():
    with patch.object(scheduler_service, "scheduler") as mock_scheduler:
        scheduler_service.start_scheduler()

    mock_scheduler.add_job.assert_called_once_with(
        scheduler_service.scheduled_signal_engine,
        trigger="interval",
        minutes=10,
        id="signal_engine",
        replace_existing=True,
    )
    mock_scheduler.start.assert_called_once()