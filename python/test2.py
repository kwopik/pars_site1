import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd

# Параметры подключения к MySQL
db_config = {
    'host': 'localhost',
    'user': 'myuser',
    'password': 'mypassword',
    'database': 'mydatabase'
}

base_url = "https://5element.by/catalog/2680-smartfony-samsung?page="
all_data = []
num_pages = 5

# Подключение к MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Создаем еще одну таблицу osnova_new, если она еще не существует
create_table_query = """
CREATE TABLE IF NOT EXISTS osnova_new (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price VARCHAR(50) NOT NULL
);
"""
cursor.execute(create_table_query)

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

# SQL-запрос для вставки данных в таблицу osnova_new
insert_query = "INSERT INTO osnova_new (name, price) VALUES (%s, %s)"

# Вставка данных в таблицу MySQL
cursor.executemany(insert_query, all_data)

# SQL-запрос для сравнения данных в таблицах osnova и osnova_new
compare_query = """
SELECT o.name, o.price AS old_price, n.price AS new_price
FROM osnova o
JOIN osnova_new n ON o.name = n.name AND o.price <> n.price
UNION
SELECT o.name, o.price AS old_price, NULL AS new_price
FROM osnova o
LEFT JOIN osnova_new n ON o.name = n.name
WHERE n.name IS NULL;
"""

# Выполнение запроса на сравнение данных
cursor.execute(compare_query)
result = cursor.fetchall()

if not result:
    print("Данные в таблицах osnova и osnova_new идентичны.")
else:
    print("Обнаружены изменения в данных между таблицами osnova и osnova_new:")
    for row in result:
        if row[2] is not None:
            print(f"Товар: {row[0]}, Было: {row[1]}, Стало: {row[2]}")
        else:
            print(f"Товар: {row[0]}, Было: {row[1]}, Стало: NULL (удалено)")

# Подтверждение изменений в базе данных
connection.commit()

# Закрытие курсора и соединения
cursor.close()
connection.close()
