from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import requests
from freezegun import freeze_time

from config import PATH_DATA_FILE
from src.utils import (df_cards_spend, df_range_current_month, df_top_transactions, get_currencies_rate,
                       get_current_date_time, get_stock_prices, greetings, read_excel)


@freeze_time("2025-04-19 12:36:00")  # замораживаем дату и время для теста
def test_get_current_date_time() -> None:
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
def test_greetings(test_datetime: str, expected_greeting: str) -> None:
    """Проверка, что функция возвращает правильное приветствие в соответствии с временем"""
    # Преобразуем строку test_datetime в объект datetime
    test_time = datetime.strptime(test_datetime, "%Y-%m-%d %H:%M:%S")
    # Передаём объект datetime в функцию greetings
    assert greetings(test_time) == expected_greeting


@patch("pandas.read_excel")  # Патчим pandas.read_excel
def test_read_excel(mock_reader: MagicMock) -> None:
    """Тестирование функции чтения xlsx файла."""
    # Подготавливаем фиктивный DataFrame для мока
    mock_df = pd.DataFrame(
        [
            {"id": 1, "name": "test", "Дата операции": "01.01.2023"},
            {"id": 2, "name": "test2", "Дата операции": "02.01.2023"},
        ]
    )

    mock_reader.return_value = mock_df  # Указываем, что read_excel вернет фиктивный DataFrame

    # Вызываем тестируемую функцию
    result = read_excel("test_path")

    # Проверяем, что pandas.read_excel был вызван с правильным аргументом
    mock_reader.assert_called_once_with(PATH_DATA_FILE / "test_path")

    # Проверяем, что результат функции совпадает с ожидаемым DataFrame
    pd.testing.assert_frame_equal(result, mock_df)


def test_df_range_current_month(test_df: pd.DataFrame) -> None:
    """Тест функции df_range_current_month"""
    # Подготовка тестовых данных
    test_date = datetime(2021, 10, 30, 15, 44)  # 30 октября 2021, 15:44
    transactions_df = test_df
    # Вызов тестируемой функции
    result = df_range_current_month(transactions_df, test_date)
    # Проверки
    assert len(result) == 2  # должно быть только 2 транзакции
    # Проверяем, что все даты в результате находятся между 1 октября и тестовой датой
    assert all(result["Дата операции"] >= datetime(2021, 10, 1))
    assert all(result["Дата операции"] <= test_date)
    # Проверяем, что все транзакции имеют отрицательную сумму
    assert all(result["Сумма платежа"] < 0)
    # Проверяем, что все транзакции имеют статус 'OK'
    assert all(result["Статус"] == "OK")


def test_df_cards_spend(test_df: pd.DataFrame) -> None:
    """Тест функции df_cards_spend"""
    transactions_df = test_df
    # Вызов тестируемой функции
    result = df_cards_spend(transactions_df)
    # Проверяем, что DataFrame сформирован по количеству заданных категорий
    assert len(result) == 3
    # Проверяем, что в DataFrame номер карты представлен в виде последних 4-х цифр
    assert result.loc[2, "last_digits"] == "7197"
    # Проверяем, что в DataFrame кэшбэк суммируется по категориям
    assert result.loc[2, "cashback"] == 2.0


def test_df_top_transactions(test_df: pd.DataFrame) -> None:
    """Тест функции df_top_transactions"""
    transactions_df = test_df
    # Вызов тестируемой функции
    result = df_top_transactions(transactions_df)
    # Проверяем, что DataFrame 5 транзакций
    assert len(result) == 5
    # # Проверяем, что в DataFrame все 5 транзакций в колонке "Сумма платежа" меньше чем следующее значение
    assert all(result["amount"] < 564.0)
    # # Проверяем точное соответствие переименованных колонок
    expected_columns = ["date", "amount", "category", "description"]
    assert list(result.columns) == expected_columns


@patch("requests.get")
def test_get_currencies_rate_success(mock_get: MagicMock) -> None:
    """Тест на проверку, что функция возвращает курс валют от API"""
    mock_get.return_value.json.return_value = {"currency": "USD", "result": 15.5}
    assert get_currencies_rate("USD") == {"currency": "USD", "rate": 15.5}


@patch("requests.get")
def test_get_currencies_rate_error(mock_get: MagicMock) -> None:
    """Тест на проверку, при ошибке выполнения API-запроса"""
    mock_get.side_effect = requests.exceptions.RequestException
    result = get_currencies_rate("USD")
    assert result == {}


@patch("requests.get")
def test_get_stock_prices_success(mock_get: MagicMock) -> None:
    """Тест на проверку, что функция возвращает стоимость акций от API"""
    mock_get.return_value.json.return_value = {"stock": "GOOGL", "Global Quote": {"05. price": "160.6100"}}
    assert get_stock_prices("GOOGL") == {"stock": "GOOGL", "price": "160.6100"}


@patch("requests.get")
def test_get_stock_prices_error(mock_get: MagicMock) -> None:
    """Тест на проверку, при ошибке выполнения API-запроса"""
    mock_get.side_effect = requests.exceptions.RequestException
    result = get_stock_prices("GOOGL")
    assert result == {}
