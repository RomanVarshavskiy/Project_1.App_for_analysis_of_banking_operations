import pandas as pd
import pytest


@pytest.fixture
def mock_dataframe():
    """Фиктивный DataFrame для имитации данных из файла"""
    return pd.DataFrame({{
        "Дата операции": ["30/03/2025", "31/03/2025", "01/04/2025"],
        "Сумма операции": [100, 200, 300],
    }
})