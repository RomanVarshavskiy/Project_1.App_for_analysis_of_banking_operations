from dotenv import load_dotenv
import os
import json
import requests
import logging

from datetime import datetime

import pandas as pd

from config import PATH_DATA_FILE, PATH_ROOT, PATH_TO_LOGGER

logging.basicConfig(
    filename=PATH_TO_LOGGER / "utils.log",
    filemode="w",
    format="%(asctime)s %(name)s:%(levelname)s: %(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)

logger = logging.getLogger()

load_dotenv()


def get_current_date_time() -> datetime:
    """Функция возвращает приветствие в зависимости от текущего времени"""
    current_date_time = datetime.now()
    logger.debug(f"Получено текущее время: {current_date_time}")
    return current_date_time


def greetings(time: datetime) -> str:
    """Функция возвращает приветствие в зависимости от текущего времени"""
    greetings_dict = {"Доброе утро": range(6, 12), "Добрый день": range(12, 18),
                     "Добрый вечер": range(18, 24), "Доброй ночи": range(0, 7)}
    hour = time.hour
    greetings_message = ""
    for key, value in greetings_dict.items():
        if hour in greetings_dict[key]:
            greetings_message = key

    logger.debug("Получено приветствие")
    return greetings_message


def read_excel(filename: str, datetime_to_timestamp: bool = True) -> pd.DataFrame:
    """Функция для чтения xlsx файла
        :param filename: путь к xlsx файлу
        :param datetime_to_timestamp: приводит столбец "Дата операции" к формату timestamp
        :return: pandas DataFrame
    """
    operations_df = pd.read_excel(PATH_DATA_FILE / filename)
    if datetime_to_timestamp:
        # Приведение даты к datetime для дальнейшей фильтрации (dayfirst - первым значением указан день)
        operations_df["Дата операции"] = pd.to_datetime(operations_df["Дата операции"], dayfirst=True, errors='coerce')
    logger.debug(f"Успешно прочитан файл: {filename}, размер данных DataFrame: {operations_df.shape}")
    return operations_df


def df_range_current_month(transactions: pd.DataFrame, date: datetime) -> pd.DataFrame:
    """Функция возвращает DataFrame, отфильтрованный за текущий месяц
        :param transactions: DataFrame с операциями
        :param date: строка в формате "DD.MM.YYYY", для которой нужно фильтровать
        :return: pandas DataFrame, отфильтрованный по текущему месяцу
    """
    # Определяем начало месяца
    first_day_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Фильтрация данных
    transactions_spend = transactions[(transactions["Сумма платежа"] < 0) & (transactions["Статус"] == "OK")]
    logger.info("Данные отфильтрованы по 'Сумма платежа' и 'Статус'")
    transactions_df_range = transactions_spend[(transactions_spend["Дата операции"] >= first_day_of_month) &
                                               (transactions_spend["Дата операции"] <= date)]
    logger.debug(f"Успешно получены данные DataFrame с начала месяца до текущей даты, размер данных DataFrame: {transactions_df_range.shape}")
    return transactions_df_range


def df_cards_spend(transactions_of_month: pd.DataFrame) -> pd.DataFrame:
    """Функция фильтрует данные по картам и возвращает DataFrame, в виде:
     последние 4 цифры карты;
     общая сумма расходов;
     кешбэк (1 рубль на каждые 100 рублей).
     """
    df_transactions_by_cards = transactions_of_month[["Номер карты", "Сумма платежа", "Кэшбэк"]].groupby("Номер карты").sum().reset_index()
    logger.info("Данные отфильтрованы по 'Номер карты', 'Сумма платежа' и 'Кэшбэк'")
    df_transactions_by_cards["Номер карты"] = df_transactions_by_cards["Номер карты"].str[-4:]
    df_transactions_by_cards = df_transactions_by_cards.rename(columns={"Номер карты": "last_digits", "Сумма платежа": "total_spent", "Кэшбэк": "cashback"})
    logger.debug(f"Данные успешно отфильтрованы по картам, размер данных DataFrame: { df_transactions_by_cards.shape}")
    return df_transactions_by_cards


def df_top_transactions(transactions_of_month: pd.DataFrame) -> pd.DataFrame:
    """Функция возвращает DataFrame из Топ-5 транзакций по сумме платежа, в виде:
    date,
    amount,
    category,
    description
    """
    top_transactions = transactions_of_month[["Дата платежа", "Сумма платежа", "Категория", "Описание"]].sort_values(by="Сумма платежа")
    logger.info("Получены ТОП 5 транзакций по сумме платежа")
    top_transactions = top_transactions.rename(
        columns={"Дата платежа": "date", "Сумма платежа": "amount", "Категория": "category", "Описание": "description"})
    logger.info("В данных ТОП 5 транзакций, переименованы названия столобцов 'Дата платежа': 'date', 'Сумма платежа': 'amount', 'Категория': 'category', 'Описание': 'description'")

    logger.debug("Успешно получены ТОП 5 транзакций по сумме платежа")
    return top_transactions


def get_currencies_rate(currency_code: str) -> dict:
    """ Функция возвращает курс валют, заданных в файле: data/'user_settings.json' """
    url = "https://api.apilayer.com/exchangerates_data/convert"
    payload = {
        "amount": "1",
        "to": "RUB",
        "from": currency_code,
    }
    headers = {"apikey": os.getenv("API_KEY_CURRENCY_RATE")}
    logger.info(f"Запрос данных с API: {url} для валюты '{currency_code}'")
    response = requests.get(url, headers=headers, params=payload)
    if response.status_code != 200:
        logger.error(f"Ошибка при выполнении API-запроса: {url} - {ValueError}")
        raise ValueError(f"Failed to get currency rate")
    logger.info(f"Успешный ответ от {url}, статус: {response.status_code}")
    data = response.json()
    currency_data = data.get("result")
    result = {
        "currency": currency_code,
        "rate": currency_data,
    }
    logger.debug(f"Успешно получен ответ от {url}")
    return result


def get_stock_prices(stock_simbol: str) -> dict:
    """ Функция возвращает стоимость акций, заданных в файле: data/'user_settings.json' """
    headers = {"apikey": os.getenv("API_KEY_STOCK_PRICES")}
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_simbol}&apikey={headers}"
    logger.info(f"Запрос данных с API: {url} для акций '{stock_simbol}'")
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Ошибка при выполнении API-запроса: {url} - {ValueError}")
        raise ValueError(f"Failed to get currency rate")
    logger.info(f"Успешный ответ от {url}, статус: {response.status_code}")
    data = response.json()
    stock_price = data["Global Quote"].get("05. price")
    result = {
        "stock": stock_simbol,
        "price": stock_price,
    }
    logger.debug(f"Успешно получен ответ от {url}")
    return result
