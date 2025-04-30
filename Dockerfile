FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# İlk olarak yalnızca çeviri gerektiren dosyaları kopyala
COPY babel.cfg .
COPY messages.pot .
COPY app/translations ./app/translations

# Dil dosyalarını derle
RUN pip install babel flask-babel
RUN pybabel compile -d app/translations

# Geri kalan tüm dosyaları kopyala
COPY . .

# Flask uygulamasının dil değişikliklerini görebilmesi için session dizini oluştur
RUN mkdir -p flask_session
RUN chmod 777 flask_session

EXPOSE 3100

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:3100", "app:create_app()"] 