import requests


def collect_currency():
    currency_data = {}  # Создаем пустой словарь для хранения данных

    # Список ссылок
    urls = [
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5",
        "https://api.monobank.ua/bank/currency",
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    ]

    try:
        for url in urls:
            response = requests.get(url)
            response.raise_for_status()  # Проверяет наличие ошибок в ответе
            json_data = response.json()

            if url == urls[0]:  # Для первой ссылки
                currency_data["privat24"] = {
                    "data_0": json_data[0],
                    "data_1": json_data[1]
                }
            elif url == urls[1]:  # Для второй ссылки
                currency_data["monobank"] = {
                    "data_0": json_data[0],
                    "data_1": json_data[1]
                }
            elif url == urls[2]:  # Для третьей ссылки
                currency_data["nbu"] = {
                    "data_24": json_data[24],
                    "data_31": json_data[31],
                    "data_23": json_data[23]
                }

        return currency_data  # Возвращаем заполненный словарь
    except requests.exceptions.RequestException as e:
        return None  # Возвращаем None в случае ошибки

