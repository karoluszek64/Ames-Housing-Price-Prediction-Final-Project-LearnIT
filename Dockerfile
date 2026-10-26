
# Wersja Pythona używana w projekcie
FROM python:3.14-slim

# Folder aplikacji w kontenerze
WORKDIR /api

# Instalacja potrzebnych bibliotek
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie API i zapisanego modelu
COPY api/ ./api/
COPY models/ ./models/

# Port, na którym działa FastAPI
EXPOSE 8000

# Uruchomienie aplikacji
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
