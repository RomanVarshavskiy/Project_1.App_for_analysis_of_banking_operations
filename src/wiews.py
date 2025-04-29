import json
from datetime import datetime

from dotenv import load_dotenv

from config import PATH_DATA_FILE
from src.utils import (
    df_cards_spend,
    df_range_current_month,
    df_top_transactions,
    get_currencies_rate,
    get_current_date_time,
    get_stock_prices,
    greetings,
    read_excel,
)

load_dotenv()


def get_result_main_page(date: datetime) -> str:
    """Функция реализует JSON-ответ для старницы 'Главная'"""
    #  Приветствие
    result["greeting"] = greetings(current_date)
    #  DataFrame: Исходные данные
    data_df = read_excel("operations.xlsx")

    #  DataFrame: Данные за текущий месяц
    data_df_range_current_month = df_range_current_month(data_df, current_date)

    #  DataFrame: Данные по расходам, сортированные по картам
    spends_by_cards = df_cards_spend(data_df_range_current_month)
    result["cards"] = spends_by_cards.to_dict(orient="records")

    #  DataFrame: Топ 5 транзакций за текущий месяц
    top_5_transactions = df_top_transactions(data_df_range_current_month)
    result["top_transactions"] = top_5_transactions.to_dict(orient="records")

    with open(PATH_DATA_FILE / "user_settings.json", "r") as file:
        data_rates = json.load(file)

    #  Курсы валют
    for value in data_rates["user_currencies"]:
        currencies_rate = get_currencies_rate(value)
        result.setdefault("currency_rates", []).append(currencies_rate)

    #  Стоимость акций
    for value in data_rates["user_stocks"]:
        stock_price = get_stock_prices(value)
        result.setdefault("stock_prices", []).append(stock_price)

    #  Вывод на консоль в json формате
    try:
        json_result = json.dumps(result, ensure_ascii=False, indent=4)
    except Exception as error:
        print(f"Произошла ошибка: {error}")

    return json_result


if __name__ == "__main__":
    result: dict = {}
    current_date = get_current_date_time()
    print(get_result_main_page(current_date))
