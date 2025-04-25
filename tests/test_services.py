import json

import pytest
import pandas as pd
from src.services import profitable_cashback


def test_valid_data():
    data = pd.DataFrame({
        "Сумма платежа": [-100, -200, 300],
        "Статус": ["OK", "OK", "CANCELLED"],
        "Дата операции": pd.to_datetime(["2025-03-01", "2025-03-15", "2025-04-01"]),
        "Категория": ["Еда", "Транспорт", "Еда"],
        "Кэшбэк": [10, 20, 30]
    })
    expected_result = {
        "Еда": 10,
        "Транспорт": 20
    }
    result = profitable_cashback(data, 2025, 3)
    assert json.loads(result) == expected_result
