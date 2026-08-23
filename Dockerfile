# ==========================================
# ESTÁGIO 1: Build do Front-end (React/Vite)
# ==========================================
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend

# Copia os arquivos de dependência e instala
COPY frontend/package*.json ./
RUN npm install

# Copia o resto do código do front e gera o build estático
COPY frontend/ .
RUN npm run build

# ==========================================
# ESTÁGIO 2: Setup do Back-end (FastAPI)
# ==========================================
FROM python:3.11-slim
WORKDIR /app

# Atualiza o sistema e instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código do backend e a base vetorial pronta
COPY src/ ./src/
COPY chroma_db/ ./chroma_db/

# Copia apenas o front-end "buildado" do Estágio 1 (isso economiza muita memória!)
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expõe a porta para a nuvem
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]