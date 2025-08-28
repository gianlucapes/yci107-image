# Base image
FROM python:3.11-slim

# Imposta directory di lavoro
WORKDIR /app

# Copia i file necessari
COPY requirements.txt .
COPY server.py .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta
EXPOSE 8828

# Comando per avviare l'app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8828"]