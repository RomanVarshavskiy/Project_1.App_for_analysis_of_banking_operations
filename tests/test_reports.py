import json

from src.reports import spending_by_category


def test_spending_by_category(test_df):
    assert spending_by_category(test_df, "Переводы", "30.11.2021") == json.dumps(
        [{"Сумма платежа": -118.12, "Категория": "Переводы"}], ensure_ascii=False, indent=4
    )
