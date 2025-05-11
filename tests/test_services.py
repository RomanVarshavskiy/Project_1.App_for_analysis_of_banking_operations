import json

import pandas as pd

from src.services import profitable_cashback


def test_profitable_cashback_valid_data(sample_data: pd.DataFrame) -> None:
    """Тест на корректность обработки валидных данных."""
    year = 2023
    month = 5
    expected_result = {"Еда": 45, "Топливо": 50, "Развлечения": 20}  # 15 + 30  # 50  # 20

    # Выполнение функции
    result_json = profitable_cashback(sample_data, year, month)
    result_dict = json.loads(result_json)  # Преобразование вывода в словарь

    # Сравнение результатов
    assert result_dict == expected_result, "Функция возвращает некорректный результат"


def test_profitable_cashback_empty_data() -> None:
    """Тест на обработку пустого DataFrame."""
    data = pd.DataFrame(columns=["Категория", "Сумма платежа", "Кэшбэк", "Статус", "Дата операции"])
    year = 2023
    month = 5

    # Выполнение функции
    result_json = profitable_cashback(data, year, month)
    result_dict = json.loads(result_json)

    # Ожидаем пустой словарь
    assert result_dict == {}, "Функция должна возвращать пустой результат для пустых данных"


def test_profitable_cashback_no_valid_transactions(sample_data: pd.DataFrame) -> None:
    """Тест на данные, где нет валидных транзакций."""
    # Добавляем ошибочные записи или фильтруем так, чтобы не осталось валидных
    sample_data = sample_data[sample_data["Статус"] == "ОШИБКА"]
    year = 2023
    month = 5

    # Выполнение функции
    result_json = profitable_cashback(sample_data, year, month)
    result_dict = json.loads(result_json)

    # Ожидаем пустой словарь
    assert result_dict == {}, "Функция должна возвращать пустой результат для данных без валидных транзакций"


def test_profitable_cashback_different_month(sample_data: pd.DataFrame) -> None:
    """Тест на данные, где транзакции находятся в другом месяце."""
    year = 2023
    month = 4  # Указываем месяц, где транзакции отсутствуют

    # Выполнение функции
    result_json = profitable_cashback(sample_data, year, month)
    result_dict = json.loads(result_json)

    # Ожидаем пустой словарь, так как транзакции в этом месяце отсутствуют
    assert result_dict == {}, "Функция должна возвращать пустой результат для месяца без транзакций"
