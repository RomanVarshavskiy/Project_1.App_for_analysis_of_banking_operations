import json
from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(test_df: pd.DataFrame) -> None:
    assert spending_by_category(test_df, "Переводы", "30.11.2021") == json.dumps(
        [{"Сумма платежа": -118.12, "Категория": "Переводы"}], ensure_ascii=False, indent=4
    )


@patch("src.reports.datetime.datetime")
def test_spending_by_category_no_date(mock_datetime: Mock, test_df: pd.DataFrame) -> None:
    # Настраиваем mock для now
    mock_datetime.now.return_value = datetime(2021, 11, 30)

    expected_result = json.dumps([{"Сумма платежа": -118.12, "Категория": "Переводы"}], ensure_ascii=False, indent=4)
    assert spending_by_category(test_df, "Переводы") == expected_result
