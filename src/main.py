from src.reports import spending_by_category
from src.services import profitable_cashback
from src.utils import get_current_date_time, read_excel
from src.views import get_result_main_page


if __name__ == "__main__":
    # Запуск программы Веб-страница/Главная:
    current_date = get_current_date_time()
    print(get_result_main_page(current_date))

    # Запуск программы Сервисы/Выгодные категории повышенного кешбэка:
    data_df = read_excel("operations.xlsx")
    print(profitable_cashback(data_df, 2025, 3))

    # Запуск программы Отчеты/Траты по категории:
    data_df = read_excel("operations.xlsx")
    print(spending_by_category(data_df, 'Супермаркеты', "18.04.2025"))
