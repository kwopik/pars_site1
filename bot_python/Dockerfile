# Используем официальный образ Python
FROM python:3.8

# Устанавливаем необходимые библиотеки
RUN pip install requests python-telegram-bot[all]

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем исходный код в контейнер
COPY . /app

# Команда, которая будет выполнена при запуске контейнера
CMD ["python", "bot1.py"]
