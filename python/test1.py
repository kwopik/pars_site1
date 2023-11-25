import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd

# Параметры подключения к MySQL
db_config = {
    'host': '192.168.99.241',
    'user': 'myuser',
    'password': 'mypassword',
    'database': 'mydatabase'
}

base_url = "https://5element.by/catalog/2680-smartfony-samsung?page="
all_data = []
num_pages = 3

# Подключение к MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

for page_num in range(1, num_pages + 1):
    url = f'{base_url}{page_num}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a', class_='c-text')
        prices = soup.find_all('div', class_='c-price')

        page_data = [(a_tag.text, price.text.strip()) for a_tag, price in zip(a_tags, prices)]

        all_data.extend(page_data)
    else:
        print(f'Ошибка при выполнении запроса для страницы {page_num}. Код состояния: {response.status_code}')

# SQL-запрос для вставки данных
insert_query = "INSERT INTO osnova (name, price) VALUES (%s, %s)"

# Вставка данных в таблицу MySQL
cursor.executemany(insert_query, all_data)

# Подтверждение изменений в базе данных
connection.commit()

# Закрытие курсора и соединения
cursor.close()
connection.close()
