import datetime
import json
from functools import wraps
from typing import Optional, Callable, Any

import pandas as pd

from config import PATH_DATA_REPORT
from src.logger import get_logger

logger = get_logger("reports")


def write_to_file(filename: str = "report.json") -> Callable:
    """Декоратор для записи данных отчета в файл
    Args:
        filename (str): Имя файла для записи отчета.
        По умолчанию — "report.json"."""

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
            # Получаем результат выполнения функции
            result = function(*args, **kwargs)  # Передаем filename аргументом явно
            with open(PATH_DATA_REPORT / filename, "w", encoding="UTF-8") as file:
                file.write(result)
            return result

        return wrapper

    return decorator


@write_to_file()    # В декоратор можно передать имя файла для записи данных
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    if date:
        date_end = datetime.datetime.strptime(date, "%d.%m.%Y")
    else:
        date_end = datetime.datetime.now()
    logger.info("Определена начальная дата")
    date_start = date_end - pd.DateOffset(months=3)
    logger.info("Определена конечная дата")

    # Фильтрация данных за последние 3 месяца
    transactions_spend = transactions[(transactions["Сумма платежа"] < 0) & (transactions["Статус"] == "OK")]
    logger.info("Данные отфильтрованы по 'Сумма платежа' и 'Статус'")
    transactions_df_range = transactions_spend[
        (transactions_spend["Дата операции"] >= date_start) & (transactions_spend["Дата операции"] <= date_end)
    ]
    logger.info(
        f"Получены данные DataFrame за последние 3 месяца, размер данных DataFrame: {transactions_df_range.shape}"
    )
    # Добавляем фильтрацию по категории
    transactions_df_category = transactions_df_range[transactions_df_range["Категория"] == category]
    logger.info(f"Данные отфильтрованы по категории '{category}', размер: {transactions_df_category.shape}")
    result_transactions_df_category = transactions_df_category[["Сумма платежа", "Категория"]]
    logger.info(
        f"Данные отфильтрованы по столбцам 'Сумма платежа', 'Категория', размер: {result_transactions_df_category.shape}"
    )

    # Преобразование в словарь и сериализация в JSON
    result_dict = result_transactions_df_category.to_dict(orient="records")
    logger.info("Данные сформированы в dict из DataFrame")

    json_result = json.dumps(result_dict, ensure_ascii=False, indent=4)
    logger.debug("Успешно получены данные в формате json для выводя в консоль")
    return json_result


# if __name__ == "__main__":
#     data_df = read_excel("operations.xlsx")
#     print(spending_by_category(data_df, 'Супермаркеты', "18.04.2025"))
