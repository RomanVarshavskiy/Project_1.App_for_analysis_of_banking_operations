from datetime import datetime

import pandas as pd
from freezegun import freeze_time

import pytest

from config import PATH_DATA_FILE
from src.utils import get_current_date_time, greetings, read_excel
from unittest.mock import MagicMock, patch

@freeze_time("2025-04-19 12:36:00") # замораживаем дату и время для теста
def test_get_current_date_time():
    """Проверка, что функция возвращает текущее время"""
    # Замороженное время, которое ожидаем вернуть
    expected_datetime = datetime(2025, 4, 19, 12, 36, 0)
    # Вызываем функцию
    result = get_current_date_time()
    # Проверяем, что функция возвращает замороженное время
    assert result == expected_datetime


@pytest.mark.parametrize(
    "test_datetime, expected_greeting",
    [
        ("2025-03-30 07:30:00", "Доброе утро"),
        ("2025-03-30 12:00:00", "Добрый день"),
        ("2025-03-30 18:00:00", "Добрый вечер"),
        ("2025-03-30 23:59:00", "Добрый вечер"),
        ("2025-03-30 01:00:00", "Доброй ночи"),
    ],
)
def test_greetings(test_datetime: str, expected_greeting: str) ->None:
    """Проверка, что функция возвращает правильное приветствие в соответствии с временем"""
    # Преобразуем строку test_datetime в объект datetime
    test_time = datetime.strptime(test_datetime, "%Y-%m-%d %H:%M:%S")
    # Передаём объект datetime в функцию greetings
    assert greetings(test_time) == expected_greeting


@patch("pd.read_excel")
def test_read_excel(mock_reader: MagicMock) -> None:
    """Проверка, что функция открывает для чтения xlsx файл"""
    # Подготавливаем фиктивный DataFrame для мока
    mock_df = pd.DataFrame([
        {"id": 1, "name": "test"},
        {"id": 2, "name": "test2"}
    ])
    mock_reader.return_value = mock_df  # Задаём поведение мока pd.read_excel

    # Вызываем тестируемую функцию
    result = read_excel("test_path")

    # Проверяем, что вызов mock_reader (pd.read_excel) был выполнен один раз
    mock_reader.assert_called_once_with(PATH_DATA_FILE / "test_path")

    # Сравниваем DataFrame на выходе функции с ожидаемым
    pd.testing.assert_frame_equal(result, mock_df)

