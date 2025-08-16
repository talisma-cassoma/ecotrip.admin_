# Imagem base Python otimizada
FROM python:3.12-slim AS base

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para evitar cache e problemas de encoding
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para aproveitar cache do Docker)
COPY requirements.txt /app/

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar entrypoint e dar permissão
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copiar restante do código do projeto
COPY . /app/

# Porta padrão
EXPOSE 8000

# Comando de inicialização
ENTRYPOINT ["/entrypoint.sh"]
