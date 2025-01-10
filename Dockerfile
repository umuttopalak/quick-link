FROM python:3.9-slim

WORKDIR /app

# Gerekli sistem paketlerini kur
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Port ayarı
EXPOSE 3000

# Çalıştırma komutu
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"] 