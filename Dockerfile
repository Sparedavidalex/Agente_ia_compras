# Usamos Python 3.11 slim
FROM python:3.11-slim

# Define a pasta de trabalho
WORKDIR /app

# Copia o requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta (não é usada para Long Polling, mas Render exige)
EXPOSE 8080

# Roda o bot via Python direto (Long Polling)
CMD ["python", "main.py"]
