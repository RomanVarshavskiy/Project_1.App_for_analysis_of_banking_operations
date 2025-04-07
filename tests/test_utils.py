import pytest
from src.utils import greetings
from unittest.mock import MagicMock, patch
from freezegun import freeze_time


@pytest.mark.parametrize(
    "mock_datetime, expected_greeting",
    [
        ("2025-03-30 07:30:00", "Доброе утро"),
        ("2025-03-30 12:00:00", "Добрый день"),
        ("2025-03-30 18:00:00", "Добрый вечер"),
        ("2025-03-30 23:59:00", "Добрый вечер"),
        ("2025-03-30 01:00:00", "Доброй ночи"),
    ],
)
def test_greetings(mock_datetime, expected_greeting):
    with freeze_time(mock_datetime):
        assert greetings() == expected_greeting
