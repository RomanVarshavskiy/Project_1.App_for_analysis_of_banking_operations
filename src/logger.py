import logging

from config import PATH_TO_LOGGER


def get_logger(module_name: str) -> logging.Logger:
    # Создаём объект логгера
    logger = logging.getLogger(module_name)
    # Создаём обработчик для записи логов в файл
    handler = logging.FileHandler(PATH_TO_LOGGER / f"{module_name}.log", encoding="utf-8")
    # Определяем формат логов
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    # Добавляем обработчик к логгеру
    logger.addHandler(handler)
    # Устанавливаем уровень для обработчика (опционально)
    handler.setLevel(logging.DEBUG)
    # Устанавливаем уровень логирования
    logger.setLevel(logging.DEBUG)
    return logger
