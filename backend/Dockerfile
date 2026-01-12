FROM python:3.10-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código
COPY . .

# Expôe a porta (o Fly.io vai injetar a variável PORT)
EXPOSE 8080

# Comando para rodar a aplicação
# Ajustamos o pythonpath para encontrar o main dentro de api/
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
