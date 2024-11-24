# Base image
FROM python:3.10

# Çalışma dizini ayarla
WORKDIR /code

# Gerekli dosyaları kopyala
COPY requirements.txt /code/

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . /code/
