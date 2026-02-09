FROM python:3.11-slim

# Installation du client MySQL pour les scripts de vérification
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source et des scripts
COPY . .

# Permissions d'exécution
RUN chmod +x scripts/*.sh

CMD ["python", "src/main.py"]