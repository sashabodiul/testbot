FROM python:3.9

# Установка рабочей директории
WORKDIR /testbot

# Копирование зависимостей и кода
COPY requirements.txt /testbot/
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py /testbot/

# Переменные окружения
ENV BOT_TOKEN=6140974164:AAE5UUYvp162X4xb5sKmYhiDTry8qb-BtOY
ENV PGUSER=postgres
ENV PGPASSWORD=postgres
ENV DATABASE=currencybot
ENV ADMIN_ID=487679465
ENV DBHOST=localhost

# Запуск бота
CMD ["python", "app.py"]