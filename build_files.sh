#!/bin/bash

# Выходим при ошибке
set -e

echo "📦 Устанавливаем Python зависимости..."
pip install -r requirements.txt

echo "📂 Собираем статические файлы..."
python manage.py collectstatic --noinput

echo "✅ Сборка завершена успешно!"