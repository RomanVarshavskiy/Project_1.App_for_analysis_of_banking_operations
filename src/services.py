import datetime
import json

from pandas import DataFrame

from src.logger import get_logger

logger = get_logger("services")


# _, last_day = calendar.monthrange(int(year), int(month))
def profitable_cashback(data: DataFrame, year: int, month: int) -> str:
    """Функция выдает JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года"""
    date_start = datetime.datetime(year, month, day=1)
    logger.info("Определена начальная дата")
    if month in [1, 3, 5, 7, 8, 10, 12]:
        date_end = datetime.datetime(year, month, day=31)
    elif month == 2:
        date_end = datetime.datetime(year, month, day=28)
    else:
        date_end = datetime.datetime(year, month, day=30)
    logger.info("Определена конечная дата")

    # Фильтрация данных за определенный месяц и год
    transactions_spend = data[(data["Сумма платежа"] < 0) & (data["Статус"] == "OK")]
    logger.info("Данные отфильтрованы по 'Сумма платежа' и 'Статус'")
    transactions_df_range = transactions_spend[
        (transactions_spend["Дата операции"] >= date_start) & (transactions_spend["Дата операции"] <= date_end)
    ]
    logger.debug(
        f"Успешно получены данные DataFrame за указанный месяц года, размер данных DataFrame: {transactions_df_range.shape}"
    )
    df_transactions_by_categories = (
        transactions_df_range[["Кэшбэк", "Категория"]].groupby("Категория").sum().reset_index()
    )
    logger.info("Данные отфильтрованы по 'Категория' и 'Кэшбэк'")

    result_dict = dict(
        zip(df_transactions_by_categories["Категория"], df_transactions_by_categories["Кэшбэк"].values.tolist())
    )
    logger.info("Данные сформированы в dict из DataFrame")
    json_result = json.dumps(result_dict, ensure_ascii=False, indent=4)
    logger.debug("Успешно получены данные в формате json для выводя в консоль")
    # return result_dict
    return json_result


# if __name__ == '__main__':
#     data_df = read_excel("operations.xlsx")
#     print(profitable_cashback(data_df, 2025, 3))
