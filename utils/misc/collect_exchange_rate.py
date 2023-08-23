import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_goverla_data():
    goverla_link = "https://goverla.ua/"
    
    # Настройка опций для headless-режима
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Включение headless-режима
    chrome_options.add_argument("--disable-gpu")  # Отключение использования GPU
    # Создание экземпляра браузера с опциями
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(goverla_link)

    # Получение отрендеренного HTML-кода
    html_content = driver.page_source

    # Закрытие браузера
    driver.quit()

    # Создание объекта BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Поиск первых трех тегов <h3> с классом "currency__code"
    currency_code_tags = soup.find_all("h3", class_="currency__code")[:3]

    # Список для хранения данных
    goverla_data_list = []

    # Проход по каждому тегу <h3> currency__code
    for currency_code_tag in currency_code_tags:
        currency_code = currency_code_tag.get_text()

        # Поиск следующего тега <div> с классом "row"
        row_div = currency_code_tag.find_parent("div", class_="row")

        # Поиск двух тегов <h3> с классом "value__absolute" внутри текущего тега <div> row
        value_absolute_tags = row_div.find_all("h3", class_="value__absolute")[:2]
        values = [value.get_text() for value in value_absolute_tags]

        # Создание словаря данных для текущего currency__code
        goverla_data = {
            "currency": currency_code,
            "values": values
        }
        goverla_data_list.append(goverla_data)
    
    return goverla_data_list

def get_privat24_data():
    current_date = datetime.now()
    formatted_date = current_date.strftime('%d.%m.%Y')
    privat24_link = f"https://api.privatbank.ua/p24api/exchange_rates?date={formatted_date}"
    
    response = requests.get(privat24_link)
    if response.status_code == 200:
        api_data = response.json()
        privat24_filtered_data = [
            {
                "baseCurrency": item["baseCurrency"],
                "currency": item["currency"],
                "saleRate": item["saleRate"],
                "purchaseRate": item["purchaseRate"]
            }
            for item in api_data["exchangeRate"]
            if item["currency"] in ["USD", "EUR", "GBP"]
        ]
        return privat24_filtered_data
    else:
        print("Error:", response.status_code)
        return []

def get_monobank_data():
    monobank_link = "https://api.monobank.ua/bank/currency"
    currency_code_mapping = {
                            840: "USD",
                            978: "EUR",
                            826: "GBP"
                            }
    response_monobank = requests.get(monobank_link)
    if response_monobank.status_code == 200:
        monobank_data = response_monobank.json()
        filtered_monobank_data = [
            {
                "currency": currency_code_mapping[item['currencyCodeA']],
                "rateBuy": item['rateBuy'],
                "rateSell": item['rateSell']
            }
            for item in monobank_data
            if item['currencyCodeA'] in currency_code_mapping.keys()
        ]
        return filtered_monobank_data
    else:
        return f"Error: {response_monobank.status_code}"

def get_nbu_data():
    nbu_link = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    
    response_nbu = requests.get(nbu_link)
    if response_nbu.status_code == 200:
        nbu_data = response_nbu.json()
        nbu_filtered_data = [
            {
                "cc": item["cc"],
                "rate": item["rate"]
            }
            for item in nbu_data
            if item["cc"] in ["USD", "EUR", "GBP"]
        ]
        return nbu_filtered_data
    else:
        print("Error:", response_nbu.status_code)
        return []


