import requests
from bs4 import BeautifulSoup

def parse_exchange_table(url, table_class, target_currency):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    exchange_table = soup.find("table", class_=table_class)

    result = []

    if exchange_table:
        rows = exchange_table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if cells and len(cells) > 0:
                currency_cell = cells[0].find("span", class_="code").text.strip()
                if target_currency in currency_cell:
                    data_values = [cell.find("span", class_="value").text.strip() for cell in cells[1:]]
                    result.append(data_values)

    return result