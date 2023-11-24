# Используем официальный образ MySQL
FROM mysql:latest

# Устанавливаем переменные окружения для MySQL
ENV MYSQL_ROOT_PASSWORD=my-secret-pw
ENV MYSQL_DATABASE=mydatabase
ENV MYSQL_USER=myuser
ENV MYSQL_PASSWORD=mypassword

# Прокидываем порт 3306
#EXPOSE 3306

# Копирование SQL-скрипта внутрь контейнера
COPY init.sql /docker-entrypoint-initdb.d/
