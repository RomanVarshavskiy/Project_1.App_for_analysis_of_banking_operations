# Проект "BankInsight"

## Описание:

"BankInsight" — это приложение на Python для анализа банковских транзакций, хранящихся в Excel-файлах. Приложение позволяет:
- Генерировать JSON-данные для веб-страниц.
- Формировать отчёты в формате Excel.
- Выполнять анализ данных, включая расчёт кешбэка и расходов по категориям.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/RomanVarshavskiy/Project_1.App_for_analysis_of_banking_operations
```

``
## Использование:

1. Для анализа транзакций используйте функции из модулей:
   - `views`: обработка данных и получение курсов валют.
   - `services`: расчёт кешбэка.
   - `reports`: генерация отчётов.

2. Для запуска программы используйте функцию модуля `main`.

3. Пример запуска анализа кешбэка:
   ```python
   from src.services import profitable_cashback
   from src.utils import read_excel

   data = read_excel("operations.xlsx")
   result = profitable_cashback(data, 2025, 3)
   print(result)
   ```

## Тестирование

Для тестирования проекта используется библиотека 'pytest'. Чтобы запустить тесты, выполните команду:
'pytest'

Тесты покрывают следующие модули и функции:
- 'utils': функции 'get_current_date_time', 'greetings', 'read_excel', 'df_range_current_month', 'df_cards_spend', 
                    'df_top_transactions', 'get_currencies_rate', 'get_stock_prices', 
- 'services': функции 'profitable_cashback.'
- 'reports': функции 'spending_by_category.'

Покрытие тестами составляет 100% кода проекта.


## Документация:

Дополнительную информацию о структуре проекта и API можно найти в [документации](docs/README.md).

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).
