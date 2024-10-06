# Etapa 1: Usar a imagem oficial do Python como base
FROM python:3.10-slim

# Etapa 2: Definir o diretório de trabalho dentro do container
WORKDIR /app

# Etapa 3: Copiar o arquivo requirements.txt para o diretório de trabalho
COPY ./requirements.txt .

# Etapa 4: Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiar todo o código da pasta app/src para o diretório de trabalho
COPY . /app

# Etapa 7: Expor a porta 8000 (porta padrão usada pelo Uvicorn)
EXPOSE 8000

# Etapa 8: Definir o comando para iniciar o servidor FastAPI usando Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
